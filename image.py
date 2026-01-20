from PIL import Image, ImageOps, ImageTk, ImageFilter

class MyImage:

    def __init__(self, file_path, id=None):
        self.file_path = file_path
        self.original_image = Image.open(file_path)
        self.image = self.original_image.resize((int(self.original_image.width/10), int(self.original_image.height/10)), Image.Resampling.LANCZOS)
        self.id = id

    def getWidth(self):
        return self.image.size[0]

    def getHeight(self):
        return self.image.size[1]

    def resize(self, w, h):
        self.image = self.original_image.resize((w, h), Image.Resampling.LANCZOS)

    def getImage(self, rw = None, rh = None):

        if rh is not None:
            new_h = rh 
            new_w = self.original_image.size[0] 

            if rw is not None:
                new_w = rw
                return self.original_image.resize((new_w, new_h))

            return self.original_image.resize((new_w, new_h))
        
        return self.original_image


    def setId(self, id):
        self.id = id