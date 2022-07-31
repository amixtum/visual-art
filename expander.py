from math import ceil


from PIL import Image, ImageDraw, ImageChops, ImageOps

from colors import apply_color_fn_range, apply_find_bluest, multiply_sin, apply_color_fn
from neighborhood import neumann, moore
from imageops import split_quadrants, glue_horizontal, glue_vertical


# expands image by factor of 2
def expand(img):
    return ImageOps.scale(img, 2.0)

def my_expand(img):
    newWidth = int(img.width * 2)
    newHeight = int(img.height * 2)
    new_img = Image.new(mode='RGB', size=(newWidth, newHeight))
    draw = ImageDraw.Draw(new_img)

    original_x = 0
    original_y = 0
    for x in range(1, newWidth, 2):
        for y in range(1, newHeight, 2):
            draw.line([(x, y), (x, y - 1)], fill=img.getpixel((original_x, original_y)))
            draw.line([(x - 1, y), (x - 1, y - 1)], fill=img.getpixel((original_x, original_y)))
            original_y += 1
        original_y = 0
        original_x += 1

    return new_img




def expand_recursive(img):
    if img.width == 1 and img.height == 1:
        new_width = 2 
        new_height = 2 
        new_img = Image.new(mode='RGB', size=(new_width, new_height))
        draw = ImageDraw.Draw(new_img)
        draw.line([(0, 1), (0, 0)], fill=img.getpixel((0, 0)))
        draw.line([(1, 1), (1, 0)], fill=img.getpixel((0, 0)))
        return new_img
    elif img.width == 1:
        new_width = 2
        new_height = int(img.height * 2)
        new_img = Image.new(mode='RGB', size=(new_width, new_height))
        draw = ImageDraw.Draw(new_img)
        y_pixel = 0
        for y in range(1, new_height):
            if y % 2 == 0:
                y_pixel += 1
            draw.line([(0, y), (0, y - 1)], fill=img.getpixel((0, y_pixel)))
            draw.line([(1, y), (1, y - 1)], fill=img.getpixel((0, y_pixel)))
        return new_img
    elif img.height == 1:
        new_height = 2
        new_width = int(img.width * 2)
        new_img = Image.new(mode='RGB', size=(new_width, new_height))
        draw = ImageDraw.Draw(new_img)
        x_pixel = 0
        for x in range(1, new_width):
            if x % 2 == 0:
                x_pixel += 1
            draw.line([(x, 0), (x - 1, 0)], fill=img.getpixel((x_pixel, 0)))
            draw.line([(x, 1), (x - 1, 1)], fill=img.getpixel((x_pixel, 0)))
        return new_img
    else:
        quadrants = split_quadrants(img) 
        new_quads = []

        for i in range(len(quadrants)):
            if i % 2 == 0:
                new_quads.append(ImageOps.flip(quadrants[i]))
            else:
                new_quads.append(ImageOps.mirror(quadrants[i]))
            new_quads[i] = ImageOps.fit(image=new_quads[i], size=(quadrants[i].width, quadrants[i].height))

        top = glue_horizontal(expand_recursive(new_quads[0]), expand_recursive(new_quads[1])) 
        bottom = glue_horizontal(expand_recursive(new_quads[2]), expand_recursive(new_quads[3]))
        complete = glue_vertical(top, bottom)
        
        for q in quadrants:
            q.close()
        top.close()
        bottom.close()

        return complete


