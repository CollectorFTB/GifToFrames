import cv2
import numpy
import os
from tkinter import Tk, Button, Label, Entry, W, END
from tkinter.filedialog import askdirectory, askopenfilename
from functools import wraps
from tkinter.messagebox import showinfo
from os.path import splitext


def force_gif_ext(file_path):
    file_path, _ = splitext(file_path)
    return file_path


class GifApp:
    def __init__(self):
        self.root = Tk(className="Gif to Frames")

        Label(master=self.root, text="Where to save the frames:").grid(row=0, sticky=W)
        self._dir_entry = Entry(master=self.root)
        self._dir_entry.grid(row=0, column=1)
        Button(self.root, text="Browse...", command=self.select_dir).grid(row=0, column=2, sticky=W)

        Button(master=self.root, text="Choose Gif", command=self.create_frames).grid(row=1, column=0)

    def select_dir(self):
        self.save_dir = askdirectory(title="Gif to Frames")

    def needs_save_dir(fun):
        @wraps(fun)
        def save_dir_checked_function(self, *args, **kwargs):
            if self.save_dir != '':
                return fun(self, *args, **kwargs)
            else:
                showinfo(parent=self.root,
                         message="Please enter your save location first!")
        return save_dir_checked_function

    @property
    def save_dir(self):
        return self._dir_entry.get()

    @save_dir.setter
    def save_dir(self, value):
        self._dir_entry.delete(0, END)
        self._dir_entry.insert(0, value)

    @needs_save_dir
    def create_frames(self):
        gif_path = askopenfilename(parent=self.root, filetypes=[("Gif File", "*.gif")], title="Your Gif", initialfile="gifname.gif")
        path_no_ext, ext = splitext(gif_path)
        i = path_no_ext.rfind('/')
        gif_name = path_no_ext[i:]

        cap = cv2.VideoCapture(gif_path)
        frame, last_frame, i = [0], [1], 1
        while True:
            frame = cap.read()[1]
            if numpy.array_equal(last_frame, frame):
                break
            cv2.imwrite(self.save_dir + gif_name + str(i) + '.png', frame)
            last_frame = frame
            i += 1

        # fixes issue 1
        os.remove(self.save_dir + gif_name + str(i - 1) + '.png')
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = GifApp()
    app.run()

if __name__ == '__main__':
    main()


