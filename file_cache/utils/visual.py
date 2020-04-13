import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import cv2
from PIL import Image


def np2png(img):
    """
    医疗图片, 像素值有负值
    """
    img = img - img.flatten().min()
    img = (np.maximum(img, 0) / img.flatten().max()) * 255.0
    img = img.astype(np.uint8)
    img = Image.fromarray(img)
    img = img.convert('RGB')
    return np.array(img)



def show_img_list(img_list, col=3, title_list=[]):
    row = int(np.ceil(len(img_list) / col))

    for i in range(len(title_list), len(img_list)):
        title_list.append('')

    for sn, (im, title) in enumerate(zip(img_list, title_list)):
        # print(sn)
        if sn % col == 0:
            plt.show()

            fig = plt.figure(figsize=(20, 5 * row))

            grid = iter(ImageGrid(fig, 111,  # similar to subplot(111)
                                  nrows_ncols=(1, col),  # creates 2x2 grid of axes
                                  axes_pad=0.3,  # pad between axes in inch.
                                  share_all=True,
                                  ))

        ax = next(grid)
        # Iterating over the grid returns the Axes.
        title = title or f"{sn // col}_{sn % col}"
        ax.set_title(title)
        im = np2png(np.array(im))
        im = cv2.resize(im, (256, 256))
        if im.ndim == 2:
            ax.imshow(im, cmap='gray')
        else:
            ax.imshow(im)

    plt.show()
