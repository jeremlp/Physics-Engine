# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:41:51 2020

@author: UTILISATEUR
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:23:36 2020

@author: Jeremy La Porte
Release 1.0
Physics engine using pyQt with a graphic view 
Move with A, D and Space
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtCore 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
import pyqtgraph as pg
import datetime
import sys
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Space:
            self.vy = -0.2*self.dt
        if e.key() == Qt.Key_Q:
            self.vx = -0.2*self.dt
        if e.key() == Qt.Key_D:
            self.vx = 0.2*self.dt
        if e.key() == Qt.Key_Shift:
            self.vx += 0.2*self.dt
        
        
    def initUI(self):
        self.setMouseTracking(True)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.resize(1020, 520)
        self.setStyleSheet("background-color: grey;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10,10,1000,500))
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(-0,-0,-1,-1)
        self.graphicsView.setScene(self.scene)
        self.show()
        
        self.dt = 15
        self.time = 0
        self.y = -250
        self.vy = 0
        self. x = -500
        self.vx = 0.45*self.dt
        self.coordList = []
        self.memex = 0
        self.memey = 0
        self.memex2 = 0
        self.memey2 = 0
        self.timer3 = pg.QtCore.QTimer()
        self.timer3.timeout.connect(self.graph)
        self.timer3.start(self.dt) # refresh rate in ms
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
 
        self.graph()

        
    def graph(self):
        self.scene.clear()
        if self.vx >= 1*self.dt:
            self.vx = 1*self.dt
        if self.vy >= 1*self.dt:
            self.vy = 1*self.dt
            
        if self.x + self.vx > 500: #colision droite
            self.vx *= -0.8
            self.x += self.vx
        if self.x + self.vx < -500: #colision gauche
            self.vx *= -0.8
            self.x += self.vx
            
        elif self.y + self.vy < 0:#colision sol
            self.vy += 0.01*self.dt
            self.y += self.vy
            
            self.x += self.vx

            
        elif self.vy == 0:
            self.x += 0.2*self.vx #frotement x
        else:
            self.vy *= -0.1 #frotement y
            self.y += self.vy 
            
        self.scene.addRect(-500,-250,1000,500,brush = QtGui.QBrush(QtGui.QColor(220,220,220)))
        self.scene.addRect(self.x+5,self.y,-10,-14,brush = QtGui.QBrush(QtGui.QColor(0,255,255)))
        self.coordList.append(self.x)
        self.coordList.append(self.y)
        if len(self.coordList) >= 50:
            self.coordList = self.coordList[2:]
        
        for coord in range(0,len(self.coordList),2): 
            self.scene.addLine(self.coordList[coord],self.coordList[coord+1],self.coordList[coord],self.coordList[coord+1],QtGui.QPen(QtCore.Qt.red,2))

        for i in range(0,1000,6):
            self.scene.addLine(0,i,0,i,QtGui.QPen(QtCore.Qt.red,1))
            self.scene.addLine(i,0,i,0,QtGui.QPen(QtCore.Qt.red,1))
            self.scene.addLine(i,0,i,0,QtGui.QPen(QtCore.Qt.red,1))
            self.scene.addLine(-i,0,-i,0,QtGui.QPen(QtCore.Qt.blue,1))
            self.scene.addLine(0,-i,0,-i,QtGui.QPen(QtCore.Qt.blue,1))
            

        
        
if __name__ == "__main__":
    """ Show and Close the window"""
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())