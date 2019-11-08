#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2


class VideoIterator:
    def __init__(self, capture):
        self._capture = capture

    def __next__(self):
        if not self._capture.isOpened():
            raise StopIteration

        success, frame = self._capture.read()
        if not success or frame is None:
            raise StopIteration
        timestamp = self._capture.get(cv2.CAP_PROP_POS_MSEC)
        return timestamp, frame


class VideoReader:
    def __init__(self, video_path):
        self._path = video_path
        self._capture = cv2.VideoCapture(video_path)
        if not self._capture.isOpened():
            raise ValueError(f'unable to open video {video_path}')

    def __del__(self):
        self._capture.release()

    def __len__(self):
        # WARNING: inaccurate (based on duration and FPS)
        return int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))

    def __iter__(self):
        return VideoIterator(self._capture)


# test
from tqdm import tqdm
if __name__ == '__main__':
    video_path = '/tmp/frames/%05d.jpg'
    reader = VideoReader(video_path)
    for timestamp, frame in tqdm(reader):
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
