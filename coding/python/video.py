#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2


class VideoInputStreamIterator:
    """
     iterator through the read video
    """
    def __init__(self, input_stream):
        self._stream = input_stream

    def __next__(self):
        return self._stream.grab_frame()


class VideoInputStream:
    """
    can be used like by :
        stream = VideoInputStream()
        stream.open(video_path)
    or more concise:
        with Video.read(video_path) as stream:
            for timestamp, frame in video_stream:
                # use frame
    """
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
        nb_frames = int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))
        # WARNING: inaccurate (based on duration and FPS)
        # so, try to see if its real
        current_position = int(self._capture.get(cv2.CAP_PROP_POS_FRAMES))
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, nb_frames+1)
        nb_frames_actual = int(self._capture.get(cv2.CAP_PROP_POS_FRAMES))
        if not nb_frames_actual == nb_frames:
            nb_frames = nb_frames_actual
        # dont forget to seek back at initial position
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, current_position)
        return nb_frames

    def __iter__(self):
        assert self._capture
        return VideoInputStreamIterator(self)

    def __enter__(self):
        # nothing to be done
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class VideoOutputStream:
    """
        with Video.read(video_path) as stream:
            for timestamp, frame in video_stream:
                # use frame
    """
    def __init__(self):
        self._recorder = None
        self._video_path = None
        self._fps = None
        self._fourcc = None
        self._size = None

    def open(self, video_path, fps=30, fourcc='avc1', size=None):
        self._video_path = video_path
        self._fps = fps
        self._fourcc = fourcc
        self._size = size
        if size is None:
            self._recorder = None
        else:
            # if size not given, postpone to first frame
            self._recorder = cv2.VideoWriter(self._video_path,  cv2.VideoWriter_fourcc(*self._fourcc), fps, size)
            if not self._recorder.isOpened():
                raise ValueError(f'unable to open video {video_path}')
        return self

    def close(self):
        self._recorder.release()

    def push_frame(self, frame):
        if self._recorder is None:
            size = tuple(frame.shape[i] for i in [1, 0])
            self.open(self._video_path, self._fps, self._fourcc, size)
        self._recorder.write(frame)

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

    @staticmethod
    def write(video_path, fps=30, fourcc='avc1', size=None):
        video_stream = VideoOutputStream()
        video_stream.open(video_path, fps, fourcc, size)
        return video_stream


# test
from tqdm import tqdm
if __name__ == '__main__':
    import urllib.request
    import os.path as path
    video_path_in = '/tmp/video_sample.mp4'
    if not path.exists(video_path_in):
        url_sample = 'https://www.sample-videos.com/video123/mp4/360/big_buck_bunny_360p_1mb.mp4'
        print(f'downloading samples ... \n\tfrom {url_sample}')
        urllib.request.urlretrieve(url_sample, video_path_in)
        print(f'done.')

    with Video.read(video_path_in) as video_stream:
        nb_read = 0
        nb_frames = len(video_stream)
        for timestamp, frame in tqdm(video_stream):
            cv2.imshow('frame', frame)
            cv2.waitKey(10)
            nb_read += 1
    assert nb_frames == nb_read

    video_stream = Video.read(video_path_in)
    nb_frames = len(video_stream)
    nb_read = 0
    for timestamp, frame in tqdm(video_stream):
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
        nb_read += 1
    video_stream.close()
    assert nb_frames == nb_read

    video_stream = VideoInputStream()
    video_stream.open(video_path_in)
    nb_frames = len(video_stream)
    nb_read = 0
    for timestamp, frame in tqdm(video_stream):
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
        nb_read += 1
    video_stream.close()
    assert nb_frames == nb_read

    video_stream = VideoInputStream()
    video_stream.open(video_path_in)
    nb_frames = len(video_stream)
    nb_read = 0
    for idx in tqdm(range(len(video_stream))):
        timestamp, frame = video_stream.grab_frame()
        cv2.imshow('frame', frame)
        cv2.waitKey(10)
        nb_read += 1
    assert nb_frames == nb_read

    video_path_out = '/tmp/frame.mp4'
    with Video.read(video_path_in) as video_in, Video.write(video_path_out, fps=30) as video_out:
        nb_frames = len(video_stream)
        nb_read = 0
        for timestamp, frame in tqdm(video_in):
            video_out.push_frame(frame)
            cv2.imshow('frame', frame)
            cv2.waitKey(10)
            nb_read += 1
    assert nb_frames == nb_read

    video_stream.close()