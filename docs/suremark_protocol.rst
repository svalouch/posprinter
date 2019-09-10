######################
Communication Protocol
######################

Communication is, on the lowest level, as simple as sending bytes over a serial connection can be. For the examples, we'll assume that ``ser`` is a ``pyserial`` object set up to communicate with the printer. The basic setup could, for example, look like this:

.. code-block:: python

    import serial

    with serial.Serial('/dev/ttyUSB0', 19200, timeout=10) as ser:
        # code goes here

Sending text and commands is as easy as issuing read and write calls. For example, to write a text and cut the paper (in the `thermal` station), one would do the following:

.. code-block:: python

    ser.send(b'Hello World')
    ser.send(b'\x0c')

This will send ``Hello World`` to the printers buffer (which will either start printing right away or wait for paper), sending ``0x0c`` instructs it to print the buffer content and then cut the paper.

This can be done on the shell as well by using ``echo(1)``:

.. code-block:: shell

    echo "Hello World" > /dev/ttyUSB0
    echo -e -n "\x0c" > /dev/ttyUSB0

Note that without ``-n``, an empty line would be print `after` the paper is cut. If the baud rate and other settings need to be adjusted on the shell, use the ``stty(1)`` utility before issuing commands.

This is already enough to control the printer and print text or change settings. However, the printer will soon stop working, as for some commands it will **answer** with a response. If it is not read, it will fill up the buffer and if it is full, no data will be transfered anymore. Use ``ser.read()`` in python or ``cat(1)`` in the terminal.

The responses are important, however, as we'll show in the next section. They give detailed information about the state of the printer and return data requested from things like the MICR reader, document scanner and so on.

Printer responses
*****************
When sending a command that triggers a response from the printer (such as status inquiries or requests for changing certain settings), the printer responds with two bytes of data that defines the `message length` (including these two bytes), followed by the message. To read the entire response, the function :func:`~posprinter.suremark.SureMark.receive_message` first reads two bytes and converts them to an integer to determin the length of the entire message, and then it reads the amount of bytes minus the two that were already read. A very simple version of this could look like this:

.. code-block:: python

    # read the first two bytes containing the message length
    length_bytes = ser.read(2)
    # convert the data read to an integer
    message_length = struct.unpack('>H', length_bytes)[0]

    message = ser.read(message_length - 2)

The message content is binary data that needs to be interpreted. The class :class:`posprinter.suremark_status.PrinterMessage` can be used to decode the message and provides a higher level interface to its contents. Additionally, :mod:`~posprinter.suremark_debug` defines some functions that help in understanding the binary data.

The message itself is always at least 8 bytes long and gives an overview over the printers current state. A set of bits indicates if the message contains extra data, such as identifying information ("Printer ID", to determin the model and features), MICR read, user flash read or MCT counters. If the corresponding bit is set, the data is appended to the message. Note that IBM chose to index their bytes beginning with `one`, not `zero` in the documentation. The bytes of the base message contain:

#. Printer ID
#. Engineering Code (EC) level, aka firmware version
#. MICR data (even if no MICR reader is present)
#. MCT response (contains the response for an MCT read command)
#. User flash data (contains the response to a read command to user flash)
#. Contents of a scanned image
#. Print buffer
#. Feed error

.. note::

    The printers won't send messages unprovoked, so in order to know when, for example, the cover has been closed, periodically checking its state and parsing the status message is required.

Base response
=============
The base response is 8 bytes long and is always sent when returning data to the user. For debugging, the function :func:`~posprinter.suremark_debug.verbose_status_byte` can decode individual bytes and produce human readable output. This function is used to generate the detail output below, which is the base message in response to a "Printer ID" query whose payload will be decoded after this section. Let's take a look at the data of the base message:

Byte 1: Command and printer status
----------------------------------
::

    Byte 0: Status byte 1
    # 76543210
    0b00001000 = 0x08 = 8
      ||||||||
      |||||||+-- 0 Command not complete
      ||||||+--- 0 Cash receipt not in right home position
      |||||+---- 0 Print head is not in left home position
      ||||+----- 1 Print head is in the right home position
      |||+------ 0 Reserved 0
      ||+------- 0 Ribbon cover not open
      |+-------- 0 No cash receipt print error
      +--------- 0 Command accepted

