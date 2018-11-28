# MathArtist

Tool for generating pictures using mathematical formulas.

## Examples

TODO: add images

## Algorithm

To create new image we perform these steps:

* Generate name using data folder with mulltiple nouns, adjectives, prepositions and pronouns and [names_generator](names_generator.py) module to convert single words into fun looking image name.
* Select operators from predefined sets and coordinates conversion transformations. All coordinates are converted to range [-1, 1] because this range nicely fits to many mathematical operations. See [coords](coords.py) module for more information.
* Generate expression tree using operators from previous step that convert each (x, y) point to color. There are multiple operators from simplest VariableX (which converts coordinate to (x, x, x) color) to difficult Mix and Closest (you can see their code in [operators](operators.pyx) module). Tree size is dynamicall so there can be something simple like Mix(x, y, Well(x)) or long multiline formula which computing can take some minutes.
* We can use [checker](checker.py) to check if generated formula is bad and recreate it. Checker is very simple - it thinks formula is good when it has different functions, has few well and tent functions (because they produce bad looking lines) and generates multicolor image (because the "Black square" by Malevich already exists). By the way sometimes checker decides that bad formula is worthy of to make an image. It's not a bug, it's a feature.
* And now we convert each point of image to color using coordinates transform from step 2 and expression tree from step 3. After all points have their colors we can draw comleted image. That's all.

## Requirements

This program uses Python 3 so you need to have Python 3 and pip for it. To install them use instructions for your OS.

It also needs some extra libraries and applications such as argparse, PIL, numpy, PyQt5, pyinstaller and Cython. To install them run this:

```bash
#if pip on your OS has version 3 or above
pip install -r requirements.txt
#or this
pip3 install -r requirements.txt
```

Some packages such as PyQt5 require additional packages on some OS. For example on deb-based systems you should also install python3-pyqt5:

``` bash
apt install python3-pyqt5 pyqt5-dev-tools
```

This tool also need C/C++ compiler because of using Cython. You can install it following instructions for your OS.

## Building

Before first run you should prepare binary libraries. To make it run

```bash
python setup.py build_ext --inplace
#or
python3 setup.py build_ext --inplace
```

### Pyinstaller

I prefer to use pyinstaller for building release versions. To build one-file release run:

```bash
pyinstaller --onefile --windowed main.py --hidden-import=palettes
```

## Usage

There are 2 work modes: console and GUI.

### Console

In console mode app generates one image, saves it and exits.

There are some extra modes:

```
usage: python main.py [-h] [--console] [--about] [--checker] [--file FILE]
                  [--generate_list]

Tool for generating pictures using mathematical formulas.

optional arguments:
  -h, --help       show this help message and exit
  --console        Run in console mode (no window)
  --about          Show about info
  --checker        Enable checker
  --file FILE      Load file
  --generate_list  Generate operators' list (developer option)
```

### GUI

TODO: keys

### Samples

There is samples folder with some nice images in text format. You can use app's read file option to convert these texts into images.

## License

In short the MathArtist uses GNU GPL3. For more information see the LICENSE file.

But there is one nuance. This program uses some code from Andrej Bauer's randomart project. Original randomart project is licensed with BSD 2-clause license. You can download it here - http://math.andrej.com/2010/04/21/random-art-in-python/

Andrej Bauer's code in this project is licensed with both BSD 2-clause and GNU GPL3 licenses. The combined project uses only GNU GPL3. You shouldn't use any part of MathArtist with BSD license. Please use GNU GPL3 only.

## Thanks

I'd like to thank:

Andrej Bauer for wonderful online random art project (http://www.random-art.org/online/), original Python randomart code (http://math.andrej.com/2010/04/21/random-art-in-python/) and great ideas which lead to this project.

Matt DesLauriers for cool color-wander project (http://color-wander.surge.sh/) and (https://github.com/mattdesl/color-wander) and nice palettes used in this project.

Volodymyr Shymanskyy for his JS randomart project (https://github.com/vshymanskyy/randomart) that gave me some ideas such as mindepth and some operators.

Halvor Kjærås for random art generator - (http://ironigardinen.net/generatorer/art2/index.html). It gave me some ideas and data for MathArtist art name generator.
