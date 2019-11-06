import argparse
import logging
import sys, os
import os.path as path
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


class TkDrawable:
    def __init__(self, scaling_factor=1.0, position=[0, 0]):
        self._canvas = None
        self._canvas_id = None
        self._scaling_factor = scaling_factor
        self._position = position

    @property
    def scaling_factor(self):
        return self._scaling_factor

    @scaling_factor.setter
    def scaling_factor(self, scaling_factor):
        self.set_scaling_factor(scaling_factor)

    def set_scaling_factor(self, scaling_factor):
        self._scaling_factor = scaling_factor

    def clear(self):
        if self._canvas_id is not None:
            self._canvas.delete(self._canvas_id)
        self._canvas_id = None

    def draw(self):
        raise NotImplementedError()

    def redraw(self):
        self.clear()
        self.draw()


class TkImage(TkDrawable):
    def __init__(self, scale=1.0, position=[0, 0]):
        super().__init__(scale, position)
        self._image_pil = None
        self._image_tk = None

    @property
    def apparent_size(self):
        if self._image_pil is None:
            return None
        scaled_image_size = [int(j * self.scaling_factor) for j in self._image_pil.size]
        return scaled_image_size

    def from_pil(self, image_pil):
        self._image_pil = image_pil
        self.redraw()
        return self

    def from_numpy(self, image_np):
        if not isinstance(image_np, np.ndarray):
            raise ValueError()
        """ expect numpy image """
        image = image_np[:, :, [2, 1, 0]]  # BGR -> RGB
        image = Image.fromarray(image)
        self.from_pil(image)

    def set_scaling_factor(self, scaling_factor):
        super().set_scaling_factor(scaling_factor)
        self.redraw()

    def draw(self):
        """ rasterize _image_tk at the given scale """
        try:
            if self._canvas is None:
                raise ValueError
            if self._image_pil is None:
                raise ValueError
            assert self._canvas is not None
            assert self._canvas_id is None  # must be cleared beforehand
            apparent_size = self.apparent_size
            scaled_image = self._image_pil.resize(apparent_size)
            self._image_tk = ImageTk.PhotoImage(scaled_image)
            center_position = [x // 2 for x in apparent_size]
            self._canvas_id = self._canvas.create_image(*center_position, image=self._image_tk)

        except ValueError:
            self._image_tk = None


class CanvasImageDisplay(tk.Canvas):
    MAGNIFICATION_WHEEL = 1.1
    item_count = 0

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        all(self.bind(e, self._on_wheel) for e in ['<Button-4>', '<Button-5>', '<MouseWheel>'])
        all(self.bind(e, self._on_drag) for e in ['<Button-1>', '<ButtonRelease-1>', '<B1-Motion>'])
        self.bind("<Configure>", self.on_resize)
        self._scaling_factor = 1.0
        self._drawables = {}  # list of TkDrawable

    def _on_wheel(self, event):
        if self.scaling_factor > 0.2 and (event.num == 5 or event.delta == -120):
            self.scaling_factor /= self.MAGNIFICATION_WHEEL
        elif self._scaling_factor < 8.0 and (event.num == 4 or event.delta == 120):
            self.scaling_factor *= self.MAGNIFICATION_WHEEL
        center = event.x, event.y

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

    def to_image_coord(self, pixel_coord):
        return [int(x / self._image.scale) for x in pixel_coord]

    def from_image_coord(self, image_coord):
        return [int(x * self._image.scale) for x in image_coord]

    @property
    def scaling_factor(self):
        return self._scaling_factor

    @scaling_factor.setter
    def scaling_factor(self, scaling_factor):
        magnification = scaling_factor / self._scaling_factor
        self._scaling_factor = scaling_factor
        super().scale('all', 0, 0, magnification, magnification)
        for drawable in self._drawables.values():
            drawable.scaling_factor = scaling_factor
        # self._redraw()

    def add_drawable(self, drawable):
        drawable._canvas = self
        item_id = self.item_count
        self._drawables[item_id] = drawable
        self.item_count += 1
        self._redraw(item_id)
        return item_id

    def _redraw(self, item_id='all'):
        # draw image
        logger.debug('redraw all')
        if item_id == 'all':
            for drawable in self._drawables.values():
                drawable.redraw()
        elif item_id in self._drawables:
            self._drawables[item_id].redraw()
        # pos = [x / 2 for x in self._image.size]
        # self._image_id = self.create_image(*pos, image=self._image._image_tk)
        # self.tag_lower(self._image_id)  # ensure image is always the lowest layer


class MainApplication(tk.Frame):
    def __init__(self, root):
        # gui
        self._parent = root
        self._parent.geometry("1400x600")
        self._parent.title('synchro')
        self._parent.bind("<Escape>", quit)
        super().__init__(root, padx=10, pady=10)
        self._image_id = None

        frame = self
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self._canvas_image = CanvasImageDisplay(frame, background='black')
        self._canvas_image.pack(fill=tk.BOTH, expand=tk.TRUE)
        button_bar = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
        button_bar.pack(fill=tk.BOTH, expand=tk.FALSE, side=tk.LEFT)
        tk.Label(button_bar, text='video frame: ').pack(side=tk.LEFT)
        tk.Button(button_bar, text="-100", command=self.point_origin).pack(side=tk.LEFT)

    def imshow(self, image_path):
        pil_img = Image.open(image_path)
        if self._image_id is None:
            tk_image = TkImage().from_pil(pil_img)
            self._image_id = self._canvas_image.add_drawable(tk_image)
        else:
            tk_image = self._canvas_image._drawables[self._image_id]
        tk_image.from_pil(pil_img)

    def point_origin(self):
        radius = 5
        width, height = self._canvas_image._image.size
        for y in np.linspace(0, height, 10):
            for x in np.linspace(0, width, 30):
                self._canvas_image.create_oval(x - radius, y - radius, x + radius, y + radius, fill='chartreuse')
        self._canvas_image.create_oval(-5, -5, 5, 5, fill='red')
        self._canvas_image.create_oval(95, -5, 105, 5, fill='blue')
        self._canvas_image.create_oval(-5, 95, 5, 105, fill='green')


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
        app.imshow(args.input)
        # for i in range(100):
        #     app.imshow(args.input)
        root.mainloop()

    except Exception as e:
        logger.critical(e)
        raise
        if args.debug:
            raise


if __name__ == "__main__":
    main()
