from math import floor
from random import choice, random


from PIL import Image, ImageDraw


from colors import find_bluest, multiply_sin
from neighborhood import neumann, moore


def draw_line(img, x_start: int, y_start: int, filled: set, color_fn):
    draw = ImageDraw.Draw(img)

    neighbors = neumann(pos=(x_start, y_start), width=img.width, height=img.height)
    (new_x, new_y) = choice(neighbors)
    can_draw = (new_x, new_y) in filled
    if not can_draw:
        for n in neighbors:
            if (n[0], n[1]) not in filled:
                while (new_x, new_y) in filled:
                    (new_x, new_y) = choice(neighbors)
                can_draw = True
                break
        
    if can_draw: 
        draw.line([(x_start, y_start), (new_x, new_y)], color_fn([img.getpixel((x_start, y_start)), img.getpixel((new_x, new_y))]))
        filled.add((x_start, y_start))
        filled.add((new_x, new_y))
        return (new_x, new_y)
    else:
        return (x_start, y_start)
