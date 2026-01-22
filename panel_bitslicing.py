from constants import ON_EVENT_RESPONSE_DELAY
from processing import BitSplice
from customtkinter import *
import math


class BitSlicePanel:

    def __init__(self, root, update_image_callback):
        self.root = root
        self.effect = BitSplice()
        self.update_image_callback = update_image_callback
        self._job = None

        self.create_panel()

    def update_effect(self):
        self.effect.PLANE = int(self.sliderPlane.get())

    def update_labels(self):
        self.sliderPlane_label.configure(text=f"Plane: {1+self.effect.PLANE}")

    def on_setting_change(self, value=None):
        if self._job:
            self.root.after_cancel(self._job)
        
        self.update_effect()    
        self.update_labels()
        self._job = self.root.after(ON_EVENT_RESPONSE_DELAY, self.update_image_callback, self)

    def create_panel(self, row_padding = 5):
        self.settings_frame = CTkFrame(master=self.root)
        self.settings_frame.pack(pady=10)

        self.sliderPlane_label = CTkLabel(self.settings_frame, text=f"Plane: {1+self.effect.PLANE}")
        self.sliderPlane_label.pack(pady=row_padding)
        self.sliderPlane = CTkSlider(self.settings_frame, from_=0, to=7, number_of_steps=8, width=500, orientation='horizontal', command=self.on_setting_change)
        self.sliderPlane.pack(pady=row_padding)
        self.sliderPlane.set(int(self.effect.PLANE))

