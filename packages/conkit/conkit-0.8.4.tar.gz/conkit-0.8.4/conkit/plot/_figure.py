# BSD 3-Clause License
#
# Copyright (c) 2016-17, University of Liverpool
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
A module containing generic Figure related objects
"""

__author__ = "Felix Simkovic"
__date__ = "07 Feb 2017"
__version__ = "0.1"

from conkit.core.contact import Contact
from conkit.core.contactmap import ContactMap
from conkit.core.contactfile import ContactFile
from conkit.core.sequence import Sequence
from conkit.core.sequencefile import SequenceFile


class Figure(object):
    """A Figure class to store common features

    Attributes
    ----------
    dpi : int
       Resolution in pixels per inch [default: 300]
    file_name : str
       The name of the figure file [default: conkit.png]
    format : str
       The format of the figure file [default: png]
    prefix : str
       The prefix of the figure file name [default: conkit]

    Warnings
    --------
    Do not instantiate this class directly. Instead use the 
    sub-classes designed for specific plots.

    """

    # From matplotlib.Figure.savefig documentation:
    #     One of the file extensions supported by the active
    #     backend. Most backends support png, pdf, ps, eps, svg and jpg.
    FORMATS = ('eps', 'jpg', 'pdf', 'png', 'ps', 'svg')

    def __init__(self, **kwargs):
        """Initialise a new :obj:`conkit.plot.Figure` object"""
        self._dpi = 300
        self._format = "png"
        self._prefix = "conkit"

        if "dpi" in kwargs:
            self.dpi = kwargs["dpi"]
        if "file_name" in kwargs:
            self.file_name = kwargs["file_name"]
        else:
            if "format" in kwargs:
                self.format = kwargs["format"]
            if "prefix" in kwargs:
                self.prefix = kwargs["prefix"]

    @property
    def dpi(self):
        """Resolution in pixels per inch"""
        return self._dpi

    @dpi.setter
    def dpi(self, dpi):
        """Define the resolution in pixels per inch"""
        self._dpi = dpi

    @property
    def file_name(self):
        """The name of the figure file

        This property is the combination of the properties
        ``Figure.prefix`` and ``Figure.format``.

        """
        return self._prefix + "." + self._format

    @file_name.setter
    def file_name(self, name):
        """Define the name of the figure file

        This property is split into the properties
        ``Figure.prefix`` and ``Figure.format``.

        """
        self.prefix, self.format = name.rsplit('.', 1)

    @property
    def format(self):
        """The format of the figure file"""
        return self._format

    @format.setter
    def format(self, format):
        """Define the format of the figure file

        Raises
        ------
        ValueError
           Figure format not supported

        """
        if format not in Figure.FORMATS:
            msg = "Figure format not supported, please use one of [ {0} ]".format(' | '.join(Figure.FORMATS))
            raise ValueError(msg)
        self._format = format

    @property
    def prefix(self):
        """The prefix of the figure file name"""
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Define the prefix of the figure file"""
        self._prefix = prefix

    @staticmethod
    def _check_hierarchy(h, t):
        """Check the hierarchy is of a specific type

        Raises
        ------
        TypeError
           Provided hierarchy is not of specified type
        ValueError
           Type is unknown

        """
        hdict = {'Contact': Contact, 'ContactMap': ContactMap, 'ContactFile': ContactFile,
                 'Sequence': Sequence, 'SequenceFile': SequenceFile}
        if t not in hdict.keys():
            raise ValueError("Type {0} is unknown".format(t))
        elif not isinstance(h, hdict[t]):
            raise TypeError("Provided hierarchy is not a {0}".format(t))

    @staticmethod
    def _correct_aspect(ax, aspect_ratio):
        """Adjust the aspect ratio"""
        # Credits to http://stackoverflow.com/q/4747051/3046533
        #     !!! Works only for non-logarithmic axes !!!
        default_ratio = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
        return float(default_ratio * aspect_ratio)
