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

import layout6

from layout6 import*
import os
#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from readdxf15 import *
#import sip


#class cadWindow(QtWidgets.QMainWindow):
class cadPreViewer(QWidget):
    def __init__(self, parent=None):
        super(cadPreViewer, self).__init__(parent)

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

        self.view.setEnabled(False)
        self.number_for_nest=0
        self.wlayout.addWidget(self.view)

        '''self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.quitAction = QAction("排版", self)
       # if(self.dxf is not NONE):
        #self.nameAction=QAction("模型的名字",self)
        self.quitAction.triggered.connect(self.get_linedit_number)
        self.addAction(self.quitAction)'''
       


        self.linedit=QLineEdit()
        self.linedit.setFixedWidth(30)
        #lineEdit=QLineEdit()
        #self.lineEdit.setValidator(QIntValidator())

        self.wlayout.addWidget(self.linedit)



        ############定义排版模型的数据,决定了每一次排版的数据的起始位置，很关键，
        ##########并且不断的更新。
        self.start_nest_x=0
        self.start_nest_y=0
        self.old_model_height=0
        self.old_model_width=0
    '''def pop_for_nest(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu) #Qt 
        # 直接把action加到自身上
        self.quitAction = QAction("排版", self)
       # if(self.dxf is not NONE):
        #self.nameAction=QAction("模型的名字",self)
        self.quitAction.triggered.connect(self.get_linedit_number)

        #self.mywindow.cad_windwo
        #self.
        #print("弹出对话框，多写点东西进来，其实其他的很多指标要加进来。")        
        #self.addAction(self.quitAction)'''
        

        #return True
        #layout.cad_window.open_dxf_file("new_nest.dxf")
       # layout.cad_window.open_dxf_file("new_nest.dxf")
        #return True

    
    '''def add_linedit_widget(self):
        self.linedit=QLineEdit()
        self.linedit.setFixedWidth(30)
        #lineEdit=QLineEdit()
        #self.lineEdit.setValidator(QIntValidator())

        self.wlayout.addWidget(self.linedit)'''

        #return self.linedit
        #self.number_for_nest=self.linedit.text()
       # return self.number_for_nest
    


    def get_linedit_number(self):
        #try:
            print("获取排版数量为",self.linedit.text())
            print("需要排版的模型名字为",self.model_name)
            nest_number=self.linedit.text()
            model=self.model_name


