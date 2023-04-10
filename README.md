# easy-wallpaper

easy-wallpaper is a simple Python program that allows you to create static wallpapers with image patterns.
It is highly customizable, allowing you to change size, background colors, images to be used in the pattern and their rotation/distribution, use images as backgrounds, and more.
For now, the pattern choices are limited to sequential or random image distribution, but more might be added in the future.

## Installation

Clone this repository in a folder of your choice and navigate to it.

```bash
git clone <url>
cd easy-wallpaper
```

To run this program, you need to install [Python](https://www.python.org/downloads/), which should already come with [pip](https://pip.pypa.io/en/stable/installation/). After that, install the only dependency ([Pillow](https://pillow.readthedocs.io/en/stable/)) by running the following command:

```bash
pip install Pillow
```

And that's it.

## Usage and examples

This program scans the `images` folder present in the root of this repository for images to generate the patterns. Along with it, there are three basic images and a background you can use to test it (note: I do not hold the rights to any of the test images). To use your custom images for the pattern, please place them in the aforementioned folder.

Notes regarding some of the program's characteristics:

- If for some reason you decide to use GIFs as background, note that their color pallette is smaller than a PNG (for example), so Pillow tries to do a conversion that may alter the colors for the images used in the pattern.
- The program preserves the aspect ratios of the images. As such, if they have very different sizes, that might be noticeable in the wallpaper, depending on the discrepancy between scale factors used to resize each image.
- Using a custom background image might increase execution time quite a bit, especially if it is high-resolution.

Below is the list of arguments you can pass to the program (and how to display it in your terminal), as well as their effects. There are also some examples of wallpapers you could generate with the provided example background and images (which are not very pleasing to look at, since they are mere proof of concepts). Hopefully you can create something prettier than those!

### Check available options

```bash
python gen.py -h
```

```
usage: gen.py [-h] [-b <filepath>] [-s <width> <height>] [-c <hexcode>] [-rc <rows> <columns>] [-sp <spacing>] [-o <filepath>] [-rd] [-rr]

Create a wallpaper based on a generated pattern of images.

options:
  -h, --help            show this help message and exit
  -b <filepath>, --background <filepath>
                        the background image's file path. If set, overrides size and color parameters.
  -s <width> <height>, --size <width> <height>
                        the background image's size, defaults to 1920x1080
  -c <hexcode>, --color <hexcode>
                        the hex code for the color of the wallpaper's background, defaults to #ffffff (white)
  -rc <rows> <columns>, --rows_cols <rows> <columns>
                        the number of image rows and columns added to the wallpaper, defaults to 5 rows and 5 columns
  -sp <spacing>, --spacing <spacing>
                        additional spacing (in pixels) between each image, defaults to 10.
  -o <filepath>, --output <filepath>
                        the output wallpaper's filepath (without file extension), defaults to 'wallpaper', saved in the current directory
  -rd, --rand_dist      randomize the distribution of images (if there is more than one in the specified folder), defaults to false (places images sequentially in alphabetical
                        order)
  -rr, --rand_rot       randomize the rotation of each image, defaults to false

Note: When choosing the number of columns/rows, try to select divisors of the width/height respectively, to avoid excessive padding at the edges of the wallpaper. For the best
results, use images for the patterns with the same or similar inner padding (in case they have transparent backgrounds).
```

### Default wallpaper

```
python gen.py -o "examples/example_1"
```

![Wallpaper 1](examples/example_1.png)

### Light blue vertical wallpaper

```
python gen.py -o "examples/example_2" -c #00ffff -s 1080 1920 -sp 30 -rd
```

![Wallpaper 2](examples/example_2.png)

### Windows XP background wallpaper

```
python gen.py -o "examples/example_3" -b "xp.jpg" -rc 7 5 -rd -rr
```

![Wallpaper 3](examples/example_3.png)

## Contributing

If you want to improve the code or add a new feature, open a pull request. If you encounter any bugs while using the program, please let me know by opening an issue. Thank you for your help!

## License

[MIT](https://choosealicense.com/licenses/mit/)
