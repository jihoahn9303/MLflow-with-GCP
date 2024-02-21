from typing import List
from itertools import product

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix


def draw_confusion_matrix(
    true_labels: np.ndarray,
    predicted_labels: np.ndarray,
    class_names: List[str]
) -> Figure:
    labels = list(range(len(class_names)))
    conf_mat = confusion_matrix(
        true_labels,
        predicted_labels,
        labels=labels
    )
    
    plt.imshow(
        conf_mat, 
        interpolation='nearest', 
        cmap=plt.cm.get_cmap("Greens_r")
    )
    plt.colorbar()
    
    tick_marks = np.arange(len(class_names))
    plt.xticks(
        ticks=tick_marks, 
        labels=class_names,
        # rotation=90,
        fontsize=13
    )
    plt.yticks(
        ticks=tick_marks,
        labels=class_names,
        fontsize=13
    )
    
    threshold = conf_mat.max() / 2.
    
    for i, j in product(range(conf_mat.shape[0]), range(conf_mat.shape[1])):
        plt.text(
            x=j,
            y=i,
            s=format(conf_mat[i, j], 'd'),
            horizontalalignment="center",
            color="black" if conf_mat[i, j] > threshold else "white",
            fontsize=11
        )
        
    plt.title("Sentiment Analysis")
    plt.ylabel("Actual_label", fontsize=15)
    plt.xlabel("Predicted label", fontsize=15)
    plt.tight_layout()
    
    return plt.gcf()
        
    