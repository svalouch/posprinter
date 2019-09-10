###
API
###

The `SureMark` class defines a large set of fields that map protocol directives to names. Some can work on their own (``CMD_PRINT_FORM_FEED_CUT``), but many require additional parameters (``CMD_SET_PRINT_MODE``). For ease of use, there are functions that can be used that build and send the command with parameters and perform validation of the parameter(s).

.. autoclass:: posprinter.suremark.SureMark
   :members:

.. autoclass:: posprinter.suremark_status.PrinterMessage
   :members:

.. autoclass:: posprinter.suremark_status.PrinterID
   :members:

Debug helper
************

.. autofunction:: posprinter.suremark_debug.hexdump

.. autofunction:: posprinter.suremark_debug.verbose_status_byte

.. autofunction:: posprinter.suremark_debug.verbose_extended_status

.. autofunction:: posprinter.suremark_debug.verbose_printer_id

