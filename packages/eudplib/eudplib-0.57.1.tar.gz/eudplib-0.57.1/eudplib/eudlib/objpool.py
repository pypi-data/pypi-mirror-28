#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import weakref

from .. import (
    core as c,
    ctrlstru as cs,
    utils as ut
)
from ..core.variable import eudv as ev

from .eudarray import EUDArray


max_fieldn = 8
max_object_num = 32768


class _ObjPoolData(c.ConstExpr):
    def __init__(self, size):
        super().__init__(self)
        self._vdict = weakref.WeakKeyDictionary()
        self.size = size

    def Evaluate(self):
        evb = ev.GetCurrentVariableBuffer()
        if evb not in self._vdict:
            self._vdict[evb] = evb.CreateMultipleVarTriggers(
                [0] * (max_fieldn * self.size)
            )

        return self._vdict[evb].Evaluate()


class ObjPool:
    def __init__(self, size):
        self.size = size
        self.remaining = c.EUDVariable(size)

        baseobj = _ObjPoolData(size)
        self.data = EUDArray(
            [baseobj + 72 * max_fieldn * i for i in range(size)])

    def full(self):
        return self.remaining == 0

    @c.EUDMethod
    def _alloc(self):
        """ Allocate one object from pool """
        if cs.EUDIf()(self.full()):
            c.EUDReturn(0)
        cs.EUDEndIf()

        self.remaining -= 1
        data = self.data[self.remaining]
        return data

    def alloc(self, basetype, *args, **kwargs):
        ut.ep_assert(
            len(basetype._fields_) <= max_fieldn,
            "Only structs less than %d fields can be allocated" % max_fieldn
        )
        data = self._alloc()
        data = basetype.cast(data)
        data.constructor(*args, **kwargs)
        return data

    def free(self, basetype, data):
        ut.ep_assert(
            len(basetype._fields_) <= max_fieldn,
            "Only structs less than %d fields can be allocated" % max_fieldn
        )

        data = basetype.cast(data)
        data.destructor()
        self.data[self.remaining] = data
        self.remaining += 1


globalPool = ObjPool(max_object_num)
