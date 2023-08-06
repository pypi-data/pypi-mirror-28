"""
Common tools
"""

import itertools
import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix


class Dataset():
    """Simple dataset container
    """

    def __init__(self, **kwds):
        """Summary

        Args:
            **kwds:
        """
        self.__dict__.update(kwds)

    def plot_examples(self, num_examples=5, fname=None):
        """Plot examples from the dataset

        Args:
            num_examples (int, optional): number of examples to
            fname (str, optional): filename for saving the plot
        """
        plot_examples(self, num_examples, fname)


def plot_image(x, ax=None):
    """Plot an image X.

    Args:
        x (2D array): image, grayscale or RGB
        ax (None, optional): Description
    """
    if ax is None:
        ax = plt.gca()

    if (x.ndim == 2) or (x.shape[-1] == 1):
        ax.imshow(x.astype('uint8'), origin='upper', cmap=plt.cm.Greys)
    else:
        ax.imshow(x.astype('uint8'), origin='upper')

    ax.set(xticks=[], yticks=[])


def plot_examples(data, num_examples=5, fname=None):
    """Plot the first examples for each class in given Dataset.

    Args:
        data (Dataset): a dataset
        num_examples (int, optional): number of examples to plot for each class
        fname (str, optional): filename for saving the plot
    """

    n = len(data.classes)
    fig, axes = plt.subplots(num_examples, n, figsize=(n, num_examples))

    for l in range(n):
        axes[0, l].set_title(data.classes[l], fontsize='smaller')
        images = data.train_images[np.where(data.train_labels == l)[0]]
        for i in range(num_examples):
            plot_image(images[i], axes[i, l])

    save_fig(fig, fname)


def plot_prediction(Yp, X, y, classes=None, top_n=False, fname=None):
    """Plot an image along with all or the top_n predictions.

    Args:
        Yp (1D array): predicted probabilities for each class
        X (2D array): image
        y (integer): true class label
        classes (1D array, optional): class names
        top_n (int, optional): number of top predictions to show
        fname (str, optional): filename for saving the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3.2))
    plt.subplots_adjust(left=0.02, right=0.98,
                        bottom=0.15, top=0.98, wspace=0.02)
    plot_image(X, ax1)

    if top_n:
        n = top_n
        s = np.argsort(Yp)[-top_n:]
    else:
        n = len(Yp)
        s = np.arange(n)[::-1]

    patches = ax2.barh(np.arange(n), Yp[s], align='center')
    ax2.set(xlim=(0, 1), xlabel='Probability', yticks=[])

    for iy, patch in zip(s, patches):
        if iy == y:
            patch.set_facecolor('C1')  # color correct patch

    if classes is None:
        classes = np.arange(0, np.size(Yp))

    for i in range(n):
        ax2.text(0.05, i, classes[s][i], ha='left', va='center')

    save_fig(fig, fname)


def plot_confusion_matrix(test_labels, y_pred, classes,
                          title='Confusion matrix',
                          fname='confusion_matrix'):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.

    The original code was developed by scikit-learn.
    """
    cm = confusion_matrix(test_labels, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100

    fig = plt.figure(figsize=(9, 9))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.YlGnBu)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], '.2f'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    # plt.tight_layout()
    plt.ylabel('True label (%)')
    plt.xlabel('Predicted label (%)')

    save_fig(fig, fname)


def plot_loss_and_accuracy(fit, fname='loss_acc_graph.png'):
    """Plot loss function value and accuracy graph

    Args:
        fit: instance of model.fit)
        fname: output path
    return: loss and accuracy plot graph
    """
    fig, (axL, axR) = plt.subplots(ncols=2, figsize=(10, 4))


    # Plot the loss in the history
    axL.plot(fit.history['loss'], label="loss for training")
    if fit.history['val_loss'] is not None:
        axL.plot(fit.history['val_loss'], label="loss for validation")
    axL.set_title('model loss')
    axL.set_xlabel('epoch')
    axL.set_ylabel('loss')
    axL.legend(loc='upper right')

    # Plot the loss in the history
    axR.plot(fit.history['acc'], label="loss for training")
    if fit.history['val_acc'] is not None:
        axR.plot(fit.history['val_acc'], label="loss for validation")
    axR.set_title('model accuracy')
    axR.set_xlabel('epoch')
    axR.set_ylabel('accuracy')
    axR.legend(loc='upper right')

    save_fig(fig, fname)


def save_fig(fig, fname='./'):
    fdir = os.path.dirname(fname)
    if not os.path.exists(fdir):
        os.makedirs(fdir, exist_ok=True)
    fig.savefig(fname, bbox_inches='tight')

    plt.close()
