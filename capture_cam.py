#!/usr/bin/env python3
import click
import cv2
import numpy as np
import time


class FreqTimer(object):
    def __init__(self, interval=1):
        self.interval = interval
        self.last = time.time()
        self.count = 0

    def update_and_print(self):
        self.count = (self.count + 1) % self.interval
        if self.count == 0:
            now = time.time()
            delta = now - self.last
            freq = self.interval / delta
            print(f"{freq:.1f} [fps]")
            self.last = now


def read(cap: cv2.VideoCapture) -> np.ndarray:
    ret, frame = cap.read()
    if ret:
        return frame
    else:
        print(".")
        cv2.waitKey(1)
        return read(cap)


@click.command()
@click.argument("cam_path")
def main(cam_path):
    cap = cv2.VideoCapture(cam_path)
    timer = FreqTimer(interval=200)
    while True:
        timer.update_and_print()
        frame = read(cap)
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) == 27:
            break


if __name__ == "__main__":
    main()
