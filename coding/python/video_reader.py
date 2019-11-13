#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2


class VideoInputStreamIterator:
    def __init__(self, capture):
        self._stream = capture

    def __next__(self):
        return self._stream.grab_frame()


class VideoInputStream:
    def __init__(self):
        self._capture = None

    def open(self, video_path):
        self._capture = cv2.VideoCapture(video_path)
        if not self._capture.isOpened():
            raise ValueError(f'unable to open video {video_path}')
        return self

    def close(self):
        self._capture.release()

    def grab_frame(self):
        if not self._capture.isOpened():
            raise StopIteration
        success, frame = self._capture.read()
        if not success:
            raise StopIteration
        timestamp = self._capture.get(cv2.CAP_PROP_POS_MSEC)
        return timestamp, frame

    def __len__(self):
        assert self._capture
        # WARNING: inaccurate (based on duration and FPS)
        return int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))

    def __iter__(self):
        assert self._capture
        return VideoInputStreamIterator(self)

    def __enter__(self):
        # nothing to be done
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Video:
    @staticmethod
    def read(video_path):
        video_stream = VideoInputStream()
        video_stream.open(video_path)
        return video_stream


# test
from tqdm import tqdm
if __name__ == '__main__':
    video_path = '/tmp/frames/%05d.jpg'
    with Video.read(video_path) as video_stream:
        for timestamp, frame in tqdm(video_stream):
            cv2.imshow('frame', frame)
            cv2.waitKey(10)

    video_stream = Video.read(video_path)
    for timestamp, frame in tqdm(video_stream):
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
    video_stream.close()

    video_stream = VideoInputStream()
    video_stream.open(video_path)
    for timestamp, frame in tqdm(video_stream):
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
    video_stream.close()

    video_stream = VideoInputStream()
    video_stream.open(video_path)
    for idx in tqdm(range(len(video_stream))):
        timestamp, frame = video_stream.grab_frame()
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
    video_stream.close()
