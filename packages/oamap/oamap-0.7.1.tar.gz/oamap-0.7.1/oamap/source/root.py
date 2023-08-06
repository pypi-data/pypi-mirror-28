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

import bisect
import numbers

import numpy

import oamap.schema
import oamap.generator
import oamap.source.packing
import oamap.util
from oamap.util import OrderedDict

try:
    import uproot
except ImportError:
    pass
else:
    uproot.tree.TTreeMethods.oamap = property(lambda self: TTreeMethods_oamap(self))

    class TTreeMethods_oamap(object):
        def __init__(self, tree):
            self.tree = tree
            self.cache = {}
            self.keycache = {}
            self.executor = None
            self.extension = None

            offsets = [0]
            for start, stop in self.tree.clusters():
                offsets.append(stop)
            self.offsets = offsets

        @property
        def offsets(self):
            return self._offsets

        @offsets.setter
        def offsets(self, value):
            try:
                out = []
                for x in value:
                    if not (isinstance(x, numbers.Integral) and x >= 0):
                        raise Exception
                    if len(out) > 0 and x <= out[-1]:
                        raise Exception
                    out.append(x)
                if len(out) == 0 or out[-1] > self.tree.numentries:
                    raise Exception
            except:
                raise ValueError("offsets must be a list of non-negative, strictly increasing integers, all less than or equal to numentries")

            self._offsets = value

        def _arrays(self, partitionid):
            entrystart, entrystop = self._offsets[partitionid], self._offsets[partitionid + 1]
            return self._ArrayDict(self, entrystart, entrystop)

        @property
        def dataset(self):
            return oamap.schema.Dataset(self.schema, extension=self.extension, partitioning=oamap.schema.Partitioning(""), name=self.tree.name, doc=self.tree.title)

        @property
        def schema(self):
            def frominterp(name, interpretation):
                if isinstance(interpretation, uproot.interp.asdtype):
                    if interpretation.todtype.names is None:
                        return oamap.schema.Primitive(interpretation.todtype, data=name)
                    else:
                        rec = oamap.schema.Record({})
                        for n in interpretation.todtype.names:
                            rec[n] = oamap.schema.Primitive(interpretation.todtype[n], data=(name + "/" + n))
                        return rec

                elif isinstance(interpretation, uproot.interp.asjagged):
                    if interpretation.asdtype.todtype.names is None:
                        return oamap.schema.List(oamap.schema.Primitive(interpretation.asdtype.todtype, data=name), starts=name, stops=name)
                    else:
                        rec = oamap.schema.Record({})
                        for n in interpretation.asdtype.todtype.names:
                            rec[n] = oamap.schema.Primitive(interpretation.asdtype.todtype[n], data=(name + "/" + n))
                        return oamap.schema.List(rec, starts=name, stops=name)

                elif isinstance(interpretation, uproot.interp.asstrings):
                    return oamap.schema.List(oamap.schema.Primitive("u1", data=name), starts=name, stops=name, name="ByteString")

                else:
                    raise NotImplementedError

            def recurse(parent):
                flats = []
                lists = OrderedDict()

                for name, branch in parent.items():
                    if len(branch.fLeaves) == 1 and branch.fLeaves[0].fLeafCount is not None:
                        leafcount = branch.fLeaves[0].fLeafCount
                        if leafcount not in lists:
                            lists[leafcount] = []
                        lists[leafcount].append((name, branch))
                    else:
                        flats.append((name, branch))

                out = oamap.schema.Record({})

                for name, branch in flats:
                    x = frominterp(name, uproot.interp.auto.interpret(branch))
                    if x is not None:
                        out[name.split(".")[-1]] = x

                for leafcount, namebranches in lists.items():
                    rec = oamap.schema.Record({})
                    for name, branch in namebranches:
                        x = frominterp(name, uproot.interp.auto.interpret(branch))
                        if x is not None:
                            assert isinstance(x, oamap.schema.List)
                            rec[name.split(".")[-1]] = x.content

                    found = False
                    for branchname, branch in self.tree.allitems():
                        if branch.fLeaves == [leafcount]:
                            found = True
                            break
                    if not found:
                        raise ValueError("could not find a single-leaf branch corresponding to leaf count {0}".format(leafcount))
                    
                    if len(rec.fields) > 0:
                        out[leafcount.fName.split(".")[-1]] = oamap.schema.List(rec, starts=branchname, stops=branchname)

                return out

            return oamap.schema.List(recurse(self.tree), starts="", stops="")

        def partition(self, partitionid):
            return self.schema(self._arrays(partitionid))

        def __iter__(self):
            for partitionid in range(len(self._offsets) - 1):
                for x in self.partition(partitionid):
                    yield x

        def __getitem__(self, index):
            if isinstance(index, slice):
                start, stop, step = oamap.util.slice2sss(index, self._offsets[-1])

                if start == self._offsets[-1]:
                    assert step > 0
                    assert stop == self._offsets[-1]
                    return oamap.proxy.PartitionedListProxy([])

                elif start == -1:
                    assert step < 0
                    assert stop == -1
                    return oamap.proxy.PartitionedListProxy([])

                else:
                    if step > 0:
                        firstid = bisect.bisect_right(self._offsets, start) - 1
                        lastid = bisect.bisect_right(self._offsets, stop) - 1
                        if stop > self._offsets[lastid]:
                            lastid += 1
                    else:
                        firstid = max(0, bisect.bisect_right(self._offsets, stop) - 1)
                        lastid = bisect.bisect_left(self._offsets, start)

                    partitions = []
                    offsets = []
                    for partitionid in range(firstid, lastid):
                        partitions.append(self.partition(partitionid))
                        offsets.append(self._offsets[partitionid])
                    offsets.append(self._offsets[lastid])

                    return oamap.proxy.PartitionedListProxy(partitions, offsets)[start:stop:step]

            else:
                normalindex = index if index >= 0 else index + self._offsets[-1]
                if not 0 <= normalindex < self._offsets[-1]:
                    raise IndexError("index {0} is out of bounds for size {1}".format(index, self._offsets[-1]))

                partitionid = bisect.bisect_right(self._offsets, normalindex) - 1
                localindex = normalindex - self._offsets[partitionid]
                return self.partition(partitionid)[localindex]

        class _ArrayDict(object):
            def __init__(self, parent, entrystart, entrystop):
                self.parent = parent
                self.entrystart = entrystart
                self.entrystop = entrystop

            def chop(self, name):
                try:
                    slashindex = name.rindex("/")
                except ValueError:
                    return str(name), None
                else:
                    return n[:slashindex], n[slashindex + 1 :]

            def getall(self, names):
                branchnames = []
                for name in names:
                    if len(name) > 0:
                        branchname, recarrayitem = self.chop(name)
                        if branchname not in branchnames:
                            branchnames.append(branchname)

                if len(branchnames) > 0:
                    arrays = self.parent.tree.arrays(branchnames, entrystart=self.entrystart, entrystop=self.entrystop, cache=self.parent.cache, keycache=self.parent.keycache, executor=self.parent.executor)
                else:
                    arrays = {}

                out = {}
                for name in names:
                    if len(name) == 0:
                        if isinstance(name, oamap.generator.StartsRole):
                            out[name] = numpy.array([0], dtype=oamap.generator.ListGenerator.posdtype)
                        elif isinstance(name, oamap.generator.StopsRole):
                            out[name] = numpy.array([self.entrystop - self.entrystart], dtype=oamap.generator.ListGenerator.posdtype)
                        else:
                            raise AssertionError

                    else:
                        branchname, recarrayitem = self.chop(name)
                        array = arrays[branchname]
                        
                        if isinstance(array, numpy.ndarray):
                            if isinstance(name, oamap.generator.StartsRole):
                                if name not in out:
                                    starts, stops = oamap.source.packing.ListCounts.fromcounts(array)
                                    out[name] = starts
                                    out[oamap.generator.StopsRole(name)] = stops

                            elif isinstance(name, oamap.generator.StopsRole):
                                if name not in out:
                                    starts, stops = oamap.source.packing.ListCounts.fromcounts(array)
                                    out[oamap.generator.StartsRole(name)] = starts
                                    out[name] = stops

                            elif isinstance(name, oamap.generator.DataRole):
                                if recarrayitem is None:
                                    out[name] = array
                                else:
                                    out[name] = array[recarrayitem]

                            else:
                                raise AssertionError

                        elif isinstance(array, uproot.interp.jagged.JaggedArray):
                            if isinstance(name, oamap.generator.StartsRole):
                                out[name] = array.starts

                            elif isinstance(name, oamap.generator.StopsRole):
                                out[name] = array.stops

                            elif isinstance(name, oamap.generator.DataRole):
                                out[name] = array.contents

                            else:
                                raise AssertionError

                        elif isinstance(array, uproot.interp.strings.Strings):
                            if isinstance(name, oamap.generator.StartsRole):
                                out[name] = array.jaggedarray.starts

                            elif isinstance(name, oamap.generator.StopsRole):
                                out[name] = array.jaggedarray.stops

                            elif isinstance(name, oamap.generator.DataRole):
                                out[name] = array.jaggedarray.contents

                            else:
                                raise AssertionError

                        else:
                            raise AssertionError

                return out
