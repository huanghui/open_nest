import sys
from tkinter import Widget
#from xml.dom.minicompat import StringTypes
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import*
import cv2
import os
#from cadviewer02 import*
from cadviewer17 import*

from readdxf15 import*
from cadPreViewer import*

from functools import partial

#from datetime import datetime
import time
###定义一个初始类用于导入dxf文件并将其转化成png图片，以便后面使
#array_of_img = [] # this if for store all of the image data
# this function is for read image,the input is directory name
'''def read_directory(directory_name):
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in os.listdir(directory_name):
        #print(filename) #just for test
        #img is used to store the image data 
        img = cv2.imread(directory_name + "/" + filename)
        array_of_img.append(img)
        #print(img)
    #print(array_of_img)
    print(len(array_of_img))'''

    ######主要是为了回收模型的类的。

class rectangle():
    
    def __init__ (self):
        self.next_begin_x=0
        self.next_begin_y=0
        self.left_height=0
        self.left_width=0
    def get_begin_x(self):
        return self.next_begin_x
    def get_begin_y(self):
        return self.next_begin_y
    def get_rectangle_length(self):
        return self.left_height 
    def get_rectangle_widht(self):
        return self.left_width
    
    

    


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('排版布局')
        self.setGeometry(400,500,1000,500)
        #全局布局（2中）：这里选择水平布局
        self.wlayout=QHBoxLayout()
        #self.wlayout.setStretch(0, 1)
        #self.wlayout.setStretch(1, 2)
	## 设置间距为0
        #self.wlayout.setSpacing(0)
        self.cad_window = cadDxfViewer()
        #self.setCentralWidget(self.mywindow)
        self.setLayout(self.wlayout)
        #局部布局：水平，垂直，网格，表单
        #self.hlayout=QHBoxLayout()
        self.vlayout = QVBoxLayout()
        #glayout=QGridLayout()
        #flayout=QFormLayout()
        #######控件设置标签，标签设置图片
        #为局部布局添加控件
        
        self.dxf_model_number=5
        #self.hlayout.addWidget(Color("blue"))

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        #self.scroll.setMinimumHeight(100)
        self.scroll.setFixedWidth(300)
        #self.model=[0]*50

        self.frame=QFrame()
        self.frame.setLayout(self.get_widget_layout(150))

        self.scroll.setWidget(self.frame)
        self.scroll.setLayout(self.vlayout)
    

        ##创建一个滚动条
        self.wlayout.addWidget(self.scroll)
        #########这里是定义主窗口
        self.wlayout.addWidget(self.cad_window)
        #准备四个控件
        #if(self.refresh[])

        ##########在layout层建立初始值才行，不能在预览图里面建立。
        self.nest_start_x=0
        self.nest_start_y=0
        self.old_model_height=0
        self.old_model_width=0

        self.old_nest_layers=0

