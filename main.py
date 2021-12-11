import base64
import datetime
import os
import random
from PIL import Image, ImageDraw
import numpy
import uuid


palettes = [
    ['#cb997e', '#ddbea9', '#ffe8d6', '#b7b7a4', '#a5a58d', '#6b705c'],
    ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51'],
    ['#e63946', '#f1faee', '#a8dadc', '#457b9d', '#1d3557'],
    ['#606c38', '#283618', '#fefae0', '#dda15e', '#bc6c25'],
    ['#22223b', '#4a4e69', '#9a8c98', '#c9ada7', '#f2e9e4'],
    ['#ccd5ae', '#e9edc9', '#fefae0', '#faedcd', '#d4a373'],
    ['#000000', '#14213d', '#fca311', '#e5e5e5', '#ffffff'],
    ['#386641', '#6a994e', '#a7c957', '#f2e8cf', '#bc4749'],
    ['#ffcdb2', '#ffb4a2', '#e5989b', '#b5838d', '#6d6875'],
    ['#cad2c5', '#84a98c', '#52796f', '#354f52', '#2f3e46'],
    ['#3d5a80', '#98c1d9', '#e0fbfc', '#ee6c4d', '#293241'],
    ['#cdb4db', '#ffc8dd', '#ffafcc', '#bde0fe', '#a2d2ff'],
    ['#f6bd60', '#f7ede2', '#f5cac3', '#84a59d', '#f28482'],
    ['#ffb5a7', '#fcd5ce', '#f8edeb', '#f9dcc4', '#fec89a'],
    ['#003049', '#d62828', '#f77f00', '#fcbf49', '#eae2b7'],
    ['#555b6e', '#89b0ae', '#bee3db', '#faf9f9', '#ffd6ba'],
    ['#390099', '#9e0059', '#ff0054', '#ff5400', '#ffbd00'],
    ['#355070', '#6d597a', '#b56576', '#e56b6f', '#eaac8b'],
    ['#f0ead2', '#dde5b6', '#adc178', '#a98467', '#6c584c'],
    ['#432371', '#714674', '#9f6976', '#cc8b79', '#faae7b'],
    ['#70d6ff', '#ff70a6', '#ff9770', '#ffd670', '#e9ff70'],
    ['#f8f9fb', '#e1ecf7', '#aecbeb', '#83b0e1', '#71a5de'],
    ['#533747', '#5f506b', '#6a6b83', '#76949f', '#86bbbd'],
    ['#e0e2db', '#d2d4c8', '#b8bdb5', '#889696', '#5f7470'],
    ['#6b9080', '#a4c3b2', '#cce3de', '#eaf4f4', '#f6fff8'],
    ['#c3a995', '#ab947e', '#6f5e53', '#8a7968', '#593d3b']
]

palette_names = [
    'sandstone query',
    'bit of irish',
    'esteemed pilot',
    'down to earth',
    'dawn to dusk',
    'desert arrangement',
    'double contrast',
    'red light green light',
    'deep sunset',
    'mystic woods',
    'aviator proper',
    'powder puff',
    'natural warmth',
    'beaches and cream',
    'bold royals',
    'light foliage',
    'to go boldy',
    'throwing shades',
    'actual tree',
    'shallow sunrise',
    'neon hilighters',
    'frozone two',
    'tinged shades',
    'neo mono',
    'og mono',
    'brown notes'
]


# random.randrange(palettes)
#  could duplicate common palettes...
palette_probability = [
    'sandstone query',
    'bit of irish',
    'esteemed pilot',
    'down to earth',
    'dawn to dusk',
    'desert arrangement',
    'double contrast',
    'red light green light',
    'deep sunset',
    'mystic woods',
    'aviator proper',
    'powder puff',
    'natural warmth',
    'beaches and cream',
    'bold royals',
    'light foliage',
    'to go boldy',
    'throwing shades',
    'actual tree',
    'shallow sunrise',
    'neon hilighters',
    'frozone two',
    'tinged shades',
    0.02,
    0.01,
    0.04
]


def print_palette(palette):
    palette_size = len(palette)
    size = palette_size * 16
    im = Image.new(mode='RGB', size=(size, 16), color='black')

    for color_index in range(palette_size):
        im.paste(Image.new(mode='RGB', size=(16, 16), color=palette[color_index]), (16 * color_index, 0))

    im.show()


