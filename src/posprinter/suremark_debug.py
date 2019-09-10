#
# This file contains definitions of text and functions useful for debugging
#

def hexdump(s):
    print(":".join("{:02x}".format(c) for c in s))

# Textual messages for the bits in the status message response
status_summary_text = [
    # byte 0
    [
        ['Command not complete','Command complete'],    # bit 0
        ['Cash receipt not in right home position','Cash receipt in right home position'],
        ['Print head is not in left home position','Print head is in left home position'],
        ['Print head is not in the document right home position','Print head is in the right home position'],
        ['Reserved 0','Reserved 0, but set 1!'],
        ['Ribbon cover not open','Ribbon cover open'],
        ['No cash receipt print error','Cash receipt print error'],
        ['Command accepted','Command rejected'],
    ],
    [
        ['Document ready','Document not ready'],
        ['Document present under the front sensor','Document not present under the front sensor'],
        ['Document present under the top sensor','Document not present under the top sensor'],
        ['Reserved 1, but set 0!','Reserved 1'],
        ['Print buffer not held','Print buffer held'],
        ['Not in the open throat position','Open throat position'],
        ['Buffer not empty','Buffer empty'],
        ['Buffer not full','Buffer full (less than 1k left)'],
    ],
    [
        ['Memory sector is not full','Memory sector is full'],
        ['No home error','Home error'],
        ['No document error','Document error'],
        ['No flash/MCR error','Flash EPROM or MCT load error'],
        ['Reserved 0','Reserved 0, but set 1!'],
        ['User flash storage sector is not full','User flash storage sector is full'],
        ['No firmware error','Firmware error, CRC on the firmware failed'],
        ['Command complete or line printed','Command not complete'],
    ],
    [
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
        ['EC: 0','EC: 1'],
    ],
    [
        ['Not responding to a Printer ID request','Responding to a Printer ID request'],
        ['Not responding to an EC level request','Responding to an EC level request'],
        ['Not responding to a MICR read command','Responding to a MICR read command'],
        ['Not responding to a MCT read command','Responding to a MCT read command'],
        ['Not responding to a user flash read command','Responding to a user flash read command'],
        ['Reserved 1, but set 0','Reserved 1'],
        ['Scan did not complete successfully','Scan completed successfully'],
        ['Not responding to a Retrieve scanned image command','Responding to a Retrieve scanned image command'],
    ],
    [
        ['Line count 0: 0','Line count 0: 1'],
        ['Line count 1: 0','Line count 1: 1'],
        ['Line count 2: 0','Line count 2: 1'],
        ['Line count 3: 0','Line count 3: 1'],
        ['Line count 4: 0','Line count 4: 1'],
        ['Line count 5: 0','Line count 5: 1'],
        ['Line count 6: 0','Line count 6: 1'],
        ['Line count 7: 0','Line count 7: 1'],
    ],
    [
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Cash drawer status 0 (GND)','Cash drawer status 1'],
        ['Print key not pressed','Print key pressed'],
        ['Reserved 1, but set 0!','Reserved 1'],
        ['Station select: Not document insert station','Station select: Document insert station'],
        ['No document feed error (MICR read/flip check)','Document feed error (MICR read/flip check)'],
    ],
    [
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 0, but set 1!'],
        ['Reserved 0','Reserved 1'],
        ['Reserved 0','Reserved 1'],
        ['Print head and motor cool enough to continue printing','Print head or motor almost to hot to continue printing'],
    ],
]

# Names of the bytes in the status message sent by the printer
status_summary_bytes = [
    'Status byte 1',
    'Status byte 2',
    'Status byte 3: Error conditions',
    'Status byte 4: Engineering code (EC) level with all status messages',
    'Status byte 5: Printer response to commands',
    'Status byte 6: Current line count',
    'Status byte 7: Extended status', # name is just a guess
    'Status byte 8: Thermal',
]

