#!/usr/bin/env python
import numpy as np
import pandas as pd
import toml
from tf.transformations import compose_matrix, euler_from_matrix


def camera_transform_matrix(toml_path, side):
    camera_pose_dict = toml.load(open(toml_path))[side]
    rx = camera_pose_dict['orientation']['roll']
    ry = camera_pose_dict['orientation']['pitch']
    rz = camera_pose_dict['orientation']['yaw']
    x = camera_pose_dict['position']['x']
    y = camera_pose_dict['position']['y']
    z = camera_pose_dict['position']['z']
    return compose_matrix(
        angles=(rx, ry, rz), translate=(x, y, z))


def test_camera_transform_matrix(toml_path, side):
    camera_pose_dict = toml.load(open(toml_path))[side]
    rx = camera_pose_dict['orientation']['roll']
    ry = camera_pose_dict['orientation']['pitch']
    rz = camera_pose_dict['orientation']['yaw'] + 0.1
    x = camera_pose_dict['position']['x'] + 0.1
    y = camera_pose_dict['position']['y'] - 0.1
    z = camera_pose_dict['position']['z']
    return compose_matrix(
        angles=(rx, ry, rz), translate=(x, y, z))


def test_solve(toml_path, side, csv_path):
    print("------- test start")
    Hc_now = camera_transform_matrix(toml_path, side)
    Hc_ref = test_camera_transform_matrix(toml_path, side)
    df = pd.read_csv(csv_path, skipinitialspace=True).T
    n = df.shape[1]
    P_ref = np.r_[df.loc[['x', 'y', 'z']].values, np.ones((1, n))]

    A = np.linalg.inv(Hc_now + np.identity(4))
    B = np.dot(Hc_ref + np.identity(4), P_ref)
    P_act = np.dot(A, B)
    P_diff = P_act - P_ref

    Hc_pred = solve(Hc_now, P_ref, P_diff)
    print("diff: {}".format(Hc_pred - Hc_ref))
    print("------- test done")


def sample_points_matrix(csv_path):
    df = pd.read_csv(csv_path, skipinitialspace=True).T
    _P_ref = df.loc[['x', 'y', 'z']].values
    _P_diff = df.loc[['dx', 'dy', 'dz']].values
    n = df.shape[1]
    return np.r_[_P_ref, np.ones((1, n))], np.r_[_P_diff, np.zeros((1, n))]


def solve(Hc_now, P_ref, P_diff):
    P_act = P_ref + P_diff
    A = np.dot(Hc_now, P_act)
    H_pred = np.dot(A, np.linalg.pinv(P_ref))
    return H_pred


def print_result(H_pred):
    position_pred = H_pred[:3, 3]
    orientation_pred = euler_from_matrix(H_pred[:3, :3])

    print("position: {}".format(position_pred))
    print("orientation: {}".format(orientation_pred))


def main():
    camera_pose_toml = "/home/ykarako/inaho_robo_sim/config/inaho_arm/calibration/camera_pose.example.toml"
    sample_points_csv = "/home/ykarako/test_data.csv"

    test_solve(camera_pose_toml, "left", sample_points_csv)

    Hc_now = camera_transform_matrix(camera_pose_toml, "left")
    P_ref, P_diff = sample_points_matrix(sample_points_csv)
    H_pred = solve(Hc_now, P_ref, P_diff)
    print_result(H_pred)


if __name__ == "__main__":
    main()
