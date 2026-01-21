from dataclasses import dataclass

@dataclass
class Pixelate:
    COLORS_QUANTIZATION = 8
    COMPRESSION_PASSES = 1
    COMPRESSION_RATE = 0.25
    BLUR = False
    BLUR_RADIUS = 10
    BORDER = False