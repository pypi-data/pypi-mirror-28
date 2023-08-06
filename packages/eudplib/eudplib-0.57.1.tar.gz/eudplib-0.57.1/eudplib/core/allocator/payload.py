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

from . import rlocint, pbuffer
from . import constexpr
from eudplib import utils as ut
from eudplib.utils import stackobjs

import random
import time

_found_objects = []
_rootobj = None
_found_objects_set = set()
_untraversed_objects = []
_dynamic_objects_set = set()
_alloctable = {}
_payload_size = 0

PHASE_COLLECTING = 1
PHASE_ALLOCATING = 2
PHASE_WRITING = 3
phase = None

_payload_compress = False

# -------

_lastTime = 0
_doLog = False


def setPayloadLoggerMode(mode):
    global _doLog
    _doLog = mode


def lprint(text, flush=False, _endingdict={True: '\n', False: '\r'}):
    global _lastTime, _doLog
    if not _doLog:
        return

    currentTime = time.time()
    if flush or (currentTime - _lastTime) >= 0.5:
        _lastTime = currentTime
        print(text, end=_endingdict[flush])


def CompressPayload(mode):
    ''' Set payload compression mode.

    :param mode: If true, enable object stacking (compression). If false,
    disable it.
    '''

    global _payload_compress
    if mode not in [True, False]:
        raise ut.EPError('Invalid type')

    if mode:
        _payload_compress = True
    else:
        _payload_compress = False


class ObjCollector:

    '''
    Object having PayloadBuffer-like interfaces. Collects all objects by
    calling RegisterObject() for every related objects.
    '''

    def __init__(self):
        pass

    def StartWrite(self):
        pass

    def EndWrite(self):
        pass

    def WriteByte(self, number):
        pass

    def WriteWord(self, number):
        pass

    def WriteDword(self, number):
        constexpr.Evaluate(number)

    def WritePack(self, structformat, arglist):
        for arg in arglist:
            if type(arg) is not int:
                constexpr.Evaluate(arg)

    def WriteBytes(self, b):
        pass

    def WriteSpace(self, spacesize):
        pass


def CollectObjects(root):
    global phase
    global _rootobj
    global _found_objects
    global _found_objects_set
    global _dynamic_objects_set
    global _untraversed_objects

    lprint('[Stage 1/3] CollectObjects', flush=True)

    phase = PHASE_COLLECTING

    objc = ObjCollector()
    _rootobj = None
    _found_objects_set = set()
    _dynamic_objects_set = set()
    _untraversed_objects = []

    # Evaluate root to register root object.
    # root may not have WritePayload() method e.g: Forward()
    constexpr.Evaluate(root)

    while _untraversed_objects:
        while _untraversed_objects:
            lprint(
                " - Collected %d / %d objects" % (
                    len(_found_objects_set),
                    len(_found_objects_set) + len(_untraversed_objects)
                )
            )

            obj = _untraversed_objects.pop()

            objc.StartWrite()
            obj.WritePayload(objc)
            objc.EndWrite()

        # Check for new objects
        for obj in list(_dynamic_objects_set):
            objc.StartWrite()
            obj.WritePayload(objc)
            objc.EndWrite()

    if len(_found_objects_set) == 0:
        raise ut.EPError('No object collected')

    # Shuffle objects -> Randomize(?) addresses
    _found_objects_set.remove(_rootobj)
    fo2 = list(_found_objects_set)
    random.shuffle(fo2)
    _found_objects = [_rootobj] + fo2

    # cleanup
    _found_objects_set = None
    phase = None

    # Final
    lprint(
        " - Collected %d / %d objects" %
        (
            len(_found_objects),
            len(_found_objects)
        ), flush=True
    )


# -------


class ObjAllocator:

    '''
    Object having PayloadBuffer-like interfaces. Collects all objects by
    calling RegisterObject() for every related objects.
    '''

    def __init__(self):
        self._sizes = {}

    def StartWrite(self):
        self._suboccupmap = 0
        self._suboccupidx = 0
        self._occupmap = []

    def _Occup0(self):
        self._suboccupidx += 1
        if self._suboccupidx == 4:
            self._occupmap.append(self._suboccupmap)
            self._suboccupidx = 0
            self._suboccupmap = 0

    def _Occup1(self):
        self._suboccupmap = 1
        self._suboccupidx += 1
        if self._suboccupidx == 4:
            self._occupmap.append(self._suboccupmap)
            self._suboccupidx = 0
            self._suboccupmap = 0

    def EndWrite(self):
        if self._suboccupidx:
            self._occupmap.append(self._suboccupmap)
            self._suboccupidx = 0
        return self._occupmap

    def WriteByte(self, number):
        if number is None:
            self._Occup0()
        else:
            self._Occup1()

    def WriteWord(self, number):
        if number is None:
            self._Occup0()
            self._Occup0()
        else:
            self._Occup1()
            self._Occup1()

    def WriteDword(self, number):
        self._occupmap.append(1)

    def WritePack(self, structformat, arglist):
        if structformat not in self._sizes:
            ssize = 0
            sizedict = {'B': 1, 'H': 2, 'I': 4}
            for i in range(len(arglist)):
                ssize += sizedict[structformat[i]]
            self._sizes[structformat] = ssize

        ssize = self._sizes[structformat]

        # Add occupiation index
        self._occupmap.extend([1] * (ssize >> 2))
        ssize &= 3
        for i in range(ssize):
            self._Occup1()

    def WriteBytes(self, b):
        ssize = len(b)
        self._occupmap.extend([1] * (ssize >> 2))
        for i in range(ssize & 3):
            self._Occup1()

    def WriteSpace(self, ssize):
        while ssize and self._suboccupidx:
            self._Occup0()
            ssize -= 1

        self._occupmap.extend([0] * (ssize >> 2))
        ssize &= 3
        for i in range(ssize):
            self._Occup0()


