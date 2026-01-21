# import tkinter as tk
from customtkinter import *

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np
import threading
import math


class ImageEditorApp:

    BACKGROUND_COLOR = "#323232"
    COLORS = 8
    COMPRESSION_PASSES = 1
    COMPRESSION_RATE = 0.25
    BLUR = False
    BLUR_RADIUS = 10
    BORDER = False

    def __init__(self, root):
        self.root = root
        self._job = None
        self.root.title("Image editing app")
        self.root.geometry("1000x600")
        self.root.configure(bg = self.BACKGROUND_COLOR)

        self.root.bind("<Configure>", self.on_resize)

        self.image_path = None
        self.preview_original_image = None 
        self.image = None

        self.blur_switch_var = StringVar(value="on")
        self.border_switch_var = StringVar(value="on")

        self.create_widgets()

    def on_resize(self, event):
        self.display_image()

    def on_slider_change_compression_rate(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.COMPRESSION_RATE = float(value) / 100.
        self.sliderCompressionRate_label.configure(text=f"Compression Rate: {100-self.COMPRESSION_RATE*100}%")
        self._job = self.root.after(200, self.update_image)

    def on_slider_change_colors(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.COLORS = 2 ** int(value)
        self.sliderColors_label.configure(text=f"# Colors: {self.COLORS}")
        self._job = self.root.after(200, self.update_image)

    def on_slider_change_blur_radius(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.BLUR_RADIUS = int(value)
        self.sliderBlur_label.configure(text=f"Blur Radius: {self.BLUR_RADIUS}")
        self._job = self.root.after(200, self.update_image)

    def on_switch_blur(self):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.BLUR = self.blur_switch_var.get() == "on"
        self._job = self.root.after(200, self.update_image)

    def on_switch_border(self):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.BORDER = self.border_switch_var.get() == "on"
        self._job = self.root.after(200, self.update_image)

    def update_image(self):
        self.process_image(from_original=False)
        self.display_image()

    def process_image(self, from_original=False):
        if self.image:
            if from_original:
                self.image = Image.open(self.image_path)
            else:
                self.image = self.preview_original_image.copy()

            maxWidth = self.image.width
            maxHeight = self.image.height

            if self.BLUR:
                self.image = self.image.filter(ImageFilter.GaussianBlur(radius=self.BLUR_RADIUS))

            for _ in range(self.COMPRESSION_PASSES):
                new_width = int(self.image.width*self.COMPRESSION_RATE)
                new_height = int(self.image.height*self.COMPRESSION_RATE)
                self.image = self.image.resize(
                    (new_width, new_height),
                    Image.Resampling.LANCZOS
                )
                self.image = self.image.quantize(colors=self.COLORS, kmeans=3)
                self.image = self.image.convert("RGB")
                while self.image.width < maxWidth and self.image.height < maxHeight:
                    self.image = self.image.resize((self.image.width * 2, self.image.height * 2), Image.NEAREST)


            image_matrix = np.array(self.image)

            if self.BORDER:
                edge_image = self.image.convert("L")
                edge_image = edge_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                edge_image = edge_image.filter(ImageFilter.FIND_EDGES)
                edge_image = edge_image.point(lambda x: 0 if x > 0 else 255)
                edge_image = edge_image.convert("RGB")
                final_matrix_edges = np.array(edge_image)

                mask = (final_matrix_edges == [0, 0, 0])
                image_matrix[mask] = 0

            self.image = Image.fromarray(image_matrix)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *png *.bmp *.gif")])
        if file_path:
            self.image_path = file_path
            tmp = Image.open(file_path)
            self.image = ImageOps.scale(tmp.copy(), 0.25)
            self.preview_original_image = self.image.copy()
            self.display_image()

    def resize_image(self, image):

        aspect_ratio = image.width / image.height
        if aspect_ratio < 1:
            new_height = int(self.root.winfo_height() * 0.45)
            new_width = int(new_height*aspect_ratio)
        else:
            new_width = int(self.root.winfo_width() * 0.45)
            new_height = int(new_width/aspect_ratio)

        return CTkImage(image.resize((new_width, new_height), Image.LANCZOS), size=(new_width, new_height))

    def display_image(self):
        if self.image:
            self.image_label.configure(image=self.resize_image(self.image))
            self.original_image_label.configure(image=self.resize_image(self.preview_original_image))

    def apply_filter(self, filter_type):
        if self.image:
            self.image = self.image.filter(filter_type)
            self.display_image()

    def reset_image(self):
        if self.preview_original_image:
            self.image = self.preview_original_image.copy()
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")])
            if file_path:
                self.doThingOnImage(from_original=True)
                self.image.save(file_path)
                messagebox.showinfo("Success", "Imaged saved successfully!")

    def create_widgets(self):
        self.create_images()
        self.create_settings()
        self.create_buttons()

    def create_images(self):
        self.image_frame = CTkFrame(master=self.root)
        self.image_frame.pack(padx=20, pady=20, fill="x")

        self.original_image_label = CTkLabel(self.image_frame, text="")
        self.original_image_label.pack(side="left", pady=10)

        self.image_label = CTkLabel(self.image_frame, text="")
        self.image_label.pack(side="right", pady=10)

    def create_buttons(self):
        self.buttons_frame = CTkFrame(master=self.root)
        self.buttons_frame.pack(pady=20)

        self.load_button = CTkButton(self.buttons_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side="left", padx=10)

        self.reset_button = CTkButton(self.buttons_frame, text="Reset Image", command=self.reset_image)
        self.reset_button.pack(side="left", padx=10)

        self.save_button = CTkButton(self.buttons_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side="left", padx=10)

    def create_settings(self, row_padding = 5):
        self.settings_frame = CTkFrame(master=self.root)
        self.settings_frame.pack(pady=10)

        self.sliderCompressionRate_label = CTkLabel(self.settings_frame, text=f"Compression Rate: {100-self.COMPRESSION_RATE*100}%")
        self.sliderCompressionRate_label.pack(pady=row_padding)
        self.sliderCompressionRate = CTkSlider(self.settings_frame, from_=0, to=100, number_of_steps=100, width=500, orientation='horizontal', command=self.on_slider_change_compression_rate)
        self.sliderCompressionRate.pack(pady=row_padding)
        self.sliderCompressionRate.set(int(self.COMPRESSION_RATE*100))

        self.sliderColors_label = CTkLabel(self.settings_frame, text=f"# Colors: {self.COLORS}")
        self.sliderColors_label.pack(pady=row_padding)
        self.sliderColors = CTkSlider(self.settings_frame, from_=1, to=6, number_of_steps=5, width=500, orientation='horizontal', command=self.on_slider_change_colors)
        self.sliderColors.pack(pady=row_padding)
        self.sliderColors.set(int(math.log(self.COLORS, 2)))

        self.switchBlur = CTkSwitch(self.settings_frame, text="Blur", command=self.on_switch_blur, variable=self.blur_switch_var, onvalue="on", offvalue="off")
        self.switchBlur.pack(pady=row_padding)
        if self.BLUR:
            self.switchBlur.select()
        else:
            self.switchBlur.deselect()

        self.sliderBlur_label = CTkLabel(self.settings_frame, text=f"Blur Radius: {self.BLUR_RADIUS}")
        self.sliderBlur_label.pack(pady=row_padding)
        self.sliderBlur = CTkSlider(self.settings_frame, from_=1, to=50, number_of_steps=49, width=500, orientation='horizontal', command=self.on_slider_change_blur_radius)
        self.sliderBlur.pack(pady=row_padding)
        self.sliderBlur.set(self.BLUR_RADIUS)

        self.switchBorder = CTkSwitch(self.settings_frame, text="Border", command=self.on_switch_border, variable=self.border_switch_var, onvalue="on", offvalue="off")
        self.switchBorder.pack(pady=row_padding)
        if self.BORDER:
            self.switchBorder.select()
        else:
            self.switchBorder.deselect()


if __name__ == "__main__":
    root = CTk()
    app = ImageEditorApp(root)
    root.mainloop()