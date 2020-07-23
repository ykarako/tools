#!/usr/bin/env python
"""Calculate and update camera pose from arm approaching data
"""
import numpy as np
import pandas as pd
import toml
import click
from tf.transformations import compose_matrix, euler_from_matrix
from subprocess import check_output, check_call


class TomlEditWrapper(object):
    def __init__(self, toml_path):
        # type: (str) -> None
        self._toml_path = toml_path
        self._cmd = "tomledit-cli -f {} ".format(toml_path)

    def _check_output(self, subcmd):
        # type: (str) -> str
        return check_output(self._cmd + subcmd, shell=True)

    def _check_call(self, subcmd):
        # type: (str) -> bool
        return check_call(self._cmd + subcmd, shell=True) == 0

    def read(self):
        # type: () -> str
        return self._check_output("get-toml")

    def update(self, keys, value):
        # type: ([str], float) -> bool
        return self._check_call('update -- "{}" Float {}'.format(".".join(keys), value))

    def get(self):
        # type: () -> dict
        return toml.load(open(self._toml_path))


def matrix_from_dict(pose_dict):
    # type: (dict) -> np.ndarray
    rx = pose_dict['orientation']['roll']
    ry = pose_dict['orientation']['pitch']
    rz = pose_dict['orientation']['yaw']
    x = pose_dict['position']['x']
    y = pose_dict['position']['y']
    z = pose_dict['position']['z']
    return compose_matrix(
        angles=(rx, ry, rz), translate=(x, y, z))


def matrix_from_csv(csv_path):
    # type: (str) -> np.ndarray
    df = pd.read_csv(csv_path, skipinitialspace=True).T
    _P_ref = df.loc[['x', 'y', 'z']].values * 1e-3
    _P_diff = df.loc[['dx', 'dy', 'dz']].values * 1e-3
    n = df.shape[1]
    return np.r_[_P_ref, np.ones((1, n))], np.r_[_P_diff, np.zeros((1, n))]


def make_dict(H_pred):
    # type: (np.ndarray) -> dict
    position_pred = H_pred[:3, 3]
    orientation_pred = euler_from_matrix(H_pred[:3, :3])
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


def update_toml(camera_pose, toml_editor, side):
    print("--- Original camera pose:")
    print(toml_editor.read())

    print("--- Calculated camera pose:")
    print(toml.dumps(camera_pose))

    if click.confirm("Do you want to overwrite?"):
        for parent_key in ["position", "orientation"]:
            for child_key in ["x", "y", "z"]:
                value = camera_pose[parent_key][child_key]
                toml_editor.update([side, parent_key, child_key], value)


def solve(H_cam_now, H_une, P_ref, P_diff):
    # type: (np.ndarray, np.ndarray, np.ndarray, np.ndarray) -> np.ndarray
    P_act = P_ref + P_diff
    H_cam_inv = np.linalg.inv(H_cam_now)
    A = np.dot(H_une, P_ref)
    B = np.dot(np.dot(H_cam_inv, H_une), P_act)
    H_pred = np.dot(A, np.linalg.pinv(B))
    return H_pred


@click.command()
@click.argument("sampling_data_csv")
@click.argument("camera_pose_toml")
@click.argument("side")
@click.option("--x-origin", type=int, default=0)
@click.option("--y-origin", type=int, default=450)
def main(sampling_data_csv, camera_pose_toml, side, x_origin, y_origin):
    toml_editor = TomlEditWrapper(camera_pose_toml)
    camera_pose_orig = toml_editor.get()

    H_cam_now = matrix_from_dict(camera_pose_orig[side])
    P_ref, P_diff = matrix_from_csv(sampling_data_csv)
    H_une = compose_matrix(translate=(x_origin * 1e-3, y_origin * 1e-3, 0))
    H_cam_pred = solve(H_cam_now, H_une, P_ref, P_diff)

    camera_pose_new = make_dict(H_cam_pred)
    update_toml(camera_pose_new, toml_editor, side)


if __name__ == "__main__":
    main()
