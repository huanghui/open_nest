# -*- coding: utf-8 -*-
from multiprocessing.spawn import old_main_modules
from pickle import NONE
from re import L
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

#from layout6 import rectangle
import os
#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from readdxf15 import *
#import sip
from model_copy_move import find_best_width_height


#class cadWindow(QtWidgets.QMainWindow):
class cadPreViewer(QWidget):
    def __init__(self, parent=None):
        super(cadPreViewer, self).__init__(parent)

        self.setWindowTitle('cadViewer')
        self.setGeometry(400,500,1000,500)
        #全局布局（2中）：这里选择水平布局

        ##########重新设计布局，因为不是centralwidget,但后期可以考虑将这个设计为centralwidget
        
        self.wlayout=QHBoxLayout()

        
        self.left_layout=QVBoxLayout()

        self.setLayout(self.wlayout)
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
       
        #self.textlayout=QVBoxLayout()
        


        self.linedit=QLineEdit()
        self.linedit.setFixedWidth(60)
        self.linedit.setStyleSheet("border-width:0;border-style:outset")
    ###########需要设置显示文本框
        self.textbrowser=QTextBrowser()
        self.textbrowser.setFont(QFont("Calibri",11))
        self.textbrowser.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        ##QFont(,10)
        self.textbrowser.setFixedSize(80,80)
        #lineEdit=QLineEdit()
        #self.lineEdit.setValidator(QIntValidator())

        
        #self.wlayout.addWidget(self.linedit)
        #self.wlayout.addWidget(self.textbrowser)
        self.left_layout.addWidget(self.textbrowser)
        self.left_layout.addWidget(self.linedit)
        

        self.wlayout.addLayout(self.left_layout)

        ############定义排版模型的数据,决定了每一次排版的数据的起始位置，很关键，
        ##########并且不断的更新。
        self.start_nest_x=0
        self.start_nest_y=0
        self.old_model_height=0
        self.old_model_width=0

        self.old_nest_number=0

        self.left_rectangle=layout6.rectangle()

        self.rectangle_list=[]
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
            #no_path_name=os.path.basename(self.model_name)
           # print("需要排版的模型名字为",self.textbrowser.append(no_path_name))
            '''width=findMaxXVertex(self.model_name)[0]-findMinXVertex(self.model_name)[0]
            height=findMaxYVertex(self.model_name)[1]-findMinYVertex(self.model_name)[1]
            self.model_size=width+"*"+height'''
            #self.textbrowser.append(self.model_size)
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

    def get_best_width(self,srcdxf,width):
        if(os.path.exists("D2.dxf")):

            os.remove("D2.dxf")
