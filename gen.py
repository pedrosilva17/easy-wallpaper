import argparse
import random
import glob
import re
from PIL import Image, UnidentifiedImageError


def positive_int(i):
    i = int(i)
    if i <= 0:
        raise argparse.ArgumentTypeError(
            "Only positive values are allowed for size and rows/columns.")
    return i


def hex_code(h):
    color_pattern = re.compile(r'^#[A-Fa-f0-9]{6}$')
    if not color_pattern.match(h):
        raise argparse.ArgumentTypeError(
            'Invalid hex code formatting. Must start with "#", followed by 6 characters from [A-F], [a-f] or [0-9].')
    return h


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='gen.py',
        description='Create a wallpaper based on a generated pattern of images.',
        epilog='Note: When choosing the number of columns/rows, try to select divisors of the width/height respectively, to avoid excessive padding at the edges of the wallpaper.\n'
        'For the best results, use images for the patterns with the same or similar inner padding (in case they have transparent backgrounds).')
    parser.add_argument(
        '-b', '--background', type=str, required=False, default=None,
        metavar="<filepath>",
        help="the background image's file path. If set, overrides size and color parameters.")
    parser.add_argument(
        '-s', '--size', type=positive_int, required=False,
        default=[1920, 1080], nargs=2, metavar=("<width>", "<height>"),
        help="the background image's size, defaults to 1920x1080")
    parser.add_argument(
        '-c', '--color', type=hex_code, required=False, default='#ffffff',
        metavar="<hexcode>",
        help="the hex code for the color of the wallpaper's background, defaults to #ffffff (white)")
    parser.add_argument(
        '-rc', '--rows_cols', type=positive_int, required=False,
        default=[5, 5], nargs=2, metavar=("<rows>", "<columns>"),
        help="the number of image rows and columns added to the wallpaper, defaults to 5 rows and 5 columns")
    parser.add_argument(
        '-sp', '--spacing', type=int, required=False, default=10,
        metavar="<spacing>",
        help="additional spacing (in pixels) between each image, defaults to 10")
    parser.add_argument(
        '-o', '--output', type=str, required=False, default='wallpaper',
        metavar="<filepath>",
        help="the output wallpaper's filepath (without file extension), defaults to 'wallpaper', saved in the current directory")
    parser.add_argument(
        '-rd', '--rand_dist', required=False,
        help="randomize the distribution of images (if there is more than one in the specified folder), defaults to false (places images sequentially in alphabetical order)",
        action='store_true')
    parser.add_argument(
        '-rr', '--rand_rot', required=False,
        help="randomize the rotation of each image, defaults to false",
        action='store_true')
    return parser.parse_args()


def resize_image(image, scale_factor):
    new_height = int(image.height * scale_factor)
    new_width = int(image.width * scale_factor)
    if (new_width <= 0) or (new_height <= 0):
        raise SystemExit(
            "At least one of the dimensions of an image is non-positive. "
            "Try lowering the spacing value or the number of rows/columns for the wallpaper.")

    image = image.resize((new_width, new_height))
    return image


def increment_index(counter, no_images, rand):
    return random.randint(0, no_images-1) if rand else (counter + 1) % no_images


def generate_wallpaper(
        background, size, color, rows, cols, spacing, path, random_dist, rotate):
    if background:
        bg = Image.open(background)
        bg.convert('RGBA')
        size[0] = bg.width
        size[1] = bg.height
    else:
        bg = Image.new('RGBA', size, hex_to_rgb(color) + (255,))
    layer = Image.new('RGBA', size, (255, 255, 255, 0))
    tile_width, tile_height = bg.width // cols, bg.height // rows
    width_error, height_error = bg.width / cols - tile_width, bg.height / rows - tile_height

    images = []
    try:
        for file in glob.glob('images/*'):
            image = Image.open(file)
            image = image.convert('RGBA')
            scale_factor = min((tile_width - spacing) / image.width, (tile_height - spacing) / image.height)
            image = resize_image(image, scale_factor)
            images.append(image)
    except UnidentifiedImageError as exc:
        raise SystemExit(
            "One of the files in the 'images' folder is not an image.") from exc
    if images == []:
        raise SystemExit(
            "The 'images' folder is empty. Place at least one image in the folder to be used by the program.")

    index = -1
    for i in range(rows):
        for j in range(cols):
            index = increment_index(index, len(images), random_dist)
            image = images[index]
            if rotate:
                image = image.rotate(random.randint(0, 359), expand=1)
                scale_factor = min((tile_width - spacing) / image.width,
                            (tile_height - spacing) / image.height)
                image = resize_image(image, scale_factor)
            x = j * tile_width + (tile_width - image.width) // 2
            y = i * tile_height + (tile_height - image.height) // 2
            layer.paste(image, (x, y), mask=image)

    bg.paste(layer, (int(width_error*cols / 2),
             int(height_error*rows / 2)), mask=layer)
    bg.save(path + ".png")


if __name__ == "__main__":
    args = parse_arguments()
    generate_wallpaper(
        args.background,
        args.size, args.color, args.rows_cols[0],
        args.rows_cols[1],
        args.spacing, args.output, args.rand_dist, args.rand_rot)
