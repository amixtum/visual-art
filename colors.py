from math import ceil, sin, cos, pi

from PIL import Image, ImageDraw

from neighborhood import *


def average_rgb(colors):
    sum = [0, 0, 0]

    for c in colors:
        sum[0] += c[0]
        sum[1] += c[1]
        sum[2] += c[2]

    return (int(sum[0] / len(colors)), int(sum[1] / len(colors)), int(sum[2] / len(colors)))

def find_bluest(colors, threshold, replacement):
    bluest_color = colors[0]
    for c in colors:
        if c[2] > bluest_color[2]:
            bluest_color = c
    if bluest_color[2] >= threshold:
        return (bluest_color[0], bluest_color[1], 0)
    else:
        return (bluest_color[0], bluest_color[1], bluest_color[2] + replacement)

def multiply_sin(colors):
    color = average_rgb(colors)
    return (
        int(color[0] - color[0] * sin((2 * pi * color[0]) / 256)), 
        int(color[1] - color[1] * cos((2 * pi * color[1]) / 256)), 
        int(color[2] + color[2] * sin((2 * pi * color[2]) / 256)),
    )

def apply_color_fn(img, color_fn, neighbor_fn):
    draw = ImageDraw.Draw(img)
    for x in range(img.width):
        for y in range(img.height):
            neighbors = neighbor_fn(pos=[x, y], width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y)))
            color = color_fn(colors)
            draw.point((x, y), fill=color)

def apply_find_bluest(img, threshold, replacement):
    draw = ImageDraw.Draw(img)
    for x in range(img.width):
        for y in range(img.height):
            neighbors = neumann(pos=[x, y], width=img.width, height=img.height) 
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y)))
            color = find_bluest(colors, threshold, replacement)
            draw.point((x, y), fill=color)