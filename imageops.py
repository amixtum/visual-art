from math import ceil, floor


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