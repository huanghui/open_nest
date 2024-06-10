# -*- coding: utf-8 -*-
from pickle import NONE
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


import os
#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#import sip

import cv2
import matplotlib.pyplot as plt
from PIL import Image

from plt_reader import*

#class cadWindow(QtWidgets.QMainWindow):
class cadViewer(QWidget):
    def __init__(self, parent=None):
        super(cadViewer, self).__init__(parent)

        self.setWindowTitle('cadViewer')
        self.setGeometry(400,500,1000,500)
        #全局布局（2中）：这里选择水平布局

        ##########重新设计布局，因为不是centralwidget,但后期可以考虑将这个设计为centralwidget
        self.wlayout=QHBoxLayout()
        self.setLayout(self.wlayout)
        self.left_layout=QVBoxLayout()
        self.model_name=''

        self.resize(1000, 500)

        self.render_params = {'linetype_renderer': 'ezdxf'}
        #self.selectedInfo = SelectedInfo(self)
        self.layers = new_layers(self)
        #self.logView = LogView(self)
        self.logView =new_log_view(self)
        self.statusLabel = QtWidgets.QLabel()
        self.view = CADGraphicsViewWithOverlay()
        self.view.setScene(QtWidgets.QGraphicsScene())
        self.view.scale(1, -1)

        self.number_for_nest=0
        self.wlayout.addWidget(self.view)
        
       #self.pop_for_nest()
        #self.wlayout.addWidget(QLabel(str(1)))

        '''self.setContextMenuPolicy(Qt.ActionsContextMenu) #Qt 
        # 直接把action加到自身上
        self.quitAction = QAction("排版", self)
        self.quitAction.triggered.connect(qApp.quit)
        self.addAction(self.quitAction)'''
        #self.
        '''self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.layers)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.selectedInfo)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.logView)'''

        '''self.wlayout.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.layers)
        self.wlayout.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.selectedInfo)
        self.wlayout.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.logView)'''


        '''self.open_file_action = QtWidgets.QAction('Open files')
        self.open_file_action.triggered.connect(self.open_file)
        #self.menuBar().addAction(self.open_file_action)
        self.select_layout_menu = self.menuBar().addMenu('Select Layout')
        self.statusBar().addPermanentWidget(self.statusLabel)

        self.view.element_selected.connect(self.selectedInfo.set_elements)
        self.view.mouse_moved.connect(self._on_mouse_moved)
        self.layers.updated_signal.connect( lambda : self.draw_layout(self.current_layout) )'''
    def pop_for_nest(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu) #Qt 
        # 直接把action加到自身上
        self.quitAction = QAction("排版", self)
       # if(self.dxf is not NONE):
        #self.nameAction=QAction("模型的名字",self)
        self.quitAction.triggered.connect(self.get_linedit_number)
        print("弹出对话框，多写点东西进来，其实其他的很多指标要加进来。")        
        self.addAction(self.quitAction)

    
    def add_linedit_widget(self):
        self.linedit=QLineEdit()
        self.linedit.setFixedWidth(30)
        #lineEdit=QLineEdit()
        #self.lineEdit.setValidator(QIntValidator())

        self.wlayout.addWidget(self.linedit)

        return self.linedit
        #self.number_for_nest=self.linedit.text()
       # return self.number_for_nest
    


    def get_linedit_number(self):
        try:
            print("获取排版数量为",self.linedit.text())
            print("需要排版的模型名字为",self.model_name)
            return self.linedit.text()
            
        except:
            print("没有东西可以获取")


    def open_file(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'CAD files (*.dxf *.DXF *.plt)')
        if filename == '':
            return
        #print("小日本的东西写得成不？")
        print(filename)
        #self.model_name=filename
        
        if(os.path.splitext(filename)[-1]==".plt"):
            #self.dxf = ezdxf.readfile(filename)
            #img2 = plt.imread(filename)
            #plt.imshow(img2)
            print("这个文件是.plt文件",filename)

            array_list,maax_x,max_y,array_lines=parse_plt(filename)
            plt_convert_name=filename+".dxf"
            plt_to_dxf(array_lines,plt_convert_name)
    #plt_to_dxf_one_line(array_lines,"ts9.dxf")
            print("执行结束，看看能不能打开，并提取模型？")
            
            self.dxf = ezdxf.readfile(plt_convert_name)
            
            #print("小日本的东西写得成不？")
            self.render_context = RenderContext(self.dxf)
            
            #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
            self.backend = PyQtBackend(use_text_cache=True)
            print("成功读入")
            self.layers.visible_names = None
            self.current_layout = None
            print("程序已经走到了这里")
            #self.select_layout_menu.clear()
            '''for layout_name in self.dxf.layout_names_in_taborder():
                action = self.select_layout_menu.addAction(layout_name)
                action.triggered.connect(self.change_layout)'''

            #self.layers.populate_layer_list( self.render_context.layers.values() )
            self.draw_layout('Model')
            self.setWindowTitle('CAD Viewer - ' + plt_convert_name)



        else:
            try:
                self.dxf = ezdxf.readfile(filename)
                
                #print("小日本的东西写得成不？")
                self.render_context = RenderContext(self.dxf)
                
                #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
                self.backend = PyQtBackend(use_text_cache=True)
                print("成功读入")
                self.layers.visible_names = None
                self.current_layout = None
                print("in openg file 175 程序已经走到了这里")
                #self.select_layout_menu.clear()
                '''for layout_name in self.dxf.layout_names_in_taborder():
                    action = self.select_layout_menu.addAction(layout_name)
                    action.triggered.connect(self.change_layout)'''

                #self.layers.populate_layer_list( self.render_context.layers.values() )
                self.draw_layout('Model')
                self.setWindowTitle('CAD Viewer - ' + filename)
            except:
                print("没有文件可以打开，请重新选择可以打开的文件")
                return



    def open_template_file(self,file_name):
        #print(filename)
        self.dxf = ezdxf.readfile(file_name)
        
        #print("小日本的东西写得成不？")
        self.render_context = RenderContext(self.dxf)
        
        #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
        self.backend = PyQtBackend(use_text_cache=True)
        print("成功读入")
        self.layers.visible_names = None
        self.current_layout = None
        print("157行，-------------程序已经走到了这里,open_template_file in cadviewer02.py")
        #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
            action = self.select_layout_menu.addAction(layout_name)
            action.triggered.connect(self.change_layout)'''

        #self.layers.populate_layer_list( self.render_context.layers.values() )
        self.draw_layout('Model')
        self.setWindowTitle('CAD Viewer - ' + file_name)



    def open_dxf_file(self,dxf_file_name):
        print(dxf_file_name)
        self.model_name=dxf_file_name
        self.dxf = ezdxf.readfile(dxf_file_name)
        
        #print("小日本的东西写得成不？")
        self.render_context = RenderContext(self.dxf)
        
        #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
        self.backend = PyQtBackend(use_text_cache=True)
        print("成功读入")
        self.layers.visible_names = None
        self.current_layout = None

        print("这是02版本-----------------------------------")
        print("排版完成-----------------------------------")
        print("排版完成-----------------------------------")
        print(" ")
        print(" ")
        print(" ")
        #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
            action = self.select_layout_menu.addAction(layout_name)
            action.triggered.connect(self.change_layout)'''

        #self.layers.populate_layer_list( self.render_context.layers.values() )
        self.draw_layout('Model')
        self.setWindowTitle('CAD Viewer - ' + dxf_file_name)



    

    def change_layout(self):
        layout_name = self.sender().text()
        self.draw_layout(layout_name)

    def draw_layout(self, layout_name):
        self.current_layout = layout_name
        self.view.begin_loading()
        new_scene = QtWidgets.QGraphicsScene()
        self.backend.set_scene(new_scene)
        layout = self.dxf.layout(layout_name)
        self.render_context.set_current_layout(layout)
        if self.layers.visible_names is not None:
            self.render_context.set_layers_state(self.layers.visible_names, state=True)
        try:
            frontend = MyFrontend(self.render_context, self.backend)
            frontend.log_view = self.logView
            frontend.draw_layout(layout)
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        
        self.view.end_loading(new_scene)
        self.view.buffer_scene_rect()
        self.view.fit_to_scene()
        self.view.setScene(new_scene)

    def _on_mouse_moved(self, mouse_pos: QtCore.QPointF):
        self.statusLabel.setText( f'mouse position: {mouse_pos.x():.4f}, {mouse_pos.y():.4f}\n' )

        print("移动的鼠标位置为",mouse_pos.x(),mouse_pos.y())

