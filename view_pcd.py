#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import open3d as o3d
import click
# import toml
# import os

# CAMERA_POSE_FILE = "~/inaho_robo/config/inaho_arm/calibration/camera_pose.toml"
# with open(os.path.expanduser(CAMERA_POSE_FILE)) as f:
#     camera_pose = toml.load(f)

axcolor = 'gold'
ax_sli = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
sli = Slider(ax_sli, 'Radius', 1, 5, valinit=0, valstep=1)


def update(val):
    rot = sli.val
    l.set_xdata(sr * np.sin(t) + sx)
    l.set_ydata(sr * np.cos(t) + sy)
    fig.canvas.draw_idle()


@click.command()
@click.argument('filename')
@click.option('--rot', type=float, default=-45.)
def main(filename, rot):
    sli.on_changed(update)
    pcd = o3d.io.read_point_cloud(filename)
    th = np.deg2rad(rot)
    R = np.array([[np.cos(th), -np.sin(th), 0],
                  [np.sin(th), +np.cos(th), 0],
                  [0, 0, 1]])
    pcd_rot = pcd.rotate(R)
    points = np.asarray(pcd_rot.points)
    fig, axes = plt.subplots(3, 3)
    for i in range(3):
        for j in range(3):
            axes[i][j].scatter(points[:, i], points[:, j], marker='.', s=2)

    labels = ['x', 'y', 'z']
    for i in range(3):
        axes[i][0].set_ylabel(labels[i])
    for j in range(3):
        axes[2][j].set_xlabel(labels[j])
    plt.show()
    # o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":
    main()
