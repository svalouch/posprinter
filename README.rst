##########
PosPrinter
##########

A Python 3 library for interacting with "`Point of sale <https://en.wikipedia.org/wiki/Point_of_sales>`_" printer stations. These printers typically support RS-232 serial communications, most of them are `thermal printers <https://en.wikipedia.org/wiki/Thermal_printing>`_, though some are `impact printers <https://en.wikipedia.org/wiki/Printer_(computing)#Impact_printers>`_ or feature an impact printing station in addition to the thermal printer.

Supported hardware
******************
Currently, the library supports the `IBM SureMark (aka IBM 4610) <https://en.wikipedia.org/wiki/IBM_4610>`_ line of products and has been tested with models TF6 and TI1.

IBM 4610 "SureMark"
===================
IBMs printers are intelligent, they hold a lot of internal state and there is a communication protocol in place to set or get settings, values etc. IBM has documented the RS-232 protocol (see Wikipedia page). Additionally, many (especially early models) support RS-485 communication, but this hasn't been tested.

The printers are intended to be set up by an operator at the store, who sets things like fonts, margins and text snippets or graphics and carries the configured printer over to the point of sale terminal. The printer remembers its state in its internal flash, the POS terminal doesn't need to care about these settings and can send text with minimal amounts of control characters.

For example, if you see an older terminal print a large preamble (store name and logo, loads of legal text) before the actual receipt is printed, this text is most likely stored in the printer and the terminal sends a simple command before the receipt data that calls the text from the printers internal memory.

On the other hand, printing is as simple as using ``echo(1)``:

.. code-block:: bash

    # Print "Hello World"
    echo "Hello World" > /dev/ttyUSB0
    # Cut the paper
    echo -e -n "\x0c" > /dev/ttyUSB0

Example
*******
The example expects a SureMark printer connected to ``/dev/ttyUSB0`` and prints information about the printer:

.. code-block:: python

    import serial
    from posprinter.suremark import SureMark
    
    with serial.Serial('/dev/ttyUSB0', 19200, timeout=10) as ser:
        p = SureMark(ser, debug=False)  # turn debug on to see extensive output
    
        print('User flash size: {} bytes'.format(p.get_user_flash_storage_size()))
        print('Manufactured (WWYY): {}'.format(p.get_printer_usage_stat_manufacture_week()))
        print('Paper cuts: {}'.format(p.get_printer_usage_stat_number_paper_cuts()))
        print('Paper cuts failed: {}'.format(p.get_printer_usage_stat_number_failed_paper_cuts()))
        print('Thermal motor steps: {}'.format(p.get_printer_usage_stats_thermal_motor_steps()))
        print('Thermal characters: {}'.format(p.get_printer_usage_stats_printed_characters_thermal()))
        print('Customer Receipt cover opened: {}'.format(p.get_printer_usage_stats_thermal_cover_opened()))
        print('Barcodes printed: {}'.format(p.get_printer_usage_stats_barcodes_printed()))
        # only for models that feature a beeper
        print('Tone sounds: {}'.format(p.get_printer_usage_stats_tone_sounds()))
        # print a barcode in the currently selected station
        p.barcode_set_hri_position(SureMark.BARCODE_HRI_POSITION_BOTH)
        p.barcode_set_hri_font(SureMark.BARCODE_HRI_FONT_DEFAULT)
        p.barcode('1234567890', type=SureMark.BARCODE_UPC_A)
        # cut the paper in the currently selected station
        p.cut()
