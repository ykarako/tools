#!/usr/bin/env python3
"""This script concat images vertically and save as a new image.
"""
import click
from pathlib import Path
from PIL import Image
from typing import List


def concat_vertical(im1: Image, im2: Image, resample=Image.BICUBIC) -> Image:
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif im1.width > im2.width:
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)

    dst = Image.new("RGB", (_im1.width, _im1.height + _im2.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (0, _im1.height))

    return dst


def concat_horizontal(im1: Image, im2: Image, resample=Image.BICUBIC) -> Image:
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif im1.height > im2.height:
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)

    dst = Image.new("RGB", (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))

    return dst


def parse_timestamp(path: Path) -> str:
    parts = path.name.split("_")
    return f"{parts[1]}_{parts[2]}"


def load_image(paths: List[Path]) -> Image:
    if paths:
        return Image.open(paths[0])
    else:
        return Image.new("RGB", (100, 100), (0, 0, 0))


def concat_and_save(input_dir: str, output_dir: str, timestamp: str) -> str:
    paths_rgb = sorted(Path(input_dir).glob(f"evt_{timestamp}*rgb.png"))
    paths_yolo = sorted(Path(input_dir).glob(f"evt_{timestamp}*yolo.png"))
    paths_projection = sorted(Path(input_dir).glob(f"evt_{timestamp}*projection.png"))
    paths_result = sorted(Path(input_dir).glob(f"evt_{timestamp}*result.jpg"))

    image1 = concat_vertical(load_image(paths_rgb), load_image(paths_yolo))
    image2 = concat_vertical(load_image(paths_result), load_image(paths_projection))
    image_all = concat_horizontal(image1, image2)

    path_new = Path(output_dir) / f"evt_{timestamp}.png"
    image_all.save(path_new)
    return path_new


@click.command()
@click.argument("input_dir")
@click.option("--output_dir", "-o", default=".")
def main(input_dir, output_dir):
    paths_all = Path(input_dir).glob("evt*")
    timestamps = sorted(set([parse_timestamp(p) for p in paths_all]))
    n = len(timestamps)
    print(f"{n} timestamps found")

    for i, timestamp in enumerate(timestamps):
        path_new = concat_and_save(input_dir, output_dir, timestamp)
        print(f"[{i:3d}/{n:3d}] save -> {path_new}")


if __name__ == "__main__":
    main()
