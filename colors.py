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
        int(color[0] + color[0] * sin(((2 * pi * color[0]) / 255) + cos((2 * pi * color[2]) / 255))), 
        int(color[1] + color[1] * sin(((2 * pi * color[1]) / 255) + cos((2 * pi * color[1]) / 255))),
        int(color[2] + color[2] * sin(((2 * pi * color[2]) / 255) + cos((2 * pi * color[0]) / 255))),
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

def apply_color_fn_range(img, color_fn, neighbor_fn, x_start, y_start, x_end, y_end):
    draw = ImageDraw.Draw(img)
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            neighbors = neighbor_fn(pos=[x, y], width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y)))
            color = color_fn(colors)
            draw.point((x, y), fill=color)

def apply_color_fn_recursive(img, color_fn, neighbor_fn):
    return apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, 0, 0, img.width, img.height)

def apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, x_start, y_start, x_end, y_end):
    draw = ImageDraw.Draw(img)
    if x_end - x_start == 1 and y_end - y_start == 1:
        neighbors = neumann(pos=(x_start, y_start), width=img.width, height=img.height)
        colors = [img.getpixel((n[0], n[1])) for n in neighbors]
        colors.append(img.getpixel((x_start, y_start)))
        color = color_fn(colors)
        draw.point((x_start, y_start), fill=color)

    elif x_end - x_start == 1:
        for y in range(y_start, y_end):
            neighbors = neumann(pos=(x_start, y), width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x_start, y)))
            color = color_fn(colors)
            draw.point((x_start, y), fill=color)

    elif y_end - y_start == 1:
        for x in range(x_start, x_end):
            neighbors = neumann(pos=(x, y_start), width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y_start)))
            color = color_fn(colors)
            draw.point((x, y_start), fill=color)

    else:
        x_mid = ceil((x_end - x_start)/ 2) + x_start
        y_mid = ceil((y_end - y_start) / 2) + y_start

        apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, x_start, y_start, x_mid, y_mid)
        apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, x_mid, y_start, x_end, y_mid)
        apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, x_start, y_mid, x_mid, y_end)
        apply_color_fn_recursive_helper(img, color_fn, neighbor_fn, x_mid, y_mid, x_end, y_end)

        apply_color_fn_range(img, color_fn, neighbor_fn, x_start, y_start, x_end, y_end)

def apply_find_bluest(img, threshold, replacement):
    draw = ImageDraw.Draw(img)
    for x in range(img.width):
        for y in range(img.height):
            neighbors = neumann(pos=[x, y], width=img.width, height=img.height) 
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y)))
            color = find_bluest(colors, threshold, replacement)
            draw.point((x, y), fill=color)

def apply_find_bluest_recursive(img, threshold, replacement):
    apply_find_bluest_recursive_helper(img, threshold, replacement, 0, 0, img.width, img.height)

def apply_find_bluest_recursive_helper(img: Image, threshold: int, replacement: int, x_start: int, y_start: int, x_end: int, y_end: int):
    draw = ImageDraw.Draw(img)
    if x_end - x_start == 1 and y_end - y_start == 1:
        neighbors = moore(pos=(x_start, y_start), width=img.width, height=img.height)
        colors = [img.getpixel((n[0], n[1])) for n in neighbors]
        colors.append(img.getpixel((x_start, y_start)))
        color = find_bluest(colors, threshold, replacement)
        draw.point((x_start, y_start), fill=color)

    elif x_end - x_start == 1:
        for y in range(y_start, y_end):
            neighbors = moore(pos=(x_start, y), width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x_start, y)))
            color = find_bluest(colors, threshold, replacement)
            draw.point((x_start, y), fill=color)

    elif y_end - y_start == 1:
        for x in range(x_start, x_end):
            neighbors = moore(pos=(x, y_start), width=img.width, height=img.height)
            colors = [img.getpixel((n[0], n[1])) for n in neighbors]
            colors.append(img.getpixel((x, y_start)))
            color = find_bluest(colors, threshold, replacement)
            draw.point((x, y_start), fill=color)

    else:
        x_mid = ceil((x_end - x_start)/ 2) + x_start
        y_mid = ceil((y_end - y_start) / 2) + y_start
        apply_find_bluest_recursive_helper(img, threshold, replacement, x_start, y_start, x_mid, y_mid)
        apply_find_bluest_recursive_helper(img, threshold, replacement, x_mid, y_start, x_end, y_mid)
        apply_find_bluest_recursive_helper(img, threshold, replacement, x_start, y_mid, x_mid, y_end)
        apply_find_bluest_recursive_helper(img, threshold, replacement, x_mid, y_mid, x_end, y_end)
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                neighbors = moore(pos=(x, y), width=img.width, height=img.height)
                colors = [img.getpixel((n[0], n[1])) for n in neighbors]
                colors.append(img.getpixel((x, y)))
                color = find_bluest(colors, threshold, replacement)
                draw.point((x, y), fill=color)