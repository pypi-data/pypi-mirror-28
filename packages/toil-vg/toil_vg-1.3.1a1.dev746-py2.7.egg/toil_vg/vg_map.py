#!/usr/bin/env python2.7
"""
vg_map.py: map to vg graph producing gam for each chrom

"""
from __future__ import print_function
import argparse, sys, os, os.path, errno, random, subprocess, shutil, itertools, glob, tarfile
import doctest, re, json, collections, time, timeit
import logging, logging.handlers, SocketServer, struct, socket, threading
import string
import urlparse
import getpass
import pdb
import gzip
import logging

from math import ceil
from subprocess import Popen, PIPE

from toil.common import Toil
from toil.job import Job
from toil.realtimeLogger import RealtimeLogger
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore

logger = logging.getLogger(__name__)

def map_subparser(parser):
    """
    Create a subparser for mapping.  Should pass in results of subparsers.add_parser()
    """

    # Add the Toil options so the job store is the first argument
    Job.Runner.addToilOptions(parser)
    
    # General options
    
    parser.add_argument("sample_name", type=str,
        help="sample name (ex NA12878)")
    parser.add_argument("xg_index", type=make_url,
        help="Path to xg index")    
    parser.add_argument("gcsa_index", type=make_url,
        help="Path to GCSA index")
    parser.add_argument("out_store",
        help="output store.  All output written here. Path specified using same syntax as toil jobStore")
    parser.add_argument("--id_ranges", type=str, default=None,
        help="Path to file with node id ranges for each chromosome in BED format.")
    parser.add_argument("--kmer_size", type=int,
        help="size of kmers to use in gcsa-kmer mapping mode")

    # Add common options shared with everybody
    add_common_vg_parse_args(parser)

    # Add mapping options
    map_parse_args(parser)

    # Add common docker options
    add_container_tool_parse_args(parser)


def map_parse_args(parser, stand_alone = False):
    """ centralize indexing parameters here """
    parser.add_argument("--gbwt_index", type=make_url,
                        help="Path to GBWT haplotype index")
    parser.add_argument("--fastq", nargs='+', type=make_url,
                        help="Input fastq (possibly compressed), two are allowed, one for each mate")
    parser.add_argument("--gam_input_reads", type=make_url, default=None,
                        help="Input reads in GAM format")
    parser.add_argument("--bam_input_reads", type=make_url, default=None,
                        help="Input reads in BAM format")
    parser.add_argument("--single_reads_chunk", action="store_true", default=False,
                        help="do not split reads into chunks")
    parser.add_argument("--reads_per_chunk", type=int,
                        help="number of reads for each mapping job")
    parser.add_argument("--alignment_cores", type=int,
                        help="number of threads during the alignment step")
    parser.add_argument("--gam_index_cores", type=int,
                        help="number of threads used for gam indexing")    
    parser.add_argument("--interleaved", action="store_true", default=False,
                        help="treat fastq as interleaved read pairs.  overrides map-args")
    parser.add_argument("--map_opts", type=str,
                        help="arguments for vg map (wrapped in \"\")")
    parser.add_argument("--multipath", action="store_true",
                        help="use vg mpmap instead of vg map")
    parser.add_argument("--mpmap_opts", type=str,
                        help="arguments for vg mpmap (wrapped in \"\")")
    

def validate_map_options(context, options):
    """
    Throw an error if an invalid combination of options has been selected.
    """                               
    require(options.fastq is None or len(options.fastq) in [1, 2], 'Exacty 1 or 2 files must be'
            ' passed with --fastq')
    require(options.interleaved == False or options.fastq is None or len(options.fastq) == 1,
            '--interleaved cannot be used when > 1 fastq given')
    require(sum(map(lambda x : 1 if x else 0, [options.fastq, options.gam_input_reads, options.bam_input_reads])) == 1,
            'reads must be speficied with either --fastq or --gam_input_reads or --bam_input_reads')
    if options.multipath:
        require('-S' in context.config.mpmap_opts,
                '-S must be used with multipath aligner to produce GAM output')
    
