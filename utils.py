from typing import Literal
from PIL import Image, ImageDraw, ImageQt
from PySide6 import QtGui


BYTE_SIZE = 8

def quweima_to_charid(qu: int, wei: int) -> int:
    return (qu - 1) * 94 + wei - 1

def charid_to_quweima(charid: int) -> tuple[int, int]:
    return charid // 94 + 1, charid % 94 + 1

def quweima_to_jineima(qu: int, wei: int) -> bytes:
    return bytes([0xa0 + qu, 0xa0 + wei])

def jineima_to_quweima(jineima: bytes) -> tuple[int, int]:
    high_byte, low_byte = jineima
    qu, wei = high_byte - 0xa0, low_byte - 0xa0
    return qu, wei

def jineima_to_char(jineima: bytes, errors: str) -> str:
    return jineima.decode(encoding = 'gb2312', errors = errors)

def char_to_jineima(char: str, errors: str) -> bytes:
    return char.encode(encoding = 'gb2312', errors = errors)

def read_char_pixels_from_file(filename: str, charid: int, char_byte_num: int) -> bytes:
    # read one character from binary ziku file
    with open(filename, 'rb') as file:
        file.seek(charid * char_byte_num)
        char_bytes = file.read(char_byte_num)
    return char_bytes

def write_char_pixels_to_file(filename: str, charid: int, char_pixels: bytes) -> None:
    # write one character into binary ziku file
    with open(filename, 'rb+') as file:
        char_byte_num: int = len(char_pixels)
        file.seek(charid * char_byte_num)
        file.write(char_pixels)

def draw_char_pixels_on_pixmap(filename: str, charid: int, char_size: int) -> QtGui.QPixmap:
    # draw one character
    # read data of the char from binary ziku file
    char_byte_num: int = 2 * char_size if char_size <= 16 else char_size ** 2 / 8
    char_bytes: bytes = read_char_pixels_from_file(filename = filename, charid = charid, char_byte_num = char_byte_num)
    # create a pure black image with size=char_size * char_size
    image: Image = Image.new(mode = '1', size = (char_size, char_size), color = 255)
    draw: ImageDraw = ImageDraw.Draw(image)
    if char_size <= 16:  # draw char on pixmap if char size < 16
        for row_index in range(char_size):
            row_data: int = int.from_bytes(bytes = char_bytes[row_index * 2: row_index * 2 + 2])
            for column_index in range(char_size):
                if row_data >> 2 * BYTE_SIZE - 1 - column_index & 1:
                    draw.point(xy = (column_index, row_index), fill = 'black')
    else:  # draw char on pixmap if char size > 16
        for byte_index, byte in enumerate(char_bytes):
            for bit_index in range(BYTE_SIZE):
                if byte >> BYTE_SIZE - 1 - bit_index & 1:
                    pixel_index: int = byte_index * BYTE_SIZE + bit_index
                    row_index, column_index = divmod(pixel_index, char_size)
                    draw.point(xy = (column_index, row_index), fill = 'black')
    # return QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))
    return image

def char_bytes_to_list(char_bytes: bytes, char_size: int) -> list[list[bool]]:
    char_list: list[list[bool]] = []
    if char_size <= 16:
        for row_index in range(char_size):
            row_list: list[bool] = []
            # extract data of 1 row(2 bytes) from char_bytes
            row_data: int = int.from_bytes(bytes = char_bytes[row_index * 2: row_index * 2 + 2])
            # append the first char_size bits of the 2 bytes into row_list
            for column_index in range(char_size):
                pixel_data: Literal[0, 1] = row_data >> 2 * BYTE_SIZE - 1 - column_index & 1
                row_list.append(bool(pixel_data))
            char_list.append(row_list)
    else:
        for row_index in range(char_size):
            row_list: list[bool] = []
            for column_index in range(char_size):
                pixel_index: int = row_index * char_size + column_index
                byte_index, bit_index = divmod(pixel_index, BYTE_SIZE)
                pixel_data: Literal[0, 1] = char_bytes[byte_index] >> BYTE_SIZE - 1 - bit_index & 1
                row_list.append(bool(pixel_data))
            char_list.append(row_list)
    return char_list

def char_list_to_pixmap(char_list: list[list[bool]]) -> QtGui.QPixmap:
    char_size: int = len(char_list)
    # init Image and ImageDraw
    image: Image = Image.new(mode = '1', size = (char_size, char_size), color = 'white')
    draw: ImageDraw = ImageDraw.Draw(image)
    # draw char onto Image
    for row_index in range(char_size):
        for column_index in range(char_size):
            if char_list[row_index][column_index]:
                draw.point(xy = (column_index, row_index), fill = 'black')
    # convert Image to QPixmap
    qpixmap: QtGui.QPixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))
    return qpixmap
