from constants import ON_EVENT_RESPONSE_DELAY
from processing import Pixelate
from customtkinter import *
import math


class PixelatePanel:

    def __init__(self, root, master, update_image_callback):
        self.root = root
        self.master = master
        self.effect = Pixelate()
        self.update_image_callback = update_image_callback
        self._job = None

        self.blur_switch_var = StringVar(value="on")
        self.border_switch_var = StringVar(value="on")

        self.create_panel()

    def update_effect(self):
        self.effect.COMPRESSION_RATE = float(self.sliderCompressionRate.get()) / 100.
        self.effect.COLORS_QUANTIZATION = 2 ** int(self.sliderColors.get())
        self.effect.BLUR_RADIUS = int(self.sliderBlur.get())
        self.effect.BLUR = self.blur_switch_var.get() == "on"
        self.effect.BORDER = self.border_switch_var.get() == "on"

    def update_labels(self):
        self.sliderCompressionRate_label.configure(text=f"Compression Rate: {100-self.effect.COMPRESSION_RATE*100}%")
        self.sliderColors_label.configure(text=f"# Colors: {self.effect.COLORS_QUANTIZATION}")
        self.sliderBlur_label.configure(text=f"Blur Radius: {self.effect.BLUR_RADIUS}")

    def on_setting_change(self, value=None):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.update_effect()    
        self.update_labels()
        self._job = self.root.after(ON_EVENT_RESPONSE_DELAY, self.update_image_callback, self)
    
    def create_panel(self, row_padding = 5):
        self.settings_frame = CTkFrame(master=self.master)
        self.settings_frame.pack(pady=10)

        self.sliderCompressionRate_label = CTkLabel(self.settings_frame, text=f"Compression Rate: {100-self.effect.COMPRESSION_RATE*100}%")
        self.sliderCompressionRate_label.pack(pady=row_padding, anchor="w")
        self.sliderCompressionRate = CTkSlider(self.settings_frame, from_=0, to=100, number_of_steps=100, width=500, orientation='horizontal', command=self.on_setting_change)
        self.sliderCompressionRate.pack(pady=row_padding, anchor="w")
        self.sliderCompressionRate.set(int(self.effect.COMPRESSION_RATE*100))

        self.sliderColors_label = CTkLabel(self.settings_frame, text=f"# Colors: {self.effect.COLORS_QUANTIZATION}")
        self.sliderColors_label.pack(pady=row_padding, anchor="w")
        self.sliderColors = CTkSlider(self.settings_frame, from_=1, to=6, number_of_steps=5, width=500, orientation='horizontal', command=self.on_setting_change)
        self.sliderColors.pack(pady=row_padding, anchor="w")
        self.sliderColors.set(int(math.log(self.effect.COLORS_QUANTIZATION, 2)))

        self.switchBlur = CTkSwitch(self.settings_frame, text="Blur", command=self.on_setting_change, variable=self.blur_switch_var, onvalue="on", offvalue="off")
        self.switchBlur.pack(pady=row_padding, anchor="w")
        if self.effect.BLUR:
            self.switchBlur.select()
        else:
            self.switchBlur.deselect()

        self.sliderBlur_label = CTkLabel(self.settings_frame, text=f"Blur Radius: {self.effect.BLUR_RADIUS}")
        self.sliderBlur_label.pack(pady=row_padding, anchor="w")
        self.sliderBlur = CTkSlider(self.settings_frame, from_=1, to=50, number_of_steps=49, width=500, orientation='horizontal', command=self.on_setting_change)
        self.sliderBlur.pack(pady=row_padding, anchor="w")
        self.sliderBlur.set(self.effect.BLUR_RADIUS)

        self.switchBorder = CTkSwitch(self.settings_frame, text="Border", command=self.on_setting_change, variable=self.border_switch_var, onvalue="on", offvalue="off")
        self.switchBorder.pack(pady=row_padding, anchor="w")
        if self.effect.BORDER:
            self.switchBorder.select()
        else:
            self.switchBorder.deselect()

