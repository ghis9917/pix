from image import MyImage
from customtkinter import *
from panel_pixelate import PixelatePanel
from panel_bitslicing import BitSlicePanel
from constants import ON_EVENT_RESPONSE_DELAY
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps

import customtkinter
import numpy as np
import threading
import math
import time

customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("catppuccin-frappe-lavender.json") 

class ImageEditorApp:

    WINDOW_RESIZING_RATIO = 0.5

    def __init__(self, root):
        self.root = root
        self._job = None
        self.root.title("PIX")
        self.root.geometry("1000x600")

        self.root.bind("<Configure>", self.on_resize)

        self.img = None

        self.create_widgets()

    def on_resize(self, event):
        if self._job:
            self.root.after_cancel(self._job)
        
        if self.img:
            def temp():
                self.display_image()
            self._job = self.root.after(ON_EVENT_RESPONSE_DELAY, temp)

    def update_image(self, fx):
        if self.img:
            self.img.process_image(
                processing_settings=fx.effect,
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
                new_width = int(self.root.winfo_width() * self.WINDOW_RESIZING_RATIO)
                new_height = int(new_width/aspect_ratio)
        else:
            new_width = int(self.root.winfo_width() * self.WINDOW_RESIZING_RATIO)
            new_height = int(new_width/aspect_ratio)
            if new_height * 2 > self.root.winfo_height():
                aspect_ratio = new_width / new_height
                new_height = int(self.root.winfo_height() * self.WINDOW_RESIZING_RATIO)
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
        self.create_effects_tabs()
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

    def create_effects_tabs(self):
        self.tabview = customtkinter.CTkTabview(master=self.root)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.pixelate_tab = self.tabview.add("Pixelate")  # add tab at the end
        self.bitslice_tab = self.tabview.add("Bit Slice")  # add tab at the end

        self.pixelate_effect = PixelatePanel(self.root, self.pixelate_tab, self.update_image)
        self.bitslicing_effect = BitSlicePanel(self.root, self.bitslice_tab, self.update_image)

if __name__ == "__main__":
    root = CTk()
    app = ImageEditorApp(root)
    root.mainloop()