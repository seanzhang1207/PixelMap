# PixelMap

Tired of drawing walking animation for your pixel game characters? Draw one frame, define how it moves and generate the rest! For example, I designed this little fella:

![](demos/design.png)

And I made something like this:

![spritesheet](demos/template.png)

Here each unique color code (black/white/transparent/colored) will be used to map the original design to each sprite.

So I hit the commands, and voila --

![](/Users/sean/Development/PixelMap/demos/spritesheet.png)



**Requirements:**

NumPy, OpenCV

## Usage

```
usage: PixelMap.py [-h] -t TEMPLATE [-f] design [design ...]

Maps a single pixel art design across a color coded animation template.

positional arguments:
  design                            The design.

optional arguments:
  -h, --help                        show this help message and exit
  -t TEMPLATE, --template TEMPLATE  The color-coded template file
  -f, --noflip                      Do not create the other side by flipping
```

## The Color Codes

**NOTE: The first sprite in the template MUST match the design!**

Black pixel: Edges. Will use one pixel from the design for all sprite edges.

White pixel: In-place pasting. Looks for the pixel at the same place in the design, and copies that pixel.

Transparent pixel: Will be ignored. 

**Any other colored pixel: Takes the position of the pixel in the first sprite. Looks for the pixel at the same place in the design, takes its color. Maps this color to all pixels that has the same color.**

## How does it work?

The script first matches the design with the first sprite in the template. Each pixel in matched and a color translation table is built. Then edges and in-place painting is taken care of by simply replacing and copy-pasting the pixels. The indexed colors are processed last using the color translation table. 