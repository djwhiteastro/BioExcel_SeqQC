#!/usr/bin/env python

"""
This script runs the Trim step of SeqQC. The script opens a
cutadapt process with the correct parameters.
"""

import shlex
import subprocess as sp
import bioexcel_seqqc.seqqcutils as sqcu

def trimAdapt(infiles, trimdir, adaptseq, threads):
    """
    Create and run subprocess for running cutadapt to remove adapter sequences
    from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    sqcu.make_paths(trimdir)
    out1 = "{0}/ATrimmed1.fastq.gz".format(trimdir)
    out2 = "{0}/ATrimmed2.fastq.gz".format(trimdir)

    command = "cutadapt -a {0} -A {0} -o {1} -p {2} -j {3} "\
        "{4} {5}".format(adaptseq, out1, out2, threads, in1, in2)

    cmdargs = shlex.split(command)

    print("STAGE: Running cutadapt, adapter trimming.")
    print(command)

    p = sp.Popen(cmdargs)

    return p, out1, out2


def trimQC(infiles, trimdir, threads):
    """
    Create and run subprocess for running cutadapt to remove poor quality
    sequences from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    sqcu.make_paths(trimdir)
    out1 = "{0}/QCTrimmed1.fastq.gz".format(trimdir)
    out2 = "{0}/QCTrimmed2.fastq.gz".format(trimdir)

    command = "cutadapt -q 20 -o {0} -p {1} \
                -j {2} {3} {4} ".format(out1, out2, threads, in1, in2)

    cmdargs = shlex.split(command)

    print("STAGE: Running cutadapt, quality trimming.")
    print(command)

    p = sp.Popen(cmdargs)

    return p, out1, out2

def trimFull(infiles, trimdir, adaptseq, threads):
    """
    Create and run subprocess for running cutadapt to remove poor quality
    sequences from sequencing data.
    """

    in1 = infiles[0]
    in2 = infiles[1]

    sqcu.make_paths(trimdir)
    out1 = "{0}/Trimmed1.fastq.gz".format(trimdir)
    out2 = "{0}/Trimmed2.fastq.gz".format(trimdir)

    command = "cutadapt -q 20 -a {0} -A {0} -o {1} -p {2} \
                -j {3} {4} {5}".format(adaptseq, out1, out2, threads, in1, in2)

    cmdargs = shlex.split(command)

    print("STAGE: Running cutadapt, both quality and adapter trimming.")
    print(command)

    p = sp.Popen(cmdargs)

    return p, out1, out2

if __name__ == "__main__":
    description = ("This script runs the Trimming step of SeqQC")
    args = sqcu.parse_command_line(description)

    args.files = sqcu.get_files(args)

    if args.trim == 'F':
        ptrimfull, f1, f2 = trimFull(args.files, args.trimdir, args.adaptseq,
                                        args.threads)
        ptrimfull.wait()
    if args.trim == 'A':
        ptrimfull, f1, f2 = trimAdapt(args.files, args.trimdir, args.adaptseq,
                                        args.threads)
        ptrimfull.wait()
    if args.trim == 'Q':
        ptrimfull, f1, f2 = trimQC(args.files, args.trimdir, args.threads)
        ptrimfull.wait()
        