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
from  PyQt5.QtChart import QChart, QChartView, QSplineSeries, QCategoryAxis, QValueAxis

import os
#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#import sip

import cv2
import matplotlib.pyplot as plt
from PIL import Image

#from plt_reader import*

#class cadWindow(QtWidgets.QMainWindow):
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor





class cadDxfViewer(QWidget):
    def __init__(self, parent=None):
        super(cadDxfViewer, self).__init__(parent)

        self.setWindowTitle('cadViewer')
        self.setGeometry(400,500,1000,500)
        #全局布局（2中）：这里选择水平布局

        ##########重新设计布局，因为不是centralwidget,但后期可以考虑将这个设计为centralwidget
        self.wlayout=QHBoxLayout()
        self.setLayout(self.wlayout)
        self.left_layout=QVBoxLayout()
        self.model_name=''

        self.resize(1000, 500)

        #self.render_params = {'linetype_renderer': 'ezdxf'}
        
        #self.statusLabel = QtWidgets.QLabel()
        #self.view = CADGraphicsViewWithOverlay()
        self.view=View()

        #那么这里没必要定义scene了。不是很简单的事情
        #self.view.setScene(QtWidgets.QGraphicsScene())
        '''self.background_color ='#232423'
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QBrush(QColor(self.background_color)))
        self.view.setScene(self.scene)
        self.view.scale(1, -1)'''

       

        self.number_for_nest=0
        self.wlayout.addWidget(self.view)
        self.singleOffset = QPoint(0, 0)          
       
        #self.layers.visible_names = None
        self.current_layout = None
        #print("in openg file 175 程序已经走到了这里")
            #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
        action = self.select_layout_menu.addAction(layout_name)
        action.triggered.connect(self.change_layout)'''
        

       # self.selectedInfo = SelectedInfo(self)
        #self.wlayout.addWidget(self.selectedInfo)

        #self.view.draw_layout('model')
        #self.new_scene = QtWidgets.QGraphicsScene()
        #self.backend.set_scene(self.new_scene)

        #self.text = QtWidgets.QPlainTextEdit()
        #self.text.setReadOnly(True)
    def mouseMoveEvent(self, event):
        s = event.windowPos()
        self.setMouseTracking(True)
        #self.label_mouse_x.setText('X:' + str(s.x()))
        #self.label_mouse_y.setText('Y:' + str(s.y()))

    

class View(CADGraphicsViewWithOverlay):
    #print("View继承自CADGraphicsViewWithOverlay")
    def __init__(self):
        super().__init__()
        self.pen = QPen()
        self.pen.setColor(Qt.green)
        self.start = QPoint()
        self.end = QPoint()
        self.setMouseTracking(True)
        self.mousePreseed = False
        self.rect, self.line = None, None
        

        self.filename=''
        self.dxf=None
        #self.selected_info=SelectedInfo()

        #sself.element_selected.connect(self.i)
        #self.element_selected.connect(self.choose_elements)

        self.pos_offset=QPointF(0,0) 
        #self.save_button=QPushButton()
        #self.button=QPushButton("保存")
        #save = QAction("保存",self)
        self.background_color ='#032423'
        self.new_scene = QGraphicsScene()
        self.new_scene.setBackgroundBrush(QBrush(QColor(self.background_color)))
        self.setScene(self.new_scene)

        self.render_context = None
        self.backend = PyQtBackend(use_text_cache=True)
        self.backend.set_scene(self.new_scene)
        self.dxf_layout=None
        #self.dxf_layout = self.dxf.layout(layout_name)
        #self.render_context.set_current_layout(self.dxf_layout)
        self.frontend=None


        self.layout_name='Model'

        self.element_selected.connect(self.choose_elements)

        self.text=''
        #elf.frontend = Frontend(self.render_context, self.backend)

        self.graphWidget = pg.PlotWidget()
        #self.addwidget(self.graphWidget)
        self.graphicsProxyWidget()
        #self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setXRange(5, 20, padding=0)
        self.graphWidget.setYRange(30, 40, padding=0)
        #self.graphWidget.setTitle("<span style=\"color:blue;font-size:20pt\">星河排版</span>")
        self.graphWidget.setTitle("恒强排版", color="b", size="20pt")
        pen = pg.mkPen(color=(255, 0, 0), width=15)
        self.graphWidget.plot(hour, temperature, pen=pen)


        ##super().__init__(*args, **kwargs)

        self.view_menu = QMenu(self)
       # self.a_grid_background = QS()
        self.setScene(QtWidgets.QGraphicsScene())
        self.setSceneRect(0,0,self.Settings.NUM_BLOCKS_X * self.Settings.WIDTH,self.Settings.NUM_BLOCKS_Y * self.Settings.HEIGHT)

        #self.create_actions()


    class Settings():

        WIDTH = 30
        HEIGHT = 30
        NUM_BLOCKS_X = 10
        NUM_BLOCKS_Y = 14

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.view_menu = QMenu(self)
       # self.a_grid_background = QS()
        self.setScene(QtWidgets.QGraphicsScene())
        self.setSceneRect(0,0,self.Settings.NUM_BLOCKS_X * self.Settings.WIDTH,self.Settings.NUM_BLOCKS_Y * self.Settings.HEIGHT)

        self.create_actions()'''
    
    def create_action(self,parent, text, slot=None,
                  shortcut=None, shortcuts=None, shortcut_context=None,
                  icon=None, tooltip=None,
                  checkable=False, checked=False):
        action = QtWidgets.QAction(text, parent)

        if icon is not None:
            action.setIcon(QIcon('2.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if shortcuts is not None:
            action.setShortcuts(shortcuts)
        if shortcut_context is not None:
            action.setShortcutContext(shortcut_context)
        if tooltip is not None:
            action.setToolTip(tooltip)
            action.setStatusTip(tooltip)
        if checkable:
            action.setCheckable(True)
        if checked:
            action.setChecked(True)
        if slot is not None:
            action.triggered.connect(slot)

        return action


    '''def create_actions(self):
        act = self.create_action(self.view_menu, "Zoom in",
                            slot=self.on_zoom_in,
                            shortcut=QKeySequence("+"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)

        act = self.create_action(self.view_menu, "Zoom out",
                            slot=self.on_zoom_out,
                            shortcut=QKeySequence("-"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)
        self.addActions(self.view_menu.actions())'''

    '''def on_zoom_in(self):
        if not self.scene():
            return

        self.scale(2, 2)

    def on_zoom_out(self):
        if not self.scene():
            return

        self.scale(1.0 / 2, 1.0 / 2)'''

    def drawBackground(self, painter, rect):
        gr = rect.toRect()
        start_x = gr.left() + self.Settings.WIDTH - (gr.left() % self.Settings.WIDTH)
        start_y = gr.top() + self.Settings.HEIGHT - (gr.top() % self.Settings.HEIGHT)
        painter.save()
        painter.setPen(QtGui.QColor(60, 70, 80).lighter(90))
        painter.setOpacity(0.7)

        for x in range(start_x, gr.right(), self.Settings.WIDTH):
            painter.drawLine(x, gr.top(), x, gr.bottom())

        for y in range(start_y, gr.bottom(), self.Settings.HEIGHT):
            painter.drawLine(gr.left(), y, gr.right(), y)

        painter.restore()

        super().drawBackground(painter, rect)
   

    def move_dxf_to_pos(self,event):
        
        #self.move_dxf_entity(self.filename,self.selected_info.select_dxf_entity,self.pos_offset.x(),self.pos_offset.y())
        self.move_dxf_entity(self.filename,self.select_dxf_entity,self.pos_offset.x(),self.pos_offset.y())
        
        #self.dxf=self.new_scene.removeItem(self.filename)
        #self.dxf = ezdxf.readfile(self.filename) 
        #self.dxf.delete_layout(self.layout_name)
        #self.dxf_layout = self.dxf.layout(self.layout_name)
        #self.render_context.set_current_layout(self.dxf_layout)
        
        self.draw_layout('Model')

    def save_dxf(self,file):
        print("保存相应的dxf文件",file)
        file.saveas("new_1.dxf")

         
    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.LeftButton:
                self.mousePreseed = True
                if(str(self.select_dxf_entity)!='POLYLINE(#None)'):
                    self.start = self.mapToScene(event.pos())
                    
                #####获取移动之前的坐标。
                    self.preMousePosition = event.pos()      
                    print("这里能够完成dxf实体的直接移动吗？,",self.preMousePosition.x(),self.preMousePosition.y())
                else:
                    print("选择的模型为方框，不能选择。")
                    return 
        
            #self.start = self.mapToScene(event.pos())
            #####获取移动之前的坐标。
            #self.preMousePosition = event.pos()      
            
            #print("这里能够完成dxf实体的直接移动吗？,",self.preMousePosition.x(),self.preMousePosition.y())
            #######可以尝试直接move entity
            #####需要正式移动entity,entity就是dxf类，无需其他东西。
            #print("鼠标按下的位置为event.pos()",event.pos())
            #self.new_scene.update()
            #self.update()
            #self.repaint()
            #self.clear()
            elif event.button() == Qt.RightButton:
                print("右键按下，需要保存")
                self.save_dxf(self.dxf)
                print("保存成功")
        except:
                return 
    #def 
    def choose_elements(self, elements, index):
        
        '''def _entity_attribs_string(dxf_entity, indent=''):
            text = ''
            for key, value in dxf_entity.dxf.all_existing_dxf_attribs().items():
                text += f'{indent}- {key}: {value}\n'
            return text'''
        #print("elments是",elements[index].data(CorrespondingDXFEntity))
        if not elements:
            self.text = 'No element selected'
        else:
            #print("index=========",index)
            self.text = f'Selected: {index + 1} / {len(elements)}    (click to cycle)\n'
            #print("index=========",index)
            element = elements[index]
            dxf_entity = element.data(CorrespondingDXFEntity)
            #print("dxf_entity的值为",dxf_entity)
            print(dxf_entity)
            if dxf_entity is None:
                print("dxf_entity None")
                self.text += 'No data'
            else:
                #print("在selecetedinfo set——elements内部",dxf_entity)
                #return dxf_entity
                self.select_dxf_entity=dxf_entity                          
        #self.text.setPlainText(self.text)

        print(self.text)
        
    def mouseMoveEvent(self,event): 
        super().mouseMoveEvent(event)
        try:

            if event.buttons() & Qt.LeftButton & self.mousePreseed:
                #self.end = self.mapToScene(event.pos())
                #self.drawShape()
                print("在函数中mouseMoveEvent接收到self.selected_info.select_dxf_entity的值",self.select_dxf_entity)
                #self.move_dxf_to_pos(event)'''
                if(str(self.select_dxf_entity)!='POLYLINE(#None)'):
                    self.pos_offset =event.pos()-self.preMousePosition
                #self.preMousePosition = event.pos() 
                    print("self.pos_offset==============偏移量===========",self.pos_offset)
                else:
                    print("选择的模型为方框，不能选择。")
                    return 
        except:
            return 
            #self.new_scene.update()
            #self.update()
            #self.repaint()
            #self.move_dxf_to_pos(self.pos_offset)
            #self.clear()
            #print("鼠标移动的位置为event.pos()",event.pos(),event.x(),event.y())'''

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.mousePreseed:
            self.mousePreseed = False
            self.isLeftPressed = False; 
            try:
                self.move_dxf_to_pos(self.pos_offset)
            except:

                return 
                    #self.new_scene.update() 
            #self.update()
            #self.clear()
            #self.repaint()
        

            #self.scene.update()
    '''def movexy(self,srcdxf,x,y):
        dxf=ezdxf.readfile(srcdxf)
        for e in dxf.entities:
            e.translate(x,y,0)
        dxf.saveas(srcdxf)'''

    

    def move_dxf_entity(self,srcdxf,dxf_entity,x,y):
       # print(dxf_entity.)
        #self.dxf=ezdxf.readfile(srcdxf)

        #for i in self.new_scene.
            #print(i)
        try:

            for e in self.dxf.entities:
                #print("dxf中e=====",e,"输入的dxf_entity===",dxf_entity)
                if(str(e)==str(dxf_entity)):
                    #self.dxf.delete(e)            
                    print("e==dxf_entity,这个等式是成立的这个等式") 
                    try:
                        self.new_scene.clear()
                    except:
                        print("场景清理异常,一般发生于模型重叠")
                    #self.frontend.draw_entities(e)
                    print("重新绘制dxf中的实体")
                    e.translate(x,y,0)
                    #try:
                    #self.frontend.draw_polyline_entity(e)

                    #self.frontend.draw_polyline_entity(e,properties=None)
                    #self.dxf.layout
                    ##self.frontend.draw_entitie(e)
                    #except:
                      #  print("重画执行不对，请重新绘制。重画执行不对，请重新绘制。重画执行不对，请重新绘制。")
                    
                    #self.update()
                else:
                    continue
           # for e in self.dxf.entities:
               #self.changeEvent()
               #self.frontend.draw_entities(e)
              # print("重新绘制dxf中的实体")
        except:
            print("产生了异常，没有文件打开，请打开文件")
            return
        #dxf_entity.translate(x,y)
        #self.dxf.saveas(srcdxf)

    def open_file(self):
        self.filename, filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'CAD files (*.dxf *.DXF *.plt)')
        if self.filename == '':
          return  
        #self.filename="new_1.dxf"
        print(self.filename)
        #self.model_name=filename 
        if(os.path.splitext(self.filename)[-1]==".plt"):
            #self.dxf = ezdxf.readfile(filename)
            #img2 = plt.imread(filename)
            #plt.imshow(img2)
            print("这个文件是.plt文件",self.filename)

            array_list,maax_x,max_y,array_lines=parse_plt(self.filename)
            plt_convert_name=self.filename+".dxf"
            plt_to_dxf(array_lines,plt_convert_name)
    #plt_to_dxf_one_line(array_lines,"ts9.dxf")
            print("执行结束，看看能不能打开，并提取模型？")
            
            self.dxf = ezdxf.readfile(plt_convert_name)
            
            #print("小日本的东西写得成不？")
            self.render_context = RenderContext(self.dxf)
            #self.backend=
            
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
            self.dxf = ezdxf.readfile(self.filename) 
            self.render_context = RenderContext(self.dxf)
            #self.view.move_dxf_to_pos(self.view,self.view.event())
            #self.backend = PyQtBackend(use_text_cache=True)
            #self.view.dragMoveEvent(self,self.dxf)
            #sself.view.event(QEvent)
            self.layout_name='Model'
            self.dxf_layout = self.dxf.layout(self.layout_name)
            self.render_context.set_current_layout(self.dxf_layout)
            #layout = self.dxf.layout(layout_name   )
            #self.draw_layout(layout_name)
            self.frontend = Frontend(self.render_context, self.backend)
            self.draw_layout(self.layout_name)
            print("打开文件再新建Frontend")
            self.fit_to_scene()

            for item in self.new_scene.items():
                if str(item.data(CorrespondingDXFEntity))!='POLYLINE(#None)':
                    print("new_scene的item是",item.GraphicsItemFlag)
                    print ("如何获取item的信息",item.data(CorrespondingDXFEntity))
                    item.setFlag(QGraphicsItem.ItemIsMovable)
                    item.setFlag(QGraphicsItem.ItemIsSelectable)
                    #item.
                    
                else:
                    print("模型选择的是'POLYLINE#None'")
                    #item.isVisible

                    #item.setFlags(item.flags() & ~Qt.ItemVisible)
                    #item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    item.setFlag(~QGraphicsItem.ItemIsSelectable)
                    print("模型选择的是'POLYLINE#None'模型选择的是'POLYLINE#None',",item.flags())
                    #@item.setFlag(item.flags,Qt.ItemIsSelectable,False)


                
 
             #self.draw_layout('Model')

        
    '''def change_layout(self):
        layout_name = self.sender().text()
        self.draw_layout(layout_name)'''
    
    def draw_layout_old(self, layout_name):
        #self.current_layout = layout_name

        #########开始载入，self.view.begin_loading 居然也不需要
        self.begin_loading()

        #########新建一个QGraphicsScene()场景。
        new_scene = QtWidgets.QGraphicsScene()
        ##########其实可以写成一个东西，没必要写成2个东西吧，这个情景
        self.backend.set_scene(new_scene)
        layout = self.dxf.layout(layout_name)
        self.render_context.set_current_layout(layout)
        #if #self.layers.visible_names is not None:
            #self.render_context.set_layers_state(self.layers.visible_names, state=True)
        try:
            frontend = Frontend(self.render_context, self.backend)
            #frontend.log_view = self.logView
            ######这里涉及到递归调用的问题？，这里不是递归，两个函数不一样的名字。frontend是系统函数
            frontend.draw_layout(layout)
            #print(str(layout))
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        
        self.end_loading(new_scene)
        ########
        #self.buffer_scene_rect()
        self.fit_to_scene()
        #self.setScene(new_scene)

    def draw_layout(self,layout_name):
       
        self.begin_loading()
        try:
            #self.frontend = Frontend(self.render_context, self.backend)
            #self.frontend.
            self.frontend.draw_layout(self.dxf_layout)
            #self.frontend.draw_entities(e)

            #print(str(layout))
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        
        self.end_loading(self.new_scene)
        ########
        #self.buffer_scene_rect()
        self.fit_to_scene()
        #self.setScene(self.new_scene)
    def draw_dxf_entities(self,dxf_entity):
        self.begin_loading()
        try:
            self.frontend.draw_entities(dxf_entity)
            #print(str(layout))
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        self.end_loading(self.new_scene)

        self.fit_to_scene()
        

    def draw_dxf_entity(self,dxf_entity):
        #self.current_layout = layout_name

        #########开始载入，self.view.begin_loading 居然也不需要
        self.begin_loading()

        #self.new_scene = QtWidgets.QGraphicsScene()
        ##########其实可以写成一个东西，没必要写成2个东西吧，这个情景
        self.backend.set_scene(self.new_scene)
        layout = self.dxf.layout(self.layout_name)
        self.render_context.set_current_layout(layout)
        #if #self.layers.visible_names is not None:
            #self.render_context.set_layers_state(self.layers.visible_names, state=True)
        try:
            frontend = Frontend()
            #frontend.log_view = self.logView
            ######这里涉及到递归调用的问题？，这里不是递归，两个函数不一样的名字。frontend是系统函数
            frontend.draw_entities(dxf_entity)
            #print(str(layout))
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{self.layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        
        self.end_loading(self.new_scene)
        ########
        #self.buffer_scene_rect()
        #self.fit_to_scene()


    def open_dxf_file_bug(self,dxf_file_name):
        print(dxf_file_name)
        self.model_name=dxf_file_name
        self.dxf = ezdxf.readfile(dxf_file_name)
        
        #print("小日本的东西写得成不？")
        self.render_context = RenderContext(self.dxf)
        
        #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
        self.backend = PyQtBackend(use_text_cache=True)
        print("成功读入")
        #self.layers.visible_names = None
        self.current_layout = None

        print("09 viewer-----------------------------------")
       
        #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
            action = self.select_layout_menu.addAction(layout_name)
            action.triggered.connect(self.change_layout)'''

        #self.layers.populate_layer_list( self.render_context.layers.values() )
        self.draw_layout('Model')
        self.fit_to_scene()
        self.setWindowTitle('CAD Viewer - ' + dxf_file_name)
        
        #print("self.label_mouse_x的位置为",str(s.x()),"self.label_mouse_y的位置为",str(s.y()))
    def open_dxf_file(self,dxf_file_name):
        self.dxf = ezdxf.readfile(dxf_file_name) 
        self.render_context = RenderContext(self.dxf)
        #self.view.move_dxf_to_pos(self.view,self.view.event())
        #self.backend = PyQtBackend(use_text_cache=True)
        #self.view.dragMoveEvent(self,self.dxf)
        #sself.view.event(QEvent)
        self.layout_name='Model'
        self.dxf_layout = self.dxf.layout(self.layout_name)
        self.render_context.set_current_layout(self.dxf_layout)
        #layout = self.dxf.layout(layout_name   )
        #self.draw_layout(layout_name)
        self.frontend = Frontend(self.render_context, self.backend)
        self.draw_layout(self.layout_name)
        print("打开文件再新建Frontend")
        print("09 viewer-----------------------------------成功读入")





if __name__ == '__main__':
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    window = cadDxfViewer()
    window.show()
    window.view.open_file()
    #try:
        #window.view.dxf.saveas(window.view.filename)

        #print("保存在,",window.view.filename,"中")
    #except:
        #print("没有东西可以保存")
    #window.open_file()
    app.exec()

    '''try:
        window.view.dxf.saveas(window.view.filename)

        print("保存在,",window.view.filename,"中")
    except:
        print("没有东西可以保存")'''