#################开始正式排版,暂时设置为1500，6000，写死，等后面继续更新的时候再说。
            self.start_nest(nest_number,model,1500,6000)
            #layout.cad_window.open_dxf_file("new_nest.dxf")
            #self.

            #self.
            #return self.linedit.text()
            #return True
        #except:
           # print("没有东西可以获取")

        #####################就近设置排版函数
    def start_nest(self,number_for_nest,model_name,width,height,start_x,start_y,old_model_height):
        
        nest_number=int(number_for_nest)
        model=model_name
        w=width
        h=height

        '''这里必须算出来模型的最大值和最小值，然后再去计算，不然很难搞的。'''
        ########
        #########找到d4文件，可以分析出来这个文件的最大的值和最小值。
        '''if(os.path.exists("D4.dxf")):

            max_y=findMaxYVertex("D4.dxf")
        '''

        if(os.path.exists("3.dxf")):
            os.remove("3.dxf")
            rotate_zdxf(model,0 ,"3.dxf")
        else:
            rotate_zdxf(model,0 ,"3.dxf")
        ########计算模型的高度和最合适的宽度，注意，有些模型可以拼合起来得到最合适的宽度
        ##########必须要组合起来才能得知，单个模型算不出来的。
        if(os.path.exists("edge.dxf")):
            os.remove("edge.dxf")
            [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        else:
            [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        
        ########这里有2种排版方式
        '''1，直接在上层排版'''
        print("self.old_model_height的值为",old_model_height,"这个值很关键")
        if(model_Height>old_model_height):
            #####原有的空间不适合排版，必须新1起1行排版。所以start_x=0
            print("最新排版的模型比上一个排版的模型高")
            start_x=0
            start_y=start_y+old_model_height
            nest_with_rest(model,nest_number,w,h,model_Width,model_Height)
            delt_x=findMinXVertex("D4.dxf")[0]
            delt_y=findMinYVertex("D4.dxf")[1]
            #mix("D4.dxf","xy.dxf","new_nest.dxf")
            movexy("D4.dxf",start_x-delt_x,start_y-delt_y)
            if(old_model_height==0):
                print("第二次进入到这个里面了吗")
                mix("D4.dxf","xy.dxf","new_nest.dxf")
            else:
                mix("D4.dxf","new_nest.dxf","new_nest.dxf")
        #if
        else:
            print("当新排版的模型高度<旧模型的高度时","新模型的高度为",model_Height,"旧模型的高度为",old_model_height)
            if((old_model_height/2)<model_Height<old_model_height):   
                left_width=1500-start_x
                other_model_num=int(left_width/model_Width) 
                print("other_model_num的大小为",other_model_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)
                delt_x=findMinXVertex("D4.dxf")[0]
                delt_y=findMinYVertex("D4.dxf")[1]
                #mix("D4.dxf","xy.dxf","new_nest.dxf")
                movexy("D4.dxf",start_x-delt_x,start_y-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                ####这里相当于形成了一个新的模型了。
                print("测试的模型应该在这里合并才对")
                ########因为是一个新的模型了，这个里必须要更新新的x和y的排版起点了。
                #####在这里增加高度是非常不对的，
                #######这里的start_x=0是不对的，很明显是start_x保持不动。
                #start_x=0
                ########这里貌似start_y也是错误的，因为这里的，model_height还是比old_model_height低的。
                start_y=start_y+old_model_height
                rest_number=nest_number-other_model_num
            #######再来排剩下的从新的一层开始,当然这里要判断是不是剩下的已经排版完成了
                if(rest_number>0):
                    nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                    #####delt_x是计算随意排版的偏移值的，在后续的模型里面应该不需要。
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    print("最后剩余的模型的start_y模型的排版位置为",start_y)
                    movexy("D4.dxf",start_x-delt_x,start_y-delt_y)
                    #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")
            ######如果模型的高度比旧模型的高度的1/2都小
            elif(model_Height<(old_model_height/2)):
                left_width=1500-start_x
                ###这个软件    
                gap_row_num=int(left_width/model_Width) 
                
                print("窄沟容纳的模型数量为",gap_row_num)
                gap_layers=int(old_model_height/model_Height)
                other_model_num=gap_row_num*gap_layers

                ##如果是奇数就得在额外增加一个排版
                if((float(left_width/model_Width)-gap_row_num)>0.5):
                    gap_row_num=gap_row_num+1
                    #nest_number=nest_number-1*gap_layers #####因为这里多塞了1个model进去了
                    other_model_num=other_model_num+gap_layers*1
                print("other_model_num的大小为",other_model_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                for i in range(0,gap_layers):
                    #if()
                    nest_with_rest(model,gap_row_num,w,h,model_Width,model_Height)
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]
                #mix("D4.dxf","xy.dxf","new_nest.dxf")
                    movexy("D4.dxf",start_x-delt_x,start_y-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                ####这里相当于形成了一个新的模型了。
                    #print("测试的模型应该在这里合并才对")
                    start_y=start_y+model_Height

                ########因为是一个新的模型了，这个里必须要更新新的x和y的排版起点了。
                #####在这里增加高度是非常不对的，
                    #start_x=0
                ######这里需要纠正过来
                start_y=start_y+old_model_height-2*model_Height
            
            #######再来排剩下的从新的一层开始,当然这里要判断是不是剩下的已经排版完成了
                rest_number=nest_number-other_model_num
                if( rest_number>0):
                    start_x=0
                    print("nest_number-other_model_num的值为",rest_number)
                    
                    nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                    #####delt_x是计算随意排版的偏移值的，在后续的模型里面应该不需要。
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    print("最后剩余的模型的start_y模型的排版位置为",start_y)
                    movexy("D4.dxf",start_x-delt_x,start_y-delt_y)
                    #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")






        #print("在排版前,得到文件x的最大值是",self.start_nest_x)

        #print("在排版后,得到文件x的最大值是",self.start_nest_y)
        #nest_with_rest(model,nest_number,w,h,model_Width,model_Height)

        '''需要寻找新的模型'''
        #delt_x=findMinXVertex("D4.dxf")[0]
        #delt_y=findMinYVertex("D4.dxf")[1]

        #movexy("D4.dxf",0-delt_x,0-delt_y)

    #copytomove("D4.dxf",0-delt_x,0-delt_y,"old_nest.dxf")
    ##########"old_nest.dxf"主要用于保存已经排版好的D4.dxf,
    #######将模型和外框整合并成1个模型，因为这里面部存在一个模型，整合起来让机器能够识别。
        #mix("D4.dxf","xy.dxf","new_nest.dxf")
        '''应该是放在排版的后面，因为排版以后才能更新排版的最后2个位置，不然会乱套的。'''
        '''这个计算明显错误的把'''
        #rest_number=int(nest_number-(nest_number/(int(1500/model_Width))))#######最后一行剩下的数量。
        print("排版前得到文件x的最大值是",start_x)
        row_number=int(1500/model_Width)
        layers=int(nest_number/row_number)
        rest_number=nest_number-layers*row_number
        print("排版后start_y的最大值是",start_y,"rest_number的值为",rest_number)

        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
        ########更新最新的start_nest_x,和start_nest_y的值。
        start_x=(rest_number*model_Width+start_x)%(1500)##########最后一行X的最大值。
        start_y=layers*model_Height+start_y

        print("排版后start_x的最大值是",start_x,"模型的宽度为",model_Width)

        print("排版后start_y的最大值是",start_y,"模型的高度为",model_Height)
        

        #####模型的最后再来更新模型的高度和宽度
        old_model_height=model_Height

        print("self.old_model_height的值为",old_model_height)
        #mix("D4.dxf","xy.dxf","new_nest.dxf")
        #nest_with_rest(model,nest_number,w,h)
        #nest_from_width_sample(model,nest_number,0)
        #nest_with_rectangle("mode15.dxf",10,1500,6000)
        print("welcome to start function,欢迎进入排版函数内部")

        return start_x,start_y,old_model_height
        #return True


        #super.
        #self.open_dxf_file(self,"new_nest.dxf"):
        
        



    def open_file(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'CAD files (*.dxf *.DXF)')
        if filename == '':
            return
        #print("小日本的东西写得成不？")
        print(filename)
        #self.model_name=filename
        self.dxf = ezdxf.readfile(filename)
        
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
        self.setWindowTitle('CAD Viewer - ' + filename)



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
        print("程序已经走到了这里")
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
        print("程序已经走到了这里")
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
            return text

        if not elements:
            text = 'No element selected'
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
    def log_message(self, message):
        self.log_view.append(message)

if __name__ == '__main__':
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    window = cadPreViewer()
    window.show()
    window.open_file()
    app.exec()