def run_mapping(job, context, fastq, gam_input_reads, bam_input_reads, sample_name, interleaved, multipath,
                xg_file_id, gcsa_and_lcp_ids, gbwt_file_id, id_ranges_file_id, reads_file_ids):
    """ split the fastq, then align each chunk.  returns outputgams, paired with total map time
    (excluding toil-vg overhead such as transferring and splitting files )"""

    # to encapsulate everything under this job
    child_job = Job()
    job.addChild(child_job)

    if not context.config.single_reads_chunk:
        reads_chunk_ids = child_job.addChildJobFn(run_split_reads, context, fastq, gam_input_reads, bam_input_reads,
                                                  reads_file_ids,
                                                  cores=context.config.misc_cores, memory=context.config.misc_mem,
                                                  disk=context.config.misc_disk).rv()
    else:
        RealtimeLogger.info("Bypassing reads splitting because --single_reads_chunk enabled")
        reads_chunk_ids = [[r] for r in reads_file_ids]
        
    return child_job.addFollowOnJobFn(run_whole_alignment, context, fastq, gam_input_reads, bam_input_reads, sample_name,
                                      interleaved, multipath, xg_file_id, gcsa_and_lcp_ids, gbwt_file_id,
                                      id_ranges_file_id, reads_chunk_ids, cores=context.config.misc_cores,
                                      memory=context.config.misc_mem, disk=context.config.misc_disk).rv()    

def run_split_reads(job, context, fastq, gam_input_reads, bam_input_reads, reads_file_ids):
    """
    split either fastq or gam input reads into chunks.  returns list of chunk file id lists
    (one for each input reads file)
    """

    # this is a list of lists: one list of chunks for each input reads file
    reads_chunk_ids = []
    if fastq and len(fastq):
        for fastq_i, reads_file_id in enumerate(reads_file_ids):
            reads_chunk_ids.append(job.addChildJobFn(run_split_fastq, context, fastq, fastq_i, reads_file_id,
                                                     cores=context.config.fq_split_cores,
                                                     memory=context.config.fq_split_mem, disk=context.config.fq_split_disk).rv())
    elif gam_input_reads:
        assert len(reads_file_ids) == 1
        reads_chunk_ids.append(job.addChildJobFn(run_split_gam_reads, context, gam_input_reads, reads_file_ids[0],
                                                  cores=context.config.fq_split_cores,
                                                  memory=context.config.fq_split_mem, disk=context.config.fq_split_disk).rv())
    else:
        assert bam_input_reads
        assert len(reads_file_ids) == 1
        reads_chunk_ids.append(job.addChildJobFn(run_split_bam_reads, context, bam_input_reads, reads_file_ids[0],
                                                  cores=context.config.fq_split_cores,
                                                  memory=context.config.fq_split_mem, disk=context.config.fq_split_disk).rv())
        
    return reads_chunk_ids


def run_split_fastq(job, context, fastq, fastq_i, sample_fastq_id):
    
    RealtimeLogger.info("Starting fastq split")
    start_time = timeit.default_timer()
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # We need the sample fastq for alignment
    fastq_path = os.path.join(work_dir, os.path.basename(fastq[fastq_i]))
    fastq_gzipped = os.path.splitext(fastq_path)[1] == '.gz'
    job.fileStore.readGlobalFile(sample_fastq_id, fastq_path)

    # Split up the fastq into chunks

    # Make sure chunk size even in case paired interleaved
    chunk_size = context.config.reads_per_chunk
    if chunk_size % 2 != 0:
        chunk_size += 1

    # 4 lines per read
    chunk_lines = chunk_size * 4

    # Note we do this on the command line because Python is too slow
    uc_fastq_name = fastq_path if not fastq_gzipped else 'input_reads.fq'
    if fastq_gzipped:
        cmd = [['gzip', '-d', '-c', os.path.basename(fastq_path)]]
    else:
        cmd = [['cat', os.path.basename(fastq_path)]]

    cmd.append(['split', '-l', str(chunk_lines),
                '--filter=pigz -p {} > $FILE.fq.gz'.format(max(1, int(context.config.fq_split_cores) - 1)),
                '-', 'fq_chunk.'])

    context.runner.call(job, cmd, work_dir = work_dir, tool_name='pigz')

    fastq_chunk_ids = []
    for chunk_name in os.listdir(work_dir):
        if chunk_name.endswith('.fq.gz') and chunk_name.startswith('fq_chunk'):
            fastq_chunk_ids.append(context.write_intermediate_file(job, os.path.join(work_dir, chunk_name)))
        
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info("Split fastq into {} chunks. Process took {} seconds.".format(len(fastq_chunk_ids), run_time))

    return fastq_chunk_ids

