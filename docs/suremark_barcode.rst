########
Barcodes
########
Barcodes of varying fashion are often required on cash receipts, and the printers offer builtin capability to print them without the need for pushing them pixel by pixel.

Additionally, the printers can add so-called `Human Readable Information` (``HRI``) below the barcode. This is a line of text that is aligned with the barcode and contains its content in letters and numbers.

The command that starts printing a barcode is :attr:`~posprinter.suremark.SureMark.CMD_BARCODE_PRINT`, followd by a byte indicating the type and the data to print, followed by a NUL byte (``0x00``). This mechanism is handled by :func:`~posprinter.suremark.SureMark.barcode`

Barcode types
*************
The printers can generate a lot of different barcodes. The following types are defined:

* :attr:`~posprinter.suremark.SureMark.BARCODE_UPC_A`
* :attr:`~posprinter.suremark.SureMark.BARCODE_UPC_E`
* :attr:`~posprinter.suremark.SureMark.BARCODE_EAN13`
* :attr:`~posprinter.suremark.SureMark.BARCODE_JAN13` (alias for EAN13)
* :attr:`~posprinter.suremark.SureMark.BARCODE_EAN8`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODE_39`
* :attr:`~posprinter.suremark.SureMark.BARCODE_ITF`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODABAR`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODE_128C`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODE_93`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODE_128A`
* :attr:`~posprinter.suremark.SureMark.BARCODE_CODE_128B` (alias for CODE_128A)

There is also a ``PDF417`` type that has not been implemented yet.

It is advised to use :func:`~posprinter.suremark.SureMark.barcode` to generate the commands to print data.

Controlling the size
*********************
The horizontal and vertical size can be controlled:

* Horizontal size using :attr:`~posprinter.suremark.SureMark.CMD_BARCODE_SET_HORIZONTAL_SIZE`

  * the size can be 2, 3 or 4
  * :func:`~posprinter.suremark.SureMark.barcode_set_horizontal_size` handles command generation and error checking

* Vertical size (height) using :attr:`~posprinter.suremark.SureMark.CMD_BARCODE_SET_HEIGHT`

  * the hight can be between 1 and 255 (inclusive)
  * :func:`~posprinter.suremark.SureMark.barcode_set_height` handles command generation and error checking

Human Readable Information (HRI)
********************************
Two commands control the positioning and font of the HRI information:

* Positioning using :attr:`~posprinter.suremark.SureMark.CMD_BARCODE_SET_HRI_POSITION`

  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_POSITION_NONE` disabled HRI printing
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_POSITION_ABOVE` places the text above the barcode
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_POSITION_BELOW` places the text below the barcode
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_POSITION_BOTH` combines above and below
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_POSITION_DEFAULT` alias for ``NONE``

* Selecting a font using :attr:`~posprinter.suremark.SureMark.CMD_BARCODE_SET_HRI_FONT`

  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_FONT_A` Font ``A``
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_FONT_B` Font ``B``
  * :attr:`~posprinter.suremark.SureMark.BARCODE_HRI_FONT_DEFAULT` alias for ``A``

Functions are defined for this which provide some error checking:

* :func:`~posprinter.suremark.SureMark.barcode_set_hri_position` takes a POSITION parameter
* :func:`~posprinter.suremark.SureMark.barcode_set_hri_font` takes a FONT parameter.

