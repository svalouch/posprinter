
###################
IBM 4610 "SureMark"
###################

This line of point of sale printers is very common, used models can be picked up from ebay for less than EUR 100 commonly. The machines are very sturdy and built to last, even the full-plastic ones like the TF6. `posprinter` is developed for this type of printer, mainly.

The sections up until This page "Communication protocol" are largely based on the Wikipedia `article <https://en.wikipedia.org/wiki/IBM_4610>`_ on IBM 4610 printers, with some additions.

Model overview
**************

Most printers come in two versions, differing only in their color:

* ``TG`` and ``TF`` models are `iron gray`
* ``TI`` and ``TM`` models are `pearl white`

Other than that, models with the same number are identical.

All printers feature a `thermal printing` station for receipts, most feature a second `impact printing` station for cheques. Text and commands are sent to the currently selected station, the printer remembers the setting.

Some printers with `impact` stations feature a ``MICR`` reader for reading cheques printed with a magnetic inc (which is not supported by this library), some can turn cheques around to print the backside in one go without requiring the operator to flip it.

Another feature is an internal journal, that records what is printed into an internal buffer that can be read back later, there are even models that can print a paper trail stored inside the housing (``TN3``/``TN4``).

+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Model             | Thermal | Impact | MICR | Flipper | Scanner | Introduced | Replaced by     | Notes                                                                                                                                |
+===================+=========+========+======+=========+=========+============+=================+======================================================================================================================================+
| ``TI1`` / ``TG1`` |  Yes    | Yes    | No   | No      | No      | 1996       | ``TI3``/``TG3`` | No Euro symbol                                                                                                                       |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI2`` / ``TG2`` |  Yes    | Yes    | Yes  | Yes     | No      |            | ``TI4``/``TG4`` | No Euro symbol                                                                                                                       |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI3`` / ``TG3`` |  Yes    | Yes    | No   | No      | No      |            |                 |                                                                                                                                      |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TN3``           |  Yes    | Yes    | No   | No      | No      |            |                 | Three-station model that includes integrated paper journaling                                                                        |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TN4``           |  Yes    | Yes    | Yes  | Yes     | No      |            |                 | Same as TN3 with additional checkque handling                                                                                        |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI4`` / ``TG4`` |  Yes    | Yes    | Yes  | Yes     | No      |            |                 |                                                                                                                                      |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI5`` / ``TG5`` |  Yes    | Yes    | No   | No      | No      | 1999       |                 | Like TI3 / TG3 but for the Chinese market, featuring DBCS character support. Additional 16MB flash for DBCS characters.              |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI8`` / ``TG8`` |  Yes    | Yes    | Yes  | Yes     | Yes     |            | ``TI9``/``TG9`` | Powered flipper, freely manageable flash storage                                                                                     |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TI9`` / ``TG9`` |  Yes    | Yes    | Yes  | Yes     | Yes     |            |                 | Powered flipper, freely manageable flash storage, compliance with Check 21 legislation                                               |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TF6`` / ``TM6`` |  Yes    | No     | No   | No      | No      |            |                 | Audible alarm (Beeper), wall mountable, spill resistant, optional additional spill cover, optional external paper roll, power switch |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+
| ``TF7`` / ``TM7`` |  Yes    | No     | No   | No      | No      |            |                 | Like TF6 / TM6 but for the Chinese market, featuring DBCS character support. Additional 16MB flash for DBCS characters.              |
+-------------------+---------+--------+------+---------+---------+------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------+

Additionally, there are models with a D instead of a T. This denotes a different warranty service ("Depot repair" instead of "IOR 24x7").

When looking for used ones to play around with, it's probably best to go for a ``Tx6`` model. It doesn't include an `impact` station, but its other features make it an alrounder, especially because it can be mounted on a wall and has a beeper.


Printer overview (Hardware)
***************************
As mentioned before, the printers are very sturdy and reliable. Early models and most models featuring an `impact` station are basically plastic-covered, heavy metal constructions, while later models reduce the amount of metal, especially the ``Tx6`` line which features an all-plastic body except for the actual thermal printing assembly. Even the ``Tx6`` is very sturdy, and its low weight allows for wall-mounting and feeding paper from a (large) role through a slot in its base.

