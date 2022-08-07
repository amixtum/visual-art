# my_test.py
from PIL import Image


from compressor import compress, compress_recursive
from expander import my_expand, expand, expand_recursive
from colors import apply_color_fn, apply_color_fn_recursive, apply_find_bluest, apply_color_fn_range, average_rgb, multiply_sin, apply_find_bluest_recursive, compare_intensity, compare_sin_intensity, more_blue, compare_diff
from neighborhood import moore, neumann
from drawing import draw_line
from imageops import partition_diagonals, partition_vertical, partition_horizontal

with Image.open('img/galaxy1.jpg') as img:
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
            apply_color_fn_recursive(img, multiply_sin, neumann)
            updated = True

        elif inp[0] == 'c' and inp[1] == 'l':
            n = int(inp[2])
            for _ in range(n):
                apply_color_fn(img, multiply_sin, neumann)
            updated = True

        elif inp == 'ph':
            partition_horizontal(img, lambda c1, c2: compare_diff(c1, c2), 0, 0, img.width - 1, img.height - 1)
            updated = True

        elif inp == 'pv':
            partition_vertical(img, lambda c1, c2: compare_diff(c1, c2), 0, 0, img.width - 1, img.height - 1)
            updated = True

        elif inp == 'pd':
            partition_diagonals(img, lambda c1, c2: compare_intensity(c1, c2))
            updated = True

        if updated:
            img.show()

        inp = input('"q" to quit: ')
        updated = False

img.close()