The first byte indicates if the command was complete, which seems to be 0 most of the times. The next three contain position indications for the print head, not all of this is applicable to all models: Models without a `impact` station seem to report the head in the right home position all the time. The sixth bit indicates whether the printer detected that its `cover` is open. It refuses to print in this state, so in order not to clog the buffer, one might want to pause during this state and query for status periodically. The next bit indicates that the last print command did not end in an error condition, and the last one indicates that the last command was accepted (mostly: syntactically correct and known to the printer).

Byte 2: Document and Buffer status
----------------------------------
::

    Byte 1: Status byte 2
    # 76543210
    0b01001111 = 0x4F = 79
      ||||||||
      |||||||+-- 1 Document not ready
      ||||||+--- 1 Document not present under the front sensor
      |||||+---- 1 Document not present under the top sensor
      ||||+----- 1 Reserved 1
      |||+------ 0 Print buffer not held
      ||+------- 0 Not in the open throat position
      |+-------- 1 Buffer empty
      +--------- 0 Buffer not full

The first three bytes indicate if it has detected a document in its `impact` station. As the ``Tx6`` doesn't feature such a station, the bits are ``1`` all the time. For a ``Tx1`` or similar, these indicate if the document is ready to be printed on (first bit), if it is detected under the front (second bit) or top (third bit) sensor.
There is a neat "trick" of sorts: if you send data to the `impact` station, it will print it as soon as it detects paper, so one does not have to wait for a document to be inserted.

The last two can be used for controlling the spooling to keep the printers buffer from overfilling while making sure it doesn't run dry. This is important (and currently not implemented in posprinter) to sustain a high printing speed, similar to keeping a backup tape spooling. Worthy of note: the printer will respond to its own head temperature, and slow down to keep it from overheating, printing less dots in a line will increase print speed. Thus, the printing speed is not guaranteed and controlling the buffer is important.

.. todo::

    bit 5 and 6

Byte 3: Error indicators
------------------------
::

    Byte 2: Status byte 3
    # 76543210
    0b00000000 = 0x00 = 0
      ||||||||
      |||||||+-- 0 Memory sector is not full
      ||||||+--- 0 No home error
      |||||+---- 0 No document error
      ||||+----- 0 No flash/MCR error
      |||+------ 0 Reserved 0
      ||+------- 0 User flash storage sector is not full
      |+-------- 0 No firmware error
      +--------- 0 Command complete or line printed

This byte contains error indicators mostly. The second byte, for example, indicates whether the printer found its home position (`impact` station only). The flash/MCR error indicates if a command working with or querying the user flash or MCR region failed. The last bit is another command status response and should be watched.

Byte 4: Engineering Code (EC) level
-----------------------------------
::

    Byte 3: Status byte 4: Engineering code (EC) level
    # 76543210
    0b01000100 = 0x44 = 68
      ||||||||
      |||||||+-- 0 EC: 0
      ||||||+--- 0 EC: 0
      |||||+---- 1 EC: 1
      ||||+----- 0 EC: 0
      |||+------ 0 EC: 0
      ||+------- 0 EC: 0
      |+-------- 1 EC: 1
      +--------- 0 EC: 0

Though it might sound odd, the printer always includes its firmware version with every status message. When checking for new firmware, the level should be read in hex, so for this particular ``Tx6``, the firmware level is ``44``.

Byte 5: Printer response to commands
------------------------------------
::

    Byte 4: Status byte 5: Printer response to commands
    # 76543210
    0b00100001 = 0x21 = 33
      ||||||||
      |||||||+-- 1 Responding to a Printer ID request
      ||||||+--- 0 Not responding to an EC level request
      |||||+---- 0 Not responding to a MICR read command
      ||||+----- 0 Not responding to a MCT read command
      |||+------ 0 Not responding to a user flash read command
      ||+------- 1 Reserved 1
      |+-------- 0 Scan did not complete successfully
      +--------- 0 Not responding to a Retrieve scanned image command

This byte is very important, it indicates the type of command this message is the response to. In this example, the printer responds to a "ID" request, the most basic request. Thus, the first bit is 1 to indicate that. Usually, only one bit is set (appart from the reserved bit 6). The second bit is hardly used as the firmware level is included with every message anyway. The next three indicate if it is a response to a MICR, MCT or user flash read command. If any of these is set, additional bytes after the end of the regular eight bytes contain the payload. An early indication for this is when the first two bytes of the raw response indicate a length of more than ten bytes.