def run_split_gam_reads(job, context, gam_input_reads, gam_reads_file_id):
    """ split up an input reads file in GAM format
    """
    RealtimeLogger.info("Starting gam split")
    start_time = timeit.default_timer()
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # We need the sample fastq for alignment
    gam_path = os.path.join(work_dir, os.path.basename(gam_input_reads))
    job.fileStore.readGlobalFile(gam_reads_file_id, gam_path)

    # Split up the gam into chunks

    # Make sure chunk size even in case paired interleaved
    chunk_size = context.config.reads_per_chunk
    if chunk_size % 2 != 0:
        chunk_size += 1

    # 1 line per read
    chunk_lines = chunk_size * 1

    cmd = [['vg', 'view', '-a', os.path.basename(gam_path)]]
    cmd.append(['split', '-l', str(chunk_lines),
                '--filter=vg view -JaG - > $FILE.gam', '-', 'gam_reads_chunk.'])

    context.runner.call(job, cmd, work_dir = work_dir)

    gam_chunk_ids = []
    for chunk_name in os.listdir(work_dir):
        if chunk_name.endswith('.gam') and chunk_name.startswith('gam_reads_chunk'):
            gam_chunk_ids.append(context.write_intermediate_file(job, os.path.join(work_dir, chunk_name)))
        
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info("Split gam into {} chunks. Process took {} seconds.".format(len(gam_chunk_ids), run_time))

    return gam_chunk_ids

def run_split_bam_reads(job, context, bam_input_reads, bam_reads_file_id):
    """ split up an input reads file in BAM format
    """
    RealtimeLogger.info("Starting bam split")
    start_time = timeit.default_timer()
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # We need the sample fastq for alignment
    bam_path = os.path.join(work_dir, os.path.basename(bam_input_reads))
    job.fileStore.readGlobalFile(bam_reads_file_id, bam_path)

    # Split up the bam into chunks

    # Make sure chunk size even in case paired interleaved
    chunk_size = context.config.reads_per_chunk
    if chunk_size % 2 != 0:
        chunk_size += 1

    # 1 line per read
    chunk_lines = chunk_size * 1

    cmd = [['samtools', 'view', '-h', os.path.basename(bam_path)]]
    cmd.append(['split', '-l', str(chunk_lines),
                '--filter=samtools view -h -O BAM - > $FILE.bam', '-', 'bam_reads_chunk.'])

    context.runner.call(job, cmd, work_dir = work_dir)

    bam_chunk_ids = []
    for chunk_name in os.listdir(work_dir):
        if chunk_name.endswith('.bam') and chunk_name.startswith('bam_reads_chunk'):
            bam_chunk_ids.append(context.write_intermediate_file(job, os.path.join(work_dir, chunk_name)))
        
    end_time = timeit.default_timer()
    run_time = end_time - start_time
    RealtimeLogger.info("Split bam into {} chunks. Process took {} seconds.".format(len(bam_chunk_ids), run_time))

    return bam_chunk_ids

    
def run_whole_alignment(job, context, fastq, gam_input_reads, bam_input_reads, sample_name, interleaved, multipath,
                        xg_file_id, gcsa_and_lcp_ids, gbwt_file_id, id_ranges_file_id, reads_chunk_ids):
    """ align all fastq chunks in parallel
    """
    
    # this will be a list of lists.
    # gam_chunk_file_ids[i][j], will correspond to the jth path (from id_ranges)
    # for the ith gam chunk (generated from fastq shard i)
    gam_chunk_file_ids = []
    gam_chunk_running_times = []

    # to encapsulate everything under this job
    child_job = Job()
    job.addChild(child_job)

    for chunk_id, chunk_filename_ids in enumerate(zip(*reads_chunk_ids)):
        #Run graph alignment on each fastq chunk
        chunk_alignment_job = child_job.addChildJobFn(run_chunk_alignment, context, gam_input_reads, bam_input_reads,
                                                      sample_name,
                                                      interleaved, multipath, chunk_filename_ids, chunk_id,
                                                      xg_file_id, gcsa_and_lcp_ids, gbwt_file_id, id_ranges_file_id,
                                                      cores=context.config.alignment_cores, memory=context.config.alignment_mem,
                                                      disk=context.config.alignment_disk)
        gam_chunk_file_ids.append(chunk_alignment_job.rv(0))
        gam_chunk_running_times.append(chunk_alignment_job.rv(1))

    return child_job.addFollowOnJobFn(run_merge_gams, context, sample_name, id_ranges_file_id, gam_chunk_file_ids,
                                      gam_chunk_running_times,
                                      cores=context.config.misc_cores,
                                      memory=context.config.misc_mem, disk=context.config.misc_disk).rv()


