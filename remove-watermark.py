#!/bin/env python3
from PIL import Image
import os

SIZE_X = 256
SIZE_Y = 256
SIZE = SIZE_X,SIZE_Y
WATERMARK = Image.open("watermark.png")
WHITES = [(255, 255, 255), (255, 255, 255, 255)]
ROOT = "../NeuralBlenderPack/assets/minecraft/textures/"
DONE = []


def clean(path, radius=2, overwrite=False):
    src = Image.open(path)
    dest = Image.new("RGBA", (SIZE))

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            p = clean_pixel(src, (x, y), radius)
            dest.putpixel((x, y), p)
    if overwrite:
        dest.save(path)
    else:
        dest.save(path[:-4] + f"-{radius}.png")


def clean_pixel(img, xy, radius):
    if not is_watermark(xy):
        return img.getpixel(xy)
    
    samples = []
    for y in range(-radius, radius+1):
        posy = xy[1] + y
        if posy >= SIZE_Y or posy < 0:
            continue
        for x in range(-radius, radius+1):
            posx = xy[0] + x
            if posx >= SIZE_X or posx < 0:
                continue
            pos = posx, posy
            if is_watermark(pos):
                continue
            samples.append(img.getpixel(pos))

    return average_cols(samples)


def average_cols(samples):
    tot = [0, 0, 0]
    for s in samples:
        for i in range(3):
            tot[i] += s[i]
    tot = [x//len(samples) for x in tot]
    return (tot[0], tot[1], tot[2], 255)


def is_watermark(xy):
    return WATERMARK.getpixel(xy) in WHITES


def clean_dir(path):
    items = os.listdir(path)
    items.sort()
    for name in items:
        if os.path.isdir(path + name):
            clean_dir(path + name + "/")
        elif name not in DONE:
            if name[-4:] == ".png":
                clean(path + name, 2, True)
                DONE.append(name)
                print(name)
                with open("done.txt", "a") as f:
                    f.write(name+"\n")
        else:
            print(name + " failed")


with open("done.txt", "r") as f:
    DONE = f.read().split("\n")
print(DONE[:10])
clean_dir(ROOT)
