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

from . import (
    dwepdio as dwm,
    cpmemio as cpm,
    byterw as brw,
    bwepdio as bwm,
    modcurpl as cp,
)
from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

# Helper functions

_bw = brw.EUDByteWriter()
_br = brw.EUDByteReader()


def f_dwwrite(ptr, dw):
    chars = dwm.f_dwbreak(dw)[2:]
    _bw.seekoffset(ptr)
    _bw.writebyte(chars[0])
    _bw.writebyte(chars[1])
    _bw.writebyte(chars[2])
    _bw.writebyte(chars[3])
    _bw.flushdword()


def f_wwrite(ptr, w):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    oldcp = cp.f_getcurpl()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(3):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * (i + 2) <= j:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([
            (c.CurrentPlayer, c.Add, k),
            (c.CurrentPlayer, c.Add, w * (256 ** i)),
        ])
        cs.EUDBreak()

    # Things gets complicated on this case.
    # We won't hand-optimize this case. This is a very, very rare case
    if cs.EUDSwitchCase()(3):
        b0, b1 = dwm.f_dwbreak(w)[2:4]
        f_bwrite(ptr, b0)
        f_bwrite(ptr + 1, b1)

    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)


def f_bwrite(ptr, b):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    oldcp = cp.f_getcurpl()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)
    for i in range(4):
        cs.EUDSwitchCase()(i)
        for j in range(31, -1, -1):
            if 8 * (i + 1) <= j:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([
            (c.EncodePlayer(c.CurrentPlayer), c.Add, k),
            (c.CurrentPlayer, c.Add, b * (256 ** i))
        ])
        cs.EUDBreak()
    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return b


# -----------------------------


@c.EUDFunc
def f_dwread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    oldcp = cp.f_getcurpl()
    dw = c.EUDVariable()
    k = c.EUDVariable()
    cs.DoActions([
        c.SetCurrentPlayer(epd),
        dw.SetNumber(0),
        k.SetNumber(0),
    ])
    cs.EUDSwitch(subp)

    # Case 0
    if cs.EUDSwitchCase()(0):
        dw << cpm.f_dwread_cp(0)
        cs.EUDBreak()

    # Else → Complex
    for i in range(1, 4):
        cs.EUDSwitchCase()(i)

        for j in range(31, -1, -1):
            if 8 * i <= j:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                        dw.AddNumber(2**(j - 8 * i))
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

            if j == 8 * i:
                break

        c.SeqCompute([
            (c.EncodePlayer(c.CurrentPlayer), c.Add, k),
            (ut.EPD(0x6509B0), c.Add, 1),
            (k, c.SetTo, 0)
        ])

        for j in range(31, -1, -1):
            if j < 8 * i:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                        dw.AddNumber(2**(j + 32 - 8 * i))
                    ]
                )

            else:
                c.RawTrigger(
                    conditions=c.Deaths(c.CurrentPlayer, c.AtLeast, 2**j, 0),
                    actions=[
                        c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**j, 0),
                        k.AddNumber(2**j),
                    ]
                )

        c.SeqCompute([
            (c.EncodePlayer(c.CurrentPlayer), c.Add, k),
        ])

        cs.EUDBreak()

    cs.EUDEndSwitch()
    cp.f_setcurpl(oldcp)
    return dw


def f_wread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    return bwm.f_wread_epd(epd, subp)


def f_bread(ptr):
    epd, subp = c.f_div(ptr - 0x58A364, 4)
    return bwm.f_bread_epd(epd, subp)
