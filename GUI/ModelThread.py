from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import random
import cv2
import numpy as np
from tensorflow.keras.models import Model, load_model
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


root = QFileInfo(__file__).absolutePath()

class ModelThread(QThread):
    changeData = pyqtSignal(list)

    def __init__(self,):
        super().__init__()
        self.image = None
        self.classification = [None, None]

    def run(self):
        image = cv2.imread(self.image, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, (400, 228))
        image = np.expand_dims(image, axis=0)

        model = load_model(root + "/two_class_resnet50/r-model.h5")
        model.load_weights(root + "/two_class_resnet50/checkpoints/weights-improvement-43-0.94.hdf5")

        self.classification[0] = np.argmax(model.predict(image))

        if self.classification[0] == 0:
            model = load_model(root + "/four_class_benign/ben-model.h5")
            model.load_weights(root + "/four_class_benign/checkpoints/weights-improvement-100-0.86.hdf5")
        elif self.classification[0] == 1:
            model = load_model(root + "/four_class_malignant/mal-model.h5")
            model.load_weights(root + "/four_class_malignant/checkpoints/weights-improvement-45-0.81.hdf5")
        else:
            self.classification[0] = None
            self.classification[1] = None
            self.changeData.emit(self.classification)
            return

        self.classification[1] = np.argmax(model.predict(image))

        self.changeData.emit(self.classification)