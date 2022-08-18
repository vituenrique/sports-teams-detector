import numpy as np
import mahotas as mh

def edginess_sobel(image):
    edges = mh.sobel(image, just_filter=True)
    edges = edges.ravel()
    return np.sqrt(np.dot(edges, edges))

def features(im):
    im = im.astype(np.uint8)
    return mh.features.haralick(im).ravel()

def histogram(im):

    # Downsample pixel values:
    im = im // 64

    # Separate RGB channels:
    r,g,b = im.transpose((2,0,1))

    pixels = 1 * r + 4 * g + 16 * b
    hist = np.bincount(pixels.ravel(), minlength=64)
    hist = hist.astype(float)
    return np.log1p(hist)
