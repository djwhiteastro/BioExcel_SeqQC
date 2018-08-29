#!/usr/bin/env python

"""
This script contains several utility functions for use with the SeqQC portion
of the IGMM Cancer Genome Sequencing workflow developed as part of BioExcel
"""

import os
import sys
import argparse
import yaml
import shutil

def parse_command_line(description):
    """
    Parser of command line arguments for SeqQC.py
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--printconfig", action='store_true',
                        help="Print example config file in current directory")
    
    opts, other = parser.parse_known_args()
    if opts.printconfig:
        return opts
    
    parser.add_argument("-f", "--files", nargs=2, required=True,
                            help="Pair of input FastQ files.")
    parser.add_argument("-o", "--outdir", default='./',
                        help="Output directory.")
    parser.add_argument("-a", "--adaptseq", type=str,
        default='AATGATACGGCGACCACCGAGATCTACACTCTTTCCCTACACGACGCTCTTCCGATCT',
                        help="The adapter sequence to be trimmed from the "
                        "FastQ file.")
    parser.add_argument("--trim", type=str, default='full',
                        choices=['full', 'adapt', 'qual'],
                        help="The type of trimming to be done on the paired "
                        "sequences: adapter or quality trimming, or full/both. "
                        "WARNING: For standalone execution of runTrim.py only!")
    parser.add_argument("-c", "--config", type=str, 
        default='', help="Location of config file, defaults to internal file"
                )
    return parser.parse_args()

def make_paths(arglist):
    """
    Create paths required for run of SeqQC pipeline
    """
    arglist.tmpdir = os.path.abspath("{0}/tmp".format(arglist.outdir))
    arglist.fqcdir = os.path.abspath("{0}/FastQC_out".format(
                                                            arglist.outdir))
    arglist.fqcdir2 = os.path.abspath("{0}/FastQC_out/2ndpass".format(
                                                            arglist.outdir))
    arglist.trimdir = os.path.abspath("{0}/Trim_out".format(arglist.outdir))
    arglist.outdir = os.path.abspath(arglist.outdir)

    for dirpath in [arglist.tmpdir, arglist.fqcdir2,
                                arglist.trimdir, arglist.outdir]:
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
    return arglist

def get_files(arglist):
    """
    Return list of files to pass through SeqQC pipeline, throws error
    """

    # make sure files exist
    for checkfile in arglist.files:
        if not os.path.isfile(checkfile):
            sys.exit("Error: Input file {} does not exist.".format(checkfile))
    # expand paths to files (now we know the all exist)
    infiles = [os.path.abspath(x) for x in arglist.files]
    return infiles

def get_config(configfile):
    """
    Read decision configuration of CheckFastQC portion of workflow
    """
    if not configfile: # Read internal file
        basepath = (os.path.dirname(__file__))
        config = yaml.safe_load(open(basepath+'/config.yml'))
    else:
        config = yaml.safe_load(open(configfile))

    return config

def print_config():
    basepath = (os.path.dirname(__file__))
    config = basepath+'/config.yml'
    shutil.copy(config,'./')