def AllocObjects():
    global phase
    global _alloctable
    global _payload_size

    phase = PHASE_ALLOCATING
    objn = len(_found_objects)

    lprint("[Stage 2/3] AllocObjects", flush=True)

    # Quick and less space-efficient approach
    if not _payload_compress:
        lallocaddr = 0
        for i, obj in enumerate(_found_objects):
            objsize = obj.GetDataSize()
            allocsize = (objsize + 3) & ~3
            _alloctable[obj] = lallocaddr
            lallocaddr += allocsize

            lprint(" - Allocated %d / %d objects" % (i + 1, objn))
        _payload_size = lallocaddr

        lprint(" - Allocated %d / %d objects" % (objn, objn), flush=True)
        phase = None
        return

    obja = ObjAllocator()

    _alloctable = {}
    dwoccupmap_dict = {}

    # Get occupation map for all objects
    for i, obj in enumerate(_found_objects):
        obja.StartWrite()
        obj.WritePayload(obja)
        dwoccupmap = obja.EndWrite()
        dwoccupmap_dict[obj] = dwoccupmap
        ut.ep_assert(
            len(dwoccupmap) == (obj.GetDataSize() + 3) >> 2,
            'Occupation map length & Object size mismatch for object'
        )
        lprint(" - Preprocessed %d / %d objects" % (i + 1, objn))

    lprint(" - Preprocessed %d / %d objects" % (objn, objn), flush=True)

    lprint(" - Allocating objects..", flush=True)
    stackobjs.StackObjects(_found_objects, dwoccupmap_dict, _alloctable)

    # Get payload length
    _payload_size = max(map(
        lambda obj: _alloctable[obj] + obj.GetDataSize(), _found_objects
    ))

    phase = None


# -------


def ConstructPayload():
    global phase

    phase = PHASE_WRITING
    lprint("[Stage 3/3] ConstructPayload", flush=True)
    objn = len(_found_objects)

    pbuf = pbuffer.PayloadBuffer(_payload_size)

    for i, obj in enumerate(_found_objects):
        objaddr, objsize = _alloctable[obj], obj.GetDataSize()

        pbuf.StartWrite(objaddr)
        obj.WritePayload(pbuf)
        written_bytes = pbuf.EndWrite()
        ut.ep_assert(
            written_bytes == objsize,
            'obj.GetDataSize()(%d) != Real payload size(%d) for object %s'
            % (objsize, written_bytes, obj)
        )

        lprint(" - Written %d / %d objects" % (i + 1, objn))

    lprint(" - Written %d / %d objects" % (objn, objn), flush=True)
    phase = None
    return pbuf.CreatePayload()


_on_create_payload_callbacks = []


def RegisterCreatePayloadCallback(f):
    _on_create_payload_callbacks.append(f)


def CreatePayload(root):
    # Call callbacks
    for f in _on_create_payload_callbacks:
        f()
    CollectObjects(root)
    AllocObjects()
    return ConstructPayload()


defri = rlocint.RlocInt(0, 4)


def GetObjectAddr(obj):
    global _alloctable
    global _found_objects
    global _found_objects_set
    global _untraversed_objects
    global _dynamic_objects_set
    global _rootobj

    if phase == PHASE_COLLECTING:
        if obj not in _found_objects_set:
            _untraversed_objects.append(obj)
            _found_objects_set.add(obj)
            if obj.DynamicConstructed():
                _dynamic_objects_set.add(obj)
            if not _rootobj:
                _rootobj = obj

        return defri

    elif phase == PHASE_ALLOCATING:
        return defri

    elif phase == PHASE_WRITING:
        # assert _alloctable[obj] & 3 == 0
        return rlocint.RlocInt(_alloctable[obj], 4)
