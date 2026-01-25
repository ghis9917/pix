from PIL import Image, ImageOps, ImageTk, ImageFilter
from processing import Pixelate
from customtkinter import *

class MyImage:

    def __init__(self, file_path, id=None):
        self.file_path = file_path
        self.cached = None
        self.preview = None
        self.processed = None
        self.is_processed = False
        self.last_processing = None

        self.load()

    def load(self, scale_factor = 0.35):
        self.cached = ImageOps.scale(Image.open(self.file_path), scale_factor)
        self.preview = self.cached.copy()
        self.processed = self.cached.copy()

    def save(self, destination_path):
        self.process_image(self.last_processing, from_original=True)
        self.processed.save(destination_path)

    def reset(self):
        self.processed = self.preview.copy()
        self.is_processed = False

    def resize(self, new_width, new_height):
        self.preview = self.cached.resize((new_width, new_height), Image.LANCZOS)
        if self.is_processed and self.last_processing:
            self.process_image(processing_settings=self.last_processing)
            self.processed = self.processed.resize((new_width, new_height), Image.LANCZOS)
        else:
            self.processed = self.cached.resize((new_width, new_height), Image.LANCZOS)

    def process_image(self, processing_settings, from_original=False):
        if self.processed:
            self.last_processing = processing_settings
            self.is_processed = True

            if from_original:
                self.processed = Image.open(self.file_path)
            else:
                self.processed = self.preview.copy()

            self.processed = processing_settings.apply_effect(self.processed.copy())