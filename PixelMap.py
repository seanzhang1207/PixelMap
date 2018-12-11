#!/usr/bin/env python3
import sys
import argparse
import os.path
import numpy as np
import cv2

parser = argparse.ArgumentParser(description='Maps a single pixel art design across a color coded animation template.')
parser.add_argument('-t', '--template', required=True)
parser.add_argument('-f','--noflip', action='store_true', default=False)
parser.add_argument('design', nargs='+')

args = parser.parse_args(sys.argv[1:])


inplace = np.array([255, 255, 255, 255])
edge = np.array([0, 0, 0, 255])
background = np.array([0, 0, 0, 0])


template = cv2.imread(args.template, cv2.IMREAD_UNCHANGED)

for designPath in args.design:
    design = cv2.imread(designPath, cv2.IMREAD_UNCHANGED)

    indices = np.unique(template.reshape(-1, template.shape[2]), axis=0)
    default = template[..., 0: template.shape[0], :]
    default = default.reshape(-1, default.shape[2])

    palette = []
    for index in indices:
        mask = (default == index).all(1)
        color = np.unique(design.reshape(-1, design.shape[2])[mask], axis=0)[0]
        palette.append((index, color))

    result = np.zeros_like(template)

    for i in range(int(template.shape[1] / template.shape[0])):

        sprite = template[..., i * template.shape[0]: (i + 1) * template.shape[0], :]
        destination = result[..., i * result.shape[0]: (i + 1) * result.shape[0], :]
        
        for index, color in palette:
            mask = (sprite == index).all(2)
            if (index == background).all(0):
                destination[mask] = color
            elif (index == edge).all(0):
                destination[mask] = color
            elif (index == inplace).all(0):
                destination[mask] = design[mask]
            else:
                pass

        for index, color in palette:
            mask = (sprite == index).all(2)
            if not ( (index == background).all(0) or (index == edge).all(0) or (index == inplace).all(0) ):
                destination[mask] = color

    if args.noflip:
        cv2.imwrite(os.path.splitext(designPath)[0] + ".painted.png", result)
    else:
        result_l = result
        result_r = cv2.flip(result.copy(), 1)

        final = np.concatenate((result_l, result_r), axis=1)

        cv2.imwrite(os.path.splitext(designPath)[0] + ".painted.png", final)