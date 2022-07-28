from cmath import exp
from compressor import compress, compress_recursive
from expander import expand, expand_recursive
from colors import apply_find_bluest, apply_color_fn, multiply_sin
from neighborhood import moore, neumann

from PIL import Image

with Image.open('img/flower.webp') as img:
    img.show()
    inp = input('Enter "x" to expand, "c" to compress, "q" to quit: ')
    while inp != 'q':
        if inp == 'c':
            img = compress_recursive(img)
            img.show()
        elif inp == 'x':
            img = expand_recursive(img)
            img.show()
        inp = input('Enter "x" to expand, "c" to compress, "q" to quit: ')