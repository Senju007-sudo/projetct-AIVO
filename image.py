# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 17:34:54 2020

@author: SENJU
"""

from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import cv2 
import numpy as np
import matplotlib.pyplot as plt


class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.setEnabled(True)
            MainWindow.resize(1350, 789)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            spacerItem = QtWidgets.QSpacerItem(20, 717, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(1165, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setMaximumSize(QtCore.QSize(1250, 720))
            self.label.setText("")
            self.label.setPixmap(QtGui.QPixmap("images/01972_hsbccelebrationoflight_1920x1080.jpg"))
            self.label.setScaledContents(True)
            self.label.setObjectName("label")
            self.gridLayout.addWidget(self.label, 1, 1, 1, 4)
            self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_2.setObjectName("pushButton_2")
            self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setObjectName("pushButton")
            self.horizontalLayout.addWidget(self.pushButton)
            self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
            self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton_3.setObjectName("pushButton_3")
            self.gridLayout.addWidget(self.pushButton_3, 0, 3, 1, 1)
            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
    
            self.retranslateUi(MainWindow)
            self.pushButton.clicked.connect(self.recuperer)
            self.pushButton_2.clicked.connect(self.grise)
            self.pushButton_3.clicked.connect(self.egalisationHistogrammeCouleur)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            
            self.filename = None #retenir adresse de l'image
            
            self.temp = None #affichage temporaire de l'image pour affichage 
        
            
        def recuperer(self):
            self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
            self.image = cv2.imread(self.filename)
            self.affichage(self.image)
            
        def affichage(self,image):
            self.temp = image
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame , frame.shape[1], frame.shape[0] , frame.strides[0],QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(image))
            
        def griser(self):
            image = cv2.imread(self.filename)
            b,v,r = cv2.split(image) #recuperation 3 matrice R V et B 
            
            y = 0.299*r + 0.587*v + 0.114*b #utilisation du formule de luminance Y
            
            image_grise = y.astype(np.uint8)
            
            return image_grise
        
            
        def grise(self):
            self.affichage(self.griser())
        
           
                
                    
        def egalisationHistogramme(self):
            
            self.image = self.griser()
            equ = cv2.equalizeHist(self.image)
            self.affichage(equ)
             
        def egalisationHistogrammeCouleur(self): 
            def egal(y):
                y = y.astype(np.uint8)       
                histo = np.zeros(256, int)      
                for i in range(0,image.shape[0]):       
                    for j in range(0,image.shape[1]):   
                        histo[y[i,j]] = histo[y[i,j]] + 1
                plt.plot(histo)
                # calcul l'histogramme cumulé hc
                hc = np.zeros(256, int)        
                hc[0] = histo[0]
                for i in range(1,256):
                    hc[i] = histo[i] + hc[i-1]
                
                #egalisation histogramme
                nbpixels = y.size
                hc = hc / nbpixels * 255
                plt.plot(hc)
                for i in range(0,y.shape[0]):     
                    for j in range(0,y.shape[1]):   
                        y[i,j] = hc[y[i,j]]
                return y      
            
            image = cv2.imread(self.filename)    
            #on divise l'image en 3 bandes R V B
            b,v,r = cv2.split(image)
            #on egalise l'histogramme de chaque bande
            imageR = egal(r)
            imageV = egal(v)
            imageB = egal(b)
            #on fusionne les 3 bandes pour avoir une seule image couleur
            y = cv2.merge((imageB,imageV,imageR))
            self.affichage(y)    
            
        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.pushButton_2.setText(_translate("MainWindow", "Grise"))
            self.pushButton.setText(_translate("MainWindow", "Ouvrir"))
            self.pushButton_3.setText(_translate("MainWindow", "Amelioration"))
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

