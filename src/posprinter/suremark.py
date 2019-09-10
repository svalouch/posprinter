#!/usr/bin/env python3

import struct

from .suremark_status import PrinterMessage, PrinterID

PRT_DEVICE = '/dev/ttyUSB0'
PRT_BAUDRATE = 19200
PRT_TIMEOUT = 5


class SureMark:
    """
    Thin layer around IBM SureMark 4610 printers.
    """

    #: Reset the printer (warm start)
    CMD_RESET_PRINTER = b'\x10\x05\x40'
    #: Request the amount of flash for use by the user
    CMD_RETRIEVE_USER_FLASH_SIZE = b'\x1b\x34\x08\xff\xff\xff'
    #: Retrieve usage statistics, requires parameter.
    CMD_RETRIEVE_PRINTER_USAGE_STATISTICS = b'\x1b\x51'
    #: Retrieve the "Printer ID", detailed information about the printer model and its features.
    CMD_RETRIEVE_PRINTER_ID = b'\x1d\x49\x01'

    #: Sets the print mode, requires parameter (mode). PDF page 129
    CMD_SET_PRINT_MODE = b'\x1b\x21'
    #: Resets the "double height" mode, requires parameter. PDF page 131
    CMD_SET_CANCEL_DOUBLE_HEIGHT_MODE = b'\x1b\x68'
    #: Changes the code page, requires parameter. PDF page 135
    CMD_SET_CODE_PAGE = b'\x1b\x74'
    #: Print a predefined logo, requires parameter (slot number).
    CMD_PRINT_PREDEFINED_LOGO = b'\x1d\x2f'

    # Barcode handling
    #: Print a barcode, requires parameter (barcode type=.
    CMD_BARCODE_PRINT = b'\x1d\x6b'
    #: Set the horizontal size of the barcode, requires parameter (size).
    CMD_BARCODE_SET_HORIZONTAL_SIZE = b'\x1d\x77'
    #: Set the height of the barcode, requires parameter (height).
    CMD_BARCODE_SET_HEIGHT = b'\x1d\x68'
    #: Set the barcode HRI (human readable information) position, requires parameter (position).
    CMD_BARCODE_SET_HRI_POSITION = b'\x1d\x48'
    #: Set the barcode HRI (human readable information) font, requires parameter (font).
    CMD_BARCODE_SET_HRI_FONT = b'\x1d\x66'

    # print etc
    #: Print a line feed (LF) in the selected station.
    CMD_PRINT_LINE_FEED = b'\x0a'
    #: Print a line feed (LF), alternate, CR (impact) station needs to be activated.
    CMD_PRINT_LINE_FEED_ALT = b'\x0d'
    #: Print buffer and form feed, if the thermal station is selected, also cut the paper.
    CMD_PRINT_FORM_FEED_CUT = b'\x0c'
    #: Set the print mode, requires parameter (mode).
    CMD_SET_PRINT_MODE = b'\x1b\x21'

    #: Beeper control, requires a set of parameters.
    CMD_BEEPER = b'\x1b\x07'

    #: Default horizontal size for barcodes
    BARCODE_HORIZONTAL_SIZE_DEFAULT = 3
    #: Default height for barcodes.
    BARCODE_HEIGHT_DEFAULT = 162
    # Position for the Human Readable Information
    #: Disable printing of HRI text
    BARCODE_HRI_POSITION_NONE = b'\x00'
    #: Place the HRI text above the barcode
    BARCODE_HRI_POSITION_ABOVE = b'\x01'
    #: Place the HRI text below the barcode
    BARCODE_HRI_POSITION_BELOW = b'\x02'
    #: Place the HRI text both above and below the barcode
    BARCODE_HRI_POSITION_BOTH = b'\x03'
    #: Alias for NONE
    BARCODE_HRI_POSITION_DEFAULT = BARCODE_HRI_POSITION_NONE

    # Font used for the Human Readable Information
    #: Select font "A"
    BARCODE_HRI_FONT_A = b'\x00'
    #: Select font "B"
    BARCODE_HRI_FONT_B = b'\x01'
    #: Alias for "A"
    BARCODE_HRI_FONT_DEFAULT = BARCODE_HRI_FONT_A

    # statistics
    STATS_RAW_RUNTIME_IMAGE_BRIGHTNESS_CONTRAST = b'\x6d'
    STATS_RAW_RUNTIME_IMAGE_FOCUS = b'\x6e'
    STATS_RAW_MANUFACTURE_WEEK = b'\x70'
    STATS_RAW_FRU_CARD_INV_USAGE_COUNTERS = b'\x80'
    STATS_RAW_NUMBER_PAPER_CUTS = b'\x81'
    STATS_RAW_NUMBER_CHARACTERS_THERMAL_LOW = b'\x82'
    STATS_RAW_NUMBER_CHARACTERS_THERMAL_HIGH = b'\x83'
    STATS_RAW_NUMBER_STEPS_THERMAL = b'\x84'
    
    STATS_RAW_NUMBER_CUST_RECEIPT_COVER_OPENED = b'\x85'
    STATS_RAW_NUMBER_CUTS_FAILED = b'\x86'
    STATS_RAW_NUMBER_CHARACTERS_IMPACT = b'\x87'
    STATS_RAW_NUMBER_STEPS_IMPACT = b'\x88'
    STATS_RAW_NUMBER_MOTOR_STARTS_IMPACT = b'\x89'
    STATS_RAW_NUMBER_HOME_ERRORS = '\x8a'
    STATS_RAW_NUMBER_IMPACT_COVER_OPENED = b'\x8b'
    STATS_RAW_NUMBER_FORMS_INSERTED_IMPACT = b'\x8c'
    STATS_RAW_NUMBER_MICR_READS = b'\x8d'
    STATS_RAW_NUMBER_MICR_READS_HIGH_INTERFERENCE = b'\x8e'
    STATS_RAW_NUMBER_MICR_READS_FAILED = b'\x8f'
    STATS_RAW_NUMBER_CHECK_FLIPS = b'\x90'
    STATS_RAW_NUMBER_CHECK_FLIPS_FAILED = b'\x91'
    STATS_RAW_REMAINDER_NUMBER_STEPS_THERMAL = b'\x92'
    STATS_RAW_REMAINDER_NUMBER_PAPER_CUTS = b'\x93'
    STATS_RAW_REMAINDER_NUMBER_CHARACTERS_IMPACT = b'\x94'
    STATS_RAW_REMAINDER_NUMBER_STEPS_IMPACT = b'\x95'
    STATS_RAW_REMAINDER_NUMBER_FORMS_INSERTED_IMPACT = b'\x96'
    STATS_RAW_REMAINDER_NUMBER_MOTOR_STARTS_IMPACT = b'\x97'
    STATS_RAW_REMAINDER_NUMBER_CHECK_FLIPS_FAILED = b'\x98'
    STATS_RAW_REMAINDER_NUMBER_MICR_READS_FAILED = b'\x99'
    STATS_RAW_REMAINDER_NUMBER_CHECK_FLIPS = b'\x9a'
    STATS_RAW_REMAINDER_NUMBER_MICR_READS = b'\x9b'
    STATS_RAW_REMAINDER_NUMBER_MICR_READS_HIGH_INTERFERENCE = b'\x9c'
    STATS_RAW_REMAINDER_NUMBER_BARCODES_PRINTED = b'\x9d'
    STATS_RAW_REMAINDER_NUMBER_SCANNED_DOCUMENTS = b'\x9e'
    STATS_RAW_REMAINDER_NUMBER_CASH_DRAWER_SUCCESSFUL = b'\x9f'
    STATS_RAW_NUMBER_FLASH_ERASE = b'\xd2'
    STATS_RAW_NUMBER_SCANNED_DOCUMENTS = b'\xd3'
    STATS_RAW_NUMBER_CHECK_QUALITY_COUNT = b'\xd4'
    STATS_RAW_NUMBER_TONE_SOUND_COUNT = b'\xd5'
    STATS_RAW_NUMBER_CASH_DRAWER_SUCCESSFUL = b'\xd6'
    STATS_RAW_NUMBER_CASH_DRAWER_FAILED = b'\xd7'
    STATS_RAW_NUMBER_BARCODES_PRINTED = b'\xd8'
    STATS_RAW_NUMBER_MAX_TEMP = b'\xd9'
    STATS_RAW_REMAINDER_NUMBER_TONE_SOUND_COUNT = b'\xda'

    # Barcode types
    #: Barcode UPC_A
    BARCODE_UPC_A = b'\x00'
    #: Barcode UPC_E
    BARCODE_UPC_E = b'\x01'
    #: Barcode EAN13
    BARCODE_EAN13 = b'\x02'
    #: Barcode JAN13 (alias for EAN13)
    BARCODE_JAN13 = BARCODE_EAN13
    #: Barcode EAN8
    BARCODE_EAN8 = b'\x03'
    #: Barcode JAN8 (alias for EAN8)
    BARCODE_JAN8 = BARCODE_EAN8
    #: Barcode CODE_39
    BARCODE_CODE_39 = b'\x04'
    #: Barcode ITF
    BARCODE_ITF = b'\x05'
    #: Barcode CODABAR
    BARCODE_CODABAR = b'\x06'
    #: Barcode CODE_128C
    BARCODE_CODE_128C = b'\x07'
    #: Barcode CODE_39
    BARCODE_CODE_93 = b'\x08'
    #: Barcode CODE_128A
    BARCODE_CODE_128A = b'\x09'
    #: Barcode CODE_128B (alias for CODE_128A)
    BARCODE_CODE_128B = BARCODE_CODE_128A

    # TODO BARCODE_PDF417

    # BEEPER

    BEEPER_ENABLE_ENABLE = b'\xff'
    BEEPER_ENABLE_DISABLE = b'\x00'

    BEEPER_NOTE_C = 0
    BEEPER_NOTE_CSHARP = 1
    BEEPER_NOTE_D = 2
    BEEPER_NOTE_DSHARP = 3
    BEEPER_NOTE_E = 4
    BEEPER_NOTE_F = 5
    BEEPER_NOTE_FSHARP = 6
    BEEPER_NOTE_G = 7
    BEEPER_NOTE_GSHARP = 8
    BEEPER_NOTE_A = 9
    BEEPER_NOTE_ASHARP = 10
    BEEPER_NOTE_B = 11
    BEEPER_NOTE_SILENCE = 12
    BEEPER_NOTE_RESERVED1 = 13
    BEEPER_NOTE_RESERVED2 = 14
    BEEPER_NOTE_NORMAL = 15

    BEEPER_OCTAVE_1 = 0
    BEEPER_OCTAVE_2 = 1
    BEEPER_OCTAVE_3 = 2
    BEEPER_OCTAVE_4 = 3

    BEEPER_VOLUME_LOUD = 0
    BEEPER_VOLUME_SOFT = 1

    ALIGN_POSITIONS = b'\x1b\x61'
    ALIGN_POSITIONS_LEFT = b'\x00'
    ALIGN_POSITIONS_CENTER = b'\x01'
    ALIGN_POSITIONS_RIGHT = b'\x02'
    ALIGN_POSITIONS_COLUMN_RIGHT = '\x04'

    MAX_PRINT_SPEED = b'\x1b\x2f'
    MAX_PRINT_SPEED_52 = b'\x00'
    MAX_PRINT_SPEED_35 = b'\x01'
    MAX_PRINT_SPEED_26 = b'\x02'
    MAX_PRINT_SPEED_15 = b'\x03'

    def __init__(self, device, model=PrinterID.MODEL_UNKNOWN, debug=False):
        """
        Initializes the class. This does not send commands to the printer yet.
        Pass an open serial device, or any device that behaves like it. An instance of serial.Serial is assumed, though.
        """
        if device is None:
            raise ValueError('Can\'t operate without a device')
        self.__device = device
        self.__model = model
        self.__debug = debug

    def hexdump(s):
        """
        Simple dumper
        """
        print(":".join("{:02x}".format(c) for c in s))

    def identify(self):
        """
        Attempts to identify the printer model and capabilities
        """
        self.__device.write(self.CMD_RETRIEVE_PRINTER_ID)
        m = self.receive_message()
        if not m.is_printer_id_response():
            raise ValueError('Expected a printer id response')
        pass

    def beep(self, enable=False, duration=0, note=None, octave=None, volume=None):
        data = bytearray(2 + 1 + 1)
        data[0:1] = self.CMD_BEEPER

        if not isinstance(enable, bool):
            raise TypeError('invalid type for "enable": {}'.format(type(enable)))
        if duration < 0 or duration > 0xfe:
            raise ValueError('duration out of bounds (0 < duration <= 254)')

        if note is None:
            note = self.BEEPER_NOTE_NORMAL
        if octave is None:
            octave = self.BEEPER_OCTAVE_1
        if volume is None:
            volume = self.BEEPER_VOLUME_SOFT

        if note < 0 or note > self.BEEPER_NOTE_NORMAL:
            raise ValueError('Note out of bounds')
        if note == self.BEEPER_NOTE_RESERVED1 or note == self.BEEPER_NOTE_RESERVED2:
            raise ValueError('Reserved value')
        if octave < self.BEEPER_OCTAVE_1 or octave > self.BEEPER_OCTAVE_4:
            raise ValueError('Octave out of bounds')

        if enable:
            if duration == 0:
                data[2] = 0xff
            else:
                data[2] = struct.pack('>I', duration)[-1]

        data[3] = 0
        data[3] |= note
        data[3] |= (octave << 4)
        data[3] |= (volume << 6)
        SureMark.hexdump(data)
        self.__device.write(data)

    def print_line_feed(self):
        """
        Prints the buffer content (if any) and feed the paper by a preset amount
        """
        self.__device.write(self.CMD_PRINT_LINE_FEED)

    def print_line_feed_alt(self):
        """
        Alternative to print_line_feed that has to be activated before it can be used
        """
        self.__device.write(self.CMD_PRINT_LINE_FEED_ALT)

    def print_form_feed_cut(self):
        """
        Prints the buffer content (if any) and form-feeds the paper until it exits the feed rollers.
        If the thermal station is selected, cuts the paper
        """
        self.__device.write(self.CMD_PRINT_FORM_FEED_CUT)

    def cut(self):
        """
        Cuts the paper (after printing the buffer content). Short for print_form_feed_cut
        """
        self.print_form_feed_cut()

    # Barcode handling commands {{{
    def barcode(self, data, type=BARCODE_EAN13):
        """
        Prints a barcode. Setup for a barcode can be done using the various barcode_set-functions.
        """
        _data = data.encode('utf-8')
        if _data[-1] != b'\x00':
            _data += b'\x00'
        self.__device.write(self.CMD_BARCODE_PRINT + type + _data)

    def barcode_set_horizontal_size(self, m):
        """
        Sets the horizontal size (magnification) of the barcode
        """
        if m < 2 or m > 4:
            raise ValueError('Barcode horizontal size (magnification) outside allowed range 2 <= m <= 4')
        self.__device.write(self.CMD_BARCODE_SET_HORIZONTAL_SIZE + m)

    def barcode_set_height(self, h):
        """
        Sets the height of the barcode
        """
        if h < 1 or h > 255:
            raise ValueError('Barcode height outside allowed range 1 <= h <= 255')
        self.__device.write(self.CMD_BARCODE_SET_HEIGHT + h)

    def barcode_set_hri_position(self, p):
        """
        Set the position of the Human Readable Information string
        """
        if p < self.BARCODE_HRI_POSITION_NONE or p > self.BARCODE_HRI_POSITION_BOTH:
            raise ValueError('Barcode HRI position invalid')
        self.__device.write(self.CMD_BARCODE_SET_HRI_POSITION + p)

    def barcode_set_hri_font(self, f):
        """
        Sets the font used for the Human Readable Information string
        """
        if f not in [self.BARCODE_HRI_FONT_A, self.BARCODE_HRI_FONT_B]:
            raise ValueError('Barcode HRI font invalid')
        self.__device.write(self.CMD_BARCODE_SET_HRI_FONT + f)

    # }}}

    def align_positions(self, align):
        '''
        Sets the alignment of text. Note that not all alignments are valid everywhere.
        PDF: Page 140
        '''
        if align < 0 or align > 2 or align != 4:
            raise ValueError('Invalid alignment')
        return self.CMD_ALIGN_POSITIONS + align

    def select_maximum_print_speed(self, speed):
        '''
        Select the maximum print speed.
        PDF: Page 132
        '''
        if speed < 0 or speed > 3:
            raise ValueError('Invalid speed')
        return self.MAX_PRINT_SPEED + speed

    def get_printer_usage_stats_raw(self, stat):
        """
        Requests the counter given in "stat". This function does not perform conversions or factors.
        Returns a message object.
        """
        self.__device.write(self.CMD_RETRIEVE_PRINTER_USAGE_STATISTICS + stat)
        return self.receive_message()

    def get_printer_usage_stat_manufacture_week(self):
        """
        Returns the week of manufacture in the form WWYY, so 2009 is 20th week 2009
        """
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_MANUFACTURE_WEEK)
        # if m.command_complete():
        return struct.unpack('>H', m.raw_payload())[0]
        # raise ValueError('command was not successful')

    def get_printer_usage_stat_number_paper_cuts(self):
        """
        Returns the number of paper cuts.
        """
        FACTOR = 32
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_PAPER_CUTS)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        cuts_flash = struct.unpack('>H', m.raw_payload())[0]
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_REMAINDER_NUMBER_PAPER_CUTS)
        if not m.is_mct_response():
            raise ValueError('Expected an MCT response')
        cuts_remainder = struct.unpack('>H', m.raw_payload())[0]
        if self.__debug:
            print('Paper cuts (w/o factor): {} flash + {} remainder'.format(cuts_flash, cuts_remainder))
        return cuts_flash * FACTOR + cuts_remainder

    def get_printer_usage_stat_number_failed_paper_cuts(self):
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_CUTS_FAILED)
        if not m.is_mct_response():
            raise ValueError('Expected an MCT response')
        cuts_failed = struct.unpack('>H', m.raw_payload())[0]
        return cuts_failed

    def get_printer_usage_stats_thermal_motor_steps(self):
        """
        Returns te number of steps the motor in the CR (thermal) station performed.
        """
        FACTOR = 50000
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_STEPS_THERMAL)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        steps_flash = struct.unpack('>H', m.raw_payload())[0]

        m = self.get_printer_usage_stats_raw(self.STATS_RAW_REMAINDER_NUMBER_STEPS_THERMAL)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        steps_remainder = struct.unpack('>H', m.raw_payload())[0]
        if self.__debug:
            print('Thermal motor steps (w/o factor): {} flash + {} remainder'.format(steps_flash, steps_remainder))
        return steps_flash * FACTOR + steps_remainder

    def get_printer_usage_stats_printed_characters_thermal(self):
        """
        TODO this number seems wrong...
        """
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_CHARACTERS_THERMAL_LOW)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        p_low = m.raw_payload()

        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_CHARACTERS_THERMAL_HIGH)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        p_high = m.raw_payload()

        return struct.unpack('>I', p_low + p_high)[0]

    def get_printer_usage_stats_thermal_cover_opened(self):
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_CUST_RECEIPT_COVER_OPENED)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        return struct.unpack('>H', m.raw_payload())[0]

    def get_printer_usage_stats_barcodes_printed(self):
        FACTOR = 32
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_BARCODES_PRINTED)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        barcodes_flash = struct.unpack('>H', m.raw_payload())[0]

        m = self.get_printer_usage_stats_raw(self.STATS_RAW_REMAINDER_NUMBER_BARCODES_PRINTED)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        barcodes_remainder = struct.unpack('>H', m.raw_payload())[0]
        if self.__debug:
            print('Barcodes printed (w/o factor): {} flash + {} remainder'.format(barcodes_flash, barcodes_remainder))
        return barcodes_flash * FACTOR + barcodes_remainder

    def get_printer_usage_stats_tone_sounds(self):
        FACTOR = 32
        m = self.get_printer_usage_stats_raw(self.STATS_RAW_NUMBER_TONE_SOUND_COUNT)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        tones_flash = struct.unpack('>H', m.raw_payload())[0]

        m = self.get_printer_usage_stats_raw(self.STATS_RAW_REMAINDER_NUMBER_TONE_SOUND_COUNT)
        if not m.is_mct_response():
            raise ValueError('Excpected an MCT response')
        tones_remainder = struct.unpack('>H', m.raw_payload())[0]
        if self.__debug:
            print('Tone sounds (w/o factor): {} flash + {} remainder'.format(tones_flash, tones_remainder))
        return tones_flash * FACTOR + tones_remainder

    def get_user_flash_storage_size(self):
        """
        Requests that the printer responds with the size of its flash available to users.
        Unit is bytes
        """
        self.__device.write(self.CMD_RETRIEVE_USER_FLASH_SIZE)
        m = self.receive_message()
        if not m.is_user_flash_read_response():
            raise ValueError('Expected a User flash read response')
        if m.has_payload():
            if m.payload_length() != 8:
                raise ValueError('Payload length was {}, expected 8'.format(m.payload_length()))

            # data is sent as ASCII decimal data
            return int(m.raw_payload())
        else:
            raise ValueError('Payload missing')

