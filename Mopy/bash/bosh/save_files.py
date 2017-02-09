# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2015 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""Save files - beta - TODOs:
- that's the headers code only - write save classes (per game)
- rework encoding/decoding
- use the alpha data from the image
"""
__author__ = 'Utumno'

import itertools
import struct
import sys
from collections import OrderedDict
from .. import bolt
from ..bolt import decode, cstrip

# Exceptions ------------------------------------------------------------------
class SaveHeaderError(Exception): pass

# Structure wrappers ----------------------------------------------------------
def unpack_str8(ins): return ins.read(struct.unpack('B', ins.read(1))[0])
def unpack_str16(ins): return ins.read(struct.unpack('H', ins.read(2))[0])
def unpack_int(ins): return struct.unpack('I', ins.read(4))[0]
def unpack_short(ins): return struct.unpack('H', ins.read(2))[0]
def unpack_float(ins): return struct.unpack('f', ins.read(4))[0]
def unpack_byte(ins): return struct.unpack('B', ins.read(1))[0]

def unpack_(ins, fmt):
    return struct.unpack(fmt, ins.read(struct.calcsize(fmt)))[0]

class SaveFileHeader(object):
    save_magic = 'OVERRIDE'
    # common slots Bash code expects from SaveHeader (added header_size and
    # turned image to a property)
    __slots__ = ('header_size', 'pcName', 'pcLevel', 'pcLocation', 'gameDays',
                 'gameTicks', 'ssWidth', 'ssHeight', 'ssData', 'masters',
                 '_mastersStart') # helper attribute to simplify writeMasters
    # map slots to (seek position, unpacker) - seek position negative means
    # seek relative to ins.tell(), otherwise to the beginning of the file
    unpackers = OrderedDict()

    def __init__(self, save_path):
        try:
            with save_path.open('rb') as ins:
                self.load_header(ins)
        #--Errors
        except (OSError, struct.error) as e:
            bolt.deprint(u'Save file error:', traceback=True)
            raise SaveHeaderError, e.message, sys.exc_info()[2]

    def load_header(self, ins):
        save_magic = unpack_(ins, '%ds' % len(self.__class__.save_magic))
        if save_magic != self.__class__.save_magic:
            raise SaveHeaderError(u'Magic wrong: %r (expected %r)' % (
                save_magic, self.__class__.save_magic))
        for attr, unp in self.__class__.unpackers.iteritems():
            if unp[0]:
                if unp[0] > 0: ins.seek(unp[0])
                else: ins.seek(ins.tell() - unp[0])
            self.__setattr__(attr, unp[1](ins))
        self.load_image_data(ins)
        self.load_masters(ins)
        # additional calculations - TODO(ut): rework decoding
        self.calc_time()
        self.pcName = decode(cstrip(self.pcName))
        self.pcLocation = decode(cstrip(self.pcLocation), bolt.pluginEncoding,
                                 avoidEncodings=('utf8', 'utf-8'))
        self.masters = [bolt.GPath(decode(x)) for x in self.masters]

    def load_image_data(self, ins):
        self.ssData = ins.read(3 * self.ssWidth * self.ssHeight)

    def _drop_alpha(self, ins): ## TODO: Setup Bash to use the alpha data
        # Game is in 32bit RGB, Bash is expecting 24bit RGB
        ssData = ins.read(4 * self.ssWidth * self.ssHeight)
        # pick out only every 3 bytes, drop the 4th (alpha channel)
        #ssAlpha = ''.join(itertools.islice(ssData, 0, None, 4))
        self.ssData = ''.join(
            itertools.compress(ssData, itertools.cycle(reversed(range(4)))))

    def load_masters(self, ins):
        self._mastersStart = ins.tell()
        self.masters = []
        numMasters = unpack_byte(ins)
        for count in xrange(numMasters):
            self.masters.append(unpack_str8(ins))

    def _load_masters_16(self, ins): # common for skyrim and fallout4
        self._mastersStart = ins.tell()
        mastersSize = unpack_int(ins)
        self.masters = []
        numMasters = unpack_byte(ins)
        for count in xrange(numMasters):
            self.masters.append(unpack_str16(ins))
        if ins.tell() != self._mastersStart + mastersSize + 4:
            raise SaveHeaderError(
                u'Save game masters size (%i) not as expected (%i).' % (
                    ins.tell() - self._mastersStart - 4, mastersSize))

    def calc_time(self): pass

    @property
    def image(self):
        return self.ssWidth, self.ssHeight, self.ssData

    def writeMasters(self, ins, out):
        """Rewrites masters of existing save file."""
        def pack(fmt, *args): out.write(struct.pack(fmt, *args))
        out.write(ins.read(self._mastersStart))
        oldMasters = self._write_masters(ins, out, pack)
        #--Copy the rest
        while True:
            buff = ins.read(0x5000000)
            if not buff: break
            out.write(buff)
        return oldMasters

    def _write_masters(self, ins, out, pack):
        unpack_int(ins) # Discard oldSize
        newSize = 1 + sum(len(x) + 2 for x in self.masters)
        pack('I', newSize)
        #--Skip old masters
        oldMasters = []
        numMasters = unpack_byte(ins)
        pack('B', len(self.masters))
        for x in xrange(numMasters):
            oldMasters.append(unpack_str16(ins))
        #--Write new masters
        for master in self.masters:
            pack('H', len(master))
            out.write(master.s)
        #--Offsets
        offset = out.tell() - ins.tell()
        #--File Location Table
        for i in xrange(6):
            # formIdArrayCount offset, unkownTable3Offset,
            # globalDataTable1Offset, globalDataTable2Offset,
            # changeFormsOffset, globalDataTable3Offset
            oldOffset = unpack_int(ins)
            pack('I', oldOffset + offset)
        return oldMasters

class OblivionSaveHeader(SaveFileHeader):
    save_magic = 'TES4SAVEGAME'
    __slots__ = ('gameTime', 'ssSize')
    unpackers = OrderedDict([
        ('header_size', (34, unpack_int)),
        ('pcName',      (42, unpack_str8)),
        ('pcLevel',     (00, unpack_short)),
        ('pcLocation',  (00, unpack_str8)),
        ('gameDays',    (00, unpack_float)),
        ('gameTicks',   (00, unpack_int)),
        ('gameTime',    (00, lambda ins: unpack_(ins, '16s'))),
        ('ssSize',      (00, unpack_int)),
        ('ssWidth',     (00, unpack_int)),
        ('ssHeight',    (00, unpack_int)),
    ])

    def _write_masters(self, ins, out, pack):
        #--Skip old masters
        numMasters = unpack_byte(ins)
        oldMasters = []
        for x in xrange(numMasters):
            oldMasters.append(unpack_str8(ins))
        #--Write new masters
        pack('B', len(self.masters))
        for master in self.masters:
            pack('B', len(master))
            out.write(master.s)
        #--Fids Address
        offset = out.tell() - ins.tell()
        fidsAddress = unpack_int(ins)
        pack('I', fidsAddress + offset)
        return oldMasters

class SkyrimSaveHeader(SaveFileHeader):
    save_magic = 'TESV_SAVEGAME'
    # extra slots - only version is really used, gameDate used once (calc_time)
    __slots__ = ('gameDate', 'saveNumber', 'version', 'raceEid')
    unpackers = OrderedDict([
        ('header_size', (00, unpack_int)),
        ('version',     (00, unpack_int)),
        ('saveNumber',  (00, unpack_int)),
        ('pcName',      (00, unpack_str16)),
        ('pcLevel',     (00, unpack_int)),
        ('pcLocation',  (00, unpack_str16)),
        ('gameDate',    (00, unpack_str16)),
        ('raceEid',     (00, unpack_str16)),
        # skip pcSex (2 bytes) and unknown 16 bytes
        ('ssWidth',     (-18, unpack_int)),
        ('ssHeight',    (00, unpack_int)),
    ])

    def load_image_data(self, ins):
        if self.version == 12: # read two unknown bytes
            ins.read(2)
        if ins.tell() != self.header_size + 17: raise SaveHeaderError(
            u'New Save game header size (%s) not as expected (%s).' % (
                ins.tell() - 17, self.header_size))
        #--Image Data
        if self.version == 12:
            self._drop_alpha(ins)
        else:
            super(SkyrimSaveHeader, self).load_image_data(ins)

    def load_masters(self, ins):
        if self.version == 12:
            self.masters = []
            # TODO: Skyrim SE masters can't be listed without lz4 support
            return
        ins.read(1) # drop unknown byte
        #--Masters
        self._load_masters_16(ins)

    def calc_time(self):
        # gameDate format: hours.minutes.seconds
        hours, minutes, seconds = [int(x) for x in self.gameDate.split('.')]
        playSeconds = hours * 60 * 60 + minutes * 60 + seconds
        self.gameDays = float(playSeconds) / (24 * 60 * 60)
        self.gameTicks = playSeconds * 1000

class Fallout4SaveHeader(SkyrimSaveHeader): # pretty similar to skyrim
    save_magic = 'FO4_SAVEGAME'

    __slots__ = ()

    def load_image_data(self, ins):
        if ins.tell() != self.header_size + 16: raise SaveHeaderError(
            u'New Save game header size (%s) not as expected (%s).' % (
                ins.tell() - 16, self.header_size))
        #--Image Data
        self._drop_alpha(ins)

    def load_masters(self, ins):
        ins.read(1) # drop unknown byte
        unpack_str16(ins) # drop "gameVersion"
        #--Masters
        self._load_masters_16(ins)

    def calc_time(self):
        # gameDate format: Xd.Xh.Xm.X days.X hours.X minutes
        days, hours, minutes, _days, _hours, _minutes = self.gameDate.split(
            '.')
        days = int(days[:-1])
        hours = int(hours[:-1])
        minutes = int(minutes[:-1])
        self.gameDays = float(days) + float(hours) / 24 + float(minutes) / (
            24 * 60)
        # Assuming still 1000 ticks per second
        self.gameTicks = (days * 24 * 60 * 60 + hours * 60 * 60 + minutes
                             * 60) * 1000

# Factory
def get_save_header_type(game_fsName):
    """:rtype: type"""
    if game_fsName == u'Oblivion':
        return OblivionSaveHeader
    elif game_fsName in {u'Skyrim',  u'Skyrim Special Edition'}:
        return SkyrimSaveHeader
    elif game_fsName == u'Fallout4':
        return Fallout4SaveHeader
