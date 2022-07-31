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


def merge_interleaved_vertical(l_img, r_img):
    pass

def merge_interleaved_horizontal(l_img, r_img):
    pass        

def split_quadrants(img):
    mid_x = floor(img.width / 2)
    mid_y = floor(img.height / 2)

    top_left = Image.new(mode='RGB', size=(mid_x, mid_y))
    draw_tl = ImageDraw.Draw(top_left)

    top_right = Image.new(mode='RGB', size=(img.width - mid_x, mid_y))
    draw_tr = ImageDraw.Draw(top_right)

    bottom_left = Image.new(mode='RGB', size=(mid_x, img.height - mid_y))
    draw_bl = ImageDraw.Draw(bottom_left)

    bottom_right = Image.new(mode='RGB', size=(img.width - mid_x, img.height - mid_y))
    draw_br = ImageDraw.Draw(bottom_right)

    for x in range(0, mid_x):
        for y in range(0, mid_y):
            draw_tl.point((x, y), fill=img.getpixel((x, y)))
    
    for x in range(mid_x, img.width):
        for y in range(0, mid_y):
            draw_tr.point((x - mid_x, y), fill=img.getpixel((x, y)))
    
    for x in range(0, mid_x):
        for y in range(mid_y, img.height):
            draw_bl.point((x, y - mid_y), fill=img.getpixel((x, y)))
    
    for x in range(mid_x, img.width):
        for y in range(mid_y, img.height):
            draw_br.point((x - mid_x, y - mid_y), fill=img.getpixel((x, y)))

    return (top_left, top_right, bottom_left, bottom_right)