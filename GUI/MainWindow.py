import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from WaitingSpinnerWidget import QtWaitingSpinner
from Classify import Classify
from ModelThread import ModelThread

root = QFileInfo(__file__).absolutePath()

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        # app.aboutToQuit.connect(lambda: self.closeApp(datetime.now()))
        self.width = width
        self.height = height
        self.setWindowTitle("Breast Cancer Classifier")
        self.setGeometry(0, 0, self.width, self.height)
        self.showMaximized()
        self.setWindowIcon(QIcon(root + "/imgs/cancer.png"))
        # backImage = QImage(root + "/imgs/back3.jpg")
        # sImage = backImage.scaled(QSize(self.width,self.height))
        # self.palette = QPalette()
        # self.palette.setBrush(10, QBrush(sImage))
        # self.setPalette(self.palette)


        self.title = QLabel('Breast Cancer Classifier')
        self.title.setStyleSheet('font-size:48px; font-weight:bold; text-align: center; color:black; border-style:none;')
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.title.setFont(QFont("Times"))


        self.cancer_logo = QLabel()
        self.cancer_logo.setFixedSize(90,110)
        self.cancer_logo_img = QPixmap(root + '/imgs/cancer.png')
        self.cancer_logo.setPixmap(self.cancer_logo_img)
        self.cancer_logo.setScaledContents(1)


        self.fast_logo = QLabel()
        self.fast_logo.setFixedSize(90,90)
        self.fast_logo_img = QPixmap(root + '/imgs/NU_Logo.png')
        self.fast_logo.setPixmap(self.fast_logo_img)
        self.fast_logo.setScaledContents(1)

        self.browse_btn = QPushButton()
        self.browse_btn.setFixedSize(80, 80)

        print("background-image:url({0}/imgs/browse-folder.png);".format(root))
        self.browse_btn.setStyleSheet("border:none;")

        self.browse_btn.setIcon(QIcon("{0}/imgs/browse-folder.png".format(root)))
        self.browse_btn.setIconSize(QSize(80, 80))
        self.browse_btn.clicked.connect(self.browse_image)

        self.classify_widget = Classify(width, height)
        self.classify_widget.setAttribute(Qt.WA_StyledBackground)

        self.model_thread = ModelThread()
        self.model_thread.changeData.connect(self.classify)

        self.initUI(self.width, self.height) # Initialize the UI


    def initUI(self, width, height):
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.cancer_logo)
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addWidget(self.fast_logo)
        self.titleLayout.setAlignment(self.fast_logo, Qt.AlignVCenter)
        self.titleWidget = QWidget()
        self.titleWidget.setLayout(self.titleLayout)
        self.titleWidget.setStyleSheet('border-style:None; border-radius:12px;')
        self.titleWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.inputImgLayout = QHBoxLayout()

        self.inputImgLayout.addWidget(self.browse_btn)
        self.inputImgLayout.setAlignment(self.browse_btn, Qt.AlignRight)
        self.inputImgWidget = QWidget()
        self.inputImgWidget.setLayout(self.inputImgLayout)
        self.inputImgWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)




        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.titleWidget)
        self.mainLayout.setAlignment(self.titleWidget, Qt.AlignTop)
        self.mainLayout.insertStretch(-1, 1)
        self.mainLayout.addWidget(self.inputImgWidget)
        self.mainLayout.setAlignment(self.inputImgWidget, Qt.AlignTop)
        self.mainLayout.insertStretch(-1, 1)
        self.mainLayout.addWidget(self.classify_widget)
        self.mainLayout.setAlignment(self.classify_widget, Qt.AlignTop)
        self.mainLayout.insertStretch(-1, 1)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)


        


    def browse_image(self):
        self.img_file, _ = QFileDialog.getOpenFileName(self, 'Select image', "", "Image files (*.jpg *.png)")
        
        if self.img_file:
            self.classify_widget.hide_results()
            self.classify_widget.loading.start()
            # self.classify_widget.classify(self.img_file)
            self.model_thread.image = self.img_file
            self.model_thread.start()
            


    @pyqtSlot(list)
    def classify(self, classification):
        self.classify_widget.classification = classification
        self.classify_widget.loading.stop()
        self.classify_widget.image_path = self.img_file
        self.classify_widget.show_results()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    V = app.desktop().screenGeometry()
    width = V.width()
    height = V.height()

    width = int(width - width*0.04)
    height = int(height - height*0.03)
    
    print(width)
    print(height)

    main = MainWindow(width, height)
    
    main.show()

    sys.exit(app.exec_())