def run_chunk_alignment(job, context, gam_input_reads, bam_input_reads, sample_name, interleaved, multipath,
                        chunk_filename_ids,
                        chunk_id, xg_file_id, gcsa_and_lcp_ids, gbwt_file_id, id_ranges_file_id):

    RealtimeLogger.info("Starting {}alignment on {} chunk {}".format(
        "multipath " if multipath else "", sample_name, chunk_id))

    # How long did the alignment take to run, in seconds?
    run_time = None
    
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()

    # Download local input files from the remote storage container
    graph_file = os.path.join(work_dir, "graph.vg")

    xg_file = graph_file + ".xg"
    job.fileStore.readGlobalFile(xg_file_id, xg_file)
    gcsa_file = graph_file + ".gcsa"
    gcsa_file_id = gcsa_and_lcp_ids[0]
    job.fileStore.readGlobalFile(gcsa_file_id, gcsa_file)
    lcp_file = gcsa_file + ".lcp"
    lcp_file_id = gcsa_and_lcp_ids[1]
    job.fileStore.readGlobalFile(lcp_file_id, lcp_file)
    
    if gbwt_file_id:
        # We have a GBWT haplotype index available.
        gbwt_file =  graph_file + ".gbwt"
        job.fileStore.readGlobalFile(gbwt_file_id, gbwt_file)
    else:
        gbwt_file = None
    
    # We need the sample reads (fastq(s) or gam) for alignment
    reads_files = []
    reads_ext = 'gam' if gam_input_reads else 'bam' if bam_input_reads else 'fq.gz'
    for j, chunk_filename_id in enumerate(chunk_filename_ids):
        reads_file = os.path.join(work_dir, 'reads_chunk_{}_{}.{}'.format(chunk_id, j, reads_ext))
        job.fileStore.readGlobalFile(chunk_filename_id, reads_file)
        reads_files.append(reads_file)
    
    # And a temp file for our aligner output
    output_file = os.path.join(work_dir, "{}_{}.gam".format(sample_name, chunk_id))

    # Open the file stream for writing
    with open(output_file, "w") as alignment_file:

        # Start the aligner and have it write to the file

        # Plan out what to run
        vg_parts = []
        
        # toggle multipath here
        if multipath:
            vg_parts += ['vg', 'mpmap']
            vg_parts += context.config.mpmap_opts
            if '-S' not in vg_parts and '--single-path-mode' not in vg_parts:
                RealtimeLogger.warning('Adding --single-path-mode to mpmap options as only GAM output supported')
                vg_parts += ['--single-path-mode']
        else:
            vg_parts += ['vg', 'map'] 
            vg_parts += context.config.map_opts
            
        for reads_file in reads_files:
            input_flag = '-G' if gam_input_reads else '-b' if bam_input_reads else '-f'
            vg_parts += [input_flag, os.path.basename(reads_file)]
        vg_parts += ['-t', str(context.config.alignment_cores)]

        # Override the -i flag in args with the --interleaved command-line flag
        if interleaved is True and '-i' not in vg_parts and '--interleaved' not in vg_parts:
            vg_parts += ['-i']
        elif interleaved is False and 'i' in vg_parts:
            del vg_parts[vg_parts.index('-i')]
        if interleaved is False and '--interleaved' in vg_parts:
            del vg_parts[vg_parts.index('--interleaved')]

        vg_parts += ['-x', os.path.basename(xg_file), '-g', os.path.basename(gcsa_file)]
        if gbwt_file is not None and not multipath:
            # We have a GBWT haplotype index to use (and we know how to use it)
            vg_parts += ['--gbwt-name', os.path.basename(gbwt_file)]

        RealtimeLogger.info(
            "Running VG for {} against {}: {}".format(sample_name, graph_file,
            " ".join(vg_parts)))
        
        # Mark when we start the alignment
        start_time = timeit.default_timer()
        command = vg_parts
        try:
            context.runner.call(job, command, work_dir = work_dir, outfile=alignment_file)
        except:
            # Dump everything we need to replicate the alignment
            context.write_output_file(job, xg_file)
            context.write_output_file(job, gcsa_file)
            context.write_output_file(job, gcsa_file + '.lcp')
            for reads_file in reads_files:
                context.write_output_file(job, reads_file)
            
            raise
        
        # Mark when it's done
        end_time = timeit.default_timer()
        run_time = end_time - start_time

    paired_end = '-i' in vg_parts or '--interleaved' in vg_parts or len(chunk_filename_ids) > 1
    RealtimeLogger.info("Aligned {}. Process took {} seconds with {} vg-{}".format(
        output_file, run_time, 'paired-end' if paired_end else 'single-end',
        'mpmap' if multipath else 'map'))

    if id_ranges_file_id is not None:
        # Break GAM into multiple chunks at the end. So we need the file
        # defining those chunks.
        id_ranges_file = os.path.join(work_dir, 'id_ranges.tsv')
        job.fileStore.readGlobalFile(id_ranges_file_id, id_ranges_file)

        # Chunk the gam up by chromosome
        gam_chunks = split_gam_into_chroms(job, work_dir, context, xg_file, id_ranges_file, output_file)

        # Write gam_chunks to store
        gam_chunk_ids = []
        for gam_chunk in gam_chunks:
            gam_chunk_ids.append(context.write_intermediate_file(job, gam_chunk))

        return gam_chunk_ids, run_time
        
    else:
        # We can just report one chunk of everything
        return [context.write_intermediate_file(job, output_file)], run_time