#    def dump_flash(self):
#        """
#        This issues a dump of the entire user flash of the printer.
#        """
#        size = self.get_user_flash_storage_size()
#        addr = 0
#        count = 100
#        buf = None
#        while addr < size:
#            print('addr: {:02X}, count: {}, size: {}'.format(addr, count, size))
#            (m, b) = retrieve_flash_storage(count, addr)
#            print('Read {} bytes'.format(len(b)))
#            addr +=

    def retrieve_flash_storage(self, count=100, addr=0):
        """
        Retrieves 'count' bytes beginning at address 'addr'.
        IBM suggests that the amount of data requested to be held below 200 bytes, at least for rs-485 connected printers.
        You can retrieve the amount of flash storage present by calling "get_user_flash_storage_size".
        """
        pass

    def receive_message(self):
        """
        Assuming that a command has been sent that triggers a response from the printer, this function retrieves it
        and returns a PrinterMessage object that represents the message. Note that the message size reported by the
        printer is discarded.
        """
        length_bytes = self.__device.read(2)
        if len(length_bytes) != 2:
            raise ValueError('Did not receive 2 length-bytes, read {} instead'.format(len(length_bytes)))
        message_length = struct.unpack('>H', length_bytes)[0]

        if self.__debug:
            print('Message length: {}'.format(message_length))
        buf = self.__device.read(message_length - 2)    # we've already read the first two bytes, they're included in the message length
        if self.__debug:
            print('RAW MESSAGE: ', end='')
            SureMark.hexdump(buf)
        return PrinterMessage(buf, debug=self.__debug)
