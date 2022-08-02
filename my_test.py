# my_test.py
from PIL import Image


from compressor import compress, compress_recursive
from expander import my_expand, expand, expand_recursive
from colors import ColorWave, apply_color_fn, apply_color_fn_recursive, apply_find_bluest, apply_color_fn_range, average_rgb, multiply_sin, apply_find_bluest_recursive
from neighborhood import moore, neumann
from drawing import draw_line, draw_lines_outward


with Image.open('img/galaxy1.jpg') as img:
    img.show()
    updated = False

    color_wav = ColorWave(8, 0.5, 2)
    inp = input('"q" to quit: ')
    while inp != 'q':
        if inp == 'c':
            img = compress(img)
            updated = True
        elif inp == 'cr':
            img = compress_recursive(img)
            updated = True
        elif inp == 'x':
            img = expand(img)
            updated = True
        elif inp == 'xr':
            img = expand_recursive(img)
            updated = True
        elif inp == 'br':
            apply_find_bluest_recursive(img, 128, 32)
            updated = True
        elif inp[0] == 'b':
            n = int(inp[1])
            for _ in range(n):
                apply_find_bluest(img, 128, 32)
            updated = True
        elif inp == 'clr':
            apply_color_fn_recursive(img, multiply_sin, neumann)
            updated = True
        elif inp[0] == 'c' and inp[1] == 'l':
            n = int(inp[2])
            for _ in range(n):
                apply_color_fn(img, multiply_sin, neumann)
            updated = True
        if updated:
            img.show()
        inp = input('"q" to quit: ')
        updated = False