Byte 6: Current line count
--------------------------
::

    Byte 5: Status byte 6: Current line count
    # 76543210
    0b00000000 = 0x00 = 0
      ||||||||
      |||||||+-- 0 Line count 0: 0
      ||||||+--- 0 Line count 1: 0
      |||||+---- 0 Line count 2: 0
      ||||+----- 0 Line count 3: 0
      |||+------ 0 Line count 4: 0
      ||+------- 0 Line count 5: 0
      |+-------- 0 Line count 6: 0
      +--------- 0 Line count 7: 0

A counter counting the number of lines, reset at power off.

Byte 7: Additional status
-------------------------
::

    Byte 6: Status byte 7: Extended status
    # 76543210
    0b00101000 = 0x28 = 40
      ||||||||
      |||||||+-- 0 Reserved 0
      ||||||+--- 0 Reserved 0
      |||||+---- 0 Reserved 0
      ||||+----- 1 Cash drawer status 1
      |||+------ 0 Print key not pressed
      ||+------- 1 Reserved 1
      |+-------- 0 Station select: Not document insert station
      +--------- 0 No document feed error (MICR read/flip check)

Another set of bits that convey status information. The documentation gives no real clue about the cash drawer status, the best guess so far is that it indicates if the solenoid was activated by a command to the printer. An important bit is bit 7, which indicates which station is selected: The `document insert station` is another name for the `impact` station, because documents (usually cheques) are inserted into it to be printed on, or the thermal station, which is the only one selectable on the ``Tx6`` model this response comes from.

The last bit indicates if there was an error feeding the document to the MICR reader or cheque flipper mechanism, which is also unused in the ``Tx6`` model.

Byte 8: Temperature
-------------------
::

    Byte 7: Status byte 8: Thermal
    # 76543210
    0b00000000 = 0x00 = 0
      ||||||||
      |||||||+-- 0 Reserved 0
      ||||||+--- 0 Reserved 0
      |||||+---- 0 Reserved 0
      ||||+----- 0 Reserved 0
      |||+------ 0 Reserved 0
      ||+------- 0 Reserved 0
      |+-------- 0 Reserved 0
      +--------- 0 Print head and motor cool enough to continue printing

The only used bit is the last one, indicating if the printer is slowing down because of the print head temperature. When printing too much in a short time frame, the printer sets this bit to ``1`` and slows the printing speed down, thereby reducing the energy needed by the print head and thus reducing its temperature. There is no control over this behaviour, and buffer control (see above) should be used to prevent overflowing the print buffer.

Response: Printer ID
====================
The above message indicates that it is the response to a "Printer ID" query, which is used to narrow down the printer model and installed features. The count begins with 0, but actually the first byte comes after the last (eighth) byte of the base response above. The message is decoded by the function :func:`~posprinter.suremark_debug.verbose_printer_id`, but we'll take a look at it for completeness and because the authors don't want to use the code as the sole source for documentation.

Byte 0: Rough device type
-------------------------
::

    Byte 0: Device type
    # 76543210
    0b00110000 = 0x30 = 48
      ||||||||
      |||||||+-- 0
      ||||||+--- 0
      |||||+---- 0
      ||||+----- 0
      |||+------ 1
      ||+------- 1
      |+-------- 0
      +--------- 0
    
As can be seen, the first byte hints at the device type. It it is ``0x30``, the printer is "`non-TIx8 or Tx9, or one of them in Tx4 compatibility mode`", if it is ``0x31`` then it is a "`Tx8 or Tx9`". This basically distinguishes between "the really old ones" and the "newer ones". Further inspection is required.

Byte 1: Device ID
-----------------
::

    Byte 1: Device ID
    # 76543210
    0b00000011 = 0x03 = 3
      ||||||||
      |||||||+-- 1
      ||||||+--- 1
      |||||+---- 0
      ||||+----- 0
      |||+------ 0
      ||+------- 0
      |+-------- 0
      +--------- 0

This byte contains the actual printer model and hints at some of the features it has. For obvious reasons, the color of the printer is not known to the firmware.

