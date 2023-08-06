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

from ... import core as c
from ... import ctrlstru as cs

from .rwcommon import br1, br2, bw1


@c.EUDFunc
def f_strcpy(dst, src):
    '''
    Strcpy equivilant in eudplib. Copy C-style string.

    :param dst: Destination address (Not EPD player)
    :param src: Source address (Not EPD player)

    :return: dst
    '''
    b = c.EUDVariable()

    br1.seekoffset(src)
    bw1.seekoffset(dst)

    if cs.EUDInfLoop()():
        c.SetVariables(b, br1.readbyte())
        bw1.writebyte(b)
        cs.EUDBreakIf(b == 0)
    cs.EUDEndInfLoop()

    bw1.flushdword()

    return dst


@c.EUDFunc
def f_strcmp(s1, s2):
    br1.seekoffset(s1)
    br2.seekoffset(s2)

    if cs.EUDInfLoop()():
        ch1 = br1.readbyte()
        ch2 = br2.readbyte()
        if cs.EUDIf()(ch1 == ch2):
            if cs.EUDIf()(ch1 == 0):
                c.EUDReturn(0)
            cs.EUDEndIf()
            cs.EUDContinue()
        if cs.EUDElse()():
            c.EUDReturn(ch1 - ch2)
        cs.EUDEndIf()
    cs.EUDEndInfLoop()