############这里只是做初步的碰撞组合
        movexdxf(srcdxf,2*width).saveas("D2.dxf")
        #movexdxf(srcdxf,width).saveas("D2.dxf")
    #saveas("D2.dxf")
        mix(srcdxf,"D2.dxf","D0.dxf")
        
        ###########微调，如果distance为真
        distance=polyCrash2("D0.dxf")
        errorDistance=distance
        #############
        #############需要进行反复修正2组模型之间的距离,注意是2组
        while(distance>0.2):
            errorDistance+=distance
            os.remove("D0.dxf")
            movexy("D2.dxf",-distance,0)
            mix(srcdxf,"D2.dxf","D0.dxf")
            distance=polyCrash2("D0.dxf")

        MaxX=findMinXVertex("D2.dxf")
        MinX=findMinXVertex(srcdxf)
    ###########我觉得放这里判断是不是很不好？但是动了这个，怕有其他问题。
        #######这个是才是实际的宽度
        width_of_2model=MaxX[0]-MinX[0]
        width=width_of_2model
        if(os.path.exists("D2.dxf")):

            os.remove("D2.dxf")
        if(os.path.exists("D0.dxf")):

            os.remove("D0.dxf")

        return width



    ##########
    '''def  recycle_rectangle(start_x,start_y,nest_nubmer,left_rectangle,w,model_Height,model_Width,row_number):
        
        start_x=(nest_nubmer%row_number)*model_Width
        start_y=(int(nest_nubmer/row_number)+1)*model_Height

        left_rectangle.next_begin_x=start_x
        left_rectangle.next_begin_y=start_y-model_Height
        left_rectangle.left_height=model_Height  #######left_height=model_height是一定的。
        left_rectangle.left_width=w-start_x

        old_model_height=model_Height
        old_model_width=model_Width
        old_nest_layers=int(nest_nubmer/row_number)
        old_nest_number=nest_nubmer

        #return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
            #old_nest_number,left_height,left_rectangle
'''

    def start_nest(self,number_for_nest,model_name,width,height,\
        start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
            old_nest_number,left_height,left_rectangle,rectangle_list):
        

        print("模型的start_x的位置为",start_x,"模型的start_y值为",start_y,"number_for_nest的值为",number_for_nest)
        nest_number=int(number_for_nest)
        model=model_name
        w=width
        h=height


        dx=2
        dy=2
        '''这里必须算出来模型的最大值和最小值，然后再去计算，不然很难搞的。'''
        ########
        #########找到d4文件，可以分析出来这个文件的最大的值和最小值。
        '''if(os.path.exists("D4.dxf")):

            max_y=findMaxYVertex("D4.dxf")
        '''
        #######暂时先定义为0
        if (left_height):
        
            left_height=left_height
        else:
            left_height=0
        if(os.path.exists("3.dxf")):
            os.remove("3.dxf")
            rotate_zdxf(model,0 ,"3.dxf")
        else:
            rotate_zdxf(model,0 ,"3.dxf")
        ########计算模型的高度和最合适的宽度，注意，有些模型可以拼合起来得到最合适的宽度
        ##########必须要组合起来才能得知，单个模型算不出来的。
        if(os.path.exists("edge.dxf")):
            os.remove("edge.dxf")
            [model_Height,model_Width]=find_best_width_height("3.dxf","edge.dxf",dx,0)
        else:
            [model_Height,model_Width]=find_best_width_height("3.dxf","edge.dxf",dx,0)
        
        ########这里有2种排版方式
        '''1，直接在上层排版'''

        #######如果是组合排版，那么2个模型组合的高度有可能高于原有模型，所以必须重新赋值。
        model_Height=findMaxYVertex("edge.dxf")[1]-findMinYVertex("edge.dxf")[1]+dy

        two_mixed_model_width=findMaxXVertex("edge.dxf")[0]-findMinXVertex("edge.dxf")[0]
        mixed_row_number=int((w*2)/two_mixed_model_width)
        #########这里是解决组合高度的问题，但是组合宽度的问题没有解决。
        print("组合模型的最终最适合的高度是",model_Height)
        print("self.old_model_height的值为",old_model_height,"这个值很关键")
        if(model_Height>old_model_height+0.01):
            #####原有的空间不适合排版，必须新1起1行排版。所以start_x=0
            print("最新排版的模型比上一个排版的模型高时")

            print("model_Height==",model_Height,"left_height==",left_height)
            #########直接在这里上矩形排版吧。
            for rect in rectangle_list:
                if(model_Height<rect.left_height and  model_Width<left_rectangle.left_width):
                    

            if(model_Height<left_rectangle.left_height and model_Width<left_rectangle.left_width):
                rectangle_nest_number=(int(left_rectangle.left_height/model_Height))*int(left_rectangle.left_width/model_Width)

                if(nest_number>rectangle_nest_number or rectangle_nest_number==nest_number):

                        nest_with_rest(model,rectangle_nest_number,left_rectangle.left_wdith,left_rectangle.left_height,model_Width,model_Height)

                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            rectangle_nest_number=rectangle_nest_number-1
                            nest_with_rest(model,rectangle_nest_number,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",left_rectangle.next_begin_x+dx-delt_x,left_rectangle.next_begin_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("直接进入左边矩形排版")


                        rest_number=nest_number-rectangle_nest_number

                        nest_with_rest(model,rest_number,w,h,model_Width,model_Height)

                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            rest_number=rest_number-1
                            row_number,num_of_height=nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("直接进入左边矩形排版")


                        #######可以定义一个函数专门回收这个面积。
                        start_x=(rest_number%row_number)*model_Width
                        start_y=(int(rest_number/row_number)+1)*model_Height

                        left_rectangle.next_begin_x=start_x
                        left_rectangle.next_begin_y=start_y-model_Height
                        left_rectangle.left_height=model_Height  #######left_height=model_height是一定的。
                        left_rectangle.left_width=w-start_x

                        old_model_height=model_Height
                        old_model_width=model_Width
                        old_nest_layers=int(rest_number/row_number)
                        old_nest_number=nest_number

                        return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                            old_nest_number,left_height,left_rectangle
                        #######这个时候不需要切割原有的矩形了，因为原有的矩形已经满了，
                        ########只需要切割剩下的矩形。
                else:
                        #if(nest_number<rectangle_nest_number):
                        ######我感觉这个可以函数处理，不然这样太浪费版面了。
                    nest_with_rest(model,nest_number,left_rectangle.left_width,left_rectangle.left_height,model_Width,model_Height)                        
                    delt_x=findMinXVertex("D4.dxf")[0]

                    delt_max_x=findMaxXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]
                    real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                    if(start_x+real_width_of_gap>w):
                        os.remove("D4.dxf")
                        rectangle_nest_number=rectangle_nest_number-1
                        nest_with_rest(model,rectangle_nest_number,w,h,model_Width,model_Height)
                        delt_x=findMinXVertex("D4.dxf")[0]
                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                    movexy("D4.dxf",left_rectangle.next_begin_x+2*dx-delt_x,left_rectangle.next_begin_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                    print("当模型的左宽足够容纳排版的熟练时，直接在矩形内排版")

                        #####回收资源
                        ####因为此时是不够排第二行的，而且这里是不够排的，那么这个牌面，不是很好打，超过1半了，哪个长方体的
                        #########会比较好一点的。
                    start_x=nest_number*model_Width+start_x
                        #start_y=(int(rest_number/row_number)+1)*model_Height
                    start_y=start_y

                    left_rectangle.next_begin_x=start_x
                    left_rectangle.next_begin_y=start_y-old_model_height
                    left_rectangle.left_height=old_model_height  #######left_height=model_height是一定的。
                    left_rectangle.left_width=w-start_x

                    old_model_height=model_Height
                    old_model_width=model_Width
                    old_nest_layers=1
                    old_nest_number=nest_number

                    rectangle_list.append(left_rectangle)

                    return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                        old_nest_number,left_height,left_rectangle,rectangle_list


            ########剩余高度还可以容纳的情况下。
            if(model_Height<left_height ):
                
                print("当模型的高度小于宽沟的高度时，模型的高度为",model_Height,"宽沟left_height==",left_height,"start_x的值为",start_x,"start_y的值为",start_y)
                ##

                start_y=start_y-left_height

                ###这里出现了巨大的错误，不是start_x，start-x=0是没错的。
                #vast_left_width=w-start_x
                #########
                old_nest_number_per_layer=int(w/(old_model_width+dx))

                ######这个判断应该不太对吧
                #if(old_nest_number<old_nest_number_per_layer  ):
                    ####当排版模型连剩下的一行都不够时，那么这个值就应当重新考虑。
                #vast_left_width=w-start_x
                #else:
                ######这里应该是计算start_x吧，有时候是x有时候又是这个。这是个新的错误。
                vast_left_width=w-(old_model_width+dx)*old_nest_number_per_layer


                vast_gap_second_number_layer=int(vast_left_width/model_Width)
                right_gap_start_x=(old_model_width+dx)*old_nest_number_per_layer+dx

                if(vast_gap_second_number_layer==0):
                    #vast_left_width=(int(old_nest_number/(old_nest_layers+1)))*old_model_width
                    vast_left_width=max(w-start_x,(int(old_nest_number/(old_nest_layers+1)))*old_model_width)
                    if(old_nest_number*old_model_width>vast_left_width):
                        print("vast_gap_second_number_layer==0,证明vast_left_width的值不太对,寨沟的值不太对,只能是根据这些参数去分析他的宽度,其实这个办法是不对的。")
                        #vast_left_width=(int(old_nest_number/(old_nest_layers+1)))*old_model_width
                        #vast_left_width=w-start_x
                        #start_x=w-vast_left_width
                        #start_x=w-vast_left_width+dx
                        #start_y=start_y+old_nest_layers*old_model_height
                        print("start_x==",start_x,"vast_left_width==",vast_left_width)
            
                        vast_gap_second_number_layer=int(vast_left_width/model_Width)
                        print("vast_left_width==",vast_left_width)
                        right_gap_start_x=w-vast_left_width
                        
                        left_height=left_height-start_y

                        start_y=start_y+(old_model_height+dx)*(old_nest_layers+1)
                    else:
                        print("宽沟的排版宽度比排版的数量多")

                        vast_gap_second_number_layer=max(int(vast_left_width/model_Width),int(2*vast_left_width/two_mixed_model_width))

                        right_gap_start_x=start_x

                vast_gap_nest_layers=int(left_height/model_Height)

                print("model_width==",model_Width,"vast_left_width==",vast_left_width,"vast_gap_second_number_layer==",vast_gap_second_number_layer,"vast_gap_nest_layers==",vast_gap_nest_layers)

                vast_gap_second_number=vast_gap_second_number_layer*vast_gap_nest_layers

                
                #right_gap_start_x=(old_model_width+dx)*old_nest_number_per_layer+dx

                print("nest_number==",nest_number,"vast_gap_seconde_number==",vast_gap_second_number,"vast_gap_nest_layers==",vast_gap_nest_layers,)
                if(nest_number>vast_gap_second_number):
                    
                    row_number,old_nest_layers=nest_with_rest(model,vast_gap_second_number,vast_left_width,h,model_Width,model_Height)
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    delt_max_x=findMaxXVertex("D4.dxf")[0]

                    width_of_after_nest=delt_max_x-delt_x

                    if(start_x+width_of_after_nest>w):
                        vast_gap_second_number=vast_gap_second_number-1
                        #if(os.path.exists("D4.dxf")):
                        os.remove("D4.dxf")
            
                        row_number,old_nest_layers=nest_with_rest(model,vast_gap_second_number,vast_left_width,h,model_Width,model_Height)
                        delt_x=findMinXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]

                    #delt_max_x=findMaxXVertex("D4.dxf")[0]
                    ########这里不是start_x了，而是left_start_x
                    #old_nest_number_per_layer=int(w/old_model_width)
                    #right_gap_start_x=old_model_width*old_nest_number_per_layer

                    movexy("D4.dxf",right_gap_start_x+dx-delt_x,start_y+dx-delt_y)

                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                    nest_number=nest_number-vast_gap_second_number
                    

                else:
                    row_number,old_nest_layers=nest_with_rest(model,nest_number,w,h,model_Width,model_Height)

                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]
                    movexy("D4.dxf",right_gap_start_x+dx-delt_x,start_y+dx-delt_y)

                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                    nest_number=0 
                start_y=start_y+left_height
                ######这里的left_height并不等于model_height，
                print("start_y==",start_y,"left_height==",left_height)


                ######这里对于left_heihgt的值并不能随便修改的，但这个赋值明显有点错误的，估计还需要

                #########model_height的值为多少
                #left_height=model_Height+left_height-model_Height
                left_height=model_Height*(old_nest_layers+1)
                start_x=(nest_number-vast_gap_second_number)*model_Width

            else:
                #####
                print("如果模型高度比窄沟的left高度要高。","left_height==",left_height,"start_y==",start_y,"old_model_height==",old_model_height)
                if(left_height==old_model_height ):

                    ######当模型的高度==之前的高度时，
                    start_y=start_y+old_model_height
                    #start_y=start_y
                    #if()
                    #start_x=old_model_width*old_nest_number
                    print("这里出现start_y或许不应该增加。")
                #left_height=model_Height

                #if()
            ###########如果model_height的高度比left_heihgt还要搞，那么间隙就不变呗，为啥要变化。
                #left_height=model_Height
            
                #print("left_height==",left_height,"start_y==",start_y,"old_model_height==",old_model_height

            ########只有当Nest_number大于0的时候才会开始排版。
            if(nest_number>0):
            ######当之前的剩余空间能够用并且能够满足，那么就要去找这个空间
            #if()
                start_x=0
                #######当新的模型比原来的模型高时，需要新起一行
                '''if(start_y+old_model_height<h or start_y+old_model_height<6000):
                    start_y=start_y+old_model_height'''
                #######这里是多余做了这一层吧
                #start_y=start_y+old_model_height
                print("star_y的值为",start_y)
                #@##因为这里的配对比前面的配对是高一个模型的高度的。
                ########这里又出现了配对错误，因为上一次的
                #########这里需要分情况讨论了，不然可能无解，老是出现这个问题。
                ############这里又碰到了这个问题，可能我需要设置一个条件，感觉是上一个条件排版完，没有更新？
                #############高度差存在多余在增加。
                #@start_y=start_y+old_model_height
                start_y=start_y
                row_number,old_nest_layers=nest_with_rest(model,nest_number,w,h,model_Width,model_Height)
                delt_x=findMinXVertex("D4.dxf")[0]
                delt_y=findMinYVertex("D4.dxf")[1]

                #delt_max_x=findMaxXVertex("D4.dxf")[0]
                #real_nest_width=
                #mix("D4.dxf","xy.dxf","new_nest.dxf")

                ##########移动2mm为了保证模型产生的间距合理
                movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                if(old_model_height==0):
                    print("第二次进入到这个里面了吗")
                    mix("D4.dxf","xy.dxf","new_nest.dxf")
                else:
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                    ######这里需要询问一下组合1行可以放多少个，不是简单的model_width的关系
                
                #row_number=max(int(1500/model_Width),mixed_row_number)
                print("单个模型的宽度为",model_Width,"双模型的宽度为",mixed_row_number,"nest_number的值为",nest_number,"row_number的值为",row_number)
                try:
                    ######这里的盲目增加1是有bug的，如果不
                    if(nest_number%row_number):
                        layers=int(nest_number/row_number)+1
                        print("排版后的模型层数为",layers)
                    else:
                        layers=int(nest_number/row_number)
                except:
                    layers=1
                #start_y=layers*model_Height+start_y

    ##############这里是个严重的错误吧！！！！！！！这里怎么能是
                #start_y=layers*model_Height+old_model_height

                start_y=layers*model_Height+start_y####这里不是上面狗屁layers+model_heihgt而是原
                ######这里的描述似乎是最上层的start_y的值吧。
                ########这里并没有定义start_x的值，这里是需要定义的。

                ##########这里还是获取模型的的最大值吧，直接测量起码是争取的，否则很多计算容易把数据跑飞了。

                ######model_width预计进行修正和优化，由于row_number的值有可能和之前的不一样。
                reaL_actual_width_after_nest=w/row_number
                start_x_1=(nest_number%row_number)*model_Width

                start_x_2=(nest_number%row_number)*reaL_actual_width_after_nest
                ####这里是获取start_x的值的最小值吗？应该是最大值吧
                #start_x=min(start_x_1,start_x_2)
            #######改成最大值试试看吧
            ########取平均值比较好
                #start_x=(start_x_1+start_x_2)/2
                #start_x=max(start_x_1,start_x_2)###
                ####增加排版补偿。
                start_3=((nest_number%row_number)*two_mixed_model_width)/2
                two_mixed_model_width
                if(start_x_1>start_x_2):
                    '当实际的数量大于计算的数量，那么start_x_1的,一般会大于'
                    #start_x=start_x_2+reaL_actual_width_after_nest/3
                    start_x=start_3
                    old_model_width=reaL_actual_width_after_nest
                
                ######这里需要标注模型的高度了
                else:
                    start_x=start_x_2
                    old_model_width=model_Width

                
                old_model_height=model_Height
                old_nest_number=nest_number

                ########这里的Layers是包含了剩余的高度，所以要
                if(nest_number%row_number):
                    layers=int(nest_number/row_number)+1
                    print("排版后的模型层数为",layers)
                    left_height=(layers-1)*model_Height
                else:
                    #layers=int(nest_number/row_number)
                    left_height=layers*model_Height
                left_height=(layers-1)*model_Height
                left_width_after_nest=w-int(w/model_Width)
                ######
                #######有个实际的排版宽度，其实这里最好的办法是获取模型的最大的宽度坐标，而不是这么去计算。
                #old_model_width=max(reaL_actual_width_after_nest,model_Width)

                print("")
                left_rectangle.next_begin_x=start_x
                left_rectangle.next_begin_y=start_y-model_Height
                left_rectangle.left_height=model_Height  #######left_height=model_height是一定的。
                left_rectangle.left_width=w-start_x

                rectangle_list.append(left_rectangle)



        else:
            print("当新排版的模型高度<旧模型的高度时","新模型的高度为",model_Height,"旧模型的高度为",old_model_height)
            if((old_model_height/2)<model_Height<old_model_height or model_Height<old_model_height+0.01):   
                left_width=w-start_x

                if(model_Height<left_rectangle.left_height and model_Width<left_rectangle.left_width):
                    rectangle_nest_number=(int(left_rectangle.left_height/model_Height))*int(left_rectangle.left_width/model_Width)
                    if(nest_number>rectangle_nest_number or rectangle_nest_number==nest_number):

                        nest_with_rest(model,rectangle_nest_number,left_rectangle.left_wdith,left_rectangle.left_height,model_Width,model_Height)

                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            rectangle_nest_number=rectangle_nest_number-1
                            nest_with_rest(model,rectangle_nest_number,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",left_rectangle.next_begin_x+dx-delt_x,left_rectangle.next_begin_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("直接进入左边矩形排版")


                        rest_number=nest_number-rectangle_nest_number

                        nest_with_rest(model,rest_number,w,h,model_Width,model_Height)

                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            rest_number=rest_number-1
                            row_number,num_of_height=nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("直接进入左边矩形排版")


                        #######可以定义一个函数专门回收这个面积。
                        start_x=(rest_number%row_number)*model_Width
                        start_y=(int(rest_number/row_number)+1)*model_Height

                        left_rectangle.next_begin_x=start_x
                        left_rectangle.next_begin_y=start_y-model_Height
                        left_rectangle.left_height=model_Height  #######left_height=model_height是一定的。
                        left_rectangle.left_width=w-start_x

                        old_model_height=model_Height
                        old_model_width=model_Width
                        old_nest_layers=int(rest_number/row_number)
                        old_nest_number=nest_number

                        rectangle_list.append(left_rectangle)

                        return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                            old_nest_number,left_height,left_rectangle,rectangle_list
                        #######这个时候不需要切割原有的矩形了，因为原有的矩形已经满了，
                        ########只需要切割剩下的矩形。
                    else:
                        #if(nest_number<rectangle_nest_number):
                        ######我感觉这个可以函数处理，不然这样太浪费版面了。
                        nest_with_rest(model,nest_number,left_rectangle.left_width,left_rectangle.left_height,model_Width,model_Height)                        
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            rectangle_nest_number=rectangle_nest_number-1
                            nest_with_rest(model,rectangle_nest_number,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]
                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",left_rectangle.next_begin_x+2*dx-delt_x,left_rectangle.next_begin_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("当模型的左宽足够容纳排版的熟练时，直接在矩形内排版")

                        #####回收资源
                        ####因为此时是不够排第二行的，而且这里是不够排的，那么这个牌面，不是很好打，超过1半了，哪个长方体的
                        #########会比较好一点的。
                        start_x=nest_number*model_Width+start_x
                        #start_y=(int(rest_number/row_number)+1)*model_Height
                        start_y=start_y

                        left_rectangle.next_begin_x=start_x
                        left_rectangle.next_begin_y=start_y-old_model_height
                        left_rectangle.left_height=old_model_height  #######left_height=model_height是一定的。
                        left_rectangle.left_width=w-start_x

                        old_model_height=model_Height
                        old_model_width=model_Width
                        old_nest_layers=1
                        old_nest_number=nest_number

                        rectangle_list.append(left_rectangle)

                        return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                            old_nest_number,left_height,left_rectangle,rectangle_list

                #########当old_model_width与组合宽度的平均宽度不一致时，仍任会产生这个错误的。
                print("old_model_nest_number的值为",old_nest_number,"int(w/old_model_width)的值为",int(w/old_model_width))
                #old_
                old_nest_number_per_layer_after_=int(w/old_model_width)
                #if(old_nest_number%(int(w/old_model_width)) and  int (old_nest_number/int(w/old_model_width))>1):
                #####只有old1_nest_number不够一排的才能有空间给剩下的使用。
                #if(old_nest_number%old_nest_number_per_layer_after_ and int(old_nest_number/old_nest_number_per_layer_after_)<1):  
                if(old_nest_number%old_nest_number_per_layer_after_ ):  
                    print("start_y==",start_y,"old_model_height==",old_model_height)
                    start_y=start_y-old_model_height###########
                   #start_y=start_y-left_height
                    print("start_y==",start_y,"old_model_height==",old_model_height)
                else:
                    start_y=start_y

                ######这里的高度已经完全没问题了，那么现在还要增加一个配置就是宽度的比较。              

                ############
                ########这里需要更新start_x和start_y的值
                print("当(old_model_height/2)<model_Height<old_model_height是,start_x=",start_x,"start_y=",start_y)

                ########由于涉及到组合模型的问题，这里需要重新计算到底能存放多少模型。
                ########这里计算
                two_model_compound_width=findMaxXVertex("edge.dxf")[0]-findMinXVertex("edge.dxf")[0]


                best_width_2model=self.get_best_width("edge.dxf",two_model_compound_width)
               #other_model_num=max(int(left_width/model_Width),int(left_width/(2*two_model_compound_width)))
                
                ####但这里有个问题就是估计以后会产生干涉，还是有问题，所以需要验证。

                ##########这样定义model_Width稍微有点草率，因为尾巴
                model_Width=best_width_2model/2
                other_model_num=int(left_width*2/best_width_2model)
                print("模型的other_model_num的大小为",other_model_num)
                #while(((other_model_num*best_width_2model)/2)>left_width):
                #  # other_model_num=other_model_num-2
                if(other_model_num%2):
                    other_model_num=other_model_num-1
                    #####当模型数量太小，有可能超出模型范围。
                if(other_model_num==2):
                    if(two_mixed_model_width>left_width):
                        other_model_num=other_model_num-1

                #if(((other_model_num/2)*two_model_compound_width+model_Width)<left_width):
                    #other_model_num=other_model_num+1

                ###########这里直接去找d4的最大X值也是可以的，但是有点浪费资源了。

                old_nest_number_per_layer=int(w/old_model_width)

                last_rest_gap=w-old_model_width*old_nest_number_per_layer-(old_nest_number_per_layer+1)*dx

                print("old_model_width的值为",old_model_width,'int(w/old_model_width)的,也即上一个模型的单排排版数量为',int(w/old_model_width))

                print("右边窄沟道的值，last_rest_gap的值为",last_rest_gap)
                nest_number_for_narrow_gap=0
                if(last_rest_gap>model_Width):
                    #####在最后剩下的宽度能排版的数量
                    print("极端情况下，最后一个模型的空隙还能做。")
                    nest_last_rest_number_per_layer=int(last_rest_gap/model_Width)
                    ##########这下问题很复杂了。
                    print("nest_in_last_rest_number的值为",nest_last_rest_number_per_layer)
                    ##########获取这个参数有难度，基本上无法做。
                    right_gap_start_y=start_y-old_nest_layers*old_model_height
                    old_nest_base_height=old_nest_layers*old_model_height
                    right_gap_start_x=w-last_rest_gap
                    #left_width=last_rest_gap
                    #for(i  in range(0,old_nest_layers)):  
                    ###########这种极端情况下就不要再进行精确的计算了。
                    nest_number_for_narrow_gap=nest_last_rest_number_per_layer*old_nest_layers
                    print("小沟窄可以容纳的数量为",nest_number_for_narrow_gap)
                    ###########当要排版的数量大于现在沟道数量，那么
                    if(nest_number>nest_number_for_narrow_gap or nest_number==nest_number_for_narrow_gap ):

                        print("当寨沟容纳的数量小于总数时")
                    #####对特殊的勾到进行排版
                        nest_with_rest(model,nest_number_for_narrow_gap,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                        delt_x=findMinXVertex("D4.dxf")[0]
                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x

                        movexy("D4.dxf",right_gap_start_x+2-delt_x,right_gap_start_y+2-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                    else:
                        if(nest_number>nest_last_rest_number_per_layer):
                            nest_with_rest(model,nest_number,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]
                            delt_max_x=findMaxXVertex("D4.dxf")[0]                        
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x

                            movexy("D4.dxf",right_gap_start_x+2-delt_x,right_gap_start_y+2-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        else:
                            nest_with_rest(model,nest_number,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]
                            delt_max_x=findMaxXVertex("D4.dxf")[0]                        
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x

                            movexy("D4.dxf",right_gap_start_x-delt_x,right_gap_start_y-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                if(last_rest_gap>model_Width):
                    rest_number_after_narrow_gap_nest=nest_number-nest_number_for_narrow_gap
                else:
                    ##########寨沟不能排版，那么就只能是宽沟排了
                    nest_number_for_narrow_gap=0
                    #########rest_number_after_narrow_gap_nest可不是0,  
                    rest_number_after_narrow_gap_nest=nest_number

                'other_model_num的值为也即是最后一排的剩余排版数量，这里不能简单的等于'

                ''
                print("rest_number_after_narrow_gap_nest的值为",rest_number_after_narrow_gap_nest)
                #other_model_num=rest_number_after_narrow_gap_nest
                if(rest_number_after_narrow_gap_nest>0 ):

                    ########如果排完最后一行还有多
                    if(rest_number_after_narrow_gap_nest>other_model_num):
############################################################
#########################################################
                        print("other_model_num的大小为",other_model_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                        nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)

                #########获取模型的位置坐标
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x

                        ###########这里要对start_x和start_y作一番更改，由于之前的排版扰乱了start-x和start_y,
                        ###########这里不改动最好,改动前面的比较好，
                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            other_model_num=other_model_num-1
                            nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x-delt_x,start_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("测试的模型应该在这里合并才对")

                        rest_number=rest_number_after_narrow_gap_nest-other_model_num
                        start_x=0
                        start_y=start_y+old_model_height

                        print("下一次排版的start_y的值为",start_y)
                        #######这里应该需要对D4.dxf进行清零，不然容易出错。
                        ##########
                        if os.path.exists("D4.dxf"):
                            os.remove("D4.dxf")

                    else:

                        ##########当宽沟的排版数量足以容纳需要排版的模型时
                        other_model_num=rest_number_after_narrow_gap_nest
                        print("rest_number_after_narrow_gap_nest的大小为",rest_number_after_narrow_gap_nest,"other_model_num的值为",other_model_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                        #other_model_num=，rest_number_after_narrow_gap_nest
                        nest_with_rest(model,rest_number_after_narrow_gap_nest,w,h,model_Width,model_Height)

                #########获取模型的位置坐标
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            other_model_num=other_model_num-1
                            nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("测试的模型应该在这里合并才对")
                        ########因为是一个新的模型了，这个里必须要更新新的x和y的排版起点了。
                        #####在这里增加高度是非常不对的，
                        #######这里的start_x=0是不对的，很明显是start_x保持不动。
                        #start_x=0
                        ########这里貌似start_y也是错误的，因为这里的，model_height还是比old_model_height低的。
                        #start_y=start_y+old_model_height
                        rest_number=-1

                        ################
                        ##########这里的start_x的值并不确定是多少，不能随便写成是0吧，因为这个排版的并不是为0
                        #start_x=0
                        #####这里还要分情况处理。如果后面还有空间，那么就得继续保留。
                        
                        #start_x=old_model_width*rest_number_after_narrow_gap_nest+(rest_number_after_narrow_gap_nest+1)*dx
                        #start_y=start_y+old_model_height

                        start_x=start_x+model_Width*rest_number_after_narrow_gap_nest+(rest_number_after_narrow_gap_nest+1)*dx 
                        ########f这里的start_x和start_y的计算都出现了错误。
                        ########若果沟道可以容纳足量的排版数量，那么应该可以start_y的数据就应该加起来才行。
                        start_y=start_y+old_model_height
                        ########这里的start_y的值是多少应该是保持不变吧。
                        ########这里的Leftheight有点不对吧，是对的，但是Model_height不太对。
                        left_height=old_model_height
                        left_widt=w-start_x
                        print("下一次排版的start_y的值为",start_y,"下一次排版的start_x的值==",start_x,"left_height==",left_height)
                        #######这里应该需要对D4.dxf进行清零，不然容易出错。
                        ##########
                        if os.path.exists("D4.dxf"):
                            os.remove("D4.dxf")
                  ########拍完寨沟的数量，那么接下来是排宽沟的数量了
                #other_model_num=nest_number-nest_number_for_narrow_gap
                ######宽沟
                '''vast_gap_nest_num=nest_number-nest_number_for_narrow_gap
                print("排完寨沟的数量后other_model_name的值为",vast_gap_nest_num)
                if(vast_gap_nest_num>0 and vast_gap_nest_num ):

                    #print("other_mode")
                    os.remove("D4.dxf")
                    nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)'''
                #rest_number=nest_number-nest_number_for_narrow_gap-rest_number_after_narrow_gap_nes
                ########这里不需要再定义了，因为前面已经定义了。
                print("rest_number的值为",rest_number,'other_model_num的值为',other_model_num,'寨沟的值为',nest_number_for_narrow_gap)
                
                #######从优先级来排，这里要排的是other_Model_num了。 #          
                            #######再来排剩下的从新的一层开始,当然这里要判断是不是剩下的已经排版完成了
                #####这里存在巨大的bug，因为other_model_num根本没有确定。 
                if(rest_number>0):
                    print("rest_number的值为",rest_number)
                    #############这里是rest_number的排版，starty就必须更新到新的一层了。
                    nest_number_per_line,y_number_of_height=nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                    #####delt_x是计算随意排版的偏移值的，在后续的模型里面应该不需要。
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    print("最后剩余的模型的start_y模型的排版位置为",start_y)
                    movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                    #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                    #这里应该是不用更新高度，因为还没有满。
                    #start_y=start_y+old_model_height
                    #############这里不一定增加高度，因为还有一个问题是如果rest_number不够一行怎么办？
                    #########因为上面统一都加了1那么这里加1才是对的。
                    actual_layers=int((rest_number*model_Width)/w)
                    actual_height=actual_layers*model_Height


                    actual_layers=int((rest_number*model_Width)/w)+1
                    actual_height=actual_layers*model_Height
                    ##########这里的start_x可能会有严重的bug，到处都是bug,这里应该去最好的bestwidth
                    ###########果然就碰到了，现在处理一下,这里的model width确实有点问题的，为了避免延时
                    ######直接先加个补偿。

                    ########这里是查不到的，因为不止一行。
                    start_x=model_Width*int((rest_number%nest_number_per_line))+(model_Width)*(6/5)                    
                    start_y=start_y+actual_height
                    print("排版后得到的start_x的值为",start_x,"排版后的start_y的值为",start_y,"rest_number%(w/model_Width)的值为",rest_number%(w/model_Width),"model_width的值为",model_Width)
                else:
                    #######
                    print("rest_number的值为小于0,也即不需要增加排版,没有多余的排版。所以other_num的值为剩余的值")
                    ####
                    #start_x=start_x+other_model_num*model_Width+(other_model_num+1)*dx
                    ######start_y保持不变                   
                    start_x=start_x
                    start_y=start_y
                    #left_height=
                    ###modle_height还是要在这里更新，不然问题肯定不对。但也不一定正确，先试试看吧                    #old_model_height=model_Height

            ######如果模型的高度比旧模型的高度的1/2都小
            elif(model_Height<(old_model_height/2)):

                if(old_nest_number%(int(w/old_model_width))):
                    
                    start_y=start_y-old_model_height###########
                else:
                    start_y=start_y
                #####
                left_width=1500-start_x
                ###这个软件    
                print("<1/2的left_width的值为",left_width,"start_x的值为",start_x)

                
                gap_row_num=max(int(left_width/model_Width),int(2*left_width/two_mixed_model_width))
                #mixed_row_number
                
                print("旧模型的高度是新模型的2倍大小以上时,窄沟容纳的模型数量为",gap_row_num)
                gap_layers=int(old_model_height/model_Height)
                other_model_num=gap_row_num*gap_layers

                ##如果是奇数就得在额外增加一个排版
                if((float(left_width/model_Width)-gap_row_num)>0.5):
                    #if()
                    #gap_row_num=gap_row_num+1
                    if((gap_row_num+1)*model_Width<left_width):
                        gap_row_num=gap_row_num+1
                        other_model_num=other_model_num+gap_layers*1
                    else:
                    #nest_number=nest_number-1*gap_layers #####因为这里多塞了1个model进去了
                        other_model_num=other_model_num
                print("other_model_num的大小为",other_model_num,"gap_layers的值为",gap_layers)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                ###########计算窄沟容纳数量
                two_model_compound_width=findMaxXVertex("edge.dxf")[0]-findMinXVertex("edge.dxf")[0]

                best_width_2model=self.get_best_width("edge.dxf",two_model_compound_width)
               #other_model_num=max(int(left_width/model_Width),int(left_width/(2*two_model_compound_width)))
                
                ####但这里有个问题就是估计以后会产生干涉，还是有问题，所以需要验证。
                ##########这样定义model_Width稍微有点草率，因为尾巴
                model_Width=best_width_2model/2
                other_model_num=int(left_width*2/best_width_2model)
                print("模型的other_model_num的大小为",other_model_num)
                #while(((other_model_num*best_width_2model)/2)>left_width):
                #  # other_model_num=other_model_num-2
                if(other_model_num%2):
                    other_model_num=other_model_num-1
                    #####当模型数量太小，有可能超出模型范围。
                if(other_model_num==2):
                    if(two_mixed_model_width>left_width):
                        other_model_num=other_model_num-1

                #if(((other_model_num/2)*two_model_compound_width+model_Width)<left_width):
                    #other_model_num=other_model_num+1


                    ##########对于沟道的计算需要慢慢的体验。
                #########当新模型的宽度大于旧模型的宽度时。
                ##############
                ################灾难性质的计算开始了

                ###########这里直接去找d4的最大X值也是可以的，但是有点浪费资源了。

                old_nest_number_per_layer=int(w/old_model_width)

                last_rest_gap=w-old_model_width*old_nest_number_per_layer-(old_nest_number_per_layer+1)*dx

                print("old_model_width的值为",old_model_width,'int(w/old_model_width)的,也即上一个模型的单排排版数量为',int(w/old_model_width))

                print("右边窄沟道的值，last_rest_gap的值为",last_rest_gap,"model_width==",model_Width)
                nest_number_for_narrow_gap=0
                if(last_rest_gap>model_Width):
                    #####在最后剩下的宽度能排版的数量
                    print("当新模型的宽度小于旧模型的宽度，并且右边还能塞进去的情况下，最后一个模型的空隙还能做。")
                    nest_last_rest_number_per_layer=int(last_rest_gap/model_Width)
                    ##########这下问题很复杂了。
                    print("nest_in_last_rest_number的值为",nest_last_rest_number_per_layer)
                    ##########获取这个参数有难度，基本上无法做。
                    #narrow_gap_layers=
                    #########由于这里的高度小于<1/2的old高度，所以这里至少要乘以2还不止。
                    right_gap_start_y=start_y-old_nest_layers*old_model_height

                    old_nest_base_height=old_nest_layers*old_model_height

                    right_gap_start_x=w-last_rest_gap

                    #left_width=last_rest_gap

                    #for(i  in range(0,old_nest_layers)):  
                    ###########这种极端情况下就不要再进行精确的计算了。
                    new_narrow_gap_layers=int((old_nest_layers*old_model_height)/model_Height)
                    nest_number_for_narrow_gap=nest_last_rest_number_per_layer*new_narrow_gap_layers

                    print("小沟窄可以容纳的数量为",nest_number_for_narrow_gap)

                    ###########当要排版的数量大于现在沟道数量，那么
                    if(nest_number>nest_number_for_narrow_gap or nest_number==nest_number_for_narrow_gap ):

                        print("当寨沟容纳的数量小于总数时")
                    #####对特殊的勾到进行排版
                        nest_with_rest(model,nest_number_for_narrow_gap,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                        delt_x=findMinXVertex("D4.dxf")[0]
                        delt_max_x=findMaxXVertex("D4.dxf")[0] 
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x

                        movexy("D4.dxf",right_gap_start_x+2-delt_x,right_gap_start_y+2-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                    else:
                        if(nest_number>nest_last_rest_number_per_layer):
                            nest_with_rest(model,nest_number,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]
                            delt_max_x=findMaxXVertex("D4.dxf")[0]                        
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x

                            movexy("D4.dxf",right_gap_start_x+2-delt_x,right_gap_start_y+2-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        else:
                            nest_with_rest(model,nest_number,last_rest_gap,old_nest_base_height,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]
                            delt_max_x=findMaxXVertex("D4.dxf")[0]                   
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x

                            movexy("D4.dxf",right_gap_start_x-delt_x,right_gap_start_y-delt_y)
                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                if(last_rest_gap>model_Width):
                    rest_number_after_narrow_gap_nest=nest_number-nest_number_for_narrow_gap
                else:
                    ##########寨沟不能排版，那么就只能是宽沟排了
                    nest_number_for_narrow_gap=0
                    #########rest_number_after_narrow_gap_nest可不是0,  


                    rest_number_after_narrow_gap_nest=nest_number


                'other_model_num的值为也即是最后一排的剩余排版数量，这里不能简单的等于'

                ''
                print("rest_number_after_narrow_gap_nest的值为",rest_number_after_narrow_gap_nest)
                #other_model_num=rest_number_after_narrow_gap_nest
                if(rest_number_after_narrow_gap_nest>0 ):

                    ########按照管理这里需要减去一个高度，但我不知道为什么之前的没有减去。
                    #start_y=start_y-old_model_height
                    ########如果排完最后一行还有多
                    vast_gap_nest_num=other_model_num*gap_layers
                    if(rest_number_after_narrow_gap_nest>vast_gap_nest_num):
############################################################
#########################################################
                        print("vast_gap_nest_num的大小为",vast_gap_nest_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                        nest_with_rest(model,vast_gap_nest_num,left_width,h,model_Width,model_Height)

                #########获取模型的位置坐标
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x

                        ###########这里要对start_x和start_y作一番更改，由于之前的排版扰乱了start-x和start_y,
                        ###########这里不改动最好,改动前面的比较好，
                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            vast_gap_nest_num=vast_gap_nest_num-1
                            nest_with_rest(model,vast_gap_nest_num,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x+dx-delt_x,start_y+dy-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        print("测试的模型应该在这里合并才对")
                        ########因为是一个新的模型了，这个里必须要更新新的x和y的排版起点了。
                        #####在这里增加高度是非常不对的，
                        #######这里的start_x=0是不对的，很明显是start_x保持不动。
                        #start_x=0
                        ########这里貌似start_y也是错误的，因为这里的，model_height还是比old_model_height低的。
                        #start_y=start_y+old_model_height
                        #rest_number=nest_number-other_model_num

                        rest_number=rest_number_after_narrow_gap_nest-vast_gap_nest_num
                        start_x=0
                        start_y=start_y+old_model_height

                        print("下一次排版的start_y的值为",start_y)
                        #######这里应该需要对D4.dxf进行清零，不然容易出错。
                        ##########
                        if os.path.exists("D4.dxf"):
                            os.remove("D4.dxf")

                    else:

                        ##########当宽沟的排版数量足以容纳需要排版的模型时
                        other_model_num=rest_number_after_narrow_gap_nest
                        print("当右边沟道容纳排版数量还有多余时","rest_number_after_narrow_gap_nest的大小为",rest_number_after_narrow_gap_nest,"other_model_num的值为",other_model_num)#############计算在高度小于第一个模型的情况下，如何填好。
                #########如果在这里并进去，那么会不会更新，因为更新在下面，不在这个函数里面的。
                        #other_model_num=，rest_number_after_narrow_gap_nest
                        nest_with_rest(model,rest_number_after_narrow_gap_nest,left_width,h,model_Width,model_Height)

                #########获取模型的位置坐标
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                #############这里需要查找找到模型的最大宽度
                        if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            other_model_num=other_model_num-1
                            nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)
                            delt_x=findMinXVertex("D4.dxf")[0]


                        #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                        #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                        ####这里相当于形成了一个新的模型了。
                        #print("测试的模型应该在这里合并才对")
                        ########因为是一个新的模型了，这个里必须要更新新的x和y的排版起点了。
                        #####在这里增加高度是非常不对的，
                        #######这里的start_x=0是不对的，很明显是start_x保持不动。
                        #start_x=0
                        ########这里貌似start_y也是错误的，因为这里的，model_height还是比old_model_height低的。
                        #start_y=start_y+old_model_height
                        rest_number=-1

                       
                        #two_mixed_model_width########
                        #########还有剩余空间
                        model_Width=min(model_Width,two_mixed_model_width/2)

                        vast_gap_nest_number=int((w-start_x)/(model_Width+dx))
                        ##########为避免重复，这里重新计算一遍，宽沟容纳数量
                        start_x=start_x+(model_Width+dx)*(rest_number_after_narrow_gap_nest%vast_gap_nest_number)+dx

                        start_y=start_y

                        print("当宽沟容纳数量远大于剩下需要排版的数量时,start_x==",start_x,"start_y==",start_y)
                        print("model_Width==",model_Width,"rest_number_after_narrow_gap_nest==",rest_number_after_narrow_gap_nest,"left_width==",left_width,"rest_number_after_narrow_gap_nest/(int(left_width/model_Width))==",rest_number_after_narrow_gap_nest/(int(left_width/model_Width)))
                        
                        real_gap_layers=int(rest_number_after_narrow_gap_nest/vast_gap_nest_number)+1

                        print("1093real_gap_layers==",real_gap_layers)
                        
                        if(real_gap_layers):

                            
                            #if():

                            #####这里对于left_height的改其实是不对的。
                            left_height=left_height-real_gap_layers*model_Height
                            print("当宽沟的模型值仍有剩余时，应当回收其高度和宽度","gap_layers==",real_gap_layers,"left_height==",left_height)
                            #left_height=left_height-real_gap_layers*model_Height
                        else:
                            #########当排版的高度为1层时，这个空间不作舍弃，我应该是搞反了。
                            left_height=old_model_height

                        print("下一次排版的start_y的值为",start_y,"下一次排版的left_height的值为",left_height,"old_Model_height==",old_model_height)
                        #######这里应该需要对D4.dxf进行清零，不然容易出错。
                        ##########
                        if os.path.exists("D4.dxf"):
                            os.remove("D4.dxf")

                ########拍完寨沟的数量，那么接下来是排宽沟的数量了



                #other_model_num=nest_number-nest_number_for_narrow_gap
                ######宽沟
                '''vast_gap_nest_num=nest_number-nest_number_for_narrow_gap
                print("排完寨沟的数量后other_model_name的值为",vast_gap_nest_num)
                if(vast_gap_nest_num>0 and vast_gap_nest_num ):

                    #print("other_mode")
                    os.remove("D4.dxf")
                    nest_with_rest(model,other_model_num,w,h,model_Width,model_Height)'''

                
                #rest_number=nest_number-nest_number_for_narrow_gap-rest_number_after_narrow_gap_nest

                #########这里不需要再定义了，因为前面已经定义了。

                print("rest_number的值为",rest_number,'other_model_num的值为',other_model_num,'寨沟的值为',nest_number_for_narrow_gap)
                
                #######从优先级来排，这里要排的是other_Model_num了。
                # 
                #
                        
                            #######再来排剩下的从新的一层开始,当然这里要判断是不是剩下的已经排版完成了
                #####这里存在巨大的bug，因为other_model_num根本没有确定。


                ######这里需要对start_x进行调整和校准，以防出现错误。
                if(rest_number>0):
                    print("rest_number的值为",rest_number)
                    #############这里是rest_number的排版，starty就必须更新到新的一层了。
                    nest_number_per_line,y_number_of_height=nest_with_rest(model,rest_number,w,h,model_Width,model_Height)
                    #####delt_x是计算随意排版的偏移值的，在后续的模型里面应该不需要。
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    print("最后剩余的模型的start_y模型的排版位置为",start_y)
                    movexy("D4.dxf",start_x+dx-delt_x,start_y+dy-delt_y)
                    #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                    mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                    #这里应该是不用更新高度，因为还没有满。
                    #start_y=start_y+old_model_height
                    #############这里不一定增加高度，因为还有一个问题是如果rest_number不够一行怎么办？
                    #########因为上面统一都加了1那么这里加1才是对的。
                    actual_layers=int((rest_number*model_Width)/w)
                    actual_height=actual_layers*model_Height


                    actual_layers=int((rest_number*model_Width)/w)+1
                    actual_height=actual_layers*model_Height
                    ##########这里的start_x可能会有严重的bug，到处都是bug,这里应该去最好的bestwidth
                    ###########果然就碰到了，现在处理一下,这里的model width确实有点问题的，为了避免延时
                    ######直接先加个补偿。

                    ########这里是查不到的，因为不止一行。

                    ######这里按道理是有考虑这个问题的
                    start_x=model_Width*int((rest_number%nest_number_per_line))+(model_Width)*(6/5)
                    
                    start_y=start_y+actual_height


                    #left_rectangle=

                    print("排版后得到的start_x的值为",start_x,"排版后的start_y的值为",start_y,"rest_number%(w/model_Width)的值为",rest_number%(w/model_Width),"model_width的值为",model_Width)
                else:
                    #######
                    print("rest_number的值为小于或者等于0,那么这个模型的值为一般,所以other_num的值为剩余的值")

                    #######这里犯了巨大的错误
                    #start_x=other_model_num*model_Width+(other_model_num+1)*dx

                    model_Width=min(model_Width,two_mixed_model_width/2)
                    #start_x=(model_Width+dx)*(rest_number_after_narrow_gap_nest%other_model_num)+dx
                    start_x=start_x
                    if(start_x>w):
                        start_x=start_x%w

                    ######start_y保持不变
                    #if(start_x==0 or start_x==2):
                    start_y=start_y+left_height
                    #else:
                        #start_y=start_y
                    ###modle_height还是要在这里更新，不然问题肯定不对。但也不一定正确，先试试看吧
                    #old_model_height=model_Height

                #######前提是number_for_nest要大于other才行
               

    
        print("排版后start_x的最大值是",start_x,"模型的宽度为",model_Width)


        if(old_nest_number%(int(w/old_model_width))):
                    
            #start_y=start_y-old_model_height###########
            old_model_height=model_Height
        #else:
            #start_y=start_y
       #old_model_height=model_Height

        old_model_width=model_Width

        print("self.old_model_height的值为",old_model_height)
        
        print("welcome to start function,欢迎进入排版函数内部")


        return start_x,start_y,old_model_height,old_model_width,\
            old_nest_layers,old_nest_number,left_height,left_rectangle,rectangle_list
        
        



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


        #######需要获取每个模型的高度和尺寸会不会好一点?但在这个地方搞？有点慢吧？

        ########在需要对其进行排版的时候再弄吧。
        self.model_name=dxf_file_name
        no_path_model_name=(os.path.basename(dxf_file_name)).split(".")[0]


        #######获取模型的名字。

        width=findMaxXVertex(self.model_name)[0]-findMinXVertex(self.model_name)[0]
        height=findMaxYVertex(self.model_name)[1]-findMinYVertex(self.model_name)[1]
        self.model_size=str(round(width,2))+"*"+str(round(height,2))

        
        self.textbrowser.setText(no_path_model_name)
        self.textbrowser.append(self.model_size)
        

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