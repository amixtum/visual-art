from math import floor


from PIL import Image, ImageDraw
from imageops import glue_horizontal, glue_vertical, split_quadrants


from neighborhood import *

from colors import *


def compress(img):
    new_width = int(img.width / 2)
    new_height = int(img.height / 2)
    new_img = Image.new('RGB', (new_width, new_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(new_img, mode='RGB')
    px = img.load()

    new_x = 0
    new_y = 0
    for x in range(0, img.width, 2):
        for y in range(0, img.height, 2):
            neighbors = neumann(pos=[x, y], width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y)))
            color = average_rgb(colors) 
            draw.point(xy=[(new_x, new_y)], fill=color)
            new_y += 1
        new_x += 1
        new_y = 0

    return new_img



def compress_recursive(img):
    if img.width == 2 and img.height == 2:
        colors = [
            img.getpixel((0, 0)),
            img.getpixel((1, 0)),
            img.getpixel((0, 1)),
            img.getpixel((1, 1)),
        ]
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(1, 1), color=color)
    elif img.width == 2 and img.height == 1:
        colors = [
            img.getpixel((0, 0)),
            img.getpixel((1, 0)),
        ]
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(1, 1), color=color)
    elif img.width == 1 and img.height == 2:
        colors = [
            img.getpixel((0, 0)),
            img.getpixel((0, 1)),
        ]
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(1, 1), color=color)
    elif img.width == 1 and img.height > 2:
        colors = []
        for y in range(img.height):
            colors.append(img.getpixel((0, y)))
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(1, ceil(img.height / 2)), color=color)
    elif img.width > 2 and img.height == 1:
        colors = []
        for x in range(img.width):
            colors.append(img.getpixel((x, 0)))
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(ceil(img.width / 2), 1), color=color)
    elif img.width == 2 and img.height == 3:
        colors = []
        for y in range(img.height):
            colors.append(img.getpixel((0, y)))
            colors.append(img.getpixel((1, y)))
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(1, 2), color=color)
    elif img.width == 3 and img.height == 2:
        colors = []
        for x in range(img.width):
            colors.append(img.getpixel((x, 0)))
            colors.append(img.getpixel((x, 1)))
        color = average_rgb(colors)
        return Image.new(mode='RGB', size=(2, 1), color=color)
    else:
        quadrants = split_quadrants(img)
        if (quadrants[0].width == 1 and quadrants[0].height == 1) and (quadrants[1].width == 1 and quadrants[1].height == 1):
            left = glue_vertical(quadrants[0], quadrants[2])
            right = glue_vertical(quadrants[1], quadrants[3])
            complete = glue_horizontal(left, right)
            return compress_recursive(complete)
        elif quadrants[0].width == 1 and quadrants[0].height == 1:
            left = glue_vertical(quadrants[0], quadrants[2])
            right = glue_vertical(quadrants[1], quadrants[3])
            complete = glue_horizontal(compress_recursive(left), compress_recursive(right))
            return complete
        elif quadrants[1].width == 1 and quadrants[1].height == 1:
            left = glue_vertical(quadrants[0], quadrants[2])
            right = glue_vertical(quadrants[1], quadrants[3])
            complete = glue_horizontal(compress_recursive(left), compress_recursive(right))
            return complete
        
        top = glue_horizontal(compress_recursive(quadrants[0]), compress_recursive(quadrants[1]))
        bottom = glue_horizontal(compress_recursive(quadrants[2]), compress_recursive(quadrants[3]))
        complete = glue_vertical(top, bottom)
        return complete