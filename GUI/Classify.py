from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from WaitingSpinnerWidget import QtWaitingSpinner

root = QFileInfo(__file__).absolutePath()

class Classify(QWidget):

    def __init__(self, width, height):
        QWidget.__init__(self)

        self.setFixedSize(width+width*0.042, height*0.78)

        self.image_path = ""
        self.classification = [None, None]
        self.result = ["", ""]

        self.image = QLabel()
        self.pixmap = QPixmap(self.image_path)
        self.image.setPixmap(self.pixmap)
        self.image.setHidden(True)

        # Optional, resize window to image size
        # self.resize(self.pixmap.width(),self.pixmap.height())


        self.cancer_label = QLabel(self.result[0])
        self.cancer_label.setAlignment(Qt.AlignCenter)
        self.cancer_label.setStyleSheet("font-size:100px;")
        self.cancer_label.setHidden(True)

        self.cancer_type = QLabel(self.result[1])
        self.cancer_type.setAlignment(Qt.AlignCenter)
        self.cancer_type.setStyleSheet("font-size:80px;")
        self.cancer_type.setHidden(True)


        self.result_layout = QVBoxLayout()
        self.result_layout.addWidget(self.cancer_label)
        self.result_layout.setSpacing(50)
        self.result_layout.addWidget(self.cancer_type)
        self.result_layout.setAlignment(Qt.AlignHCenter)
        self.result_widget = QWidget()
        self.result_widget.setLayout(self.result_layout)

        self.all_layout = QHBoxLayout()
        self.all_layout.addWidget(self.image)
        self.all_layout.addWidget(self.result_widget)
        self.all_widget = QWidget()
        self.all_widget.setLayout(self.all_layout)

        self.loading = QtWaitingSpinner()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.loading)
        self.layout.addWidget(self.all_widget)
        self.setLayout(self.layout)


    # def classify(self, image):

    #     self.loading.start()


    #     self.image_path = image
    #     image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    #     image = cv2.resize(image, (400, 228))
    #     image = np.expand_dims(image, axis=0)

    #     model = load_model(root + "/two_class_resnet50/r-model.h5")
    #     model.load_weights(root + "/two_class_resnet50/checkpoints/weights-improvement-43-0.94.hdf5")

    #     self.classification[0] = np.argmax(model.predict(image))

    #     if self.classification[0] == 0:
    #         model = load_model(root + "/four_class_benign/ben-model.h5")
    #         model.load_weights(root + "/four_class_benign/checkpoints/weights-improvement-100-0.86.hdf5")
    #     elif self.classification[0] == 1:
    #         model = load_model(root + "/four_class_malignant/mal-model.h5")
    #         model.load_weights(root + "/four_class_malignant/checkpoints/weights-improvement-45-0.81.hdf5")
    #     else:
    #         self.classification[1] = None
    #         return

    #     self.classification[1] = np.argmax(model.predict(image))

        



    def get_image(self, image_path):
        self.image_path = image_path


    def show_results(self):
        if self.classification[0] == 0:
            self.result[0] = "Benign"
            cancer_label_color = QGraphicsColorizeEffect()
            cancer_label_color.setColor(Qt.darkGreen)
            cancer_type_color = QGraphicsColorizeEffect()
            cancer_type_color.setColor(Qt.darkGreen)
            self.cancer_label.setGraphicsEffect(cancer_label_color)
            self.cancer_type.setGraphicsEffect(cancer_type_color)
            if self.classification[1] == 0:
                self.result[1] = "Adenosis"
            elif self.classification[1] == 1:
                self.result[1] = "Fibroadenoma"
            elif self.classification[1] == 2:
                self.result[1] = "Phyllodes Tumor"
            elif self.classification[1] == 3:
                self.result[1] = "Tubular Adenoma"
            else:
                self.result[1] = "Undefined"

        elif self.classification[0] == 1:
            self.result[0] = "Malignant"
            cancer_label_color = QGraphicsColorizeEffect()
            cancer_label_color.setColor(Qt.red)
            cancer_type_color = QGraphicsColorizeEffect()
            cancer_type_color.setColor(Qt.red)
            self.cancer_label.setGraphicsEffect(cancer_label_color)
            self.cancer_type.setGraphicsEffect(cancer_type_color)
            if self.classification[1] == 0:
                self.result[1] = "Ductal Carcinoma"
            elif self.classification[1] == 1:
                self.result[1] = "Lobular Carcinoma"
            elif self.classification[1] == 2:
                self.result[1] = "Mucinous Carcinoma"
            elif self.classification[1] == 3:
                self.result[1] = "Papillary Carcinoma"
            else:
                self.result[1] = "Undefined"
        else:
            self.result[0] = "Undefined"
            self.result[1] = "Undefined"
            
        self.pixmap = QPixmap(self.image_path)
        self.image.setPixmap(self.pixmap)
        
        self.cancer_label.setText(self.result[0])
        self.cancer_type.setText(self.result[1])

        self.image.setHidden(False)
        self.cancer_label.setHidden(False)
        self.cancer_type.setHidden(False)

        self.loading.stop()


    def hide_results(self):
        self.image.setHidden(True)
        self.cancer_label.setHidden(True)
        self.cancer_type.setHidden(True)


    

        