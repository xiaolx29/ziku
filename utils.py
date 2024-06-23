import binascii
import codecs
from PIL import Image, ImageDraw, ImageQt
from PySide6 import QtGui

def quweima_to_charid(qu: int, wei: int) -> int:
    return (qu - 1) * 94 + wei - 1

def charid_to_quweima(charid: int) -> tuple[int, int]:
    return charid // 94 + 1, charid % 94 + 1

def quweima_to_jineima(qu: int, wei: int) -> bytes:
    return bytes[0xa0 + qu, 0xa0 + wei]

def jineima_to_quweima(jineima: bytes) -> tuple[int, int]:
    high_byte, low_byte = jineima
    qu, wei = high_byte - 0xa0, low_byte - 0xa0
    return qu, wei

def jineima_to_char(jineima: bytes, errors: str) -> str:
    return jineima.decode(encoding = 'gb2312', errors = errors)

def char_to_jineima(char: str, errors: str) -> bytes:
    return char.encode(encoding = 'gb2312', errors = errors)

def get_character(filename: str, character_index: int) -> bytes:
    # read one character from binary font file
    with open(filename, 'rb') as file:
        file.seek(32 * character_index)
        character_data = file.read(32)
    return character_data

def draw_character_on_pixmap(filename: str, character_index: int) -> QtGui.QPixmap:
    # draw one character
    image = Image.new(mode = '1', size = (16, 16), color = 255)
    # position_x, position_y = position
    draw = ImageDraw.Draw(image)
    character_data = get_character(filename = filename, character_index = character_index)
    for y in range(16):
        line_data = int.from_bytes(bytes = character_data[y * 2: y * 2 + 2])
        for x in range(16):
            if (line_data >> (15 - x)) & 1:
                draw.point(xy = (x, y), fill = 'black')
    return QtGui.QPixmap.fromImage(ImageQt.ImageQt(image))

def get_charinfo_by_charid(charid: int):
    qu, wei = charid // 94 + 1, charid % 94 + 1
    jineima = bytes([0xA0 + qu, 0xA0 + wei])
    char = jineima.decode(encoding = 'gb2312', errors = 'replace')
    return char, f'{int.from_bytes(jineima):#X}', f'{qu:02d} {wei:02d}'

def get_charid_by_char(char: str):
    try:
        jineima = char_to_jineima(char)
        # detect half-width characters, they are not in gb2312
        if len(jineima) != 2:
            return None
        jineima_high, jineima_low = jineima
        return (jineima_high - 0xA1) * 94 + jineima_low - 0xA1
    # detect other characters that are also not in gb2312
    except UnicodeEncodeError:
        return None