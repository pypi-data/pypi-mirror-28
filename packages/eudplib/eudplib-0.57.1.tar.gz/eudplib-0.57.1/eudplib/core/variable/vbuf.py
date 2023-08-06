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

from ..eudobj import EUDObject
from ... import utils as ut
from ..allocator import RegisterCreatePayloadCallback


class EUDVarBuffer(EUDObject):
    """Variable buffer

    72 bytes per variable.
    """

    def __init__(self):
        super().__init__()

        self._initvals = []

    def DynamicConstructed(self):
        return True

    def CreateVarTrigger(self, initval):
        ret = self + (72 * len(self._initvals))
        self._initvals.append(initval)
        return ret

    def CreateMultipleVarTriggers(self, initvals):
        ret = self + (72 * len(self._initvals))
        self._initvals.extend(initvals)
        return ret

    def GetDataSize(self):
        return 2408 + 72 * (len(self._initvals) - 1)

    def WritePayload(self, emitbuffer):
        output = bytearray(2408 + 72 * (len(self._initvals) - 1))

        for i in range(len(self._initvals)):
            # 'preserve rawtrigger'
            output[72 * i + 2376:72 * i + 2380] = b'\x04\0\0\0'

        heads = 0
        for i, initval in enumerate(self._initvals):
            heade = 72 * i + 348
            if initval == 0:
                continue
            elif isinstance(initval, int):
                output[72 * i + 348:72 * i + 352] = ut.i2b4(initval)
                continue
            emitbuffer.WriteBytes(output[heads:heade])
            emitbuffer.WriteDword(initval)
            heads = 72 * i + 352

        if heade > heads:
            emitbuffer.WriteBytes(output[heads:heade + 4])

        tails = 72 * (len(self._initvals) - 1) + 352
        emitbuffer.WriteBytes(output[tails:])


_evb = None


def RegisterNewVariableBuffer():
    global _evb
    _evb = EUDVarBuffer()


def GetCurrentVariableBuffer():
    return _evb


RegisterCreatePayloadCallback(RegisterNewVariableBuffer)
