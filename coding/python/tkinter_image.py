import argparse
import logging
import sys
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter_canvas_image import TkScatter, TkImage, CanvasImageDisplay

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class MainApplication(tk.Frame):
    def __init__(self, root):
        # gui
        self._parent = root
        self._parent.geometry("1400x600")
        self._parent.title('synchro')
        self._parent.bind("<Escape>", quit)
        super().__init__(self._parent, padx=10, pady=10)
        self._image_id = None

        frame = self
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self._canvas_image = CanvasImageDisplay(frame, background='black')
        self._canvas_image.pack(fill=tk.BOTH, expand=tk.TRUE)
        button_bar = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
        button_bar.pack(fill=tk.BOTH, expand=tk.FALSE, side=tk.LEFT)
        tk.Label(button_bar, text='actions: ').pack(side=tk.LEFT)
        tk.Button(button_bar, text="grid", command=self.grid).pack(side=tk.LEFT)
        tk.Button(button_bar, text="redraw", command=self.redraw).pack(side=tk.LEFT)

    def imshow(self, image_path):
        pil_img = Image.open(image_path)
        if self._image_id is None:
            tk_image = TkImage().from_pil(pil_img)
            self._image_id = self._canvas_image.add_drawable(tk_image)
        else:
            tk_image = self._canvas_image._drawables[self._image_id]
        tk_image.from_pil(pil_img)

    def redraw(self):
        self._canvas_image.redraw()

    def grid(self):
        width, height = self._canvas_image._drawables[self._image_id].resolution
        points = np.meshgrid(np.arange(0, width, 60), np.arange(0, height, 50))
        points = np.vstack([x.flatten() for x in points])
        plot = TkScatter(radius=2).from_numpy(points)
        self._canvas_image.add_drawable(plot)


def main():
    try:
        parser = argparse.ArgumentParser(description='Plot the GPS track in the camera frame.')
        parser.add_argument('-v', '--verbose', action='count', default=0,
                            help='verbosity level')
        parser.add_argument('-i', '--input',
                            help='input image file')

        args = parser.parse_args()

        if args.verbose:
            logger.setLevel(logging.INFO)
        if args.verbose > 1:
            logger.setLevel(logging.DEBUG)

        root = tk.Tk()
        app = MainApplication(root)
        app.imshow(args.input)
        root.mainloop()

    except Exception as e:
        logger.critical(e)
        raise


if __name__ == "__main__":
    main()