def split_gam_into_chroms(job, work_dir, context, xg_file, id_ranges_file, gam_file):
    """
    Create a Rocksdb index then use it to split up the given gam file
    (a local path) into a separate gam for each chromosome.  
    Return a list of filenames.  the ith filename will correspond
    to the ith path in the options.path_name list
    """

    # transfer id ranges to N:M format for new vg chunk interface
    cid_ranges_file = os.path.join(work_dir, 'cid_ranges.txt')
    with open(cid_ranges_file, 'w') as ranges, open(id_ranges_file) as in_ranges:
        for line in in_ranges:
            toks = line.strip().split()
            if len(toks) == 3:
                ranges.write('{}:{}\n'.format(toks[1], toks[2]))
 
    # index on node positions
    output_index = gam_file + '.index'    
    index_cmd = ['vg', 'index', '-a', os.path.basename(gam_file),
                 '-d', os.path.basename(output_index), '-t', str(context.config.gam_index_cores)]
    context.runner.call(job, index_cmd, work_dir = work_dir)
        
    # Chunk the alignment into chromosomes using the id ranges
    # (note by using id ranges and 0 context and -a we avoid costly subgraph extraction)

    output_bed_name = os.path.join(work_dir, 'output_bed.bed')
    
    # Now run vg chunk on the gam index to get our gams
    # Note: using -a -c 0 -R bypasses subgraph extraction, which is important
    # as it saves a ton of time and memory
    chunk_cmd = ['vg', 'chunk', '-x', os.path.basename(xg_file),
                 '-a', os.path.basename(output_index), '-c', '0',
                 '-R', os.path.basename(cid_ranges_file),
                 '-b', os.path.splitext(os.path.basename(gam_file))[0],
                 '-t', str(context.config.alignment_cores),
                 '-E', os.path.basename(output_bed_name)]
    
    context.runner.call(job, chunk_cmd, work_dir = work_dir)
    
    # scrape up the vg chunk results into a list of paths to the output gam
    # chunks and return them.  we expect the filenames to be in the 4th column
    # of the output bed from vg chunk. 
    gam_chunks = []
    with open(output_bed_name) as output_bed:
        for line in output_bed:
            toks = line.split('\t')
            if len(toks) > 3:
                gam_chunks.append(os.path.join(work_dir, os.path.basename(toks[3].strip())))
                assert os.path.splitext(gam_chunks[-1])[1] == '.gam'

    return gam_chunks


