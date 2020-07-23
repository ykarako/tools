#!/usr/bin/env python
import numpy as np
import pandas as pd
import toml
import click
from tf.transformations import compose_matrix, euler_from_matrix


def camera_transform_matrix(camera_pose_dict, side):
    rx = camera_pose_dict[side]['orientation']['roll']
    ry = camera_pose_dict[side]['orientation']['pitch']
    rz = camera_pose_dict[side]['orientation']['yaw']
    x = camera_pose_dict[side]['position']['x']
    y = camera_pose_dict[side]['position']['y']
    z = camera_pose_dict[side]['position']['z']
    return compose_matrix(
        angles=(rx, ry, rz), translate=(x, y, z))


def sample_points_matrix(csv_path):
    df = pd.read_csv(csv_path, skipinitialspace=True).T
    _P_ref = df.loc[['x', 'y', 'z']].values * 1e-3
    _P_diff = df.loc[['dx', 'dy', 'dz']].values * 1e-3
    n = df.shape[1]
    return np.r_[_P_ref, np.ones((1, n))], np.r_[_P_diff, np.zeros((1, n))]


def solve(Hc_now, Hu, P_ref, P_diff):
    P_act = P_ref + P_diff
    Hc_inv = np.linalg.inv(Hc_now)
    A = np.dot(Hu, P_ref)
    B = np.dot(np.dot(Hc_inv, Hu), P_act)
    H_pred = np.dot(A, np.linalg.pinv(B))
    return H_pred


def make_dict(H_pred):
    position_pred = H_pred[:3, 3]
    orientation_pred = euler_from_matrix(H_pred[:3, :3])
    print(position_pred)
    print(orientation_pred)
    return {
        "position": {
            "x": float(position_pred[0]),
            "y": float(position_pred[1]),
            "z": float(position_pred[2]),
        },
        "orientation": {
            "roll": orientation_pred[0],
            "pitch": orientation_pred[1],
            "yaw": orientation_pred[2],
        },
    }


def overwrite_toml(camera_pose_dict, toml_path):
    print("--- Calculated camera pose:")
    print(toml.dumps(camera_pose_dict))
    if click.confirm("Do you want to overwrite?"):
        toml.dump(camera_pose_dict, open(toml_path, "w"))


@click.command()
@click.argument("csv_path")
@click.argument("toml_path")
@click.argument("side")
def main(csv_path, toml_path, side):
    camera_pose_dict = toml.load(open(toml_path))
    Hc_now = camera_transform_matrix(camera_pose_dict, side)
    Hu = compose_matrix(translate=(0, 0.450, 0))
    P_ref, P_diff = sample_points_matrix(csv_path)
    Hc_pred = solve(Hc_now, Hu, P_ref, P_diff)
    camera_pose_dict[side] = make_dict(Hc_pred)
    overwrite_toml(camera_pose_dict, toml_path)


if __name__ == "__main__":
    main()