def verbose_status_byte(c, bytenum):
    """
    Detailed print of a single byte of the status message sent by the printer.
    c is the byte in question, bytenum is used as an index in  "status_summary_text"
    """
    b0 = int(c & (1 << 0) != 0)
    b1 = int(c & (1 << 1) != 0)
    b2 = int(c & (1 << 2) != 0)
    b3 = int(c & (1 << 3) != 0)
    b4 = int(c & (1 << 4) != 0)
    b5 = int(c & (1 << 5) != 0)
    b6 = int(c & (1 << 6) != 0)
    b7 = int(c & (1 << 7) != 0)
    print('''Byte {17}: {18}
# 76543210
0b{7}{6}{5}{4}{3}{2}{1}{0} = 0x{16:02X} = {16}
  ||||||||
  |||||||+-- {0} {8}
  ||||||+--- {1} {9}
  |||||+---- {2} {10}
  ||||+----- {3} {11}
  |||+------ {4} {12}
  ||+------- {5} {13}
  |+-------- {6} {14}
  +--------- {7} {15}
    '''.format(
        b0, b1, b2, b3, b4, b5, b6, b7,
        status_summary_text[bytenum][0][b0],
        status_summary_text[bytenum][1][b1],
        status_summary_text[bytenum][2][b2],
        status_summary_text[bytenum][3][b3],
        status_summary_text[bytenum][4][b4],
        status_summary_text[bytenum][5][b5],
        status_summary_text[bytenum][6][b6],
        status_summary_text[bytenum][7][b7],
        c,
        bytenum,
        status_summary_bytes[bytenum],
    ))

# names of the bytes in the extended status response (printer id)
extended_status_byte_name = [
    'Device type',
    'Device ID',
    'First byte of features',
    'Second byte of features',
    'EC level (of loaded code)',
]

def verbose_extended_status(c, bytenum):
    """
    Verbosely prints a single byte of the extended status info (printer id)
    c is the byte in question, bytenum is used as an index for "extended_status_byte_name"
    """
    b0 = int(c & (1 << 0) != 0)
    b1 = int(c & (1 << 1) != 0)
    b2 = int(c & (1 << 2) != 0)
    b3 = int(c & (1 << 3) != 0)
    b4 = int(c & (1 << 4) != 0)
    b5 = int(c & (1 << 5) != 0)
    b6 = int(c & (1 << 6) != 0)
    b7 = int(c & (1 << 7) != 0)
    print('''Byte {9}: {10}
# 76543210
0b{7}{6}{5}{4}{3}{2}{1}{0} = 0x{8:02X} = {8}
  ||||||||
  |||||||+-- {0}
  ||||||+--- {1}
  |||||+---- {2}
  ||||+----- {3}
  |||+------ {4}
  ||+------- {5}
  |+-------- {6}
  +--------- {7}
    '''.format(
        b0, b1, b2, b3, b4, b5, b6, b7,
        c,
        bytenum,
        extended_status_byte_name[bytenum]
    ))

