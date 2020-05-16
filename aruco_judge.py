#!/usr/bin/env python3
import cv2
import numpy as np
import click
from collections import deque

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
TIME_AVERAGE_NUM = 5
WINDOW_NAME = 'aruco'
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
Y_THRESHOLD = np.array([620, 660, 700, 750, 850, 950, IMAGE_HEIGHT])
NUM_IDS = len(Y_THRESHOLD) - 1


def open_camera(device_id):
    print(f'open: {device_id}')
    cap = cv2.VideoCapture(device_id)

    return cap


def setup_camera(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)


def calc_center_pos(corners):
    center = corners.mean(axis=0)
    return center


def time_average(img_buf):
    return np.array(img_buf).mean(axis=0).astype(np.uint8)


def in_range(ys):
    result = np.zeros(NUM_IDS, dtype=np.bool)
    for y in ys:
        result += (y < Y_THRESHOLD[1:]) * (y > Y_THRESHOLD[:-1])
    return result


def draw_threshold_lines(img, ok_flags):
    MAGENTA = (255, 0, 255)
    YELLOW = (0, 255, 255)
    for ok, y in zip(ok_flags, Y_THRESHOLD):
        color = YELLOW if ok else MAGENTA
        img = cv2.line(img, (0, y), (IMAGE_WIDTH, y), color, thickness=2)
    return img


def bool_to_str(ok):
    return '   o' if ok else '   x'


@click.command()
@click.argument('device_id')
def main(device_id):
    cap = open_camera(device_id)
    setup_camera(cap)
    img_buf = deque(maxlen=TIME_AVERAGE_NUM)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)

    while True:
        # Retrieve image (& time averaging)
        ret, frame = cap.read()
        img_buf.append(frame)
        img_ave = time_average(img_buf)

        # Detect markers
        corners_list, ids, rejectedImgPoints = cv2.aruco.detectMarkers(img_ave, ARUCO_DICT)
        if ids is None or len(ids) == 0:
            continue

        # Calculation
        ys = [calc_center_pos(corners[0])[1] for corners in corners_list]
        ys_sorted = sorted(ys)
        marker_exists = in_range(ys_sorted)

        # Print info
        print("y markers: " + " ".join([f'{y:4.0f}' for y in ys_sorted]))
        print("exisists : " + " ".join([bool_to_str(x) for x in marker_exists]))
        print("threshold: " + " ".join([f'{y:4.0f}' for y in Y_THRESHOLD]))
        print()

        # Visualization
        frame_overlay = cv2.aruco.drawDetectedMarkers(img_ave, corners_list, ids)
        frame_overlay = draw_threshold_lines(frame_overlay, marker_exists)
        cv2.imshow(WINDOW_NAME, frame_overlay)

        # Key input
        k = cv2.waitKey(1)
        if k == 27:  # Esc key
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
