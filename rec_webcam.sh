#!/bin/bash -e
video="/dev/video4"
audio="1"
output="output.mp4"

ffmpeg -f alsa \
    -f v4l2 -s 640x480 -i $video \
    -c:v h264_omx -b:v 768k \
    -c:a aac \
    $output