############必须要补充的参数，没有办法的
        self.old_nest_number=0

        self.left_height=0

        self.rectangle_list=[]

        self.left_rectangle=rectangle()

        ##############默认排版距离为2
        self.distance_of_nest=2

        self.sheet_size_width=1500
        self.sheet_size_height=6000

        #self.model_size

    #def set_distance_of_nest(self,distance_of_nest):
        #self.distance_of_nest=distance_of_nest
        #将窗口本身设置为全局布局
    def get_widget_layout(self,number_of_model):
        self.frame_layout=QVBoxLayout()
        self.layout2=QHBoxLayout()
    
        self.model_viewer=[0]*number_of_model
        #self.refresh=[0]*number_of_model
        for x in range(0,number_of_model):
            #self.model_viewer[x]=cadViewer()
            self.model_viewer[x]=cadPreViewer()
            
            #self.model_viewer[x].number_for_nest=self.model_viewer[x].add_linedit_widget()
            #####获取该排版模型需要排版的数量，存在self.linedit.text()中
            #self.model_viewer[x].add_linedit_widget()

            self.model_viewer[x].setContextMenuPolicy(Qt.ActionsContextMenu)
            self.model_viewer[x].quitAction = QAction("排版", self)
        # if(self.dxf is not NONE):
            #self.nameAction=QAction("模型的名字",self)
           # self.model_viewer[x].quitAction.triggered.connect(lambda: self.get_nest_number_and_name(x))
            self.model_viewer[x].quitAction.triggered.connect(partial(self.get_nest_number_and_name,x))
            self.model_viewer[x].addAction(self.model_viewer[x].quitAction)
            self.model_viewer[x].setMinimumSize(270,200)
            #self.model_viewer[x].move(20,x*300+20)
            #self.frame_layout.addLayout(self.layout2)
            self.frame_layout.addWidget(self.model_viewer[x])

        return self.frame_layout

    ##########再layout层调用排版函数应该会好一点，但现在有问题是这个函数谁来调用？

    ###########还是要做一个action

    def get_height_of_rect(self,rect_left):

        print("获取的矩形的y坐标为self.left_rectangle.next_begin_y================",self.left_rectangle.next_begin_y)
        return  self.rect_left.next_begin_y
    

    def get_nest_number_and_name(self,index):
        print("get_nest_number_and_name获取模型名字和数据,排版的间距设置为",self.distance_of_nest)
        #self.model_viewer[i].lineedit
        #self.model_viewer[i].model_name
        self.distance_of_nest=int(self.distance_of_nest)
        #self.distance_of_nest=distance_of_nest

        #########在这个里面或许可以搞定这个事情的
        self.model_number=self.model_viewer[index].linedit.text()

        self.model_name=self.model_viewer[index].model_name



        #self.distance_of_nest=nest_distance
        ##########把模型名字加进去试试看
        #no_path_model_name=os.path.basename(model_name)
        #print("no_path_model_name[:-1]的值为",no_path_model_name)
        #width=findMaxXVertex(model_name)[0]-findMinXVertex(model_name)[0]
        #height=findMaxYVertex(model_name)[1]-findMinYVertex(model_name)[1]
        #self.model_size=str(width)+"*"+str(height)

        #self.model_viewer[index].textbrowser.append(self.model_size)

        #self.nest_start_x,self.nest_start_y,self.old_model_height=self.model_viewer[index].start_nest(model_number,model_name,1500,6000,self.nest_start_x,self.nest_start_y,self.old_model_height)
        
        '''self.nest_start_x,self.nest_start_y,self.old_model_height,\
            self.old_model_width,self.old_nest_layers,self.old_nest_number,\
            self.left_height,self.left_rectangle,self.rectangle_list=\
            self.model_viewer[index].start_nest(model_number,model_name,1500,6000,\
            self.nest_start_x,self.nest_start_y,self.old_model_height,\
            self.old_model_width,self.old_nest_layers,self.old_nest_number,self.left_height,self.left_rectangle,self.rectangle_list)
        '''

        print("排版的版面的宽为self.sheet_size_width===",self.sheet_size_width,"self.sheet_size_height==",self.sheet_size_height)
    
        self.nest_start_x,self.nest_start_y,self.old_model_height,self.old_model_width,\
        self.old_nest_layers,self.old_nest_number,self.left_height,self.left_rectangle,self.rectangle_list,self.distance_of_nest=\
        self.model_viewer[index].start_nest_new(self.model_number,self.model_name,self.sheet_size_width,self.sheet_size_height,\
        self.nest_start_x,self.nest_start_y,self.old_model_height,\
        self.old_model_width,self.old_nest_layers,self.old_nest_number,self.left_height,\
        self.left_rectangle,self.rectangle_list,self.distance_of_nest)
        
        
        #self.rectangle_list.append(self.left_rectangle)

        #try:
        self.rectangle_list.sort(key=lambda x:x.next_begin_y,reverse=True)
 
            #self.rectangle_list.sort(key=self.left_rectangle.rect_)
        #except:f
        num_of_rect=len(self.rectangle_list)
        if(num_of_rect>2):
            #try:
                for i in range(num_of_rect):
                    for j in range(i):
                        print("for i,j in range(len(self.rectangle_list))","i_________________",i,"j_________________",j)
                        if(int(self.rectangle_list[i].next_begin_y)==int(self.rectangle_list[j].next_begin_y)):

                            print("极端情况：当y值相当，而且模型x小的应该先排版，不然会产生回收错误","矩形索引值为",i,j)
                            if(self.rectangle_list[i].next_begin_x>self.rectangle_list[j].next_begin_x):
                                if(abs(i)>abs(j)):
                                    print("极端情况：当y值相当，而且模型x小的应该先排版，不然会产生回收错误")
                                    self.rectangle_list[i],self.rectangle_list[j]=self.rectangle_list[j],self.rectangle_list[i]
                #except:
              #  print("剩下的矩形数量",num_of_rect,"矩形不存在左右顺序问题，不需要交换")

                

          #  print("没有矩形，排不了序")
        
        print("对剩余的矩形进行了倒序排序")
        for rect in self.rectangle_list:
            
            
            
            print("rect.next_begin_x==",rect.next_begin_x,"rect.next_begin_y==",rect.next_begin_y,"rect.left_height==",rect.left_height,"rect.left_width==",rect.left_width)

        if(self.left_rectangle!=0):

            print("该打印信息位于layout6的顶层,self.nest_start_x,self.nest_start_y的值为",\
                self.nest_start_x,self.nest_start_y,"model_name的值为",self.model_number,\
                    "model_name的值为",self.model_name,"原来模型的宽度为",self.old_model_width,\
                "剩下来的矩形为",self.left_rectangle.next_begin_x,\
                self.left_rectangle.next_begin_y,\
                self.left_rectangle.left_height,\
                self.left_rectangle.left_width,\
                "排版的距离设置为",self.distance_of_nest)

        
