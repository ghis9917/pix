from PIL import Image, ImageOps, ImageTk, ImageFilter
import numpy as np
from processing import Pixelate

class MyImage:

    def __init__(self, file_path, id=None):
        self.file_path = file_path
        self.preview = None
        self.processed = None

        self.load()

    def load(self, scale_factor = 0.35):
        tmp = Image.open(self.file_path)
        self.preview = ImageOps.scale(tmp, scale_factor)
        self.processed = self.preview.copy()
        del tmp

    def save(self, destination_path):
        self.process_image(from_original=True)
        self.processed.save(destination_path)

    def reset(self):
        self.processed = self.preview.copy()

    def on_resize(self, window_width, window_height, ratio):
        aspect_ratio = self.preview.width / self.preview.height

        if aspect_ratio < 1:
            new_height = int(window_height * ratio)
            new_width = int(new_height*aspect_ratio)
        else:
            new_width = int(window_width * ratio)
            new_height = int(new_width/aspect_ratio)

        self.preview = self.preview.resize((new_width, new_height), Image.LANCZOS)
        self.processed = self.processed.resize((new_width, new_height), Image.LANCZOS) 

    def process_image(self, processing_settings=Pixelate(), from_original=False):
        if self.processed:
            if from_original:
                self.processed = Image.open(self.file_path)
            else:
                self.processed = self.preview.copy()

            maxWidth = self.processed.width
            maxHeight = self.processed.height

            if processing_settings.BLUR:
                self.processed = self.processed.filter(ImageFilter.GaussianBlur(radius=processing_settings.BLUR_RADIUS))

            for _ in range(processing_settings.COMPRESSION_PASSES):
                new_width = int(self.processed.width*processing_settings.COMPRESSION_RATE)
                new_height = int(self.processed.height*processing_settings.COMPRESSION_RATE)
                self.processed = self.processed.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.processed = self.processed.quantize(colors=processing_settings.COLORS_QUANTIZATION, kmeans=3)
                self.processed = self.processed.convert("RGB")
                while self.processed.width < maxWidth and self.processed.height < maxHeight:
                    self.processed = self.processed.resize((self.processed.width * 2, self.processed.height * 2), Image.NEAREST)


            image_matrix = np.array(self.processed)

            if processing_settings.BORDER:
                edge_image = self.processed.convert("L")
                edge_image = edge_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
                edge_image = edge_image.filter(ImageFilter.FIND_EDGES)
                edge_image = edge_image.point(lambda x: 0 if x > 0 else 255)
                edge_image = edge_image.convert("RGB")
                final_matrix_edges = np.array(edge_image)

                mask = (final_matrix_edges == [0, 0, 0])
                image_matrix[mask] = 0

            self.processed = Image.fromarray(image_matrix)