#!/usr/bin/env python3
import os
from datetime import datetime
import pathlib
import cv2
import numpy as np
import click
from collections import deque

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
WINDOW_NAME = 'aruco'
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
FPS = 30
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def open_camera(device):
    print(f'open: {device}')
    cap = cv2.VideoCapture(device)
    return cap


def setup_camera(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'set properties -> size={str(width)}x{str(height)}, fps={str(fps)}')


def time_average(img_buf):
    return np.array(img_buf).mean(axis=0).astype(np.uint8)


@click.command()
@click.argument('device')
@click.option('--num_average', type=click.IntRange(1, 5), default=1, help='frame number of time averaging')
@click.option('--save_interval', type=int, default=1, help='frame number interval to save images')
@click.option('--save_dir', type=str, default='/tmp/aruco_detector', help='directory to save images')
def main(device, num_average, save_interval, save_dir):
    cap = open_camera(device)
    setup_camera(cap)
    img_buf = deque(maxlen=num_average)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
    pathlib.Path(save_dir).mkdir(exist_ok=True)
    loop = 0

    while True:
        # Retrieve image (& time averaging)
        ret, frame = cap.read()
        if not ret:
            k = cv2.waitKey(1)
            if k == 27:  # Esc key
                break
            continue
        img_buf.append(frame)
        img_ave = time_average(img_buf)

        # Detect markers
        corners_list, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img_ave, ARUCO_DICT)
        frame_overlay = cv2.aruco.drawDetectedMarkers(img_ave, corners_list, ids)

        if ids is None or len(ids) == 0:
            print("markers not found")

        cv2.imshow(WINDOW_NAME, frame_overlay)
        t_now = datetime.now()
        if (loop % save_interval == save_interval - 1):
            t_str = t_now.strftime(DATETIME_FORMAT)
            filename = os.path.join(save_dir, f"{t_str}-{loop:04d}.png")
            print(f"save --> {filename}")
            cv2.imwrite(filename, frame_overlay)

        # Key input
        k = cv2.waitKey(1)
        if k == 27:  # Esc key
            break

        loop += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
