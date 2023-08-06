#!/usr/bin/env python

# Copyright (c) 2017, DIANA-HEP
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

import codecs
import sys

import numpy

import oamap.generator

class _GenerateBytes(object):
    py3 = sys.version_info[0] >= 3

    def _generatebytes(self, arrays, index, cache):
        if self.schema.nullable:
            mask = cache.arraylist[self.generic.maskidx]
            if mask is None:
                self._getarrays(arrays,
                                cache,
                                {self.generic.mask: self.generic.maskidx},
                                {self.generic.mask: self.generic.maskdtype},
                                {self.generic.mask: ()},
                                {self.generic.mask: oamap.generator.MASK})
                mask = cache.arraylist[self.generic.maskidx]

            value = mask[index]
            if value == self.generic.maskedvalue:
                return None
            else:
                index = value

        listgen = self.generic
        primgen = self.generic.content

        starts = cache.arraylist[listgen.startsidx]
        stops  = cache.arraylist[listgen.stopsidx]
        data   = cache.arraylist[primgen.dataidx]
        if starts is None or stops is None or data is None:
            self._getarrays(arrays,
                            cache,
                            {listgen.starts: listgen.startsidx,      listgen.stops: listgen.stopsidx,      primgen.data: primgen.dataidx},
                            {listgen.starts: listgen.posdtype,       listgen.stops: listgen.posdtype,      primgen.data: primgen.dtype},
                            {listgen.starts: (),                     listgen.stops: (),                    primgen.data: ()},
                            {listgen.starts: oamap.generator.STARTS, listgen.stops: oamap.generator.STOPS, primgen.data: oamap.generator.DATA})
            starts = cache.arraylist[listgen.startsidx]
            stops  = cache.arraylist[listgen.stopsidx]
            data   = cache.arraylist[primgen.dataidx]

        array  = data[starts[index]:stops[index]]

        if isinstance(array, numpy.ndarray):
            return array.tostring()
        elif self.py3:
            return bytes(array)
        else:
            return "".join(map(chr, array))

    def degenerate(self, obj):
        if obj is None:
            return obj

        elif self.py3:
            if isinstance(obj, bytes):
                return obj
            else:
                return codecs.utf_8_encode(obj)[0]

        else:
            if isinstance(obj, str):
                return map(ord, obj)
            else:
                return map(ord, codecs.utf_8_encode(obj)[0])

class ByteStringGenerator(_GenerateBytes, oamap.generator.ExtendedGenerator):
    pattern = {"name": "ByteString", "type": "list", "content": {"type": "primitive", "dtype": "uint8", "dims": [], "nullable": False}}

    def _generate(self, arrays, index, cache):
        return self._generatebytes(arrays, index, cache)
            
class UTF8StringGenerator(_GenerateBytes, oamap.generator.ExtendedGenerator):
    pattern = {"name": "UTF8String", "type": "list", "content": {"type": "primitive", "dtype": "uint8", "dims": [], "nullable": False}}

    def _generate(self, arrays, index, cache):
        out = self._generatebytes(arrays, index, cache)
        if out is None:
            return out
        else:
            return codecs.utf_8_decode(out)[0]
