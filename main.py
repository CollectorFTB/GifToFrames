import cv2
import numpy
import os
from tkinter import Tk, Button, Label, Entry, W, END
from tkinter.filedialog import askdirectory, askopenfilename
from functools import wraps
from tkinter.messagebox import showinfo
from os import path


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
    
    @staticmethod
    def gif_iterator(gif_path):
        cap = cv2.VideoCapture(gif_path)
        not_empty = True
        while not_empty:
            not_empty,frame = cap.read()
            if not_empty:
                yield frame

    @needs_save_dir
    def create_frames(self):
        gif_path = askopenfilename(parent=self.root, filetypes=[("Gif File", "*.gif")], title="Your Gif", initialfile="gifname.gif")
        gif_name, _ = path.splitext(os.path.basename(gif_path))
        frame_iterator = self.gif_iterator(gif_path)
        for i, frame in enumerate(frame_iterator, start=1):
            cv2.imwrite(path.join(self.save_dir, gif_name + str(i) + '.png'), frame)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    app = GifApp()
    app.run()

if __name__ == '__main__':
    main()


