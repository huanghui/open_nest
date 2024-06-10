# -*- coding: utf-8 -*-
from asyncio import start_server
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

import layout7

from layout7 import*

#from layout6 import rectangle
import os
#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


from readdxf15 import *
#import sip
from model_copy_move import find_best_width_height

from shapely.geometry import Polygon




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

        self.left_rectangle=layout7.rectangle()

        self.rectangle_list=[]

        self.distance_of_nest=0
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
    def over_lap(self,box1,box2):
        minx=max(box1.next_begin_x,box2.next_begin_x)
        miny=max(box1.next_begin_y,box2.next_begin_y)
        maxx=min(box1.next_begin_x+box1.left_width,box2.next_begin_x+box2.left_width)
        maxy=min(box1.next_begin_y+box1.left_height,box2.next_begin_y+box2.left_height)
        if(minx>maxx or minx==maxx or miny>maxy or miny==maxy):
            return False
        else:
            return True


######回收矩形就可以实现代码更简洁。
    def  recycle_rect(self,x,y,height,width,rectangle_list,index,width_of_sheet,height_of_sheet):
        #########既然是矩形，至少要大于10才是一个好的矩形，零碎的举行没有排版意义
        #for rect in rectangle_list:
        ########width_of_sheet一般情况下式版面的宽度，这里默认为1500，因为有很多情况下经常出现超出宽度的
           # x!=rect.next_begin_x and y!=rect.next_begin_y
            #poly_rect=Polygon()
       # width_of_sheet=1500
        #height_of_seet=6000
        print("回收的废品矩形为,x==",x,"y==",y,"height==",height,"width==",width)
        dx=2
        if((x>0)and (x<width_of_sheet) and (y>-0.01) and (height>15) and (width>10)):
        
            left_rect_after_nest=layout7.rectangle()

            left_rect_after_nest.next_begin_x=x
            left_rect_after_nest.next_begin_y=y

           
            left_rect_after_nest.left_height=height  #######left_height=model_height是一定的。
            left_rect_after_nest.left_width=width
            if(left_rect_after_nest.next_begin_x+width>width_of_sheet or left_rect_after_nest.next_begin_x+width==width_of_sheet):
                left_rect_after_nest.left_width=width_of_sheet- left_rect_after_nest.next_begin_x-dx
                if( left_rect_after_nest.left_width<10):
                    print("模型在遇到特殊的宽度处理时出现了负值，应当予以取消")
                    return 
                        #####需要将这个left_rectangle回收到rectangle_list里面，以便下一次使用。
            
            for i in range(len(rectangle_list)):
                ############
                #######因为index是本体矩形。
                if(i!=index):
            #for rect in rectangle_list:
                #rect!=rectangle_list[i]
                    while(self.over_lap(left_rect_after_nest,rectangle_list[i])):
                        print("矩形存在重叠，需要削减宽度")
                        #if(left_rect_after_nest.left_width>0):
                        left_rect_after_nest.left_width= left_rect_after_nest.left_width-5*dx
                        #left_rect_after_nest.next_begin_y=left_rect_after_nest.next_begin_y-dx
                        

            print("矩形的起点为====left_rect_after_nest.next_begin_x===",left_rect_after_nest.next_begin_x,\
                            " left_rect_after_nest.next_begin_y==", left_rect_after_nest.next_begin_y,\
                            "left_rect_after_nest.left_height==",left_rect_after_nest.left_height,\
                            "left_rect_after_nest.left_width==",left_rect_after_nest.left_width)
            if(left_rect_after_nest.left_width>0 and left_rect_after_nest.next_begin_x<width_of_sheet):
                rectangle_list.append(left_rect_after_nest)
            else:
                print("矩形宽度为负数,不符合要求,不能加入矩形队列,left_rect_after_nest.left_width------------",left_rect_after_nest.left_width)

        ########这里需要返回吗？似乎目前并不需要。

                                ####这里相当于形成了一个新的模型了。

    def  max_num_of_nest_layers(self,model_height,model_width,two_mixed_width,rect_width,rect_height,dx):
        model_Height=findMaxYVertex("edge.dxf")[1]-findMinYVertex("edge.dxf")[1]+dx

        #two_mixed_model_width  =findMaxXVertex("edge.dxf")[0]-findMinXVertex("edge.dxf")[0]
        _rect_height=rect_height+dx
        rectangle_nest_number=(int(_rect_height/model_height))*int(rect_width/(model_width+dx))
        rectangle_nest_number_2=2*(int(_rect_height/model_height))*int(rect_width/two_mixed_width)
        
        print("排版高度的层数为>>>>>>>>>>>>>>>>>",int(_rect_height/model_height),"一层容纳的列数为",int(rect_width/(model_width+dx)))
        print("排版高度的层数为>>>>>>>>>>>>>>>>>",(int(_rect_height/model_height)),"一层容纳的列数为",int(rect_width/two_mixed_width))
        print("rectangle_nest_number===",rectangle_nest_number,"rectangle_nest_number_2===",rectangle_nest_number_2)

        return max(rectangle_nest_number,rectangle_nest_number_2)


    def start_nest_new(self,number_for_nest,model_name,width,height,\
        start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
            old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest):
        

        print("模型的宽为width===",width,"height==",height,"模型的start_x的位置为",start_x,"模型的start_y值为",start_y,"number_for_nest的值为",number_for_nest,\
           "排版间隔===",distance_of_nest )

        if(number_for_nest==''):
            print("排版数量不正确，请输入正确的排版数量")
        
            return
        nest_number=int(number_for_nest)
        model=model_name
        w=int(width)
        h=int(height)
        print("w===-=-=-=-=-=-=-=-=-=-=",w,"h+=============",h)
        


        dx=distance_of_nest
        print("2个模型的间隔为",dx)
        dy=distance_of_nest
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
        model_Height=findMaxYVertex("edge.dxf")[1]-findMinYVertex("edge.dxf")[1]+dx

        two_mixed_model_width=findMaxXVertex("edge.dxf")[0]-findMinXVertex("edge.dxf")[0]+dx
        mixed_row_number=int((w*2)/two_mixed_model_width)
        #########这里是解决组合高度的问题，但是组合宽度的问题没有解决。
        print("组合模型的最终最适合的高度是",model_Height,"组合模型的最适宽度为",two_mixed_model_width)
        print("self.old_model_height的值为",old_model_height,"这个值很关键")
        if(model_Height>old_model_height+0.01+dx):
            #####原有的空间不适合排版，必须新1起1行排版。所以start_x=0
            print("最新排版的模型比上一个排版的模型高时,model_height>>>>>>>>>>>>>>>>>>>>>old_Model_height")

            print("model_Height==",model_Height,"left_height==",left_height)
            #if(rectangle_list==NULL):

            for i in range(len(rectangle_list)-1,-1,-1):
            #########直接在这里上矩形排版吧。
            #for rect in rectangle_list:
                if(model_Height<rectangle_list[i].left_height+0.01+dx and  model_Width<rectangle_list[i].left_width+0.01):
                    #if(model_Height<left_rectangle.left_height and model_Width<left_rectangle.left_width):
                    print("选择的排版矩形为","rect.next_begin_x===",rectangle_list[i].next_begin_x,\
                            "rect.next_begin_y===",rectangle_list[i].next_begin_y,"rect.left_height==",\
                            rectangle_list[i].left_height,"rect.left_width==",rectangle_list[i].left_width)                        
                    rectangle_nest_number=(int(rectangle_list[i].left_height/model_Height))\
                        *int(rectangle_list[i].left_width/model_Width)

                    if(nest_number>rectangle_nest_number or rectangle_nest_number==nest_number):

                            row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,\
                            rectangle_list[i].left_width,rectangle_list[i].left_height,model_Width,model_Height,dx)

                            delt_x=findMinXVertex("D4.dxf")[0]

                            delt_max_x=findMaxXVertex("D4.dxf")[0]
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x


                    #############这里需要查找找到模型的最大宽度
                            #if(start_x+real_width_of_gap>w):
                            if(rectangle_list[i].next_begin_x+real_width_of_gap>w):

                                print("start_x==========",start_x,"real_width_of_gap=========",real_width_of_gap,\
                                      "start_x+real_width_of_gap==================",start_x+real_width_of_gap)
                                os.remove("D4.dxf")
                                rectangle_nest_number=rectangle_nest_number-1
                                row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,w,h,model_Width,model_Height,dx)
                                delt_x=findMinXVertex("D4.dxf")[0]


                            #mix("D4.dxf","xy.dxf","new_nest.dxf")
                            movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                            #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                            ####这里相当于形成了一个新的模型了。
                            #print("直接进入左边矩形排版,剩下的排版数量为",rest_number)


                            #nest_number=nest_number-rectangle_nest_number

                            new_rect_width=min((nest_number%row_number)*(model_Width+dx)+dx,\
                            ((nest_number%row_number)/2)*(two_mixed_model_width+dx)+dx)
                            print("###########################新排版的模型最顶层的宽度new_rect_width====",\
                                  new_rect_width,"old_nest_layers==============",old_nest_layers)
                            ########当old_nest_layers的值为0时，回收矩形会有很大的问题。
                            if(old_nest_layers==0):
                                old_nest_layers=1


                            if((nest_number%row_number)==0):
                                #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                            #rectangle_list.remove(rectangle_list[i])
                            ######回收矩形上面的矩形
                            self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+\
                                              (old_nest_layers)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                
                                #if(rectangle_list[i].left_height-(old_nest_layers-1)*model_Height===)
                            self.recycle_rect(rectangle_list[i].next_begin_x+new_rect_width,\
                                              rectangle_list[i].next_begin_y+(old_nest_layers-1)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers-1)*model_Height,\
                                    rectangle_list[i].left_width-new_rect_width,rectangle_list,i,w,h)
                            
                            rectangle_list.remove(rectangle_list[i])
                            #rectangle_list.pop(i)

                            nest_number=nest_number-rectangle_nest_number
                            


                            #######这个时候不需要切割原有的矩形了，因为原有的矩形已经满了，
                            ########只需要切割剩下的矩形。
                    elif(nest_number>0):
                            #if(nest_number<rectangle_nest_number):
                            ######我感觉这个可以函数处理，不然这样太浪费版面了。
                        row_number,old_nest_layers=nest_with_rest(model,nest_number,rectangle_list[i].left_width,\
                                    rectangle_list[i].left_height,model_Width,model_Height,dx)                        
                        delt_x=findMinXVertex("D4.dxf")[0]

                        delt_max_x=findMaxXVertex("D4.dxf")[0]
                        delt_y=findMinYVertex("D4.dxf")[1]
                        real_width_of_gap=delt_max_x-delt_x


                    #############这里需要查找找到模型的最大宽度
                        error=rectangle_list[i].next_begin_x+real_width_of_gap-w
                            #####采用矩形排版以后start_x的概念就没有了，因为所有的模型都是在矩形内排好。
                        if(error>0):

                        #if(start_x+real_width_of_gap>w):
                            os.remove("D4.dxf")
                            #nest_number=rectangle_nest_number-1
                            row_number,old_nest_layers=nest_with_rest(model,nest_number,w-error,h,model_Width,model_Height,dx)
                            delt_x=findMinXVertex("D4.dxf")[0]
                            #mix("D4.dxf","xy.dxf","new_nest.dxf")
                        movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                            #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                        mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                            ####这里相当于形成了一个新的模型了。
                        print("当模型的左宽足够容纳排版的熟练时，直接在矩形内排版,old_nest_layers===",old_nest_layers)

                            #####回收资源
                            ####因为此时是不够排第二行的，而且这里是不够排的，那么这个牌面，不是很好打，超过1半了，哪个长方体的
                            #########会比较好一点的。
                        if(old_nest_layers==0):
                            old_nest_layers=1
                        rectangle_list.remove(rectangle_list[i])
                        #self.recycle_rect(start_x,start_y-old_model_height+old_nest_layers*model_Height,\
                           # old_model_height-old_nest_layers*model_Height,w-start_x,rectangle_list)

                        self.recycle_rect(start_x,start_y-rectangle_list[i].left_height+model_Height,\
                           rectangle_list[i].left_height-model_Height,(nest_number%row_number)*model_Width,rectangle_list,i,w,h)

                        start_x=nest_number*model_Width+start_x
                            #start_y=(int(rest_number/row_number)+1)*model_Height
                        start_y=start_y
                        #rectangle_list.remove(rect)

                        ######这里只涉及start_x的变化并没有涉及y的变化，为什么不是start_y-old_model_height,因为很多时候
                        ########这个值并不对。这里的高度是不变的。
                        self.recycle_rect(start_x,rectangle_list[i].next_begin_y,rectangle_list[i].left_height,w-start_x,\
                                          rectangle_list,i,w,h)
                        
                        #self.recycle_rect(start_x,start_y-old_model_height+layers*model_Height,old_model_height-layers*model_Height,w-start_x,rectangle_list)

                        old_model_height=model_Height
                        old_model_width=model_Width
                        old_nest_layers=1
                        old_nest_number=nest_number

                        #rest_number=0
                        nest_number=0
                        #rectangle_list.append(left_rectangle)
                #elif(model_Height>rectangle_list[i].left_height+0.01+dx and  model_Width<rectangle_list[i].left_width+0.01):
                    #print("注意：模型高度大于矩形，需要占用新的空间！！！！！！！！！！！！！")
            if(nest_number==0):

                return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
            

        ###########直接砍掉之前的。
            if(nest_number>0):
            ######当之前的剩余空间能够用并且能够满足，那么就要去找这个空间
            #if()
                print(sys._getframe().f_lineno,"没有矩形可以选择了，只能重新排版，")
                ###重新排版可能没有办法重新排了，start_x不能光等于0了。只能是选择最后有个矩形来实现吧？还是怎么样？
                #@#@index=len(rectangle_list)-1
                #######如果矩形的宽度够。要判断。
                print("len(rectangle_list)!=0的值为",len(rectangle_list))
                if(len(rectangle_list)!=0):
                    print("len(rectangle_list)!=0的值为",len(rectangle_list),"进入到了if(len(rectangle_list)!=0)里面")
                    for i in range(len(rectangle_list)-1,-1,-1):
            #########直接在这里上矩形排版吧。
            
                        print("第",i,"个矩形为","rect.next_begin_x==",rectangle_list[i].next_begin_x,"rect.next_begin_y==",\
                              rectangle_list[i].next_begin_y,"rect.left_height==",rectangle_list[i].left_height,\
                                "rect.left_width==",rectangle_list[i].left_width)

                        #if(self.left_rectangle!=0):
                        if(model_Width<rectangle_list[i].left_width+0.01 and model_Height<2*rectangle_list[i].left_height):
                            rectangle_nest_number=int(rectangle_list[i].left_width/model_Width)

                            print("nest_number=====================",nest_number,"rectangle_list[0].left_width============",\
                                rectangle_list[i].left_width,"rectangle_nest_number======",rectangle_nest_number)
                            #rectangle_nest_number=int(rectangle_list[0].left_width/model_Width)

                            #print("nest_number")

                            if(nest_number>rectangle_nest_number or rectangle_nest_number==nest_number):

                                print("nest_number=====================",nest_number,"准备好排版的数量为rectangle_nest_number",rectangle_nest_number)
                            
                                #因为这里只排了一行
                                row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,rectangle_list[i].left_width,model_Height+dx,model_Width,model_Height,dx)
                                #row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,\
                                   #     rectangle_list[i].left_width, rectangle_list[i].left_height,model_Width,model_Height,dx)
                                delt_x=findMinXVertex("D4.dxf")[0]

                                delt_max_x=findMaxXVertex("D4.dxf")[0]
                                delt_y=findMinYVertex("D4.dxf")[1]
                                real_width_of_gap=delt_max_x-delt_x


                        #############这里需要查找找到模型的最大宽度
                                #if(start_x+real_width_of_gap>w):
                                if(rectangle_list[i].next_begin_x+real_width_of_gap>w):

                                    print("start_x==========",start_x,"real_width_of_gap=========",real_width_of_gap,\
                                            "start_x+real_width_of_gap==================",start_x+real_width_of_gap)
                                    os.remove("D4.dxf")
                                    rectangle_nest_number=rectangle_nest_number-1
                                    row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,rectangle_list[i].left_width,model_Height+dx,model_Width,model_Height,dx)
                                    delt_x=findMinXVertex("D4.dxf")[0]


                                #mix("D4.dxf","xy.dxf","new_nest.dxf")
                                movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                                mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                                ##########这里是重新排版，低台阶排版的时候，new_rect_width的值就不能取余数了，只能是最右边排版剩下的矩形了
                                #new_rect_width=min((nest_number%row_number)*(model_Width+dx)+dx,((nest_number%row_number)/2)*(two_mixed_model_width+dx)+dx)
                                new_rect_width=rectangle_nest_number*model_Width+dx
                                print("--------------------------------new_rect_width====",new_rect_width,"old_nest_layers==============",old_nest_layers)
                                ########当old_nest_layers的值为0时，回收矩形会有很大的问题。
                                if(old_nest_layers==0):
                                    old_nest_layers=1


                                if((nest_number%row_number)==0):
                                    #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                    new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                                #rectangle_list.remove(rectangle_list[i])
                                ######回收矩形上面的矩形
                                ######上面的矩形不需要了，不存在
                                #self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+(old_nest_layers)*model_Height,\
                                # rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                rect=rectangle_list[i]
                                rectangle_list.remove(rectangle_list[i])
                                    #if(rectangle_list[i].left_height-(old_nest_layers-1)*model_Height===)
                                #self.recycle_rect(rect.next_begin_x+new_rect_width,rect.next_begin_y+(old_nest_layers-1)*model_Height,\
                                    #rect.left_height-(old_nest_layers-1)*model_Height,rect.left_width-new_rect_width,rectangle_list,i,w,h)
                                
                                #rectangle_list.remove(rectangle_list[0])
                                #rectangle_list.pop(i)

                                #nest_number=nest_number-rectangle_nest_number

                                print(sys._getframe().f_lineno,"rectangle_list[0].next_begin_x+new_rect_width====================",\
                                    rect.next_begin_x,"new_rect_width=====",new_rect_width)
                                self.recycle_rect(rect.next_begin_x+new_rect_width,rect.next_begin_y+\
                                                (old_nest_layers-1)*model_Height,\
                                    model_Height,rect.left_width-new_rect_width,rectangle_list,i,w,h)
                                
                                #########当矩形最开始的左侧高于右侧时，应当回收左侧的矩形，或者说如果矩形没有高度的要求，那么高度应该是很高的。
                                ######但我之前碰到一个矩形的问题就是当矩形的进过几次排版以后，会产生冲突，要结合起来解决

                                self.recycle_rect(dx,rect.next_begin_y+old_model_height,\
                                model_Height-rect.left_height,rect.next_begin_x,rectangle_list,i,w,h)

                                print(sys._getframe().f_lineno,"最终还是没有返回值吗？")

                                
                                start_x=0
                                start_y=rect.next_begin_y+model_Height
                                old_model_height=model_Height
                                old_model_width=model_Width
                                old_nest_layers=0
                                old_nest_number=nest_number
                                left_height=0
                                left_rectangle=0
                                #rectangle_list
                                distance_of_nest=2
                                #nest_number=nest_number-rectangle_nest_number
                                nest_number=nest_number-rectangle_nest_number
                                #return start_x,start_y,old_model_height,old_model_width,\
                # old_nest_layers,old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
                            
                            elif(nest_number<rectangle_nest_number):
                                print("nest_number=====================",nest_number)

                                row_number,old_nest_layers=nest_with_rest(model,nest_number,rectangle_list[i].left_width,model_Height+dx,model_Width,model_Height,dx)

                                delt_x=findMinXVertex("D4.dxf")[0]

                                delt_max_x=findMaxXVertex("D4.dxf")[0]
                                delt_y=findMinYVertex("D4.dxf")[1]
                                real_width_of_gap=delt_max_x-delt_x


                        #############这里需要查找找到模型的最大宽度
                                #if(start_x+real_width_of_gap>w):
                                if(rectangle_list[i].next_begin_x+real_width_of_gap>w):

                                    print("start_x==========",start_x,"real_width_of_gap=========",real_width_of_gap,\
                                            "start_x+real_width_of_gap==================",start_x+real_width_of_gap)
                                    os.remove("D4.dxf")
                                    rectangle_nest_number=rectangle_nest_number-1
                                    row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,rectangle_list[i].left_width,model_Height+dx,model_Width,model_Height,dx)
                                    delt_x=findMinXVertex("D4.dxf")[0]


                                #mix("D4.dxf","xy.dxf","new_nest.dxf")
                                movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                                mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                                new_rect_width=min((nest_number%row_number)*(model_Width+dx)+dx,((nest_number%row_number)/2)*(two_mixed_model_width+dx)+dx)
                                print("###########################新排版的模型最顶层的宽度new_rect_width====",new_rect_width,"old_nest_layers==============",old_nest_layers)
                                ########当old_nest_layers的值为0时，回收矩形会有很大的问题。
                                if(old_nest_layers==0):
                                    old_nest_layers=1

                                rect=rectangle_list[0]
                                rectangle_list.remove(rectangle_list[0])

                                if((nest_number%row_number)==0):
                                    #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                    new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                                #rectangle_list.remove(rectangle_list[i])
                                ######回收矩形上面的矩形
                                ######上面的矩形不需要了，不存在
                                #self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+(old_nest_layers)*model_Height,\
                                # rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                    
                                    #if(rectangle_list[i].left_height-(old_nest_layers-1)*model_Height===)
                                #self.recycle_rect(rect.next_begin_x+new_rect_width,rect.next_begin_y+(old_nest_layers-1)*model_Height,\
                                #  rect.left_height-(old_nest_layers-1)*model_Height,rect.left_width-new_rect_width,rectangle_list,i,w,h)
                                
                                #rectangle_list.remove(rectangle_list[0])

                                print("rectangle_list[0].next_begin_x+new_rect_width====================",\
                                    rectangle_list[i].next_begin_x,"new_rect_width=====",new_rect_width)

                                self.recycle_rect(rect.next_begin_x+new_rect_width,rect.next_begin_y+\
                                                (old_nest_layers-1)*model_Height,\
                                    model_Height,rect.left_width-new_rect_width,rectangle_list,i,w,h)
                                

                                self.recycle_rect(dx,rect.next_begin_y+old_model_height,\
                                    model_Height-rect.left_height,rect.next_begin_x,rectangle_list,i,w,h)

                                print("回收矩形完毕，正在回收其他参数")
                                #rectangle_list.pop(i)
                                

                                start_x=0
                                start_y=start_y
                                old_model_height=model_Height
                                old_model_width=model_Width
                                old_nest_layers=0
                                old_nest_number=nest_number
                                left_height=0
                                left_rectangle=0
                                #rectangle_list
                                distance_of_nest=2
                                #nest_number=nest_number-rectangle_nest_number
                                nest_number=0
                                return start_x,start_y,old_model_height,old_model_width,\
                    old_nest_layers,old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
                            
                                    ##if(nest_number>0):                              
                else:

                    start_x=0
                    ######因为是新排版的，不可能有矩形重复，所以i直接=-1
                    i=-1
                    #######当新的模型比原来的模型高时，需要新起一行
                    '''if(start_y+old_model_height<h or start_y+old_model_height<6000):
                        start_y=start_y+old_model_height'''
                    #######这里是多余做了这一层吧
                    #start_y=start_y+old_model_height
                    print("in line 527,star_y的值为-------------------------------",start_y)
                    
                    #start_y=start_y-old_model_height
                
                    row_number,old_nest_layers=nest_with_rest(model,nest_number,w,h,model_Width,model_Height,dx)
                    if(row_number==0):
                        print("产生异常，模型的超过了最大排版面积")
                    start_x=0
                    start_y=0
                    old_model_height=0
                    old_model_width=0
                    old_nest_layers=0
                    old_nest_number=0
                    left_height=0
                    left_rectangle=0
                    #rectangle_list
                    distance_of_nest=0
                    #return start_x,start_y,old_model_height,old_model_width,\
                #@old_nest_layers,old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
                    
                    delt_x=findMinXVertex("D4.dxf")[0]
                    delt_y=findMinYVertex("D4.dxf")[1]

                    delt_max_x=findMaxXVertex("D4.dxf")[0]
                    #real_nest_width=
                    #mix("D4.dxf","xy.dxf","new_nest.dxf")

                    real_width_of_gap=delt_max_x-delt_x


                    error=start_x+real_width_of_gap-w

                #############这里需要查找找到模型的最大宽度
                    if(error>0):
                        os.remove("D4.dxf")
                        #rectangle_nest_number=rectangle_nest_number-1
                        w=w-3*error
                        row_number,old_nest_layers=nest_with_rest(model,nest_number,w,h,model_Width,model_Height,dx)
                        delt_x=findMinXVertex("D4.dxf")[0]
                    
                    ##########移动2mm为了保证模型产生的间距合理
                    movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                    if(old_model_height==0):
                        print("第二次进入到这个里面了吗")
                        if(os.path.exists("new_nest.dxf")):
                            os.remove("new_nest.dxf")

                        if(os.path.exists("userdefine.dxf")):
                            mix("D4.dxf","userdefine.dxf","new_nest.dxf")
                        else:
                            #mix("D4.dxf","xy.dxf","new_nest.dxf")
                            #"D4.dxf".
                        # mix("D4.dxf",'',"new_nest.dxf")
                            save_as("D4.dxf","new_nest.dxf")
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


                    print("real_width_of_gap====",real_width_of_gap,"layers*model_Height===",layers*model_Height)

                    '''if(layers-1==0):
                        rect_height=layers*model_Height
                    else:
                        rect_height=(layers-1)*model_Height'''
                    rect_height=layers*model_Height
                        
                    ##############因为是重新排版了，所以这个i估计是不需要的了。那我应该怎么排版比较好？i直接赋值为-1吧，比较好
                    self.recycle_rect(real_width_of_gap,start_y,rect_height-dx,w-(real_width_of_gap),rectangle_list,i,w,h)
                    #######因为start_y在这里有所改变了，所以这里回收比较合适

                    start_y=layers*model_Height+start_y####这里不是上面狗屁layers+model_heihgt而是原


                    print("排版完以后的的start_y================",start_y)
                    ######这里的描述似乎是最上层的start_y的值吧。
                    ########这里并没有定义start_x的值，这里是需要定义的。

                    ##########这里还是获取模型的的最大值吧，直接测量起码是争取的，否则很多计算容易把数据跑飞了。

                    ######model_width预计进行修正和优化，由于row_number的值有可能和之前的不一样。
                    reaL_actual_width_after_nest=w/row_number
                    start_x_1=(nest_number%row_number)*model_Width

                    start_x_2=(nest_number%row_number)*reaL_actual_width_after_nest
                
                    start_3=((nest_number%row_number)*two_mixed_model_width)/2
                    #two_mixed_model_width
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
                    if(nest_number%row_number and int(nest_number/row_number)):
                        layers=int(nest_number/row_number)+1
                        print("当排版的数量有余数，而且排版层数大于1行，排版后的模型层数为",layers)
                        left_height=(layers-1)*model_Height
                        ######这里不需要减了， 因为本身就是这个值
                        self.recycle_rect(start_x,start_y-model_Height,model_Height,w-start_x,rectangle_list,i,w,h)
                    else:
                        #layers=int(nest_number/row_number)

                        #####如果是整除的，那么这个矩形不应该添加在里面
                        left_height=layers*model_Height

                        #self.recycle_rect(start_x,start_y,model_Height,w-start_x,rectangle_list)
                    left_height=(layers-1)*model_Height
                    left_width_after_nest=w-int(w/model_Width)
                    
                    ########当另起路炉灶时需要回收这些模型。
                    print("")
                
                    print("")

                    return start_x,start_y,old_model_height,old_model_width,\
                old_nest_layers,old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest

        else:
            print(sys._getframe().f_lineno," in 644当新排版的模型高度<<<<<<<<<<<旧模型的高度时","新模型的高度为",model_Height,"旧模型的高度为",old_model_height)
            if((old_model_height/2)<model_Height<old_model_height or model_Height<old_model_height+0.01):   
                #####这种情况其实更好处理，因为这个情况下，是一定会有长方形能够容纳一部分的，然后，然后后面的排版就真的不需要了。
                ######

                number_of_rect=len(rectangle_list)
                print("长方形的数量===================-------------------------=======================",number_of_rect)
                for i in range(len(rectangle_list)-1,-1,-1):
                #for rect in rectangle_list:
                   print("遍历的矩形为","rect.next_begin_x===",rectangle_list[i].next_begin_x,\
                   "rect.next_begin_y===",rectangle_list[i].next_begin_y,"rect.left_height==",\
                    rectangle_list[i].left_height,"rect.left_width==",rectangle_list[i].left_width)
                   #print("模型的数量指示是多少？这个i的数量是，",i,'为什么会超出范围？')
                   if(model_Height<(rectangle_list[i].left_height)+0.01+dx and model_Width<(rectangle_list[i].left_width)+0.01):
                #if(model_Height<left_rectangle.left_height and model_Width<left_rectangle.left_width):
                        print("选择的排版矩形为","rect.next_begin_x===",rectangle_list[i].next_begin_x,\
                        "rect.next_begin_y===",rectangle_list[i].next_begin_y,"rect.left_height==",\
                        rectangle_list[i].left_height,"rect.left_width==",rectangle_list[i].left_width)

                        ######这里已经判断了，那这么会多出来一个？
                        #rectangle_nest_number=(int(rect.left_height/model_Height))\
                            #*int(rect.left_width/(model_Width+dx))

                        rectangle_nest_number=self.max_num_of_nest_layers(model_Height,model_Width,two_mixed_model_width,rectangle_list[i].left_width,rectangle_list[i].left_height,dx)
                        print("所选择的矩形容纳模型的数量为rectangle_nest_number",rectangle_nest_number)
                        ########矩形不够排时
                        if(rectangle_nest_number==0):
                            print("所选择的矩形容纳模型的数量为rectangle_nest_number--------------0",rectangle_nest_number,\
                                  "有可能是组合模型的宽度") 
                            continue
                        if(nest_number>rectangle_nest_number):
                                print("所选择的矩形不够排","nest_number===",nest_number,"rectangle_nest_number===",rectangle_nest_number)
                                
                                row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,rectangle_list[i].left_width,rectangle_list[i].left_height,model_Width,model_Height,dx)
                                print("实际排版中返回的列数为fwofjowejownvwenjv0wejvwej",row_number,"实际排版的行数为fwjo9ifnwoenwoenweonownsd",old_nest_layers) 
                                delt_x=findMinXVertex("D4.dxf")[0]

                                delt_max_x=findMaxXVertex("D4.dxf")[0]
                                delt_y=findMinYVertex("D4.dxf")[1]
                                real_width_of_gap=delt_max_x-delt_x

                                error=real_width_of_gap-w
                        #############这里需要查找找到模型的最大宽度
                                if(error>-0.1):

                                    #print()
                                    os.remove("D4.dxf")
                                    #rectangle_nest_number=rectangle_nest_number-1
                                    row_number,old_nest_layers=nest_with_rest(model,rectangle_nest_number,w-error,rectangle_list[i].left_height,model_Width,model_Height,dx)
                                    delt_x=findMinXVertex("D4.dxf")[0]


                                #mix("D4.dxf","xy.dxf","new_nest.dxf")
                                #movexy("D4.dxf",rectangle_list[i].next_begin_x+dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                                movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                                mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                                ####这里相当于形成了一个新的模型了。
                                #nest_number=nest_number-rectangle_nest_number
                                print("现有模型不够排，寻找下一个矩形排版","nest_number==",nest_number,"rectangle_nest_number==",rectangle_nest_number)
                                #print("剩下的排版数量为,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",nest_number)
                                #rectangle_list.remove(rectangle_list[i])       


                                if(old_nest_layers==0):
                                    old_nest_layers=1
                                elif(rectangle_nest_number%row_number==0):
                                    old_nest_layers=old_nest_layers
                                else:
                                    old_nest_layers=old_nest_layers+1

                                
                                #if((rectangle_nest_number%row_number)==0):
                                    #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                    #new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                                    #old_nest_layers=old_nest_layers-1



                                #new_rect_width=row_number
                                new_rect_width=min(row_number*(model_Width+dx)+dx,(row_number/2)*(two_mixed_model_width+dx)+dx)
                                #new_rect_width=min((nest_number%row_number)*(model_Width+dx)+dx,((nest_number%row_number)/2)*(two_mixed_model_width+dx)+dx)
                                print("###########################新排版的模型最顶层的宽度new_rect_width====",new_rect_width,\
                                      "old_nest_layers----------------------------------------------",old_nest_layers)

                                #if((nest_number%row_number)==0):
                                #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                    #new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                                #######这里应该要回收矩形。
                                self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+(old_nest_layers)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                
                                #if(rectangle_list[i].left_height-(old_nest_layers-1)*model_Height===)

                                ###########当矩形不够排的情况，y的起点应该是不需要增加的。就是next_beigin_Y
                                #self.recycle_rect(rectangle_list[i].next_begin_x+new_rect_width,rectangle_list[i].next_begin_y+(old_nest_layers-1)*model_Height,\
                                #rectangle_list[i].left_height-(old_nest_layers-1)*model_Height,rectangle_list[i].left_width-new_rect_width,rectangle_list,i,w,h)
                                

                                self.recycle_rect(rectangle_list[i].next_begin_x+new_rect_width,rectangle_list[i].next_begin_y,\
                                rectangle_list[i].left_height-(old_nest_layers-1)*model_Height,rectangle_list[i].left_width-new_rect_width,rectangle_list,i,w,h)
                                rectangle_list.remove(rectangle_list[i])     

                                nest_number=nest_number-rectangle_nest_number

                                print("剩下的排版数量为,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",nest_number)

                        elif(nest_number>0):
                                #if(nest_number<rectangle_nest_number):
                                ######我感觉这个可以函数处理，不然这样太浪费版面了。
                            print("矩形足够容纳排版数量============================================",\
                                "nest_number====",nest_number,"rectangle_nest_number==",rectangle_nest_number)
                            
                            row_number,old_nest_layers=nest_with_rest(model,nest_number,rectangle_list[i].left_width,rectangle_list[i].left_height,model_Width,model_Height,dx)                        
                            delt_x=findMinXVertex("D4.dxf")[0]

                            delt_max_x=findMaxXVertex("D4.dxf")[0]
                            delt_y=findMinYVertex("D4.dxf")[1]
                            real_width_of_gap=delt_max_x-delt_x
                            ############这里需要查找找到模型的最大宽度

                            #error=start_x+real_width_of_gap-w
                            error=rectangle_list[i].next_begin_x+real_width_of_gap-w
                            #####采用矩形排版以后start_x的概念就没有了，因为所有的模型都是在矩形内排好。
                            if(error>0):
                                print("超出了排版范围需要重新排版！！！！！！！！！！！！")
                                os.remove("D4.dxf")
                                #rectangle_nest_number=rectangle_nest_number-1
                                row_number,old_nest_layers=nest_with_rest(model,nest_number,rectangle_list[i].left_width-error,rectangle_list[i].left_height,model_Width,model_Height,dx)
                                delt_x=findMinXVertex("D4.dxf")[0]
                                delt_y=findMinYVertex("D4.dxf")[1]


    
                            movexy("D4.dxf",rectangle_list[i].next_begin_x+2*dx-delt_x,rectangle_list[i].next_begin_y+dx-delt_y)
                                #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
                            mix("D4.dxf","new_nest.dxf","new_nest.dxf")

                            print("矩形的参数为==========","rect.next_begin_x==",rectangle_list[i].next_begin_x,"rect.next_begin_y==",rectangle_list[i].next_begin_y)
                                ####这里相当于形成了一个新的模型了。
                            #print("当模型的左宽足够容纳排版的数量时，直接在矩形内排版")

                                #####回收资源
                                ####因为此时是不够排第二行的，而且这里是不够排的，那么这个牌面，不是很好打，超过1半了，哪个长方体的
                                #########会比较好一点的。

                            print(sys._getframe().f_lineno,"当模型的左宽足够容纳排版的数量时，直接在矩形内排版,old_nest_layers===",old_nest_layers)

                           
                            if(old_nest_layers==0):
                                old_nest_layers=1
                            else:
                                old_nest_layers=old_nest_layers+1

                            #####这是个余数宽度，不是整体宽度。
                            #new_rect_width=(nest_number%row_number)*(model_Width+dx)+dx
                            new_rect_width=min((nest_number%row_number)*(model_Width+dx)+dx,((nest_number%row_number)/2)*(two_mixed_model_width+dx)+dx)
                            print("###########################新排版的模型最顶层的宽度new_rect_width====",new_rect_width)

                            if((nest_number%row_number)==0):
                                #####nest_number恰好能放置所有的模型，十分少见，但也碰到过，如果不处理将导致矩形回收产生问题。
                                new_rect_width=min((nest_number*(model_Width+dx)+dx,(nest_number/2)*(two_mixed_model_width+dx)+dx))
                                old_nest_layers=old_nest_layers-1

                            #######x不变，

                            #######这个矩形构建是错误的，这里需要考虑，当余数的宽度比矩形宽度大过1半时，我们认为主要考虑上面的矩形。
                            #########当余数的模型宽度小于矩形的一半宽度时，我们认为主要选择高度更高的矩形。

                            ######因为这里old_nest_layers已经加了1了。
                            if(nest_number>0.3*int(w/model_Width)):
                                print("当排版的数量超过矩形的一半时,old_nest_layers==================",old_nest_layers)
                               
                                self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+(old_nest_layers)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                
                                #if(rectangle_list[i].left_height-(old_nest_layers-1)*model_Height===)
                                self.recycle_rect(rectangle_list[i].next_begin_x+new_rect_width,rectangle_list[i].next_begin_y+(old_nest_layers-1)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers-1)*model_Height,rectangle_list[i].left_width-new_rect_width,rectangle_list,i,w,h)
          
                            else:

                                print("当排版的数量不够矩形的一半时rect.next_begin_x+new_rect_width===",\
                                    rectangle_list[i].next_begin_x+new_rect_width," rect.left_height==", rectangle_list[i].left_height\
                                    ,"(old_nest_layers)*model_Height===",(old_nest_layers)*model_Height)
                                
                                self.recycle_rect(rectangle_list[i].next_begin_x,rectangle_list[i].next_begin_y+(old_nest_layers)*model_Height,\
                                rectangle_list[i].left_height-(old_nest_layers)*model_Height,new_rect_width,rectangle_list,i,w,h)
                                
                                self.recycle_rect(rectangle_list[i].next_begin_x+new_rect_width,rectangle_list[i].next_begin_y+(old_nest_layers-1)*model_Height,\
                            rectangle_list[i].left_height-(old_nest_layers-1)*model_Height,rectangle_list[i].left_width-new_rect_width,rectangle_list,i,w,h)

                            start_x=(nest_number%row_number)*(model_Width+dx)+dx+start_x
                                #start_y=(int(rest_number/row_number)+1)*model_Height
                            start_y=start_y


                            layers=int(nest_number/row_number)+1
                            #else:
                                
                            #########y不变，X=row_number*model_Width+dx才是对的吧
                            '''self.recycle_rect(rect.next_begin_x+(nest_number%row_number)*(model_Width+dx)+dx\
                                ,rect.next_begin_y,rect.left_height,\
                                w-(rect.next_begin_x+(nest_number%row_number)*(model_Width+dx)+dx),rectangle_list)'''
                            #####最窄处的，而不是次高处的。
                            #@
                            
                            '''self.recycle_rect(rectangle_list[i].next_begin_x+row_number*(model_Width+dx)+dx\
                                ,rectangle_list[i].next_begin_y,rectangle_list[i].left_height,\
                                w-(rectangle_list[i].next_begin_x+(row_number*(model_Width+dx)+dx)),rectangle_list,i,w,h)'''
                            

                            self.recycle_rect(rectangle_list[i].next_begin_x+row_number*(model_Width+dx)+dx\
                                ,rectangle_list[i].next_begin_y,rectangle_list[i].left_height,\
                                rectangle_list[i].left_width-(rectangle_list[i].next_begin_x+(row_number*(model_Width+dx)+dx)),rectangle_list,i,w,h)
                            old_model_height=model_Height
                            old_model_width=model_Width
                            old_nest_layers=1
                            old_nest_number=nest_number

                            rest_number=0
                            nest_number=0
                            rectangle_list.remove(rectangle_list[i])

                            #return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                                #old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest

                              ######else的情况下是可以return的，因为他已经排完了，但是当不够矩形时，应该重新排版的。
            #########此事start_x=0,
        if(nest_number==0):
        
            return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
            old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
    #   
        if(nest_number>0):
            start_x=0
            i=-1

            print("最后剩下来的排版数量为",nest_number)

            #####当在else环境下，starty也需要增加高度吧
            start_y=start_y
            #nest_number=nest_number-rectangle_nest_number
            if(os.path.exists("D4.dxf")):
                os.remove("D4.dxf")
            if(os.path.exists("Dy.dxf")):
                os.remove("Dy.dxf")
            row_number,num_of_height=nest_with_rest(model,nest_number,w,h,model_Width,model_Height,dx)

            delt_x=findMinXVertex("D4.dxf")[0]

            delt_max_x=findMaxXVertex("D4.dxf")[0]
            delt_y=findMinYVertex("D4.dxf")[1]
            real_width_of_gap=delt_max_x-delt_x

                            ##########不用管了，这里是重新新的一行了。
                    #############这里需要查找找到模型的最大宽度

                    #########这里是排完剩下的排版吧，但是这里也会有剩余的矩形，有没有回收?

            error=start_x+real_width_of_gap-w

    #############这里需要查找找到模型的最大宽度
            if(error>0):
                os.remove("D4.dxf")
                #rectangle_nest_number=rectangle_nest_number-1
                w=w-error
                row_number,old_nest_layers=nest_with_rest(model,nest_number,w,h,model_Width,model_Height,dx)
                delt_x=findMinXVertex("D4.dxf")[0]
            
                delt_max_x=findMaxXVertex("D4.dxf")[0]
                delt_y=findMinYVertex("D4.dxf")[1]
                real_width_of_gap=delt_max_x-delt_x
                
                        #########这里是排完剩下的排版吧，但是这里也会有剩余的矩形，有没有回收?

            ######这里做第二次循环的时候，是为了防止出现-1个仍然出界的产生。
            if(start_x+real_width_of_gap>w):
                os.remove("D4.dxf")
                nest_number=nest_number-1
                row_number,num_of_height=nest_with_rest(model,nest_number,w,h,model_Width,model_Height,dx)
                delt_x=findMinXVertex("D4.dxf")[0]


                            ######这里没有rest_number要归0
                            #rest_number=0
                            #nest_number=0
                            #mix("D4.dxf","xy.dxf","new_nest.dxf")
            movexy("D4.dxf",start_x+dx-delt_x,start_y+dx-delt_y)
                            #movexy("D4.dxf",self.start_nest_x-delt_x,self.start_nest_y-delt_y)
            mix("D4.dxf","new_nest.dxf","new_nest.dxf")
                            ####这里相当于形成了一个新的模型了。
            print("直接进入左边矩形排版")


                            #######可以定义一个函数专门回收这个面积。

                            #rest_number=0
                            #nest_number=0
            ########如果2个模型的复合宽度比2个模型的宽度小，那么出大事了。
            if(two_mixed_model_width<2*model_Width):
                start_x=((nest_number%row_number)/2)*two_mixed_model_width

                print("当two_mixed_model_width<2*model_Width时，two_mixed_model_width==",\
                two_mixed_model_width,"2*model_Width===",2*model_Width,"start_x==",start_x)
            else:
                start_x=(nest_number%row_number)*(model_Width+dx)
                print("当two_mixed_model_width<2*model_Width时，two_mixed_model_width==",\
                two_mixed_model_width,"2*model_Width===",2*model_Width,"start_x==",start_x)

            ####
            new_x=(model_Width+dx)*row_number

            #那么有可能是重写的复合宽度了，这里就应该直接去测量
            if(new_x>w):
                new_x=(two_mixed_model_width+dx)*(row_number/2)

                print("new_x============================",new_x)
            print("new_x============================",new_x)

            new_y=start_y
            if(int(nest_number/row_number)):
                #self.recycle_rect(new_x,new_y,model_Height,w-start_x,rectangle_list)

                self.recycle_rect(new_x,new_y,int(nest_number/row_number)*model_Height,w-new_x,rectangle_list,i,w,h)


            start_y=(int(nest_number/row_number)+1)*model_Height+start_y

            #######问题出在这个地方
            print("第三次回收矩形，回收最右边侧面的矩形，有时候计算会出错")
            self.recycle_rect(start_x,start_y-model_Height,model_Height,w-start_x,rectangle_list,i,w,h)
            ####
            #new_x=(model_Width+dx)*row_number

            # new_y=
            #self.recycle_rect(new_x,start_y-model_Height,model_Height,w-start_x,rectangle_list)


            old_model_height=model_Height
            old_model_width=model_Width
            old_nest_layers=int(nest_number/row_number)
            old_nest_number=nest_number
                            #######必须在这里处理，不然影响old_nest_number的值。
            #nest_number=0
            nest_number=0

            return start_x,start_y,old_model_height,old_model_width,old_nest_layers,\
                old_nest_number,left_height,left_rectangle,rectangle_list,distance_of_nest
                                #######这个时候不需要切割原有的矩形了，因为原有的矩形已经满了，
                                ########只需要切割剩下的矩形。

                ##########当没有矩形可以容纳的时候，那必须另起高度，注意这个很重要。

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
        print("in cadPreViewer.py中，程序已经走到了这里")
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
    #def log_message(self, message):
        #self.log_view.append(message)

if __name__ == '__main__':
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    window = cadPreViewer()
    window.show()
    window.open_file()
    app.exec()