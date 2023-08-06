# coding: utf-8

# Copyright:
#  Copyright (C) 2014 by Ronnie Sahlberg<ronniesahlberg@gmail.com>
#  Copyright (C) 2015 by Markus Rosjat<markus.rosjat@gmail.com>
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
from pyscsi.pyscsi.scsi_cdb_exchangemedium import ExchangeMedium
from pyscsi.pyscsi.scsi_cdb_getlbastatus import GetLBAStatus
from pyscsi.pyscsi.scsi_cdb_initelementstatus import InitializeElementStatus
from pyscsi.pyscsi.scsi_cdb_initelementstatuswithrange import InitializeElementStatusWithRange
from pyscsi.pyscsi.scsi_cdb_inquiry import Inquiry
from pyscsi.pyscsi.scsi_cdb_modesense6 import ModeSense6, ModeSelect6
from pyscsi.pyscsi.scsi_cdb_modesense10 import ModeSense10, ModeSelect10
from pyscsi.pyscsi.scsi_cdb_movemedium import MoveMedium
from pyscsi.pyscsi.scsi_cdb_openclose_exportimport_element import OpenCloseImportExportElement
from pyscsi.pyscsi.scsi_cdb_positiontoelement import PositionToElement
from pyscsi.pyscsi.scsi_cdb_preventallow_mediumremoval import PreventAllowMediumRemoval
from pyscsi.pyscsi.scsi_cdb_read10 import Read10
from pyscsi.pyscsi.scsi_cdb_read12 import Read12
from pyscsi.pyscsi.scsi_cdb_read16 import Read16
from pyscsi.pyscsi.scsi_cdb_readcapacity10 import ReadCapacity10
from pyscsi.pyscsi.scsi_cdb_readcapacity16 import ReadCapacity16
from pyscsi.pyscsi.scsi_cdb_readelementstatus import ReadElementStatus
from pyscsi.pyscsi.scsi_cdb_report_luns import ReportLuns
from pyscsi.pyscsi.scsi_cdb_report_priority import ReportPriority
from pyscsi.pyscsi.scsi_cdb_testunitready import TestUnitReady
from pyscsi.pyscsi.scsi_cdb_write10 import Write10
from pyscsi.pyscsi.scsi_cdb_write12 import Write12
from pyscsi.pyscsi.scsi_cdb_write16 import Write16
from pyscsi.pyscsi.scsi_cdb_writesame10 import WriteSame10
from pyscsi.pyscsi.scsi_cdb_writesame16 import WriteSame16
from pyscsi.pyscsi.scsi_enum_command import spc, sbc, smc, ssc, mmc


