# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:41:51 2020

@author: Jeremy La Porte
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:23:36 2020

@author: Jeremy La Porte
Release 2.0
Physics engine using pyQt with a graphic view 
Move with A, D and Space
"""
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5.QtCore 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
import pyqtgraph as pg
import datetime
from PIL import Image
import sys
import numpy as np
import time
        

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.width, self.high = 1500,800
        self.setMouseTracking(True)
        self.setGeometry(50, 50, self.width, self.high)
        self.setWindowTitle('Event handler')
        self.resize(self.width+20, self.high+20)
        # self.setStyleSheet("background-color: grey;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)



        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10,10,self.width, self.high))
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,-1,-1)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.dt = 15 # Tickrate
        self.x ,self.vx = -450, 0.45*self.dt
        self.y ,self.vy =  -200, 0
        
        self.x_obj, self.vx_obj = 0, 0
        self.y_obj, self.vy_obj = -250,0

        self.largeur, self.hauteur = 16,32
        self.E_col,self.E_rebond, self.friction_x = 0.8, 0.1, 0.3
        self.E_rebond_obj = 0.5
        self.g = 0.01
        self.sol = 0.25  #pourcentage du sol sur l'ecran
        self.ciel = 1-self.sol
        self.sol_coor = self.high*(-self.sol+1/2)
        self.ciel_coor = self.high*-1/2

        self.coordList, self.tail = [], 75
        self.arr_simu = []
        self.timer3 = pg.QtCore.QTimer()
        self.timer3.timeout.connect(self.graph)
        self.timer3.start(self.dt) # refresh rate in ms

        
        self.top = QtGui.QPixmap("../../image/ciel_pix.jpg")
        self.top_size = self.top.scaled(self.width, self.high*self.ciel)
        itemTop = self.scene.addPixmap(self.top_size)
        itemTop.setPos(-self.width/2,self.ciel_coor)
    
        self.bot = QtGui.QPixmap("../../image/sol.jpg")
        self.bot_size = self.bot.scaled(self.width, self.high*self.sol)
        itemBot = self.scene.addPixmap(self.bot_size)
        itemBot.setPos(-self.width/2,self.sol_coor)
        
        self.house = QtGui.QPixmap("../../image/chale.png")
        self.house_size = self.house.scaled(150,200)
        itemHouse = self.scene.addPixmap(self.house_size)
        itemHouse.setPos(-300,self.sol_coor-200)
        
        font = QtGui.QFont('SansSerif', 12)
        font.setBold(True)
        # font.setWeight(75)
        self.FPS = QtWidgets.QLabel(self.centralwidget)
        self.FPS.setGeometry(QtCore.QRect(20,20, 161, 50))
        self.FPS.setFont(font)
        self.colision = False
        self.show()

        self.graph()
        
    def onTheGround(self):
        return abs(self.vy) <= 5**-2 and self.y <= 0.5+self.sol_coor
    def sprinting(self):
        return keyboard.is_pressed('shift')
    def jump(self):
        self.vy = -0.2*self.dt
        
    def left(self):
        self.vx = -0.2*self.dt
        if self.onTheGround() and self.sprinting():
            self.vx = -0.35/self.friction_x*self.dt
        elif self.onTheGround():
            self.vx = -0.2/self.friction_x*self.dt
    def right(self):
        self.vx = 0.2*self.dt
        if self.onTheGround() and self.sprinting():
            self.vx = 0.35/self.friction_x*self.dt
        elif self.onTheGround():
            self.vx = 0.2/self.friction_x*self.dt
    def hitBox(self):
        if self.x_obj > self.x-self.largeur/2 and self.x_obj < self.x+self.largeur/2 and self.y_obj < self.y-self.hauteur and self.y_obj > self.y:
            self.colision = True
            
        
    
    def graph(self):
        start_time = time.time()
        self.scene.clear()
        #======= Mouvements==================================
        if keyboard.is_pressed('q'):
            self.left()
        if keyboard.is_pressed('d'):
            self.right()
        if keyboard.is_pressed(' '):
            self.jump()
        
        #======= Display Pixmap Elements ===================
        itemBot = self.scene.addPixmap(self.bot_size)
        itemBot.setPos(-self.width/2,self.sol_coor)
        
        itemTop = self.scene.addPixmap(self.top_size)
        itemTop.setPos(-self.width/2,self.ciel_coor)
        
        itemHouse = self.scene.addPixmap(self.house_size)
        itemHouse.setPos(300,self.sol_coor-200)
        #======= Vitesses max ===============================
            
        if self.onTheGround():
            self.vy = 0
        if abs(self.vx) <= 10**-5 :
            self.vx = 0

        if self.x + self.vx > self.width/2: #colision droite
            self.vx *= -self.E_col #Perte d'energie de colision
            self.x += self.vx
        if self.x + self.vx < -self.width/2: #colision gauche
            self.vx *= -self.E_col #Perte d'energie de colision
            self.x += self.vx
        elif self.y + self.vy < self.sol_coor:# En l'air
            self.vy += self.g* self.dt
            self.y += self.vy
            self.x += self.vx
        elif self.onTheGround():  #Au sol
            self.vx *= self.friction_x #frotement x
            self.x += self.vx 
        else:
            self.vy *= -self.E_rebond #Perte d'energie de rebond
            self.y += self.vy 
            
        # self.scene.addRect(-500,-250,1000,500,brush = QtGui.QBrush(QtGui.QColor(255,255,255)))
        # print("v: ",self.vx,self.vy)
        self.scene.addRect(self.x+7,self.y-29, -14,-14,brush = QtGui.QBrush(QtGui.QColor(0,255,255))) #tête
        self.scene.addRect(self.x+8,self.y, -16,-28,brush = QtGui.QBrush(QtGui.QColor(0,255,255)))#corp
        
        self.scene.addRect(self.x-4,self.y-38, 2,2,brush = QtGui.QBrush(QtGui.QColor(255,255,255)))#yeux
        self.scene.addRect(self.x+2,self.y-38, 2,2,brush = QtGui.QBrush(QtGui.QColor(255,255,255)))
        
        self.scene.addEllipse(self.x_obj,self.y_obj,15,15, brush = QtGui.QBrush(QtGui.QColor(255,255,0)))
        self.coordList.append(self.x)
        self.coordList.append(self.y)
        if len(self.coordList) >= self.tail:
            self.coordList = self.coordList[2:]
        
        for coord in range(0,len(self.coordList),2): 
            self.scene.addLine(self.coordList[coord],self.coordList[coord+1],self.coordList[coord],
                               self.coordList[coord+1],QtGui.QPen(QtCore.Qt.red,coord/10))

        # for i in range(0,1000,6):
        #     self.scene.addLine(0,i,0,i,QtGui.QPen(QtCore.Qt.red,1))
        #     self.scene.addLine(i,0,i,0,QtGui.QPen(QtCore.Qt.red,1))
        #     self.scene.addLine(i,0,i,0,QtGui.QPen(QtCore.Qt.red,1))
        #     self.scene.addLine(-i,0,-i,0,QtGui.QPen(QtCore.Qt.blue,1))
        #     self.scene.addLine(0,-i,0,-i,QtGui.QPen(QtCore.Qt.blue,1))
        temps_simu = (time.time() - start_time)*1000
        if temps_simu > self.dt:
            print(round(temps_simu,4),'ms --- FPS Lost')
        if temps_simu < self.dt:
            self.FPS.setText(str(int(1000/self.dt))+ 'FPS')
        else:
            self.FPS.setText(str(int(1000/temps_simu))+ 'FPS')
        # print("%s ms" % (round(temps_simu,3)))
        print(self.vx)


        
        
if __name__ == "__main__":
    """ Show and Close the window"""
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
