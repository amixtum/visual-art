from cmath import exp
from compressor import compress, compress_recursive
from expander import expand, expand_recursive
from colors import apply_color_fn, apply_color_fn_recursive, apply_find_bluest, apply_color_fn_range, average_rgb, multiply_sin, apply_find_bluest_recursive
from neighborhood import moore, neumann

from PIL import Image

with Image.open('img/clouds.jpg') as img:
    img.show()
    updated = False
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
            apply_color_fn_recursive(img, average_rgb, neumann)
            updated = True
        elif inp[0] == 'c' and inp[1] == 'l':
            n = int(inp[2])
            for _ in range(n):
                apply_color_fn(img, multiply_sin, moore)
            updated = True
        if updated:
            img.show()
        inp = input('"q" to quit: ')
        updated = False