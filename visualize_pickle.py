#!/usr/bin/env python2

import os
import numpy as np
from matplotlib import pyplot as plt
import pickle
import glob
import cv2
import click

KEYS_PICKLE = [
    [
        '/see3cam/rgb/left',
        '/see3cam/rgb/right',
    ], [
        '/camera_r/depth_near/image_raw',
        '/camera_l/depth_near/image_raw',
    ], [
        '/camera_r/depth_far/image_raw',
        '/camera_l/depth_far/image_raw',
    ]
]


def open_pickle(path_pickle):
    # (path) -> dict

    with open(path_pickle) as f:
        return pickle.load(f)


def save_image(path_pickle, dir_save):
    # (path, path) -> None
    # side effect: save png file

    data = open_pickle(path_pickle)
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 10))

    for row in range(3):
        for col in range(2):
            imgs = data[KEYS_PICKLE[row][col]]

            if len(imgs) == 0:
                continue

            if row == 0:  # see3cam image
                img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2RGB)
            else:  # depth image
                img = np.rot90(imgs[0], k=-1)

            axes[row][col].imshow(img)

    axes[1][0].set_ylabel('near')
    axes[2][0].set_ylabel('far')
    axes[2][0].set_xlabel('right')
    axes[2][1].set_xlabel('left')
    fig.suptitle('{} ({})'.format(path_pickle, data.get('/sensor_id', 'not defined')))

    path_fig = '{}/{}.png'.format(dir_save, os.path.basename(path_pickle))
    print('save: {}'.format(path_fig))
    fig.savefig(path_fig)
    plt.close(fig)


@click.command()
@click.argument('dir_pickle', type=click.Path(exists=True))
@click.option('--dir_save', type=click.Path(), default=None)
def main(dir_pickle, dir_save):
    paths_pickle = glob.glob('{}/*.pickle'.format(dir_pickle))
    print('{} pickle files exist'.format(len(paths_pickle)))

    dir_save = dir_pickle if dir_save is None else dir_save
    if not os.path.exists(dir_save):
        print('make a new directory: {}'.format(dir_save))
        os.makedirs(dir_save)

    for p in paths_pickle:
        print('open: {}'.format(p))
        save_image(p, dir_save)


if __name__ == '__main__':
    main()
