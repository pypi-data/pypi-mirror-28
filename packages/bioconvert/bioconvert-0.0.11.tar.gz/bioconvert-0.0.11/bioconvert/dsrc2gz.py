# -*- coding: utf-8 -*-
##############################################################################
#  This file is part of Bioconvert software
#
#  Copyright (c) 2017 - Bioconvert Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/biokit/bioconvert
#  documentation: http://bioconvert.readthedocs.io
##############################################################################
""" Convert a compressed fastq.gz file to :term:`DSRC` compression format """

from bioconvert import ConvBase
import colorlog
logger = colorlog.getLogger(__name__)


__all__ = ["DSRC2GZ"]


class DSRC2GZ(ConvBase):
    """Convert compressed fastq.dsrc file into fastq.gz compressed file

    .. plot::

         from bioconvert.dsrc2gz import DSRC2GZ
         from bioconvert import bioconvert_data
         from easydev import TempFile

         with TempFile(suffix=".gz") as fh:
             infile = bioconvert_data("test_SP1.fq.dsrc")
             convert = DSRC2GZ(infile, fh.name)
             convert.boxplot_benchmark()

    """
    input_ext = [".dsrc"]
    output_ext = [".gz"]

    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile: input DSRC filename
        :param str outfile: output GZ filename

        """
        super(DSRC2GZ, self).__init__(infile, outfile, *args, **kargs)
        self._default_method = "dsrcpigz"

    def _method_dsrcpigz(self, *args, **kwargs):
        """
        do the conversion dsrc -> :term:'GZ`
        """
        cmd = "dsrc d -s -t {threads} {input} | pigz -c -p {threads} > {output}"
        self.execute(cmd.format(
            threads=self.threads,
            input=self.infile,
            output=self.outfile))


