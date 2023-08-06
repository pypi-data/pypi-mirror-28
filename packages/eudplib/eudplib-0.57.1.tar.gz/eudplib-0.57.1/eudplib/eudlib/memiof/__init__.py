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

from .modcurpl import (
    f_setcurpl,
    f_getcurpl
)


from .dwepdio import (
    f_dwepdread_epd,
    f_dwread_epd,
    f_epdread_epd,

    f_flagread_epd,

    f_dwwrite_epd,
    f_dwadd_epd,
    f_dwsubtract_epd,
    f_dwbreak,
    f_dwbreak2,
)

from .cpmemio import (
    f_dwepdread_cp,
    f_dwread_cp,
    f_epdread_cp,

    f_dwwrite_cp,
    f_dwadd_cp,
    f_dwsubtract_cp,
)


from .safedwmemio import (
    f_dwread_epd_safe,
    f_epdread_epd_safe,
    f_dwepdread_epd_safe,
)


from .byterw import (
    EUDByteReader,
    EUDByteWriter,
)

from .ptrmemio import (
    f_dwwrite,
    f_wwrite,
    f_bwrite,
    f_dwread,
    f_wread,
    f_bread,
)

from .mblockio import (
    f_repmovsd_epd,
    f_memcpy,
)
