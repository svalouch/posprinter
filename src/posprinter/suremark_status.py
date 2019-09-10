
from .suremark_debug import verbose_status_byte, verbose_extended_status

class PrinterMessage:
    """
    Represents a message from the printer. A message consists of the following:

    * 2 bytes indicating the message size including these two bytes
    * 8 bytes of general status response
    * depending on the previous command and indicated by bits set in the previous 8 bytes, additional information such as:

     * Printer ID
     * EC level
     * MICR data
     * MCT read
     * user flash read
     * contents of a scanned image
     * print buffer
     * feed error
     * etc.

    Not all of the above are available for all printer models.
    The additional data is referred to as "payload" in this class.

    Note that he first two bytes indicating the message length have to be omitted when working with this class!
    Also note that IBMs documentation indexes the response bytes beginning with 1 in the tabular documentation.
    """

    def __init__(self, data, debug=False):
        if len(data) < 8:
            raise ValueError('Length of data less than minimum message length (8)')
        self._data = data
        self._debug = debug

        if debug:
            verbose_status_byte(data[0], 0)
            verbose_status_byte(data[1], 1)
            verbose_status_byte(data[2], 2)
            verbose_status_byte(data[3], 3)
            verbose_status_byte(data[4], 4)
            verbose_status_byte(data[5], 5)
            verbose_status_byte(data[6], 6)
            verbose_status_byte(data[7], 7)

    def has_payload(self):
        return len(self._data) > 8

    def payload_length(self):
        return len(self._data) - 8

    def raw_payload(self):
        if not self.has_payload():
            return None
        return self._data[8:]

    # ########
    # Byte 0 #
    # ########
    def command_complete(self):
        # byte 0 bit 0
        return self._data[0] & (1 << 0) != 0

    def command_rejected(self):
        # byte 0 bit 7
        return self._data[0] & (1 << 7) != 0

    # ########
    # Byte 1 #
    # ########
    # ########
    # Byte 2 #
    # ########
    # ########
    # Byte 3 #
    # ########
    def engineering_code_level(self):
        # byte 3
        return self._data[3]

    # ########
    # Byte 4 #
    # ########
    def is_printer_id_response(self):
        # byte 4 bit 0
        return self._data[4] & (1 << 0) != 0

    def is_ec_level_response(self):
        # byte 4 bit 1
        return self._data[4] & (1 << 1) != 0

    def is_micr_response(self):
        # byte 4 bit 2
        return self._data[4] & (1 << 2) != 0

    def is_mct_response(self):
        """
        Things like statistics counters etc.
        """
        # byte 4 bit 3
        return self._data[4] & (1 << 3) != 0

    def is_user_flash_read_response(self):
        # byte 4 bit 4
        return self._data[4] & (1 << 4) != 0

    def scan_success(self):
        # byte 4 bit 6
        return self._data[4] & (1 << 6) != 0

    def is_retrieve_scanned_image_response(self):
        # byte 4 bit 7
        return self._data[4] & (1 << 7) != 0

    #def user_flash_size(self):
    #    if not self.is_user_flash_

    # ########
    # Byte 5 #
    # ########
    def current_line_count(self):
        # byte 5
        return self._data[5]


    # ########
    # Byte 6 #
    # ########
    # ########
    # Byte 7 #
    # ########

    # payload handling

class PrinterID:
    """
    Represents the printer ID response information for ease of access.
    Note that it is not possible to figure out the *exact* model. One of the reasons is that the printer does not know the color
    of its case, so it is never possible to tell a TI3 from a TG3. It is also not possible to distinguish Tx1 and Tx2 based on
    the information available here. Tx2 has a MICR reader and cheque flipper, so it could be possible to probe for the features
    elsewhere.
    """

    MODEL_UNKNOWN = 0
    MODEL_Tx1 = 1
    MODEL_Tx2 = 2
    MODEL_Tx3 = 3
    MODEL_Tx4 = 4
    MODEL_Tx6 = 5
    MODEL_Tx8 = 6
    MODEL_Tx9 = 7

    def __init__(self, data):
        self.__data = data

    def is_Tx1(self):
        return self.__data[1] == 0x00 and self.__data[2] & (1 << 0) == 0

    def is_Tx2(self):
        return self.__data[1] == 0x00 and self.__data[2] & (1 << 0) != 0

    def is_Tx3(self):
        if self.__data[0] == 0x30:
            return self.__data[1] in [0x01, 0x02, 0x04]
        return False

    def is_Tx4(self):
        return self.is_Tx3()

    def is_Tx8(self):
        return False
