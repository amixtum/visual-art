from math import ceil, floor

from random import randint, choice
from turtle import color


from PIL import Image, ImageDraw


def glue_horizontal(l_img, r_img):
    new_width = l_img.width + r_img.width
    new_height = max(l_img.height, r_img.height)
    glued = Image.new(mode='RGB', size=(new_width, new_height))
    glued.paste(l_img, box=(0, 0, l_img.width, new_height))
    glued.paste(r_img, box=(l_img.width, 0, new_width, new_height))
    return glued

def glue_vertical(l_img, r_img):
    new_width = max(l_img.width, r_img.width)
    new_height = l_img.height + r_img.height
    glued = Image.new(mode='RGB', size=(new_width, new_height))
    glued.paste(l_img, box=(0, 0, new_width, l_img.height))
    glued.paste(r_img, box=(0, l_img.height, new_width, new_height))
    return glued

def split_quadrants(img: Image):
    mid_x = floor(img.width / 2)
    mid_y = floor(img.height / 2)

    top_left = img.crop(box=(0, 0, mid_x, mid_y))
    top_right = img.crop(box=(mid_x, 0, img.width, mid_y))
    bottom_left = img.crop(box=(0, mid_y, mid_x, img.height))
    bottom_right = img.crop(box=(mid_x, mid_y, img.width, img.height))

    return (top_left, top_right, bottom_left, bottom_right)

def swap_pixels(img, p1, p2):
    draw = ImageDraw.Draw(img)
    c1 = img.getpixel(p1)
    draw.point(p1, fill=img.getpixel(p2))
    draw.point(p2, fill=c1)

def partition_strip_horizontal(img, color_compare, x_l, x_r, y):
    p_index = randint(x_l, x_r)
    pivot = img.getpixel((p_index, y))

    swap_pixels(img, (x_l, y), (p_index, y))

    left = x_l + 1
    right = x_r

    while left < right:
        while left < x_r and color_compare(img.getpixel((left, y)), pivot) < 0:
            left += 1

        while right > x_l and color_compare(img.getpixel((right, y)), pivot) >= 0:
            right -= 1

        swap_pixels(img, (left, y), (right, y))

    swap_pixels(img, (left, y), (right, y))

    swap_pixels(img, (x_l, y), (right, y))

    return (right, y)

def partition_strip_diagonal(img, color_compare, x_l, y_l, x_r, y_r):
    p_index = randint(x_l, x_r)

    m = (y_r - y_l) / (x_r - x_l)
    b = floor(y_r - m * x_r)

    pivot = img.getpixel((p_index, m * p_index + b))

    swap_pixels(img, (x_l, floor(m * x_l + b)), (p_index, floor(m * p_index + b)))

    top_left = (x_l + 1, floor(m * (x_l + 1) + b))
    bottom_right = (x_r, floor(m * x_r + b))

    while top_left[0] < bottom_right[0]:
        while top_left[0] < x_r and m * top_left[0] + b < y_r and color_compare(img.getpixel(top_left), pivot) < 0:
            new_x = top_left[0] + 1
            new_y = floor(m * new_x + b)
            top_left = (new_x, new_y)

        while bottom_right[0] > x_l and m * bottom_right[0] + b > y_l and color_compare(img.getpixel(bottom_right), pivot) >= 0:
            new_x = bottom_right[0] - 1
            new_y = floor(m * new_x + b)
            bottom_right = (new_x, new_y)

        swap_pixels(img, top_left, bottom_right)

    swap_pixels(img, top_left, bottom_right)

    swap_pixels(img, (x_l, floor(m * x_l + b)), bottom_right)

    return bottom_right

def partition_diagonals(img, color_compare):
    m = 1
    b = img.height - 2

    while b >= 0:
        x_l = 0
        y_l = int(m * x_l + b)

        x_r = floor((img.height - 1 - b) / m)
        y_r = img.height - 1

        if y_l >= 0 and y_l < img.height and x_r >= 0 and x_r < img.width and y_r >= 0 and y_r < img.height and x_l < x_r and y_l < y_r:
            partition_strip_diagonal(img, color_compare, x_l, y_l, x_r, y_r)

        b -= 1
    
    while b > -img.height + 2:
        y_l = 0
        x_l = floor((y_l - b) / m)

        x_r = img.width - 1
        y_r = int(m * x_r) + b

        if x_l >= 0 and x_l < img.width and y_l >= 0 and y_l < img.height and x_r >= 0 and x_r < img.width and y_r >= 0 and y_r < img.height and x_l < x_r and y_l < y_r:
            partition_strip_diagonal(img, color_compare, x_l, y_l, x_r, y_r)

        b -= 1
    

def partition_horizontal(img, color_compare, x_l, y_l, x_r, y_r):
    p_index = floor((x_r - x_l) / 2) + x_l + randint(-(floor((x_r - x_l) / 2)), floor((x_r - x_l) / 2))
    ps = []

    for y in range(y_l, y_r):
        pivot = img.getpixel((p_index, y))

        swap_pixels(img, (x_l, y), (p_index, y))

        left = x_l + 1
        right = x_r

        while left < right:
            while left < img.width - 1 and color_compare(img.getpixel((left, y)), pivot) < 0:
                left += 1

            while right > 0 and color_compare(img.getpixel((right, y)), pivot) >= 0:
                right -= 1

            swap_pixels(img, (left, y), (right, y))

        swap_pixels(img, (left, y), (right, y))

        swap_pixels(img, (x_l, y), (right, y))

        ps.append((right, y))

    return ps

def partition_vertical(img, color_compare, x_l, y_l, x_r, y_r):
    p_index = floor((y_r - y_l) / 2) + y_l + randint(-(floor((y_r - y_l) / 2)), (floor((y_r - y_l) / 2)))

    ps = []

    for x in range(x_l, x_r):
        pivot = img.getpixel((x, p_index))

        swap_pixels(img, (x, y_l), (x, p_index))

        left = y_l + 1
        right = y_r

        while left < right:
            while left < img.height- 1 and color_compare(img.getpixel((x, left)), pivot) < 0:
                left += 1

            while right > 0 and color_compare(img.getpixel((x, right)), pivot) >= 0:
                right -= 1

            swap_pixels(img, (x, left), (x, right))

        swap_pixels(img, (x, left), (x, right))

        swap_pixels(img, (x, y_l), (x, right))

        ps.append((x, right))

    return ps