class SCSI(object):
    """
    The interface to  the specialized scsi classes
    """
    def __init__(self, dev, blocksize=0):
        """
        initialize a new instance

        :param dev: a SCSIDevice object
        :param blocksize:  integer defining a blocksize
        """
        self.device = dev
        self._blocksize = blocksize
        self.__init_opcode()

    def __call__(self, dev):
        """
        call the instance again with new device

        :param dev: a SCSIDevice object
        """
        self.device = dev
        self.__init_opcode()

    def __init_opcode(self):
        """
        Small helper method to terminate the type of
        the scsi device and assigning a proper opcode
        mapper.
        """
        if self.device is not None:
            self.device.devicetype = self.inquiry().result['peripheral_device_type']
            if self.device.devicetype in (0x00, 0x04, 0x07, ):  # sbc
                self.device.opcodes = sbc
            elif self.device.devicetype in (0x01, 0x02, 0x09):  # ssc
                self.device.opcodes = ssc
            elif self.device.devicetype in (0x03,):  # spc
                self.device.opcodes = spc
            elif self.device.devicetype in (0x08,):  # smc
                self.device.opcodes = smc
            elif self.device.devicetype in (0x05,):  # mmc
                self.device.opcodes = mmc

    @property
    def blocksize(self):
        """
        getter method of the blocksize property

        :return: blocksize in bytes
        """
        return self._blocksize

    @blocksize.setter
    def blocksize(self, value):
        """
        setter method of the blocksize property

        :param: blocksize in bytes
        """
        self._blocksize = value

    def exchangemedium(self, xfer, source, dest1, dest2, **kwargs):
        """
        Returns a ExchangeMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest1: destination 1 element
        :param dest2: destination 2 element
        :param kwargs: inv1=0 invert/rotate the medium before loading
                       inv2=0 invert/rotate the medium before loading
        :return: an ExchangeMedium instance
        """
        return ExchangeMedium(self, xfer, source, dest1, dest2, **kwargs)

    def getlbastatus(self, lba, **kwargs):
        """
        Returns a GetLBAStatus Instance

        :param lba: starting lba
        :param kwargs: a dict with key/value pairs
                       alloc_len = 16384: size of requested datain
        :return: a GetLBAStatus instance
        """
        return GetLBAStatus(self, lba, **kwargs)

    def inquiry(self, **kwargs):
        """
        Returns a Inquiry Instance

        :param kwargs: a dict with key/value pairs
                       evpd = 0, a byte indicating if vital product data is supported
                       page_code = 0, a byte representing a page code for vpd
                       alloc_len = 96, the size of the data_in buffer
        :return: a Inquiry instance
        """
        return Inquiry(self, **kwargs)

    def initializeelementstatus(self):
        """
        Returns a InitializeElementStatus Instance

        :return: a InitializeElementStatus instance
        """
        return InitializeElementStatus(self)

    def initializeelementstatuswithrange(self, xfer, elements, **kwargs):
        """
        Returns a InitializeElementStatusWithRange Instance

        :param xfer: two byte indicating the address of the starting element
        :param elements: two byte representing a range of elements that should be initialized
        :param kwargs: a dict with key/value pairs
                       range = 0, a integer indicating if elements should be ignored
                       fast = 0, a integer indicating if  elements should be scanned for media presence
        :return: a InitializeElementStatusWithRange instance
        """
        return InitializeElementStatusWithRange(self, xfer, elements, **kwargs)

    def modeselect6(self, data, **kwargs):
        """
        Returns a ModeSelect6 Instance

        :param data: a dict containing the mode page to set
        :param kwargs: a dict with key/value pairs
                       pf = 0, Page Format flag
                       sp = 0, Save Pages flag
        :return: a ModeSelect6 instance
        """
        return ModeSelect6(self, data, **kwargs)

    def modesense6(self, page_code, **kwargs):
        """
        Returns a ModeSense6 Instance

        :param page_code:  The page requested
        :param kwargs: a dict with key/value pairs
                       sub_page_code = 0, Requested subpage
                       dbd = 0, Disable Block Descriptors flag
                       pc = 0, Page Control flag
                       alloclen = 96
        :return: a ModeSense6 instance
        """
        return ModeSense6(self, page_code, **kwargs)

    def modesense10(self, page_code, **kwargs):
        """
        Returns a ModeSense10 Instance

        :param page_code:  The page requested
        :param kwargs: a dict with key/value pairs
                       llbaa = 0, long LBA accepted can be 0 or 1
                       dbd = 0, disable block descriptor can be 0 or 1.
                       pc = 0, page control field, a value between 0 and 3
                       alloclen = 0, the max number of bytes allocated for the data_in buffer
        :return: a ModeSense10 instance
        """
        return ModeSense10(self, page_code, **kwargs)

    def modeselect10(self, data, **kwargs):
        """
        Returns a ModeSelect10 Instance

        :param data: a dict containing the mode page to set
        :param kwargs: a dict with key/value pairs
                       pf = 0, Page Format flag
                       sp = 0, Save Pages flag
        :return: a ModeSelect10 instance
        """
        return ModeSelect10(self, data, **kwargs)

    def opencloseimportexportelement(self, xfer, acode, **kwargs):
        """
        Returns a OpenCloseImportExportElement Instance

        :param xfer: a dict containing the mode page to set
        :param acode: Page Format flag
        :param kwargs: a dict with key/value pairs
        :return: a OpenCloseImportExportElement instance
        """
        return OpenCloseImportExportElement(self, xfer, acode, **kwargs)

    def positiontoelement(self, xfer, dest, **kwargs):
        """
        Returns a PositionToElement Instance

        :param xfer: medium transport element to use
        :param dest: destination element
        :param kwargs: a dict with key/value pairs
                       invert=0, invert/rotate the medium before loading
        :return: an PositionToElement instance
        """
        return PositionToElement(self, xfer, dest, **kwargs)

    def preventallowmediumremoval(self, **kwargs):
        """
        Returns a PreventAllowMediumRemoval Instance

        :param kwargs: a dict with key/value pairs
                       prevent=0, prevent/allow the medium to be removed
        :return: an PreventAllowMediumRemoval instance
        """
        return PreventAllowMediumRemoval(self, **kwargs)

    def read10(self, lba, tl, **kwargs):
        """
        Returns a Read10 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read10 Instance
        """
        return Read10(self, lba, tl, **kwargs)

    def read12(self, lba, tl, **kwargs):
        """
        Returns a Read12 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read12 Instance
        """
        return Read12(self, lba, tl, **kwargs)

    def read16(self, lba, tl, **kwargs):
        """
        Returns a Read16 Instance

        :param lba: Logical Block Address
        :param tl: Transfer Length
        :param kwargs: a dict with key/value pairs
                       rdprotect = 0, ReadProtect flags
                       dpo = 0, DisablePageOut flag
                       fua = 0, Force Unit Access flag
                       rarc = 0, Rebuild Assist Recovery control flag
                       group = 0, Group Number
        :returns a Read16 Instance
        """
        return Read16(self, lba, tl, **kwargs)

    def readcapacity10(self, **kwargs):
        """
        Returns a ReadCapacity10 Instance

        :param kwargs: a dict with key/value pairs
                       alloc_len = 8, size of requested datain
        :return: a ReadCapacity10 instance
        """
        return ReadCapacity10(self, **kwargs)

    def readcapacity16(self, **kwargs):
        """
        Returns a ReadCapacity16 Instance

        :param kwargs: a dict with key/value pairs
                       alloc_len = 32, size of requested datain
        :return: a ReadCapacity16 instance
        """
        return ReadCapacity16(self, **kwargs)

    def readelementstatus(self, start, num, **kwargs):
        """
        Returns a ReadElementStatus Instance

        :param start: starting address for first element to return
        :param num: numbver of elements to return
        :param kwargs: a dict with key/value pairs
                       element_type, type of elements to return
                       voltag = 0, whether volume tag data should be returned
                       curdata = 1, check current data
                       dvcid = 0, whether to return device identifiers
                       alloclen=16384, max amount od data to return
        :return: an ReadElementStatus instance
        """
        return ReadElementStatus(self, start, num, **kwargs)

    def movemedium(self, xfer, source, dest, **kwargs):
        """
        Returns a MoveMedium Instance

        :param xfer: medium transport element to use
        :param source: source element
        :param dest: destination element
        :param kwargs: a dict with key/value pairs
                       invert=0, invert/rotate the medium before loading
        :return: an MoveMedium instance
        """
        return MoveMedium(self, xfer, source, dest, **kwargs)

    def testunitready(self):
        """
        Returns a TestUnitReady Instance

        """
        return TestUnitReady(self)

    def write10(self, lba, tl, data, **kwargs):
        """
        Returns a Write10 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write10 instance
        """
        return Write10(self, lba, tl, data, **kwargs)

    def write12(self, lba, tl, data, **kwargs):
        """
        Returns a Write12 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write12 instance
        """
        return Write12(self, lba, tl, data, **kwargs)

    def write16(self, lba, tl, data, **kwargs):
        """
        Returns a Write16 Instance

        :param lba: Logical Block Address to write to
        :param tl: Transfer Length in blocks
        :param data: bytearray containing the data to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       dpo = 0, disable Page Out flag
                       fua = 0, Force Unit Access flag
                       group = 0, Group Number
        :return: a Write16 instance
        """
        return Write16(self, lba, tl, data, **kwargs)

    def writesame16(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame16 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       anchor = 0, Anchor flag
                       unmap = 0, Unmap flag
                       ndob = 0, NoDataOutBuffer flag. When set data is None.
                       group = 0, Group Number
        :return: a WriteSame16 instance
        """
        return WriteSame16(self, lba, nb, data, **kwargs)

    def writesame10(self, lba, nb, data, **kwargs):
        """
        Returns a WriteSame10 Instance

        :param lba: Logical Block Address to write to
        :param nb: Number of blocks
        :param data: bytearray containing the block to write
        :param kwargs: a dict with key/value pairs
                       wrprotect = 0, WriteProtect flags
                       anchor = 0, Anchor flag
                       unmap = 0, Unmap flag
                       group = 0, Group Number
        :return: a WriteSame10 instance
        """
        return WriteSame10(self, lba, nb, data, **kwargs)

    def reportluns(self, **kwargs):
        """
        Return a ReportLuns Instance

        :param kwargs: a dict with key/value pairs
                       report=0x00, type of logical unit addresses that shall be reported
                       alloclen=96, size of requested datain
        :return: a ReportLuns instance
        """
        return ReportLuns(self, **kwargs)

    def reportpriority(self, **kwargs):
        """
        Return a ReportPriority Instance

        :param kwargs: a dict with key/value pairs
                       priority=0, specifies information to be returned in data_in buffer
                       alloclen=16384, size of requested datain
        :return: a ReportLuns instance
        """
        return ReportPriority(self, **kwargs)
