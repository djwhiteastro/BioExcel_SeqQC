#!/usr/bin/env python

"""
This script performs the full Sequence Quality Control step of the Cancer
Genome Variant pipeline, controlling the processes and
decision making for each step.
"""

import runFastQC as rfqc
import checkFastQC as cfqc
import seqqcUtils as sqcu

if __name__ == "__main__":

    description = ("This script performs the Sequence "
                "Quality Control step of the Cancer Genome Variant pipeline.")

    args = sqcu.parse_command_line(description)
    args = sqcu.make_paths(args)
    args.files = sqcu.get_files(args)

    ### Run FastQC
    pfqc = rfqc.run_fqc(args, args.fqcdir1, args.files)
    pfqc.wait()

    ### Check FastQC output, simple yes/no to quality trimming
    ### Output and resubmission of jobs handled by checkFastQC
    cfqc.check_qc(args)
