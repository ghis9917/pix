from image import MyImage
from customtkinter import *
from processing import Pixelate
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps

import customtkinter
import numpy as np
import threading
import math
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("catppuccin-frappe-lavender.json") 

class ImageEditorApp:

    RESPONSE_DELAY = 200
    WINDOW_RESIZING_RATIO = 0.5
    OVERFLOW_RESIZING_RATIO = 0.5

    # TODO: track these through a Pixelate object
    COLORS = 8
    COMPRESSION_PASSES = 1
    COMPRESSION_RATE = 0.25
    BLUR = False
    BLUR_RADIUS = 10
    BORDER = False

    def __init__(self, root):
        self.root = root
        self._job = None
        self.root.title("PIX")
        self.root.geometry("1000x600")

        self.root.bind("<Configure>", self.on_resize)

        self.img = None

        self.blur_switch_var = StringVar(value="on")
        self.border_switch_var = StringVar(value="on")

        self.create_widgets()

    def on_resize(self, event):
        if self._job:
            self.root.after_cancel(self._job)
        
        if self.img:
            def temp():
                self.display_image()
            self._job = self.root.after(self.RESPONSE_DELAY, temp)

    def on_slider_change_compression_rate(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.COMPRESSION_RATE = float(value) / 100.
        self.sliderCompressionRate_label.configure(text=f"Compression Rate: {100-self.COMPRESSION_RATE*100}%")
        self._job = self.root.after(self.RESPONSE_DELAY, self.update_image)

    def on_slider_change_colors(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.COLORS = 2 ** int(value)
        self.sliderColors_label.configure(text=f"# Colors: {self.COLORS}")
        self._job = self.root.after(self.RESPONSE_DELAY, self.update_image)

    def on_slider_change_blur_radius(self, value):
        if self._job:
            self.root.after_cancel(self._job)

        self.BLUR_RADIUS = int(value)
        self.sliderBlur_label.configure(text=f"Blur Radius: {self.BLUR_RADIUS}")
        self._job = self.root.after(self.RESPONSE_DELAY, self.update_image)

    def on_switch_blur(self):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.BLUR = self.blur_switch_var.get() == "on"
        self._job = self.root.after(self.RESPONSE_DELAY, self.update_image)

    def on_switch_border(self):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.BORDER = self.border_switch_var.get() == "on"
        self._job = self.root.after(self.RESPONSE_DELAY, self.update_image)

    def update_image(self):
        if self.img:
            self.img.process_image(
                processing_settings=Pixelate(
                    COLORS_QUANTIZATION=self.COLORS,
                    COMPRESSION_PASSES=self.COMPRESSION_PASSES,
                    COMPRESSION_RATE=self.COMPRESSION_RATE,
                    BLUR=self.BLUR,
                    BLUR_RADIUS=self.BLUR_RADIUS,
                    BORDER=self.BORDER
                ),
                from_original=False
            )
            self.display_image()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *png *.bmp *.gif")])
        if file_path:
            self.img = MyImage(file_path)
            self.display_image()

    def resize_images(self):
        aspect_ratio = self.img.preview.width / self.img.preview.height

        if aspect_ratio < 1:
            new_height = int(self.root.winfo_height() * self.WINDOW_RESIZING_RATIO)
            new_width = int(new_height*aspect_ratio)
            if new_width * 2 > self.root.winfo_width():
                aspect_ratio = new_width / new_height
                new_width = int(self.root.winfo_width() * self.OVERFLOW_RESIZING_RATIO)
                new_height = int(new_width/aspect_ratio)
        else:
            new_width = int(self.root.winfo_width() * self.WINDOW_RESIZING_RATIO)
            new_height = int(new_width/aspect_ratio)
            if new_height * 2 > self.root.winfo_height():
                aspect_ratio = new_width / new_height
                new_height = int(self.root.winfo_height() * self.OVERFLOW_RESIZING_RATIO)
                new_width = int(new_height*aspect_ratio)

        self.img.resize(new_width, new_height)

    def display_image(self):
        if self.img:
            self.resize_images()
            self.preview_image.configure(light_image=self.img.preview, size=(self.img.preview.width, self.img.preview.height))
            self.processed_image.configure(light_image=self.img.processed, size=(self.img.processed.width, self.img.processed.height))

    def reset_image(self):
        if self.img:
            self.img.reset()
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")])
            if file_path:
                self.img.save(file_path)
                messagebox.showinfo("Success", "Imaged saved successfully!")

    def create_widgets(self):
        self.create_images()
        self.create_settings()
        self.create_buttons()

    def create_images(self):
        self.image_frame = CTkFrame(master=self.root)
        self.image_frame.pack(padx=20, pady=20)

        self.preview_image = CTkImage(Image.new("RGB", (0, 0), (0, 0, 0)), size=(0, 0))
        self.preview_image_label = CTkLabel(self.image_frame, image=self.preview_image, text="")
        self.preview_image_label.pack(side="left", pady=10)

        self.processed_image = CTkImage(Image.new("RGB", (0, 0), (0, 0, 0)), size=(0, 0))
        self.processed_image_label = CTkLabel(self.image_frame, image=self.processed_image, text="")
        self.processed_image_label.pack(side="left", pady=10)

    def create_buttons(self):
        self.buttons_frame = CTkFrame(master=self.root)
        self.buttons_frame.pack(pady=20)

        self.load_button = CTkButton(self.buttons_frame, text="Load Image", text_color="black", command=self.load_image)
        self.load_button.pack(side="left", padx=10)

        self.reset_button = CTkButton(self.buttons_frame, text="Reset Image", text_color="black", command=self.reset_image)
        self.reset_button.pack(side="left", padx=10)

        self.save_button = CTkButton(self.buttons_frame, text="Save Image", text_color="black", command=self.save_image)
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