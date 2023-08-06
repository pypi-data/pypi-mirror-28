# coding: utf-8

# Copyright:
# Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from pyscsi.pyscsi.scsi_command import SCSICommand
from pyscsi.utils.converter import encode_dict, decode_bits

#
# SCSI InitializeElementStatus command and definitions
#


class InitializeElementStatus(SCSICommand):
    """
    A class to hold information from a InitializeElementStatus command to a scsi device
    """
    _cdb_bits = {'opcode': [0xff, 0], }

    def __init__(self, scsi):
        """
        initialize a new instance

        :param scsi:
        """
        SCSICommand.__init__(self, scsi, 0, 0)
        self.cdb = self.build_cdb()
        self.execute()

    def build_cdb(self):
        """
        Build a InitializeElementStatus CDB

        :return: a byte array representing a code descriptor block
        """
        cdb = {
            'opcode': self.scsi.device.opcodes.INITIALIZE_ELEMENT_STATUS.value, }
        return self.marshall_cdb(cdb)

    @staticmethod
    def unmarshall_cdb(cdb):
        """
        Unmarshall a InitializeElementStatus cdb

        :param cdb: a byte array representing a code descriptor block
        :return result: a dict
        """
        result = {}
        decode_bits(cdb, InitializeElementStatus._cdb_bits, result)
        return result

    @staticmethod
    def marshall_cdb(cdb):
        """
        Marshall a InitializeElementStatus cdb

        :param cdb: a dict with key:value pairs representing a code descriptor block
        :return result: a byte array representing a code descriptor block
        """
        result = bytearray(6)
        encode_dict(cdb, InitializeElementStatus._cdb_bits, result)
        return result