* ``0x00`` indicates ``Tx1`` and ``Tx2``, which are the first models released, with `thermal` and `impact` stations.
* ``0x01`` indicates ``Tx3``, ``Tx4``, ``Tx8``, ``Tx9``, ``TG3`` or ``TG4``, featuring a higher printing speed as the earlier models.
* ``0x02`` stands for ``Tx3``, ``Tx4´´, TG3`` or ``TG4`` with the `2MB option`, but otherwise identical to the base model.
* ``0x03`` means that it is a ``Tx6`` base model, meaning no `impact` station and 512K of flash.
* ``0x04`` denotes the same models as ``0x02`` but with the `8MB option` installed.
* ``0x05`` is like ``0x03`` with the `8MB option` installed.
* ``0x06`` is marked as `reserved` in the documentation.
* ``0x07`` is like ``0x03``, but with the `2MB option` installed.

Bytes 2 and 3: Features
-----------------------
::

    Byte 2: First byte of features
    # 76543210
    0b00001000 = 0x08 = 8
      ||||||||
      |||||||+-- 0
      ||||||+--- 0
      |||||+---- 0
      ||||+----- 1
      |||+------ 0
      ||+------- 0
      |+-------- 0
      +--------- 0
    
    Byte 3: Second byte of features
    # 76543210
    0b00000000 = 0x00 = 0
      ||||||||
      |||||||+-- 0
      ||||||+--- 0
      |||||+---- 0
      ||||+----- 0
      |||+------ 0
      ||+------- 0
      |+-------- 0
      +--------- 0

The two following bytes the details of the features the printer has. Depending on the first byte that divides the world into two categories, the bits have different meanings: The "newer" models define most of the bits as `reserved`. Unless otherwise noted, the following table gives the meaning for a set (1) bit:

+----------+-----------------------------------------------------+----------------+
| Byte/Bit | ``0x30``                                            | ``0x31``       |
+==========+=====================================================+================+
| 0/0      | MICR reader present                                 | Reserved       |
+----------+-----------------------------------------------------+                |
| 0/1      | Cheque flipper present                              |                |
+----------+-----------------------------------------------------+                |
| 0/2      | 2MB option present                                  |                |
+----------+-----------------------------------------------------+----------------+
| 0/3      | XON/XOFF mode (0=software, 1=hardware flow control)                  |
+----------+----------------------------------------------------------------------+
| 0/4      | Reserved                                                             |
+----------+-----------------------------------------------------+----------------+
| 0/5      | 2MB user flash option                               | Reserved       |
+----------+-----------------------------------------------------+----------------+
| 0/6      | Two-colour printing enabled                                          |
+----------+----------------------------------------------------------------------+
| 0/7      | Model 4 emulation mode active                                        |
+----------+----------------------------------------------------------------------+
| 1/0      | Set for 58mm paper                                                   |
+----------+-----------------------------------------------------+----------------+
| 1/1      | ``Tx8`` or ``Tx9`` emulating ``Tx4``                | Not applicable |
+----------+-----------------------------------------------------+----------------+
| 1/2      | Full scanning Model ``Tx9`` printer                                  |
+----------+----------------------------------------------------------------------+
| 1/3      | USB interface is: "internal" / "not internal or using RS-232/RS-485" |
+----------+----------------------------------------------------------------------+
| 1/4      | Printer is an RPQ, scanner disabled                                  |
+----------+----------------------------------------------------------------------+
| 1/5      | Reserved                                                             | 
+----------+                                                                      |
| 1/6      |                                                                      |
+----------+                                                                      |
| 1/7      |                                                                      |
+----------+----------------------------------------------------------------------+

Byte 4: EC level
----------------
::

    Byte 4: EC level (of loaded code)
    # 76543210
    0b01000100 = 0x44 = 68
      ||||||||
      |||||||+-- 0
      ||||||+--- 0
      |||||+---- 1
      ||||+----- 0
      |||+------ 0
      ||+------- 0
      |+-------- 1
      +--------- 0

The last byte indicates the firmware level, as mentioned above, this is a hexadecimal number, so this particular model has level (or version) ``44``

Response: MICR read
===================

Response: MCT read
==================

Response: User flash read
=========================

Response: Document scan
=======================

