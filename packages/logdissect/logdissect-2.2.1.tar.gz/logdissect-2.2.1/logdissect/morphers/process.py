# MIT License
# 
# Copyright (c) 2017 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from logdissect.morphers.type import MorphModule as OurModule
from logdissect.data import LogEntry
from logdissect.data import LogData

class MorphModule(OurModule):
    def __init__(self, args):
        """Initialize the process morphing module"""
        self.name = "process"
        self.desc = "match a source process"

        args.add_argument('--process', action='append', dest='process',
                help='match a source process')

    def morph_data(self, data, args):
        """Return entries from specified process (single log)"""
        if not args.process:
            return data
        else:
            newdata = LogData()
            newdata.source_path = data.source_path
            newdata.source_file = data.source_file
            newdata.source_file_mtime = data.source_file_mtime
            newdata.parser = data.parser

            for entry in data.entries:
                for p in args.process:
                    if entry.source_process == p:
                        newdata.entries.append(entry)
                        break

            return newdata
