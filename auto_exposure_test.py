#!/usr/bin/env python3
import click
import cv2

DEVICE_ID = "/dev/v4l/by-id/usb-KYE_Systems_Corp._USB_Camera_200901010001-video-index0"

def show_params(cap):
    print(" width: {}".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(" height: {}".format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(" fps: {}".format(cap.get(cv2.CAP_PROP_FPS)))
    print(" auto_exposure: {}".format(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)))
    print(" exposure: {}".format(cap.get(cv2.CAP_PROP_EXPOSURE)))

def set_params(cap, width, height, fps, auto_exposure, exposure):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

@click.command()
@click.option('--enable-auto-exposure', '-e', is_flag=True)
def main(enable_auto_exposure):
    cap = cv2.VideoCapture(DEVICE_ID)
    print(f"Auto Exposure Test for Camera '{DEVICE_ID}'")
    print(f"Enable Auto Exposure: {enable_auto_exposure}")

    print("\nOld parameters")
    show_params(cap)

    print("\nSet parameters")
    if enable_auto_exposure:
        set_params(cap, width=640, height=480, fps=30, auto_exposure=1.0, exposure=-1)
    else:
        set_params(cap, width=640, height=480, fps=30, auto_exposure=0.25, exposure=50)

    print("\nNew parameters")
    show_params(cap)

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()