#!/usr/bin/env python
import toml
import cv2
w_set = 1280
h_set = 720
fps_set = 30
TOML_PATH = "/home/ykarako/inaho_robo/config/aspara_detector/dualzense_l.toml"


def confirm_prop(cap, prop_id, value_arg):
    value_act = cap.get(prop_id)
    if value_act != value_arg:
        raise RuntimeError("failed to set property. arg: {}, act: {}".format(
            value_arg, value_act))


def open_cam():
    dict_toml = toml.load(open(TOML_PATH))
    device_id = dict_toml['Rgb']['device_id']

    image_width = int(dict_toml['Rgb']['width'])
    image_height = int(dict_toml['Rgb']['height'])

    cap = cv2.VideoCapture(device_id)
    if cap.isOpened():
        print("succeeded to open {}".format(device_id))
    else:
        print("failed to open {}".format(device_id))
        raise RuntimeError("failed to open see3cam camera. device id : {} ".format(device_id))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)
    cap.set(cv2.CAP_PROP_FPS, int(dict_toml['Rgb']['fps']))
    print('see3cam properties set: {}x{} {} fps'.format(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH),
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
        cap.get(cv2.CAP_PROP_FPS)))
    confirm_prop(cap, cv2.CAP_PROP_FRAME_WIDTH, image_width)
    confirm_prop(cap, cv2.CAP_PROP_FRAME_HEIGHT, image_height)
    confirm_prop(cap, cv2.CAP_PROP_FPS, dict_toml['Rgb']['fps'])


cap = open_cam()
