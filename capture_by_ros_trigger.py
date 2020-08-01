#!/usr/bin/env python3
import rospy
import click
import cv2
import numpy as np
from datetime import datetime
from retry import retry
from pathlib import Path
from std_msgs.msg import Bool


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class NewFrameNotReturned(RuntimeError):
    pass


class ImageRecorder(object):
    MAX_BUFFER_SIZE = 1000

    def __init__(self, cam_path: str, rec_directory: str, enable_preview: bool) -> None:
        self._cap = cv2.VideoCapture(cam_path)
        self._rec_directory = Path(rec_directory)
        self._enable_preview = enable_preview

        self._buffer = []
        self._period = 0
        self._enable_rec = False
        self._start_time = None

        rospy.Subscriber("/capture_trigger", Bool, self._trigger_cb)

    @retry(NewFrameNotReturned, tries=10)
    def _get_new_frame(self) -> np.ndarray:
        ret, frame = self._cap.read()

        if ret:
            return frame
        else:
            print(".", end="")
            cv2.waitKey(1)
            raise NewFrameNotReturned()

    def _trigger_cb(self, msg: Bool) -> None:
        rospy.loginfo(f"Received trigger: {msg.data}")

        if msg.data:
            self._start_time = get_timestamp()
            self._enable_rec = True
        else:
            self.save()

    def save(self) -> None:
        if not self._buffer:
            return

        rec_directory_period = self._rec_directory / self._start_time
        rec_directory_period.mkdir(parents=True)

        for i, frame in enumerate(self._buffer):
            cv2.imwrite(str(rec_directory_period / f"{i:03d}.png"), frame)

        self._buffer = []
        self._period += 1
        self._enable_rec = False

        rospy.loginfo(f"Save images -> {rec_directory_period}")

    def run(self) -> None:
        while not rospy.is_shutdown():
            frame = self._get_new_frame()

            if self._enable_preview:
                cv2.imshow("preview", frame)

            if self._enable_rec:
                self._buffer.append(frame)

                if len(self._buffer) >= self.MAX_BUFFER_SIZE:
                    rospy.logwarn("Buffer size is over")
                    self.save()

            if cv2.waitKey(1) == 27:  # Esc
                break


@click.command()
@click.argument("cam_path")
@click.option("--rec_directory", "-o", default="rec")
@click.option("--enable_preview", "-p", is_flag=True)
def main(cam_path, rec_directory, enable_preview):
    rospy.init_node("capture_by_ros_trigger")
    recorder = ImageRecorder(cam_path, rec_directory, enable_preview)
    try:
        recorder.run()
    finally:
        recorder.save()


if __name__ == "__main__":
    main()
