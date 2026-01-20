import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QCheckBox, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QImage
from PIL import Image
from PIL.ImageQt import ImageQt

class ImageDropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drop an image here")
        self.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # Open image with PIL
                pil_image = Image.open(file_path)
                # Convert PIL image to QImage using ImageQt
                qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, pil_image.width * 3, QImage.Format_RGB888)
                # Convert QImage to QPixmap
                pixmap = QPixmap.fromImage(qimage)
                # Set the pixmap to the label
                self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                # Optional: Store the PIL image object
                self.pil_image = pil_image  # Keep reference to avoid garbage collection
                event.accept()
            else:
                self.setText("Unsupported file type")
        else:
            self.setText("No valid file dropped")


def getSettingsLayout():
    layoutVertical = QVBoxLayout()

    checkBoxBlur = QCheckBox("Blur")
    checkBoxBlur.setCheckState(Qt.Checked)
    checkBoxBlur.stateChanged.connect(switchBlur)

    checkBoxBorder = QCheckBox("Borders")
    checkBoxBorder.setCheckState(Qt.Checked)
    checkBoxBorder.stateChanged.connect(switchBorder)

    compressionRateSlider = QSlider(Qt.Horizontal)
    compressionRateSlider.setRange(1, 100)
    compressionRateSlider.setSingleStep(1)
    compressionRateSlider.valueChanged.connect(changeCompressionRate)

    layoutVertical.addWidget(checkBoxBlur)
    layoutVertical.addWidget(checkBoxBorder)
    layoutVertical.addWidget(compressionRateSlider)

    return layoutVertical

def switchBlur(s):
    BLUR = s == Qt.Checked
    # Don't forget to call each time some sort of refresh function that changes the previewed image

def switchBorder(s):
    BORDER = s == Qt.Checked
    # Don't forget to call each time some sort of refresh function that changes the previewed image

def changeCompressionRate(v):
    COMPRESSION_RATE = v/100
    # Don't forget to call each time some sort of refresh function that changes the previewed image


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Drop with PIL")
        self.resize(500, 400)

        layoutVertical = QVBoxLayout()

        layout = QHBoxLayout()
        self.image_label_out = ImageDropLabel()
        self.image_label = ImageDropLabel()
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_label_out)

        self.settings = getSettingsLayout()

        layoutVertical.addLayout(layout)
        layoutVertical.addLayout(self.settings)
        self.setLayout(layoutVertical)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())