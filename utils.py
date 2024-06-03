from typing import Tuple
from PIL import Image, ImageDraw

def get_character(filename: str, character_index: int) -> bytes:
    # read one character from binary font file
    with open(filename, 'rb') as file:
        file.seek(32 * character_index)
        character_data = file.read(32)
    return character_data

def draw_character(filename: str, img: Image, position: Tuple[int, int], character_index: int) -> None:
    # draw one character
    position_x, position_y = position
    draw = ImageDraw.Draw(img)
    character_data = get_character(filename = filename, character_index = character_index)
    for y in range(16):
        line_data = int.from_bytes(bytes = character_data[y * 2: y * 2 + 2], byteorder = 'big')
        for x in range(16):
            if (line_data >> (15 - x)) & 1:
                draw.point(xy = (position_x * 16 + x, position_y * 16 + y), fill = 'black')

def draw_page(filename: str, page_index: int) -> Image:
    # draw 1000(50x20) characters on one page
    page_image = Image.new(mode = '1', size = (16 * 50, 16 * 20), color = 255)
    for i in range(1000):  # draw one character on each position
        position_x, position_y = i % 50, i // 50
        draw_character(filename = filename, img = page_image, position = (position_x, position_y), character_index = page_index * 1000 + i)
    return page_image

if __name__ == '__main__':
    image = draw_page(filename = '/link/to/test/file', page_index = 0)
    image.show()