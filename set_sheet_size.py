import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QLineEdit,QLabel

import ezdxf
from ezdxf.math import Vec3
from ezdxf.render import forms

import ezdxf
import sys
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.pyqt import PyQtBackend, CorrespondingDXFEntity, CorrespondingDXFParentStack
from ezdxf.addons.drawing.properties import is_dark_color
from ezdxf.lldxf.const import DXFStructureError
from ezdxf.addons.drawing.qtviewer import CADGraphicsViewWithOverlay
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*


########定义返回信号给主窗口
#_signal = pyqtSignal(str)

class set_sheet_size(QDialog):

    _signal =pyqtSignal(str,str)
     #= pyqtSignal(int,str)  
    def __init__(self,parent=None):
        super(set_sheet_size, self).__init__(parent)
        self.main_layout = QVBoxLayout()
        self.text_brow = QTextBrowser()
        self.main_layout.addWidget(self.text_brow)
        self.setLayout(self.main_layout)

        self.title = '版面设置'
        self.left = 800
        self.top = 400
        self.width = 320
        self.height = 200
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # create textbox
        self.textname1=QLabel(self)
        self.textname1.setText("设置版面宽度(mm)")
        self.textname1.move(40, 30)
        #self.textname1.setFontSize(20)
        
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(160, 20)
        self.textbox1.resize(100,40)


        self.textname2=QLabel(self)
        self.textname2.setText("设置版面长度(mm)")
        self.textname2.move(40, 100)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(160,80)
        self.textbox2.resize(100,40)

        
        # Create a button in the window
        self.button = QPushButton('设置完成', self)
        self.button.move(120, 160)
        

        self.textboxValue1=0
        self.textboxValue2=0
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    def event(self, event):
        if event.type()==QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText('Help')
        return QDialog.event(self,event)
    def on_click(self):
        self.textboxValue1 = self.textbox1.text()
        self.textboxValue2 = self.textbox2.text()

        #print("函数响应挺及时宽度为",textboxValue1,'长度为',textboxValue2)
        '''QMessageBox.question(self, "Message", '设置的宽度为:' + textboxValue1+'设置的长度为:'+textboxValue2,
                             QMessageBox.Ok, QMessageBox.Ok)'''
        """打印完毕之后清空文本框"""
        #self.textbox1.setText('')
        #self.textbox2.setText('')
        print("函数响应挺及时宽度为",self.textboxValue1,'长度为',self.textboxValue2)
        self.send_sheet_data(self.textboxValue1,self.textboxValue2)
        #self.send_sheet_data(self.textboxValue2)
        # Use argument setup=True to setup the default dimension styles.

        self.close()
    #def open_template(sel):

    def send_sheet_data(self, str_data1,str_data2):
        # str_data = self.qline.text()
        print("函数响应挺及时宽度为",self.textboxValue1,'长度为',self.textboxValue2)
        print(str_data1,str_data2)
        #####这里发射信号，不得不说，这种发射机制实际上是比较麻烦的，这边负责发射，那边要负责接收。
        self._signal.emit(str_data1,str_data2)

    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("程序执行到这里")
            event.accept()
            
        else:
            event.ignore()
        



class set_nest_distance(QDialog):
    #######定义返回信号返回给主窗口
    _signal = pyqtSignal(str)
    def __init__(self,parent=None):
        super(set_nest_distance,self).__init__(parent)
        self.main_layout = QVBoxLayout()
        self.text_brow = QTextBrowser()
        self.main_layout.addWidget(self.text_brow)
        self.setLayout(self.main_layout)

        self.title = '排版间隔'
        self.left = 800
        self.top = 400
        self.width = 320
        self.height = 200
        self.initUI()
        self.textboxValue1=2


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # create textbox
        self.textname1=QLabel(self)
        self.textname1.setText("设置间隔(mm)")
        self.textname1.move(40, 30)
        #self.textname1.setFontSize(20)
        
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(160, 20)
        self.textbox1.resize(100,40)
        #self.textboxValue1=0
        # Create a button in the window
        self.button = QPushButton('设置完成', self)
        self.button.move(120, 160)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    def event(self, event):
        if event.type()==QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText('Help')
        return QDialog.event(self,event)

    def on_click(self):
        self.textboxValue1 = self.textbox1.text()
        #textboxValue2 = self.textbox2.text()

        #print("函数响应挺及时宽度为",textboxValue1,'长度为',textboxValue2)
        '''QMessageBox.question(self, "Message", '设置的宽度为:' + textboxValue1+'设置的长度为:'+textboxValue2,
                             QMessageBox.Ok, QMessageBox.Ok)'''
        """打印完毕之后清空文本框"""
        #self.textbox1.setText('')
        #self.textbox2.setText('')
        print("函数响应挺及时宽度为self.textboxValue==",self.textboxValue1,"mm")

        self.send_data(self.textboxValue1)
        #return self.textboxValue1
        #self.get_nest_distance(textboxValue1)
       # self.textboxValue1=self.get_nest_distance()
        self.close()

    def send_data(self, str_data):
        # str_data = self.qline.text()
        print(str_data)

        self._signal.emit(str_data)
    #def open_template(sel):

    def get_nest_distance(self):

        print("排版间隔设置的值为self.textboxValue1===",self.textboxValue1)

        return self.textboxValue1

    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', '确认退出？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("程序执行到这里")
            event.accept()
            
        else:
            event.ignore()




if __name__ == '__main__':
    app=QApplication(sys.argv)
    #t=set_sheet_size()
    #t.show()

    d=set_nest_distance()
    #d.show()
    print("d.textboxValue1===",d.textboxValue1)
    #d.get_nest_distance()
    sys.exit(app.exec_())

    print("d.textboxValue1===",d.textboxValue1)
    #d.get_nest_distance()