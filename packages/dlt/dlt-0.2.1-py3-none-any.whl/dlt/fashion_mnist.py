"""
Module to load the Fashion MNIST database of handwritten digits
See http://yann.lecun.com/exdb/mnist/

The images are 28x28 pixels (grayscale) showing a single handwritten digit from
0 to 9. The dataset contains 60000 training and 10000 test images.
"""

import numpy as np
from keras.datasets import fashion_mnist

from dlt.utils import Dataset

Fashion_mnist_labels = np.array([
    "T-short/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
])


def load_data():
    """Load the Fashion-MNIST dataset.

    Returns:
        Dataset: Fashion-MNIST data
        (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
    """

    print("Downloading Fashion-MNIST dataset")
    (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

    data = Dataset()
    data.train_images = X_train
    data.train_labels = y_train
    data.test_images = X_test
    data.test_labels = y_test
    data.classes = Fashion_mnist_labels
    return data
