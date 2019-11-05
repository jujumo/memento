import argparse
import logging
import sys, os
import os.path as path
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class CanvasImageData:
    def __init__(self):
        self._image_pil = None
        self._image_tk = None
        self._scale = 1.0

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self.rasterize()

    @property
    def size(self):
        assert self._image_pil is not None
        scaled_image_size = (int(j * self._scale) for j in self._image_pil.size)
        return scaled_image_size

    def set_image(self, image_pil):
        self._image_pil = image_pil
        self.rasterize()

    def rasterize(self):
        # ...and then to ImageTk format
        scaled_image = self._image_pil.resize(self.size)
        self._image_tk = ImageTk.PhotoImage(scaled_image)


class CanvasImageDisplay(tk.Canvas):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        all(self.bind(e, self._on_wheel) for e in ['<Button-4>', '<Button-5>', '<MouseWheel>'])
        all(self.bind(e, self._on_drag) for e in ['<Button-1>', '<ButtonRelease-1>', '<B1-Motion>'])
        self.bind("<Configure>", self.on_resize)
        self._image = CanvasImageData()
        self._image_id = None

    def _on_wheel(self, event):
        MAG_INCREMENT = 0.1
        scale = self._image.scale
        if scale > 0.5 and (event.num == 5 or event.delta == -120):
            magnification = 1 - MAG_INCREMENT
        elif scale < 2.0 and (event.num == 4 or event.delta == 120):
            magnification = 1 + MAG_INCREMENT
        else:
            magnification = 1.
        self.scale(magnification)

    def _on_drag(self, event):
        if tk.EventType.ButtonPress == event.type:
            # self._viewport['drag_from'] = np.array([event.x, event.y])
            self.scan_mark(event.x, event.y)
        elif tk.EventType.ButtonRelease == event.type:
            pass
        elif tk.EventType.Motion == event.type:
            self.scan_dragto(event.x, event.y, gain=1)

    def on_resize(self, event):
        pass

    def scale(self, magnification):
        new_scale = magnification * self._image.scale
        self._image.scale = new_scale
        super().scale('all', 0, 0, magnification, magnification)
        self._redraw()

    def set_image_numpy(self, image_np):
        if not isinstance(image_np, np.ndarray):
            raise ValueError()
        """ expect numpy image """
        image = image_np[:, :, [2, 1, 0]]  # BGR -> RGB
        image = Image.fromarray(image)
        self.set_image_pil(image)

    def set_image_pil(self, image_pil):
        self._image.set_image(image_pil)
        self._redraw()

    def fit_image(self):
        pass

    def _redraw(self):
        # draw image
        logger.debug('redraw all')
        if self._image_id is not None:
            self.delete(self._image_id)
            self._image_id = None

        pos = [x / 2 for x in self._image.size]
        self._image_id = self.create_image(*pos, image=self._image._image_tk)
        self.tag_lower(self._image_id)


class MainApplication(tk.Frame):
    def __init__(self, root):
        # gui
        self._parent = root
        self._parent.geometry("1400x600")
        self._parent.title('synchro')
        self._parent.bind("<Escape>", quit)
        super().__init__(root, padx=10, pady=10)

        frame = self
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self._canvas_image = CanvasImageDisplay(frame, background='black')
        self._canvas_image.pack(fill=tk.BOTH, expand=tk.TRUE)

    def load_image(self, image_path):
        img = Image.open(image_path)
        self._canvas_image.set_image_pil(img)
        width, height = self._canvas_image._image.size
        for y in np.linspace(0, height, 50):
            for x in np.linspace(0, width, 50):
                self._canvas_image.create_oval(x - 2, y - 2, x + 2, y + 2, fill='chartreuse')


def main():
    try:
        parser = argparse.ArgumentParser(description='Plot the GPS track in the camera frame.')
        parser.add_argument('-v', '--verbose', action='count', default=0,
                            help='verbosity level')
        parser.add_argument('-d', '--debug', action='store_true', default=False,
                            help='raise exceptions')
        parser.add_argument('-i', '--input',
                            help='input video file')

        args = parser.parse_args()

        if args.verbose:
            logger.setLevel(logging.INFO)
        if args.verbose > 1:
            logger.setLevel(logging.DEBUG)

        root = tk.Tk()
        app = MainApplication(root)
        app.load_image(args.input)
        root.mainloop()

    except Exception as e:
        logger.critical(e)
        raise
        if args.debug:
            raise


if __name__ == "__main__":
    main()
