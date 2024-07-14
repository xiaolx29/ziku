from PIL import Image, ImageDraw, ImageQt
from PySide6 import QtGui, QtCore

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

def read_char_pixels_from_file(filename: str, charid: int) -> bytes:
    # read one character from binary font file
    with open(filename, 'rb') as file:
        file.seek(32 * charid)
        character_data = file.read(32)
    return character_data

def write_char_pixels_to_file(filename: str, charid: int, char_pixels: bytes) -> None:
    with open(filename, 'rb+') as file:
        file.seek(32 * charid)
        file.write(char_pixels)

def draw_char_pixels_on_pixmap(filename: str, charid: int) -> QtGui.QPixmap:
    # draw one character
    image = Image.new(mode = 'L', size = (16, 16), color = 255)
    # position_x, position_y = position
    draw = ImageDraw.Draw(image)
    character_data = read_char_pixels_from_file(filename = filename, charid = charid)
    for y in range(16):
        line_data = int.from_bytes(bytes = character_data[y * 2: y * 2 + 2])
        for x in range(16):
            if (line_data >> (15 - x)) & 1:
                draw.point(xy = (x, y), fill = 'black')
    return QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))