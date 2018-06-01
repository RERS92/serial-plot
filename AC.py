# -*- coding: utf-8 -*-
"""

@author: RERS
"""

import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import sys
#sys.path.insert(0, u'/…/…/…/python2.7/site-packages')
import pyqtgraph as pg
import serial
import serial.tools.list_ports

class MainWindow(QtGui.QWidget):
    def __init__(self,):
        super(MainWindow,self).__init__()
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        self.btnConect = QtGui.QPushButton("Connect")
        self.btnConect.clicked.connect(self.conect)
        self.btnDconect = QtGui.QPushButton("Disconnect")
        self.btnDconect.clicked.connect(self.dconect)
        self.btnStartRecord = QtGui.QPushButton("Record")
        self.btnStartRecord.clicked.connect(self.startrecord)
        self.btnStopRecord = QtGui.QPushButton("Stop Rec.")
        self.btnStopRecord.clicked.connect(self.stoprecord)   
        self.btnStopRecord.setEnabled(False)
        self.recording = 0
        self.btnDconect.setEnabled(False);
        self.btnSalir = QtGui.QPushButton("Salir")
        self.cb = QtGui.QComboBox();
        self.cb_baud = QtGui.QComboBox();
        self.btnSalir.clicked.connect(self.salir)
        self.textbox = QtGui.QLineEdit()
        self.textbox.setFixedWidth(100)
        #self.textbox.setAlignment(QtCore.Qt.AlignVCenter)
        self.textbox.setText("data.txt")

        layout.addWidget(self.cb,0,0)
        layout.addWidget(self.cb_baud,1,0)
        layout.addWidget(self.btnConect,2,0)
        layout.addWidget(self.btnDconect,3,0)
        layout.addWidget(self.textbox,4,0)
        layout.addWidget(self.btnStartRecord,5,0)
        layout.addWidget(self.btnStopRecord,6,0)
        layout.addWidget(self.btnSalir,7,0)
        self.cb_baud.addItem("9600")
        self.cb_baud.addItem("19200")
        self.cb_baud.addItem("38400")
        self.cb_baud.addItem("57600")
        self.cb_baud.addItem("74880")
        self.cb_baud.addItem("115200")
        self.cb_baud.addItem("230400")
        self.cb_baud.addItem("250000")
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.cb.addItem(p[0])
        self.timer=QtCore.QTimer(self)
        self.p = pg.PlotWidget(background=QtGui.QColor(0,0,0))
        pg.setConfigOptions(antialias=True)
        self.p.setYRange(0,1024)#16777216)
        self.p.setLabel('bottom', 'Index', units='s')
        layout.addWidget(self.p,0,1,9,1)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.updateGraph)
        self.width = 200*1
        self.xdata = [0]*self.width
        self.ydata = [0]*self.width
        self.zdata = [0]*self.width
        self.curve1 = pg.PlotCurveItem(self.xdata, pen=pg.mkPen('r', width = 3), name='X')
        #self.curve2 = pg.PlotCurveItem(self.ydata, pen='r', name='Y')
        #self.curve3 = pg.PlotCurveItem(self.zdata, pen='g', name='Z')
        self.p.addItem(self.curve1)
        #self.p.addItem(self.curve2)
        #self.p.addItem(self.curve3)
        self.xmin = 0
        self.xmax = 99

    def conect(self):
        self.s = serial.Serial(str(self.cb.currentText()), int(self.cb_baud.currentText()))
        self.timer.start()
        self.btnConect.setEnabled(False);
        self.btnDconect.setEnabled(True);
        
    def dconect(self):
        try:
            self.s.close()            
            self.timer.stop()
            self.btnConect.setEnabled(True);
            self.btnDconect.setEnabled(False);
        except:
            pass        
    
    def startrecord(self):
        self.recording = 1
        self.file = open(self.textbox.text(), "w")
        self.btnStopRecord.setEnabled(True)
        self.btnStartRecord.setEnabled(False)

    def stoprecord(self):
        self.recording = 0
        self.file.close()
        self.btnStopRecord.setEnabled(False)
        self.btnStartRecord.setEnabled(True)

    def salir(self):
        try:
            self.s.close()
        except:
            pass
        try:
            self.recording = 0
            self.file.close()
        except:
            pass
        try:         
            self.timer.stop()
        except:
            pass
        QtCore.QCoreApplication.instance().quit()


    def shift(self,array,n,keep=True):
        if n>0:
            return [array[0]]*n + array[0:-n]
        else:
            n= -n
            return array[n:] + [array[-1]]*n

    def updateGraph(self):
        while self.s.inWaiting():
            A = self.s.readline()
            #aplt = map(float, A.split("\r\n"))
            x = int(A)
           # y = aplt[1]
            #z = aplt[2]
            self.xdata[-1] = x
            #self.ydata[-1] = y
            #self.zdata[-1] = z
            self.curve1.setData(self.xdata)
           # self.curve2.setData(self.ydata)
            #self.curve3.setData(self.zdata)
            self.xmin += 1
            self.xmax += 1
            self.xdata = self.shift(self.xdata,-1)
            #self.ydata = self.shift(self.ydata,-1)
           #self.zdata = self.shift(self.zdata,-1)
            if(self.recording):
                self.file.write(str(x))
                #self.file.write("\t")
               # self.file.write(str(y))
                #self.file.write("\t")
                #self.file.write(str(z))
                self.file.write("\n")

def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(800, 600)
   #mw.showFullScreen()
    mw.setWindowTitle('Serial-Plot')
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()