def verbose_printer_id(response):
    """
    Expects the five bytes from the extended status and parses them
    Prints the capabilities of the printer id response
    """
    if len(response) != 5:
        raise ValueError('Expected 5 bytes, got {} instead'.format(len(response)))
    verbose_extended_status(response[0], 0)
    verbose_extended_status(response[1], 1)
    verbose_extended_status(response[2], 2)
    verbose_extended_status(response[3], 3)
    verbose_extended_status(response[4], 4)

    if response[0] == 0x30:
        print('Type: non-TI8/TG8 or TI9/TG9 model, or TI8/TG8 or TI9/TG9 in TI4 mode')
    elif response[0] == x31:
        print('Type: TI8/TG8 or TI9/TG9 models in TI8 or TI9 mode')
    else:
        print('Type: unknown model 0x{:02X}'.format(response[0]))

    if response[1] == 0x00:
        print('Device ID: Models TI1 and TI2 (impact DI/thermal CR)')
    elif response[1] == 0x01:
        print('Device ID: Models TI3, TI4, TI8, TI9, TG3, and TG4 (high speed; impact DI/thermal CR)')
    elif response[1] == 0x02:
        print('Device ID: Models TI3, TI4, TG3, and TG4 with the 2MB option')
    elif response[1] == 0x03:
        print('Device ID: Models TF6 and TM6 (512K; thermal CR)')
    elif response[1] == 0x04:
        print('Device ID: Models TI3, TI4, TG3, and TG4 with the 8MB option')
    elif response[1] == 0x05:
        print('Device ID: Models TF6 and TM6 with the 8MB option')
    elif response[1] == 0x06:
        print('Reserved (0x06)')
    elif response[1] == 0x07:
        print('Models TF6 and TM6 with the 2MB option')
    else:
        print('Device ID: unknown model 0x{:02X}'.format(response[1]))

    if response[0] == 0x30:
        if response[2] & (1 << 0) != 0:
            print('Feature: [X] MICR is present')
        else:
            print('Feature: [ ] MICR is not present')
        
        if response[2] & (1 << 1) != 0:
            print('Feature: [X] Check Flipper is present')
        else:
            print('Feature: [ ] Check flipper is not present')

        if response[2] & (1 << 2) != 0:
            print('Feature: [X] Printer has the 2MB option')
        else:
            print('Feature: [ ] Printer does not have the 2MB option')

    if response[0] == 0x31:
        if response[2] & (1 << 0) != 0:
            print('Feature: [X] Reserved')
        else:
            print('Feature: [ ] Reserved')
        
        if response[2] & (1 << 1) != 0:
            print('Feature: [X] Reserved')
        else:
            print('Feature: [ ] Reserved')

        if response[2] & (1 << 2) != 0:
            print('Feature: [X] Reserved')
        else:
            print('Feature: [ ] Reserved')

    if response[2] & (1 << 3) != 0:
        print('Feature: [X] Printer is in XON/XOFF mode (software flow control)')
    else:
        print('Feature: [ ] Printer is not in XON/XOFF mode (hardware flow control)')

    if response[2] & (1 << 4) != 0:
        print('Feature: [X] Reserved')
    else:
        print('Feature: [ ] Reserved')

    if response[0] == 0x30:
        if response[2] & (1 << 5) != 0:
            print('Feature: [X] 2MB option is used for user flash memory')
        else:
            print('Feature: [ ] 2MB option is not used for user flash memory')
    if response[0] == 0x31:
        if response[2] & (1 << 5) != 0:
            print('Feature: [X] Reserved')
        else:
            print('Feature: [ ] Reserved')
        
    if response[2] & (1 << 6) != 0:
        print('Feature: [X] Two-color printing is enabled')
    else:
        print('Feature: [ ] Two color printing is disabled')

    if response[2] & (1 << 7) != 0:
        print('Feature: [X] Printer is in Model 4 emulation mode')
    else:
        print('Feature: [ ] Printer is not emulating Model 4')
    
    if response[3] & (1 << 0) != 0:
        print('Feature: [X] Printer is set for 58 mm paper')
    else:
        print('Feature: [ ] Printer is not set for 58 mm paper')

    if response[0] == 0x30:
        if response[3] & (1 << 1) != 0:
            print('Feature: [X] Model TI8/TG8 or TI9/TG9 is in TI4 mode')
        else:
            print('Feature: [ ] Model TI8/TG8 or TI9/TG9 is not in TI4 mode')
    elif response[0] == 0x31:
        print('Feature: [ ] Not applicable (TI8/TG8, TI9/TG9 in TI4 mode)')

    if response[3] & (1 << 2) != 0:
        print('Feature: [X] Full scanning Model TI9 or TG9 printer')
    else:
        print('Feature: [ ] Not a full scanning Model TI9 or TG9 printer')

    if response[3] & (1 << 3) != 0:
        print('Feature: [X] USB interface is internal to the printer')
    else:
        print('Feature: [ ] USB interface is not internal to the printer or using RS232/RS485 interface')

    if response[3] & (1 << 4) != 0:
        print('Feature: [X] Printer is an RPQ, scanner disabled')
    else:
        print('Feature: [X] Printer is not an RPQ')

    if response[3] & (1 << 5) != 0:
        print('Feature: [X] Reserved')
    else:
        print('Feature: [ ] Reserved')

    if response[3] & (1 << 6) != 0:
        print('Feature: [X] Reserved')
    else:
        print('Feature: [ ] Reserved')

    if response[3] & (1 << 7) != 0:
        print('Feature: [X] Reserved')
    else:
        print('Feature: [ ] Reserved')

    print('EC level of loaded code: {:02X}'.format(response[4]));

