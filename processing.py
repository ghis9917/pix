from dataclasses import dataclass
from PIL import Image, ImageOps, ImageTk, ImageFilter

import numpy as np

DEFAULT_COLORS_QUANTIZATION = 8
DEFAULT_COMPRESSION_PASSES = 1
DEFAULT_COMPRESSION_RATE = 0.25
DEFAULT_BLUR = False
DEFAULT_BLUR_RADIUS = 5
DEFAULT_BORDER = False

class Pixelate:

    def __init__(
        self, 
        COLORS_QUANTIZATION=DEFAULT_COLORS_QUANTIZATION, 
        COMPRESSION_PASSES=DEFAULT_COMPRESSION_PASSES, 
        COMPRESSION_RATE=DEFAULT_COMPRESSION_RATE,
        BLUR=DEFAULT_BLUR,
        BLUR_RADIUS=DEFAULT_BLUR_RADIUS,
        BORDER=DEFAULT_BORDER
        ):
        self.COLORS_QUANTIZATION = COLORS_QUANTIZATION
        self.COMPRESSION_PASSES = COMPRESSION_PASSES
        self.COMPRESSION_RATE = COMPRESSION_RATE
        self.BLUR = BLUR
        self.BLUR_RADIUS = BLUR_RADIUS
        self.BORDER = BORDER

    def apply_effect(self, image):
        maxWidth = image.width
        maxHeight = image.height

        if self.BLUR:
            image = image.filter(ImageFilter.GaussianBlur(radius=self.BLUR_RADIUS))

        for _ in range(self.COMPRESSION_PASSES):
            new_width = int(image.width*self.COMPRESSION_RATE)
            new_height = int(image.height*self.COMPRESSION_RATE)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            image = image.quantize(colors=self.COLORS_QUANTIZATION, kmeans=3)
            image = image.convert("RGB")
            while image.width < maxWidth and image.height < maxHeight:
                image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

        if self.BORDER:
            image_matrix = np.array(image)
            edge_image = image.convert("L")
            edge_image = edge_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            edge_image = edge_image.filter(ImageFilter.FIND_EDGES)
            edge_image = edge_image.point(lambda x: 0 if x > 0 else 255)
            edge_image = edge_image.convert("RGB")
            final_matrix_edges = np.array(edge_image)

            mask = (final_matrix_edges == [0, 0, 0])
            image_matrix[mask] = 0

            return Image.fromarray(image_matrix)

        else:
            return image