from math import ceil


from PIL import Image, ImageDraw


def glue_horizontal(l_img, r_img):
    new_width = l_img.width + r_img.width
    new_height = max(l_img.height, r_img.height)
    glued = Image.new(mode='RGB', size=(new_width, new_height))
    draw = ImageDraw.Draw(glued)

    new_x = 0
    new_y = 0
    for x in range(l_img.width):
        for y in range(l_img.height):
            if new_y < new_height:
                draw.point((new_x, new_y), fill=l_img.getpixel((x, y)))
                new_y += 1
        new_x += 1
        new_y = 0
    
    for x in range(r_img.width):
        for y in range(r_img.height):
            if new_y < new_height:
                draw.point((new_x, new_y), fill=r_img.getpixel((x, y)))
                new_y += 1
        new_x += 1
        new_y = 0

    return glued

def glue_vertical(l_img, r_img):
    new_width = max(l_img.width, r_img.width) 
    new_height = l_img.height + r_img.height
    glued = Image.new(mode='RGB', size=(new_width, new_height))
    draw = ImageDraw.Draw(glued)

    new_x = 0
    new_y = 0
    for y in range(l_img.height):
        for x in range(l_img.width):
            if new_x < new_width:
                draw.point((new_x, new_y), fill=l_img.getpixel((x, y)))
                new_x += 1
        new_y += 1
        new_x = 0
    
    for y in range(r_img.height):
        for x in range(r_img.width):
            if new_x < new_width:
                draw.point((new_x, new_y), fill=r_img.getpixel((x, y)))
                new_x += 1
        new_y += 1
        new_x = 0

    return glued


def merge_interleaved_vertical(l_img, r_img):
    new_width = min(l_img.width, r_img.width) 
    new_height = l_img.height + r_img.height
    merged = Image.new(mode='RGB', size=(new_width, new_height))
    draw = ImageDraw.Draw(merged)

    l_x = 0
    l_y = 0
    r_x = 0
    r_y = 0
    use_left = True
    l_done = False
    r_done = False
    color = (0, 0, 0)
    for x in range(new_width):
        for y in range(new_height):
            if use_left and not l_done and l_y < l_img.height:
                color = l_img.getpixel((l_x, l_y))
                l_y += 1
                if r_y <= r_img.height - 1:
                    use_left = False
            elif (not use_left) and (not r_done) and r_y < r_img.height:
                color = r_img.getpixel((r_x, r_y))
                r_y += 1
                if l_y <= l_img.height - 1:
                    use_left = True
            else:
                color = (0, 0, 0)
            draw.point((x, y), fill=color)
        if l_x < l_img.width - 1:
            l_x += 1
        else:
            if not l_done:
                l_done = True

        if r_x < r_img.width - 1:
            r_x += 1
        else:
            if not r_done:
                r_done = True

        l_y = 0
        r_y = 0

    return merged

def merge_interleaved_horizontal(l_img, r_img):
    new_width = l_img.width + r_img.width 
    new_height = min(l_img.height, r_img.height)
    merged = Image.new(mode='RGB', size=(new_width, new_height))
    draw = ImageDraw.Draw(merged)

    l_x = 0
    l_y = 0
    r_x = 0
    r_y = 0
    use_left = True
    l_done = False
    r_done = False
    color = (0, 0, 0)
    for y in range(new_height):
        for x in range(new_width):
            if use_left and not l_done and l_x < l_img.width:
                color = l_img.getpixel((l_x, l_y))
                l_x += 1
                if r_x <= r_img.width - 1:
                    use_left = False
            elif (not use_left) and (not r_done) and r_x < r_img.width:
                color = r_img.getpixel((r_x, r_y))
                r_x += 1
                if l_x <= l_img.width - 1:
                    use_left = True
            else:
                color = (0, 0, 0)
            draw.point((x, y), fill=color)
        if l_y < l_img.height - 1:
            l_y += 1
        else:
            if not l_done:
                l_done = True

        if r_y < r_img.height - 1:
            r_y += 1
        else:
            if not r_done:
                r_done = True

        l_x = 0
        r_x = 0

    return merged
        

def split_quadrants(img):
    mid_x = ceil(img.width / 2)
    mid_y = ceil(img.height / 2)

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