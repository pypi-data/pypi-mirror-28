# -*- coding: UTF-8 -*-
#
# Copyright © 2003 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Wammu <https://wammu.eu/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Wammu - Phone manager
IMAP UTF-7 codec
'''
from __future__ import unicode_literals

import codecs

def modified_base64(s):
    s_utf7 = s.encode('utf-7')
    return s_utf7[1:-1].replace('/', ',')

def modified_unbase64(s):
    s_utf7 = '+' + s.replace(',', '/') + '-'
    return s_utf7.decode('utf-7')

def encoder(s):
    r = []
    _in = []
    for c in s:
        if ord(c) in (list(range(0x20, 0x26)) + list(range(0x27, 0x7f))):
            if _in:
                r.extend(['&', modified_base64(''.join(_in)), '-'])
                del _in[:]
            r.append(str(c))
        elif c == '&':
            if _in:
                r.extend(['&', modified_base64(''.join(_in)), '-'])
                del _in[:]
            r.append('&-')
        else:
            _in.append(c)
    if _in:
        r.extend(['&', modified_base64(''.join(_in)), '-'])
    return (''.join(r), len(s))

def decoder(s):
    r = []
    decode = []
    for c in s:
        if c == '&' and not decode:
            decode.append('&')
        elif c == '-' and decode:
            if len(decode) == 1:
                r.append('&')
            else:
                r.append(modified_unbase64(''.join(decode[1:])))
            decode = []
        elif decode:
            decode.append(c)
        else:
            r.append(c)
    if decode:
        r.append(modified_unbase64(''.join(decode[1:])))
    return (''.join(r), len(s))

class StreamReader(codecs.StreamReader):
    def decode(self, s, errors='strict'):
        return decoder(s)

class StreamWriter(codecs.StreamWriter):
    def decode(self, s, errors='strict'):
        return encoder(s)

def imap4_utf_7(name):
    if name == 'imap4-utf-7':
        return (encoder, decoder, StreamReader, StreamWriter)

codecs.register(imap4_utf_7)