def run_merge_gams(job, context, sample_name, id_ranges_file_id, gam_chunk_file_ids, gam_chunk_running_times):
    """
    Merge together gams, doing each chromosome in parallel
    """
    
    if id_ranges_file_id is not None:
        # Get the real chromosome names
        id_ranges = parse_id_ranges(job, id_ranges_file_id)
        chroms = [x[0] for x in id_ranges]
    else:
        # Dump everything in a single default chromosome chunk with a default
        # name
        chroms = ["default"]
    
    chr_gam_ids = []

    for i, chr in enumerate(chroms):
        shard_ids = [gam_chunk_file_ids[j][i] for j in range(len(gam_chunk_file_ids))]
        chr_gam_id = job.addChildJobFn(run_merge_chrom_gam, context, sample_name, chr, shard_ids,
                                       cores=context.config.fq_split_cores,
                                       memory=context.config.fq_split_mem,
                                       disk=context.config.fq_split_disk).rv()
        chr_gam_ids.append(chr_gam_id)

    total_running_time = 0
    for running_time in gam_chunk_running_times:
        if running_time is None:
            total_running_time = None
            break
        else:
            total_running_time += float(running_time)
    
    return chr_gam_ids, total_running_time


def run_merge_chrom_gam(job, context, sample_name, chr_name, chunk_file_ids):
    """
    Make a chromosome gam by merging up a bunch of gam ids, one 
    for each  shard.  
    """
    # Define work directory for docker calls
    work_dir = job.fileStore.getLocalTempDir()
    
    output_file = os.path.join(work_dir, '{}_{}.gam'.format(sample_name, chr_name))

    if len(chunk_file_ids) > 1:
        # Would be nice to be able to do this merge with fewer copies.. 
        with open(output_file, 'a') as merge_file:
            for chunk_gam_id in chunk_file_ids:
                tmp_gam_file = os.path.join(work_dir, 'tmp_{}.gam'.format(uuid4()))
                job.fileStore.readGlobalFile(chunk_gam_id, tmp_gam_file)
                with open(tmp_gam_file) as tmp_f:
                    shutil.copyfileobj(tmp_f, merge_file)
                
        chr_gam_id = context.write_intermediate_file(job, output_file)
    else:
        chr_gam_id = chunk_file_ids[0]
                
    # checkpoint to out store
    if len(chunk_file_ids) == 1:
        job.fileStore.readGlobalFile(chunk_file_ids[0], output_file)
    return context.write_output_file(job, output_file)

def map_main(context, options):
    """
    Wrapper for vg map. 
    """

    validate_map_options(context, options)
        
    # How long did it take to run the entire pipeline, in seconds?
    run_time_pipeline = None
        
    # Mark when we start the pipeline
    start_time_pipeline = timeit.default_timer()

    with context.get_toil(options.jobStore) as toil:
        if not toil.options.restart:

            start_time = timeit.default_timer()
            
            # Upload local files to the remote IO Store
            inputXGFileID = toil.importFile(options.xg_index)
            inputGCSAFileID = toil.importFile(options.gcsa_index)
            inputLCPFileID = toil.importFile(options.gcsa_index + ".lcp")
            if options.gbwt_index is not None:
                inputGBWTIndex = toil.importFile(options.gbwt_index)
            else:
                inputGBWTIndex = None
            if options.id_ranges is not None:
                inputIDRangesFileID = toil.importFile(options.id_ranges)
            else:
                inputIDRangesFileID = None
            inputReadsFileIDs = []
            if options.fastq:
                for sample_reads in options.fastq:
                    inputReadsFileIDs.append(toil.importFile(sample_reads))
            elif options.gam_input_reads:
                inputReadsFileIDs.append(toil.importFile(options.gam_input_reads))
            else:
                assert options.bam_input_reads
                inputReadsFileIDs.append(toil.importFile(options.bam_input_reads))
            end_time = timeit.default_timer()
            logger.info('Imported input files into Toil in {} seconds'.format(end_time - start_time))

            # Make a root job
            root_job = Job.wrapJobFn(run_mapping, context, options.fastq,
                                     options.gam_input_reads, options.bam_input_reads,
                                     options.sample_name,
                                     options.interleaved, options.multipath,
                                     inputXGFileID,
                                     (inputGCSAFileID, inputLCPFileID),
                                     inputGBWTIndex,
                                     inputIDRangesFileID, inputReadsFileIDs,
                                     cores=context.config.misc_cores,
                                     memory=context.config.misc_mem,
                                     disk=context.config.misc_disk)

            # Init the outstore
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context, sys.argv)
            init_job.addFollowOn(root_job)            
            
            # Run the job and store the returned list of output files to download
            toil.start(init_job)
        else:
            toil.restart()
            
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
 
    print("All jobs completed successfully. Pipeline took {} seconds.".format(run_time_pipeline))
    
