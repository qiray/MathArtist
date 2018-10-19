# -*- coding: utf-8 -*-
import random
from PIL import Image
import numpy

def draw(path):
    random.seed()
    length = 512*512
    pixels = [0 for x in range(length)]
    for i in range(length):
        pixels[i] = (
            int(random.random() * 255), #much faster then randInt
            int(random.random() * 255),
            int(random.random() * 255)
        )
    img = Image.new('RGB', (512, 512))
    img.putdata(pixels)
    img.save(path)

draw("image.png")