##########恭喜这一行可以不需要了
        ########传递rect_list过去
        #self.cad_window.view.open_dxf_file("new_nest.dxf") 
        self.cad_window.view.open_dxf_file("new_nest.dxf",self.rectangle_list) 

    
       
    def set_all_dxf_model(self,dxf_model_number,dxf_model_name):
        '''for i in range(dxf_model_number):
            png=QtGui.QPixmap(dxf_model_name)
            self.model[i].setPixmap(png)'''
        print("这里要打开导入新的模型")
            #png=png.scaledToWidth(150)

            #@cad_view=self.cad_window
            #self.model[i].addWidget(cad_view)
            
            #self.model[i].setMaximumSize(150, 150)
            #self.model[i].setScaledContents(True)
            #self.model[i].move(20,i*155)
    def set_single_dxf_model(self,index_of_model,dxf_model_name):           
            png=QtGui.QPixmap(dxf_model_name)
            ##p#ng=png.scaledToWidth(1000)
            #png=QtGui.QPixmap(QString)
            self.model[index_of_model].setPixmap(png)
            #print("设置dxf图像总共被调用",index_of_model,"次数")
            #self.model[index_of_model]
            '''self.model[index_of_model].setMaximumSize(150, 150)
            self.model[index_of_model].setScaledContents(True)
            self.model[index_of_model].move(20,20+index_of_model*155)'''

    def set_single_dxf_model_to_preview(self,index_of_model,dxf_model_name):           
            #png=QtGui.QPixmap(dxf_model_name)
            ##p#ng=png.scaledToWidth(1000)
            #png=QtGui.QPixmap(QString)
            #self.model[index_of_model].setPixmap(png)
        print(dxf_model_name)
        #self.dxf = ezdxf.readfile(dxf_model_name)

        #####要做类移植，不然没法调用cadviewer的变量。
        self.dxf=ezdxf.readfile(dxf_model_name)
        
        #print("小日本的东西写得成不？")
        self.cad_window.render_context = RenderContext(self.dxf)
        
        #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
        self.cad_window.backend = PyQtBackend(use_text_cache=True)
        print("成功读入")
        self.cad_window.layers.visible_names = None
        self.cad_window.current_layout = None
        print("程序已经走到了这里in set_single_dxf_model_to_preview")
        #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
            action = self.select_layout_menu.addAction(layout_name)
            action.triggered.connect(self.change_layout)'''

        self.cad_window.layers.populate_layer_list(self.cad_window.render_context.layers.values())
        print("程序已经执行完成，是否出现了想要的效果？步子不要迈太大")
        self.cad_window.draw_layout('model')
        #self.cad_window.setWindowTitle('CAD Viewer - ' + dxf_model_name)

        print("程序已经执行完成，是否出现了想要的效果？步子不要迈太大")


    def set_model_to_preview(self,index_of_model,dxf_model_name):           
        print(index_of_model,dxf_model_name)
        self.model_viewer[index_of_model].open_dxf_file(dxf_model_name)

        


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=MyWindow()
    win.show()
    #win.cad_window.open_dxf_file("new_nest.dxf")
    win.cad_window.view.open_file()
    #win.cad_window.show()
    #read_directory('E:/')

    QApplication.processEvents()
             #睡眠一秒
    time.sleep(1)
    #win.showMaximized()
    #win.list_all_dxf_model(10,win.topFiller)
    print("设置图片显示的数量为10")
    #win.set_all_dxf_model(5,"10.jpg")
    #win.cad_window.open_file()
    sys.exit(app.exec_())

   
