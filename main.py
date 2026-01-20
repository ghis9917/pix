from PIL import Image
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from tqdm import tqdm


image = Image.open('image.png')  # Replace with your image path
original_matrix = np.array(image)

for _ in tqdm(range(200)):
    new_width = int(original_matrix.shape[1]*0.1)
    new_height = int(original_matrix.shape[0]*0.1)
    resized_image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )
    resized_matrix = np.array(resized_image) 
    image = resized_image.resize((resized_image.width * 2, resized_image.height * 2), Image.NEAREST)
    while image.size[0] < original_matrix.shape[1] and image.size[1] < original_matrix.shape[0]:
        image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

plt.imshow(image)
plt.axis('off')
plt.show()