def create_image(mode, size, color):
    im = Image.new(mode=mode, size=size, color=color)

    # Create rectangle
    im.paste((256,256,0),(0,0,100,100))

    # Color a single pixel
    pixels = im.load()
    pixels[32, 16] = (0,0,0)

    # Color gradient
    for i in range(0, 256):
        im.paste((256-i, 128-i, 64-i), (i,i,128,128))

    r,g,b=im.split()
    im = Image.merge("RGB", (g,b,r))

    for n in range(2):
        a = numpy.random.rand(128,128,3) * 255
        im.paste(Image.fromarray(a.astype('uint8')).convert('RGB'))

    draw = ImageDraw.Draw(im)
    draw.line((100, 200, 150, 300), fill='green', width=5, joint="curve")
    draw.line((150, 300, 200, 100), fill='red', width=6, joint="curve")

    im.show()


def create_pixels(size=(16, 16)):
    x_size = size[0]
    y_size = size[1]
    im = Image.new(mode="RGB", size=size, color='black')
    # Color gradient
    for i in range(0, 256):
        im.paste((256-i, 128-i, 64-i), (i,i,16,16))
    im.show()


def draw_dots():
    size = (512,512)
    im = Image.new(mode='RGB', size=size, color='black')

    rows = 3
    cols = 4
    radius = 5

    draw = ImageDraw.Draw(im)

    for row in range(1, rows+1):
        for col in range(1, cols+1):
            x = size[0]/(rows+1) * row
            y = size[1]/(cols+1) * col
            draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill='white')

    im.show()


def draw_lines():
    palette_index = random.randrange(len(palettes))
    palette = palettes[palette_index]
    size = (5120, 5120)
    rows = 3
    cols = 4
    radius = int((size[0]+size[1]) / 250)
    points = []

    im = Image.new(mode='RGB', size=size, color='black')
    draw = ImageDraw.Draw(im)
    uid_prefix = f"{palette_names[palette_index]} "
    uid = ''
    metadata = f"{datetime.date.today()}"

    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            x = size[0] / (rows + 1) * row
            y = size[1] / (cols + 1) * col
            # x = round(x,1)
            # y = round(y,1)
            x = int(x)
            y = int(y)
            points.append((x, y))
            if random.randint(0, 2) > 0:
                random_index = random.randrange(len(palette))
                color = palette[random_index]
                (end_x, end_y) = points[random.randrange(len(points))]
                draw.line((x, y, end_x, end_y), fill=color, width=(radius+1)*2, joint="curve")
                draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=color)
                draw.ellipse([(end_x-radius, end_y-radius), (end_x+radius, end_y+radius)], fill=color)
                uid += f"_{random_index}-{x}{y}{end_x}{end_y}"
            else:
                random_index = random.randrange(len(palette))
                color = palette[random_index]
                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color)
                uid += f"-{x}{y}{x}{y}"

    apply_rotate = False
    apply_aa = True
    if apply_rotate:
        im = im.rotate(90)
    if apply_aa:
        im = im.resize(size=(512, 512), resample=Image.ANTIALIAS)

    im.show()
    # print(uuid.uuid4())
    encoded_uid = str_decode(uid)
    im.save(f"C:\\Users\\brand\\OneDrive\\Pictures\\Lines\\{uid_prefix}{encoded_uid}.png")
    # im.save(os.path.join('C:\\Users\\brand\\OneDrive\\Pictures\\Lines', f"{uid}.png"))


def str_encode(num):
    num = hex(num)[2:].rstrip("L")

    if len(num) % 2:
        num = "0" + num

    return base64.b64encode(num.decode('hex'))


def str_decode(alpha):
    num_bytes = base64.b64decode(alpha)
    return int(num_bytes.encode('hex'), 16)


def generate_metadata():
    # 1 in 100 chance of a gradient background!
    # some palettes rarer than others
    # the palette
        # the colors used in the palette
    # how many lines?
        # connected segments
        # total length of all lines
    # how many dots? 0 is pretty rare but possible
        # complicated bc not all dots are visible, not all dots are endpoints!
    print('')


if __name__ == '__main__':
    # for palette in range(len(palettes)):
    #     print_palette(palettes[palette])

    # draw_dots()

    draw_lines()

    # create_pixels((32,32))

    # create_image('RGB', (400, 300), 'white')
    # create_image("CMYK", 400, 300, (209, 123, 193, 100))