Power
=====
There are mostly two ways to power the printers:

* Traditionally, power is fed in through a ``PoweredUSB``-connection, which is an attempt at delivering high amounts of current while still being compatible with traditional USB connectors. The `Wikipedia article <https://en.wikipedia.org/wiki/PoweredUSB>`_ has a nice overview. The sockets can be found almost exclusively on point of sale terminals and in case of the SureMark printers does not deliver data, but power only. In this mode, communication is exclusively made through RS-232. Printers typically require 24V at up to 4A. The plug is a **TODO**, power can be delivered through a decent-sized power-brick and a custom cable.
* In-band with RS-485 at 35V, which also selects this as the sole communications method.

Newer models (those with a USB socket for data) may contain different connectors for power delivery.

Interface
=========
The older models feature, as mentioned above, RS-232 and RS-485, while IBM released newer models or swappable interface cards for some models that feature USB connection. Note that not all printers have swappable interface cards, especially the aforementioned ``Tx6`` models have the interface built into them to allow for smaller size. This library is not tested with RS-485 or USB connections due to a lack of suitable hardware.

Printers communicate at:

* RS-232: either 9600 or 19200 baud, the newer ``Tx9`` and ``Tx9`` operate at up to 115200 baud
* RS-485: 185.5 kbit/s
* USB: 12MBit/s

Additionally, some models feature a registered jack (RJ) that is meant to operate the solenoid in a cash register. This was probably done so that the expensive sales terminal doesn't need to deal with high currents which could damage the electronics if the wiring is damaged and instead uses the relatively cheap printer that has a large power budget anyway and doesn't need additional power to operate the solenoid.

Printer overview (Software)
***************************
The printers do, unlike traditional printers you might use at work, feature some intelligence. They have an internal flash that contains settings and state information that is persistet across power cycles. When used in a traditional shop (usually integrated into the cover of the point of sales terminal, the units are most commonly set up by an operator behind the scenes and then carried to the terminal. The printers can store relatively large blocks of text and some graphics, which can be printed using a command with the slot ID of the memory area. Thus, a terminal does not need to send the large amounts of legal texts or shove the stores logo pixel by pixel over the line (which could very well block the sales terminal until it's done sending), but instead just instructs the printer to print from a predefined storage slot. This also eliminates the need to update the sales terminal with new texts or logos, which can be a tedious process. Instead, at the end of the day, an operator collects the printers, reprograms them with the new texts and logos and moves them back.

Most commands send to the printer that change settings like character size, font, margins etc. are sticky and persistent. If, for example, **bold** font is selected, all text following that command will be printed in **bold** font, until the next change to that setting is sent.

To support all this, the printers are equipped with their own operating system, and offer a large amount of backwards compatibility, commands sent to a 1996 ``Tx1`` work (with very few excptions) on a 1999 ``Tx5`` or an even later ``Tx6``, provided that the `impact` station is not used.

The printer is also able to respon to queries about itself. The printers keep counters that give an indication of how (much) a particular one has been used, such as how often the paper was cut or how much distance the paper was moved.


TODO
****

The :class:`~posprinter.suremark.SureMark` contains definitions of a large set of binary data that represents commands. It also 



IBMs printers are intelligent, they hold a lot of internal state and there is a communication protocol in place to set or get settings, values etc. IBM has documented the RS-232 protocol (see Wikipedia page). Additionally, many (especially early models) support RS-485 communication, but this hasn't been tested.

The printers are intended to be set up by an operator at the store, who sets things like fonts, margins and text snippets or graphics and carries the configured printer over to the point of sale terminal. The printer remembers its state in its internal flash, the POS terminal doesn't need to care about these settings and can send text with minimal amounts of control characters.

For example, if you see an older terminal print a large preamble (store name and logo, loads of legal text) before the actual receipt is printed, this text is most likely stored in the printer and the terminal sends a simple command before the receipt data that calls the text from the printers internal memory.

On the other hand, printing is as simple as using ``echo(1)``:
.. code-block:: bash

    # Print "Hello World"
    echo "Hello World" > /dev/ttyUSB0
    # Cut the paper
    echo -e -n "\x0c" > /dev/ttyUSB0
