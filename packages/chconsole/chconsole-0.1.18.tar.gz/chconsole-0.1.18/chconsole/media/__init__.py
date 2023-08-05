from .text import get_block_plain_text, set_top_cursor, is_comment, to_comment, de_comment, is_letter_or_number
from .text import default_editor
from .image import register_qimage, insert_qimage_format, copy_image, save_image, get_image
from .image import svg_to_qimage, jpg_to_qimage, png_to_qimage, latex_to_qimage
from .text_register import TextRegister

__author__ = 'Manfred Minimair <manfred@minimair.org>'