class SelectedInfo(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(SelectedInfo, self).__init__(parent)
        self.text = QtWidgets.QPlainTextEdit()
        self.text.setReadOnly(True)
        self.setWidget( QtWidgets.QWidget() )
        self.widget().setLayout( QtWidgets.QVBoxLayout() )
        self.widget().layout().addWidget(self.text)
        self.setWindowTitle('Selected Info')

    def set_elements(self, elements, index):
        
        def _entity_attribs_string(dxf_entity, indent=''):
            text = ''
            for key, value in dxf_entity.dxf.all_existing_dxf_attribs().items():
                text += f'{indent}- {key}: {value}\n'
            print(text)
            return text


        if not elements:
            text = 'No element selected'
            print(text)
        else:
            text = f'Selected: {index + 1} / {len(elements)}    (click to cycle)\n'
            element = elements[index]
            dxf_entity = element.data(CorrespondingDXFEntity)
            if dxf_entity is None:
                text += 'No data'
            else:
                text += f'Selected Entity: {dxf_entity}\nLayer: {dxf_entity.dxf.layer}\n\nDXF Attributes:\n'
                text += _entity_attribs_string(dxf_entity)

                dxf_parent_stack = element.data(CorrespondingDXFParentStack)
                if dxf_parent_stack:
                    text += '\nParents:\n'
                    for entity in reversed(dxf_parent_stack):
                        text += f'- {entity}\n'
                        text += _entity_attribs_string(entity, indent='    ')
                        
        self.text.setPlainText(text)

class Layers(QtWidgets.QDockWidget):
    updated_signal = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        super(Layers, self).__init__(parent)

        self.visible_names = None

        self.model = QtGui.QStandardItemModel()
        self.view = QtWidgets.QListView()
        self.view.setModel(self.model)
        self.view.setStyleSheet( 'QListWidget {font-size: 12pt;} QCheckBox {font-size: 12pt; padding-left: 5px;}' )
        self.setWidget( QtWidgets.QWidget() )
        self.widget().setLayout( QtWidgets.QVBoxLayout() )
        self.widget().layout().addWidget(self.view)
        self.setWindowTitle('Layers')
        
        self.model.dataChanged.connect(self.layers_updated)
            
    def populate_layer_list(self, layers):
        self.model.clear()
        for layer in layers:
            item = QtGui.QStandardItem(layer.layer)
            item.setData(layer)
            item.setCheckable(True)
            item.setCheckState( QtCore.Qt.Checked if layer.is_visible else QtCore.Qt.Unchecked )
            text_color = '#FFFFFF' if is_dark_color(layer.color, 0.4) else '#000000'
            item.setForeground( QtGui.QBrush(QtGui.QColor(text_color)) )
            item.setBackground( QtGui.QBrush(QtGui.QColor(layer.color)) )
            self.model.appendRow(item)

    def layers_updated(self):
        self.visible_names = []
        for row in range( self.model.rowCount() ):
            item = self.model.item(row, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self.visible_names.append( item.text() )
        self.updated_signal.emit(self.visible_names)


class new_layers(QtWidgets.QDockWidget):
    #updated_signal = QtCore.pyqtSignal(list)
    def __init__(self, parent=None):
        #super(new_layers, self).__init__(parent)

        self.visible_names = None

        '''self.model = QtGui.QStandardItemModel()
        self.view = QtWidgets.QListView()
        self.view.setModel(self.model)
        self.view.setStyleSheet( 'QListWidget {font-size: 12pt;} QCheckBox {font-size: 12pt; padding-left: 5px;}' )
        self.setWidget( QtWidgets.QWidget() )
        self.widget().setLayout( QtWidgets.QVBoxLayout() )
        self.widget().layout().addWidget(self.view)
        self.setWindowTitle('Layers')'''
        
        #self.model.dataChanged.connect(self.layers_updated)
            
    


class LogView(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent)
        self.text = QtWidgets.QTextBrowser()
        self.setWidget( QtWidgets.QWidget() )
        self.widget().setLayout( QtWidgets.QVBoxLayout() )
        self.widget().layout().addWidget(self.text)
        self.setWindowTitle('Log')

    def append(self, text):
        self.text.append(text)


class new_log_view(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        #super(LogView, self).__init__(parent)
        '''self.text = QtWidgets.QTextBrowser()
        self.setWidget( QtWidgets.QWidget() )
        self.widget().setLayout( QtWidgets.QVBoxLayout() )
        self.widget().layout().addWidget(self.text)
        self.setWindowTitle('Log')'''

    def append(self, text):
        self.text.append(text)

class MyFrontend(Frontend):
    log_view = None
    #def log_message(self, message):
       # self.log_view.append(message)

if __name__ == '__main__':
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    window = cadViewer()
    window.show()
    window.open_file()
    app.exec()