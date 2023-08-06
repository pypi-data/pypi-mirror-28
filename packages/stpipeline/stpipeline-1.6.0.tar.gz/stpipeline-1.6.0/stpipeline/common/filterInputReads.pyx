import sys
import time
import os
import re
import Queue
import pysam
import ctypes
import multiprocessing
import subprocess
import logging
from stpipeline.common.utils import safeOpenFile, fileOk, is_fifo
from stpipeline.common.fastq_utils import *
from stpipeline.common.sam_utils import convert_to_AlignedSegment
from stpipeline.common.adaptors import removeAdaptor
from stpipeline.common.stats import qa_stats
from itertools import izip
from sqlitedict import SqliteDict

class InputReadsFilter():
    """
    This class handles the input read filtering in parrallel using several python subrpocesses.
      - It performs a sanity check (forward and reverse reads same length and order)
      - It performs a BWA-based quality trimming discarding very short reads
      - It removes adaptors from the reads (optional)
      - It checks for AT and GC content (optional)
      - It performs a sanity check on the UMI (optional)
    Reads that do not pass the filters are discarded (both R1 and R2)
    Reads that pass the filter are written as BAM (R2)
    :param rv: the bam file with the reverse reads
    :param out_fw: the name of the output file for the forward reads
    :param out_rv: the name of the output file for the reverse reads
    :param out_rv_discarded: the name of the output file for discarded reverse reads
    :param barcode_length: length of the barcode sequence (integer)
    :param start_position: the start position of the barcode
    :param filter_AT_content: % of A and T bases a read2 must have to be discarded
    :param filter_GC_content: % of G and C bases a read2 must have to be discarded
    :param umi_start: the start position of the UMI
    :param umi_end: the end position of the UMI
    :param min_qual: the min quality value to use in the trimming
    :param min_length: the min valid length for a read after trimming
    :param polyA_min_distance: if >5 remove PolyA adaptors from the reads
    :param polyT_min_distance: if >5 remove PolyT adaptors from the reads
    :param polyG_min_distance: if >5 remove PolyG adaptors from the reads
    :param polyC_min_distance: if >5 remove PolyC adaptors from the reads
    :param polyN_min_distance: if >5 remove PolyN adaptors from the reads
    :param qual64: true of qualities are in phred64 format
    :param umi_filter: performs a UMI quality template filter when True
    :param umi_filter_template: the template to use for the UMI filter
    :param umi_quality_bases: the number of low quality bases allowed in an UMI
    :param adaptor_missmatches: number of miss-matches allowed when removing adaptors
    """

    def __init__(self, verbose=False, max_reads_in_memory=10000000, stat_line_interwall=100000, chunk_size=100000):
        """
        Initiates the instance and setting default values
        :param verbose: set to true to write more info to stderr
        :param max_reads_in_memory: Maximum number of reads to keep in memory at once
        :param stat_line_interwall: how often info line s should be written of verbose is true
        :param chunk_size: how many reads should be sent to workers in one chunk
        """
        self.verbose = verbose
        self.aborted = False
        self.stat_line_interwall = stat_line_interwall
        self.chunk_size = chunk_size
        self.max_chunks_in_queue = min(32767,max_reads_in_memory/(self.chunk_size*2))
        #if self.verbose:
        #    self.logger.debug('InputReadsFilter::INFO:: initiation completed.')

    def input_arguments(
                    self,
                    fw,
                    rv,
                    out_rv,
                    out_rv_discarded,
                    barcode_length,
                    start_position,
                    filter_AT_content,
                    filter_GC_content,
                    umi_start,
                    umi_end,
                    min_qual,
                    min_length,
                    polyA_min_distance,
                    polyT_min_distance,
                    polyG_min_distance,
                    polyC_min_distance,
                    polyN_min_distance,
                    qual64,
                    umi_filter,
                    umi_filter_template,
                    umi_quality_bases,
                    adaptor_missmatches,
                    threads,
                    overhang):
        """
        Sets the input arguments
        :param rv: the bam file with the reverse reads
        :param out_fw: the name of the output file for the forward reads
        :param out_rv: the name of the output file for the reverse reads
        :param out_rv_discarded: the name of the output file for discarded reverse reads
        :param barcode_length: length of the barcode sequence (integer)
        :param start_position: the start position of the barcode
        :param filter_AT_content: % of A and T bases a read2 must have to be discarded
        :param filter_GC_content: % of G and C bases a read2 must have to be discarded
        :param umi_start: the start position of the UMI
        :param umi_end: the end position of the UMI
        :param min_qual: the min quality value to use in the trimming
        :param min_length: the min valid length for a read after trimming
        :param polyA_min_distance: if >5 remove PolyA adaptors from the reads
        :param polyT_min_distance: if >5 remove PolyT adaptors from the reads
        :param polyG_min_distance: if >5 remove PolyG adaptors from the reads
        :param polyC_min_distance: if >5 remove PolyC adaptors from the reads
        :param polyN_min_distance: if >5 remove PolyN adaptors from the reads
        :param qual64: true of qualities are in phred64 format
        :param umi_filter: performs a UMI quality template filter when True
        :param umi_filter_template: the template to use for the UMI filter
        :param umi_quality_bases: the number of low quality bases allowed in an UMI
        :param adaptor_missmatches: number of miss-matches allowed when removing adaptors
        :param threads: number of subprocesses to start
        :param overhang: extra bases on the edges of the barcode to include in bam tag
        """

        #if self.verbose:
        #    self.logger.debug('InputReadsFilter::INFO:: Getting input arguments.')

        self.logger = logging.getLogger("STPipeline")
        if not (os.path.isfile(fw) or is_fifo(fw)) or not (os.path.isfile(rv) or is_fifo(rv)):
            error = "Error doing quality trimming, input file/s not present {}\n{}\n".format(fw,rv)
            self.logger.error(error)
            raise RuntimeError(error)

        # Check if discarded files must be written out
        self.keep_discarded_files = out_rv_discarded is not None

        # Build fake sequence adaptors with the parameters given
        self.adaptorA = "".join("A" for k in xrange(polyA_min_distance))
        self.adaptorT = "".join("T" for k in xrange(polyT_min_distance))
        self.adaptorG = "".join("G" for k in xrange(polyG_min_distance))
        self.adaptorC = "".join("C" for k in xrange(polyC_min_distance))
        self.adaptorN = "".join("N" for k in xrange(polyN_min_distance))

        # Not recommended to do adaptor trimming for adaptors smaller than 5
        self.do_adaptorA = polyA_min_distance >= 5
        self.do_adaptorT = polyT_min_distance >= 5
        self.do_adaptorG = polyG_min_distance >= 5
        self.do_adaptorC = polyC_min_distance >= 5
        self.do_adaptorN = polyN_min_distance >= 5
        self.do_AT_filter = filter_AT_content > 0
        self.do_GC_filter = filter_GC_content > 0

        # Quality format
        self.phred = 64 if qual64 else 33

        self.umi_filter = umi_filter
        self.umi_start = umi_start
        self.umi_end = umi_end
        self.umi_filter_template = umi_filter_template
        self.umi_quality_bases = umi_quality_bases
        self.filter_AT_content = filter_AT_content
        self.filter_GC_content = filter_GC_content
        self.adaptor_missmatches = adaptor_missmatches
        self.min_length = min_length
        self.min_qual = min_qual
        self.barcode_length = barcode_length
        self.start_position = start_position
        self.threads = threads
        self.overhang = overhang

        self.fw = fw
        self.rv = rv
        self.out_rv = out_rv
        self.out_rv_discarded = out_rv_discarded

    def run(self, ):
        """
        Function that starts and controlls the subprocesses and finally merges the outputs
        """

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process pid='+str(os.getpid())+'.')

        # create queues and connections
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Creating queues and connections.')
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Creating input reads queue.')
        self.input_read_queue = multiprocessing.Queue(self.max_chunks_in_queue)
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Creating output reads queue.')
        self.output_read_queue = multiprocessing.Queue(self.max_chunks_in_queue)
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Creating counter pipe.')
        self.counter_connection_send_end, counter_connection_recv_end = multiprocessing.Pipe()

        self.reader_running = multiprocessing.Value(ctypes.c_bool, True)
        self.workers_running= multiprocessing.Value(ctypes.c_bool, True)

        # start reader subprocess
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Starting reader.')
        self.reader = multiprocessing.Process(target=self.input_files_reader)
        self.reader.start()

        # start worker pool
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Starting pool.')
        self.worker_pool = [ multiprocessing.Process(target=self.parallel_worker_function)
                            for i in range(self.threads-1) ]
        for process in self.worker_pool: process.start()
        worker_process_ids = [process.pid for process in self.worker_pool]

        # start writer subprocess
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Creating writer.')
        self.writer = multiprocessing.Process(target=self.output_files_writer)
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - Stariting writer.')
        self.writer.start()
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - writer started.')

        # wait for reader to complete
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - waiting for reader.')
        self.reader.join()

        # wait for worker pool to complete
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - waiting for pool.')
        for process in self.worker_pool: process.join()
        self.workers_running.value = False

        # merge bam files
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - merging bam files produced by workers.')
        worker_bams = [ self.out_rv.rstrip('.bam')+'.WORKER_{}.bam'.format(process_id)
                        for process_id in worker_process_ids ]
        command = 'samtools merge -@ {} {} {}'.format(
            self.threads,
            self.out_rv,
            ' '.join(worker_bams)
            )
        subprocess.check_call(command, shell=True)
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - removing bam files produced by workers.')
        for bam in worker_bams: os.remove(bam)

        # wait for writer to complete
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - waiting for writer.')
        self.writer.join()

        # get the counters from the writer process
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - fetching counter.')
        read_pair_counters = counter_connection_recv_end.recv()
        counter_connection_recv_end.close()
        self.counter_connection_send_end.close()

        if self.verbose:
            self.logger.debug(
                'InputReadsFilter::INFO:: main process - updating logs and checking for prescence of files.'
                )
        # Write info to the log
        self.logger.info("Trimming stats total reads (pair): {}".format(read_pair_counters['total_reads']))
        self.logger.info("Trimming stats {} reads have been dropped!".format(read_pair_counters['dropped_rv']))
        perc2 = '{percent:.2%}'.format(
                            percent=float(read_pair_counters['dropped_rv'])/float(read_pair_counters['total_reads'])
                            )
        self.logger.info("Trimming stats you just lost about {} of your data".format(perc2))
        self.logger.info("Trimming stats reads remaining: {}".format(
                            read_pair_counters['total_reads'] - read_pair_counters['dropped_rv'])
                         )
        self.logger.info("Trimming stats dropped pairs due to incorrect UMI: {}".format(
                            read_pair_counters['dropped_umi_template'])
                         )
        self.logger.info("Trimming stats dropped pairs due to low quality UMI: {}".format(
                            read_pair_counters['dropped_umi'])
                         )
        self.logger.info("Trimming stats dropped pairs due to high AT content: {}".format(
                            read_pair_counters['dropped_AT'])
                         )
        self.logger.info("Trimming stats dropped pairs due to high GC content: {}".format(
            read_pair_counters['dropped_GC'])
                         )
        self.logger.info("Trimming stats dropped pairs due to presence of artifacts: {}".format(
            read_pair_counters['dropped_adaptor'])
                         )
        self.logger.info("Trimming stats dropped pairs due to length after trimming: {}".format(
            read_pair_counters['to_short_after_trimming'])
                         )

        # Check that output file was written ok
        if not fileOk(self.out_rv):
            error = "Error doing quality trimming checks of raw reads." \
            "\nOutput file not present {}\n".format(self.out_rv)
            self.logger.error(error)
            raise RuntimeError(error)

        # Adding stats to QA Stats object
        qa_stats.input_reads_forward = read_pair_counters['total_reads']
        qa_stats.input_reads_reverse = read_pair_counters['total_reads']
        qa_stats.reads_after_trimming_forward = (read_pair_counters['total_reads'] - read_pair_counters['dropped_rv'])
        qa_stats.reads_after_trimming_reverse = (read_pair_counters['total_reads'] - read_pair_counters['dropped_rv'])
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: main process - completed.')

    def input_files_reader(self, ):
        """
        Worker function for the input reader subprocess,
        reading input files and sending data to workers thorugh a multiprocessing queue
        """

        cdef double start_time = time.time()
        cdef int count = 0
        cdef double last_time = start_time
        cdef int last_count = count
        cdef str identity = 'READER'

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: Starting input files reader pid={}.'.format(os.getpid()))

        # Open fastq files with the fastq parser
        fw_file = safeOpenFile(self.fw, "rU")
        rv_file = safeOpenFile(self.rv, "rU")

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: input files reader - starting to parse reads.')
        if self.verbose:
            self.print_stat_line(start_time, last_time, count, last_count, identity, header=True)
        cdef list chunk = []
        cdef tuple read_one
        cdef tuple read_two
        for read_one, read_two in izip(readfq(fw_file), readfq(rv_file)):
            chunk.append((read_one, read_two))
            if len(chunk) == self.chunk_size:
                self.input_read_queue.put( chunk )
                chunk = []
            count += 1
            if self.verbose and count % self.stat_line_interwall == 0:
                self.print_stat_line(start_time, last_time, count, last_count, identity)
                last_time = time.time()
                last_count = count

        self.input_read_queue.put( chunk )

        if self.verbose:
            self.print_stat_line(start_time, last_time, count, last_count, identity)
            last_time = time.time()
            last_count = count

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: input files reader - all reads parsed.')
        fw_file.close()
        rv_file.close()

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: input files reader - closing and joining queue.')
        self.input_read_queue.close()
        self.input_read_queue.join_thread()
        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: input files reader - shutting down.')
        self.reader_running.value = False

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: input files reader - completed.')

    def output_files_writer(self, ):
        """
        Worker function for writing outputfiles and incrementing counters
        Note that the bamfiles a written by the workers and merged by the class.run function
        Only discarded files are written here
        """

        cdef double start_time = time.time()
        cdef int count = 0
        cdef double last_time = start_time
        cdef int last_count = count
        cdef str identity = 'WRITER'

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: Starting output files writer pid={}.'.format(os.getpid()))

        # Create output file writers
        if self.keep_discarded_files:
            out_rv_handle_discarded = safeOpenFile(self.out_rv_discarded, 'w')
            out_rv_writer_discarded = writefq(out_rv_handle_discarded)

        # Some counters
        cdef dict read_pair_counters = {
            'total_reads':0,
            'dropped_rv':0,
            'dropped_umi':0,
            'dropped_umi_template':0,
            'dropped_AT': 0,
            'dropped_GC':0,
            'dropped_adaptor':0,
            'to_short_after_trimming':0
        }
        cdef list chunk
        cdef dict read_pair

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: output files writer - starting to parse reads from queue.')
        while self.workers_running.value or not self.output_read_queue.empty():

            while not self.output_read_queue.empty():

                chunk = self.output_read_queue.get()
                for (discard_reason, header_rv, orig_sequence_rv, orig_quality_rv) in chunk:

                    read_pair_counters['total_reads'] += 1
                    if discard_reason:
                        read_pair_counters[ discard_reason ] += 1

                    # Write reverse read to output
                    if discard_reason:
                        read_pair_counters['dropped_rv'] += 1
                        if self.keep_discarded_files:
                            out_rv_writer_discarded.send((header_rv, orig_sequence_rv, orig_quality_rv))

                    count += 1
                    if self.verbose and count % self.stat_line_interwall == 0:
                        self.print_stat_line(start_time, last_time, count, last_count, identity)
                        last_time = time.time()
                        last_count = count
            #if self.verbose: self.logger.debug('InputReadsFilter::INFO:: output files writer - queue empty.')

        if self.verbose:
            self.print_stat_line(start_time, last_time, count, last_count, identity)
            last_time = time.time()
            last_count = count

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: output files writer - all reads parsed.')

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: output files writer - sending counter to parent process.')
        self.counter_connection_send_end.send(read_pair_counters)

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: output files writer - closing outfiles.')
        if self.keep_discarded_files:
            out_rv_handle_discarded.flush()
            out_rv_handle_discarded.close()
            out_rv_writer_discarded.close()

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: output files writer - completed.')

    def parallel_worker_function(self, ):
        """
        Worker function for the parallel worker processes
        Here read trimming is performed for the chunks from the input_files_reader
        and trimmed data is written to the output bam files
        """

        start_time = time.time()
        count = 0
        last_time = start_time
        last_count = count
        identity = 'WORKER_'+str(os.getpid())

        if self.verbose:
            self.logger.debug('InputReadsFilter::INFO:: Starting parallel worker process pid={}.'.format(os.getpid()))

        if self.verbose:
            self.logger.debug(
            'InputReadsFilter::INFO:: parallel worker process pid={} - starting to parse reads.'.format(os.getpid())
            )
        
        bam_header = {
                'HD': {'VN': '1.5', 'SO':'unsorted'},
                'RG': [{'ID': '0', 'SM' : 'unknown_sample', 'PL' : 'ILLUMINA' }]
            }
        bam_file = pysam.AlignmentFile(self.out_rv.rstrip('.bam')+'.{}.bam'.format(identity), "wbu", header=bam_header)

        while self.reader_running.value or not self.input_read_queue.empty():

            while not self.input_read_queue.empty():

                try:
                    in_chunk = self.input_read_queue.get(timeout=10)
                except Queue.Empty: continue
                out_chunk = []
                for (header_fw, sequence_fw, quality_fw), (header_rv, sequence_rv, quality_rv) in in_chunk:

                    discard_reason = None
                    orig_sequence_rv, orig_quality_rv = sequence_rv, quality_rv

                    if not sequence_fw or not sequence_rv:
                        error = "Error doing quality trimming, Checks of raw reads.\n" \
                        "The input files are not of the same length"
                        #"The input files {},{} are not of the same length".format(fw,rv)
                        self.logger.error(error)

                    if header_fw.split()[0] != header_rv.split()[0]:
                        self.logger.warning("Pair reads found with different " \
                                       "names {} and {}".format(header_fw,header_rv))

                    # get the barcode sequence
                    barcode = sequence_fw[max(0,self.start_position-self.overhang):(self.start_position+self.barcode_length+self.overhang)]

                    # If we want to check for UMI quality and the UMI is incorrect
                    # then we discard the reads
                    umi_seq = sequence_fw[self.umi_start:self.umi_end]
                    if self.umi_filter \
                    and not check_umi_template(umi_seq, self.umi_filter_template):
                        discard_reason = 'dropped_umi_template'

                    # Check if the UMI has many low quality bases
                    umi_qual=quality_fw[self.umi_start:self.umi_end]
                    if not discard_reason and (self.umi_end - self.umi_start) >= self.umi_quality_bases and \
                    len([b for b in umi_qual if (ord(b) - self.phred) < self.min_qual]) > self.umi_quality_bases:
                        discard_reason = 'dropped_umi'

                    # If reverse read has a high AT content discard...
                    if not discard_reason and self.do_AT_filter and \
                    ((sequence_rv.count("A") + sequence_rv.count("T")) / len(sequence_rv)) * 100 >= self.filter_AT_content:
                        discard_reason = 'dropped_AT'

                    # If reverse read has a high GC content discard...
                    if not discard_reason and self.do_GC_filter and \
                    ((sequence_rv.count("G") + sequence_rv.count("C")) / len(sequence_rv)) * 100 >= self.filter_GC_content:
                        discard_reason = 'dropped_GC'

                    if not discard_reason:

                        if self.do_adaptorA and len(sequence_rv) > self.min_length:
                            sequence_rv, quality_rv = removeAdaptor(
                                sequence_rv, quality_rv, self.adaptorA, self.adaptor_missmatches)
                        if self.do_adaptorT and len(sequence_rv) > self.min_length:
                            sequence_rv, quality_rv = removeAdaptor(
                                sequence_rv, quality_rv, self.adaptorT, self.adaptor_missmatches)
                        if self.do_adaptorG and len(sequence_rv) > self.min_length:
                            sequence_rv, quality_rv = removeAdaptor(
                                sequence_rv, quality_rv, self.adaptorG, self.adaptor_missmatches)
                        if self.do_adaptorC and len(sequence_rv) > self.min_length:
                            sequence_rv, quality_rv = removeAdaptor(
                                sequence_rv, quality_rv, self.adaptorC, self.adaptor_missmatches)
                        if self.do_adaptorN and len(sequence_rv) > self.min_length:
                            sequence_rv, quality_rv = removeAdaptor(
                                sequence_rv, quality_rv, self.adaptorN, self.adaptor_missmatches)

                        # Check if the read is smaller than the minimum after removing artifacts
                        if len(sequence_rv) < self.min_length:
                            discard_reason = 'dropped_adaptor'
                        else:
                            # Trim reverse read (will return None if length of trimmed sequence is less than min_length)
                            sequence_rv, quality_rv = trim_quality(
                                                        sequence_rv,
                                                        quality_rv,
                                                        self.min_qual,
                                                        self.min_length,
                                                        self.phred)
                            if not sequence_rv or not quality_rv:
                                discard_reason = 'to_short_after_trimming'

                    if not discard_reason:
                        bam_file.write(
                            convert_to_AlignedSegment(
                                header_rv,
                                sequence_rv,
                                quality_rv,
                                barcode,
                                umi_seq
                                )
                            )
                        out_chunk.append( (discard_reason, None, None, None) )
                    else:
                        out_chunk.append( (discard_reason, header_rv, orig_sequence_rv, orig_quality_rv) )

                    count += 1
                    if self.verbose and count % self.stat_line_interwall == 0:
                        self.print_stat_line(start_time, last_time, count, last_count, identity)
                        last_time = time.time()
                        last_count = count

                self.output_read_queue.put( out_chunk )
            # if self.verbose:
            #    self.logger.debug(
            #       'InputReadsFilter::INFO:: parallel worker process pid='+str(os.getpid())+' - queue empty.')

        if self.verbose:
            self.print_stat_line(start_time, last_time, count, last_count, identity)
            last_time = time.time()
            last_count = count
        bam_file.close()
        if self.verbose:
            self.logger.debug(
                'InputReadsFilter::INFO:: parallel worker process pid={} - completed.'.format(os.getpid())
                )

    def print_stat_line(self, start_time, last_time, count, last_count, identity, header=False):
        """
        Function that prints a "current status" row to stderr
        """

        if header:
            self.logger.debug('PROCESS\tREADSPROCESSED\tTIME (s)\tAV_SPEED (reads/s)\tCU_SPEED (reads/s)')

        self.logger.debug(
                str(identity)+'\t'+\
                str(count)+'\t'+\
                str(round(time.time()-start_time,3))+'\t'+\
                str(round(count/(time.time()-start_time),2))+'\t'+\
                str(round((count-last_count)/(time.time()-last_time),2))+''
            )