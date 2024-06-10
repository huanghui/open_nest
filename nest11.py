##############成功实现了基本dxf文件通过matplotlib读入到qt 界面中
#############实现这一步的是下一步实现排版的起步，万里长征只走了第一步。
###########

#####第二步目标，实现设置排版区域或则会读入一个文件的形状大小并且读入，然后在该版面上画东西，
###########有些形状很不规则，暂不考虑。先设置工作区大小，然后放里面放置单个形状试试看。

########解析dxf文件应该是下一步的重要步骤。


##########0.2版本成功实现了打开指定目录的dxf文件并成功的在qt界面嵌入显示。


##########0.3版本需要将dxf文件设定实际排版区域，其他区域设置为不见。
from calendar import c
import sys
import os
from xml.dom.minidom import TypeInfo
#
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *

#import dxfgrabber

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

#import sys
import matplotlib.pyplot as plt
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import matplotlib
#import readdxf
from  modelcatch05 import extractdxf

#from readdxf15 import nest_from_width_sample
from readdxf15 import *

from layout7 import*


from cadviewer17 import*

import set_sheet_size

from set_sheet_size import*

import time
from urllib import response
#class Dxf():
from parse import*

from datetime import datetime
#inputdxf='G:/Nest/test/1.dxf'
###############定义matplotlib类，实   
####################以上是matplotlib类,dxf文件需在上面类里面显示。

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        #self.setSize(800,600)
        #########将坐标设置为不见。
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        super(MplCanvas, self).__init__(fig)
        #return fig
    def showdxf(self,dxfile):

# Safe loading procedure (requires ezdxf v0.14):
        try:
    #doc, auditor = recover.readfile(inputdxf1)
            self.doc, self.auditor = recover.readfile(dxfile)
        #doc = recover.readfile(inputdxf)
            print("读入dxf文件成功！")
        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)

# The auditor.errors attribute stores severe errors,
# which may raise exceptions when rendering.
#if not auditor.has_errors:
        #dxf = plt.figure()
        #ax = self.axes([0, 0, 1, 1])
        #ax.axes.xaxis.set_visible(False)
        #ax.axes.yaxis.set_visible(False)
        self.ctx = RenderContext(self.doc)
        self.out = MatplotlibBackend(self.axes)
        Frontend(self.ctx, self.out).draw_layout(self.doc.modelspace(), finalize=True)
    #fig.saveas('.dxf', dpi=300)
        #self.setGeometry(20,40,300,500)
        self.show()

    def nestdxf(self):
        print("调用sc类的函数成功！！！")
inputdxf='G:/Nest/Piece6-S2.dxf'

#############软件开机启动imge
class MySplashScreen(QSplashScreen):

    def mousePressEvent(self,event):
        pass


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
       
        super(MainWindow,self).__init__(parent)
        self.mywindow = MyWindow()

        #self.cad_viewer=cadViewer()
        self.cad_viewer=cadDxfViewer()
        self.setCentralWidget(self.mywindow)
        ############设置待打开的文件名称
        #openfile_name
        
        self.dxf_file='0'
        self.font = QtGui.QFont()
        self.font.setFamily(".PingFang SC")
        self.font.setPointSize(40)
        self.setFont(QFont("SimSun",18,QFont.Bold))
        self.setWindowIcon(QIcon('c.ico'))
        #self.lineEdit.setFont(QFont("SimSun", 18, QFont.Bold))  
         #font.setSize(20)
        self.layout = QHBoxLayout()
        self.bar = self.menuBar()
        
        #########设置菜单栏选项
        self.file = self.bar.addMenu("文件")
        self.edit_menu=self.bar.addMenu("提取")
        self.edit_menu.addAction("模型提取")

        self.nest_menu=self.bar.addMenu("排版")
        self.nest_menu.addAction("横向排版")
        self.nest_menu.addAction("竖向排版")
    
        self.set_nest_size_menu=self.bar.addMenu("版面设置")
        self.set_nest_size_menu.addAction("设置标准尺寸版面1400mm*6000mm")
        self.set_nest_size_menu.addAction("自定义版面")

        self.set_nest_size_menu.triggered[QAction].connect(self.set_nest_size)


        self.set_nest_distance=self.bar.addMenu("设置排版间隔")
        self.set_nest_distance.addAction("设置版面间隔")
        self.set_nest_distance.triggered[QAction].connect(self.set_nest_distance_func)

        self.set_nest_distance_text=0

        self.help_menu=self.bar.addMenu("帮助")

        
        
        self.file.setSizeIncrement(QtCore.QSize(20, 20))
        self.file.addAction("打开")
        self.save = QAction("导入总图",self)
        self.save.setShortcut("Ctrl+S")
        self.file.addAction(self.save)
        
        #edit = file.addMenu("所有模型")
        self.file.addAction("导入模型")
        #edit.addAction("copy")
        #edit.addAction("paste")
        self.quit1 = QAction("Quit",self)
        self.file.addAction(self.quit1)
        
      
        #####定义一些预览的功能
    
    
        #############链接到openfile 函数
        self.file.triggered[QAction].connect(self.process_menu)
        #edit_menu.triggered[QAction].connect(self.openfile)
        self.nest_menu.triggered[QAction].connect(self.process_nest_menu)

        ################提取需要裁减的模型成独立的dxf文件
        self.edit_menu.triggered[QAction].connect(self.model_extract)
        
        #save.triggered[QAction].connect(self.slot_open_image)
        self.setLayout(self.layout)
        self.setWindowTitle("尚书排版")
        self.resize(1500,750)
        self.setSizeIncrement(QtCore.QSize(20, 20))
        

        self.file_paths = []  # 文件列表
        self.file_index = 0

        #self.mywindow.distance_of_nest=self.set_nest_gap_distance.textboxValue1
        #if( self.mywindow.distance_of_nest!=self.set_nest_gap_distance.textboxValue1):

        self.filename=None
        #print()
##############要与signal信号通信
    def show_new_window(self, checked):
    #    #self.w.show()
        self.w._signal.connect(self.process_data)

    #######这2个函数应该是没什么用的。
    def show_new_window(self, checked):
    #    #self.w.show()
        self.w._signal.connect(self.process_sheet_size_data)
        

    def set_nest_size(self,q):
        print( q.text()+" is triggered")
        if(q.text()=='设置标准尺寸版面1400mm*6000mm'):
            try:
                self.cad_viewer.resize(1400,6000)
            except:
                print("没有打开文件，请重新打开")
        if(q.text()=="自定义版面"):
            try:
                #self.cad_viewer.resize(1000,3000)
                print("自定义版面")
                #self.sheet_size_app = QApplication(sys.argv)
                #set_sheet_size = sheet_size()
                #self.sheet_size_app.exit(self.sheet_size_app.exec_())
                #self.set_sheet_size=sheetsize()
                self.setSheetSize=set_sheet_size()

                self.setSheetSize._signal.connect(self.process_sheet_size_data)
                
                try:
                    self.doc = ezdxf.new(setup=True)
                    print("很好，进入到了正常处理流程,self.setSheetSize.textboxValue1==",self.x_of_nest,\
                    "self.setSheetSize.textboxValue2==",self.y_of_nest)
        # Add new entities to the modelspace:
                    self.msp = self.doc.modelspace()
                    # Add a rectangle: width=4, height = 2.5, lower left corner is WCS(x=2, y=3)
                    #origin = Vec3(2, 3)
                    self.origin = Vec3(0, 0)
                    #origin_1= Vec3(0,0)
                    self.msp.add_lwpolyline(
                        forms.translate(forms.box(self.x_of_nest,self.y_of_nest), self.origin),
                        close=True
                    )   

                    self.filename="template.dxf"
                    self.doc.saveas(self.filename)
                    self.mywindow.sheet_size_height=self.y_of_nest
                    self.mywindow.sheet_size_width=self.x_of_nest
                    self.mywindow.cad_window.open_template_file(self.filename)
                except:
                    print("文件没有打开,进入异常处理")
                    return
            except:
                print("没有打开文件，请重新打开")
    def process_sheet_size_data(self, str_data1,str_data2):
        #self.qlabel.setText(str_data)
        self.x_of_nest=str_data1
        self.y_of_nest=str_data2

        #self.cad_viewer.resize(str_data,str_data)
        print("排版间隔距离宽设置为==============",str_data1)
        print("排版间隔距离高设置为==============",str_data2)
        #print("排版间隔距离设置为==============",str_data)

        #try:
        self.doc = ezdxf.new(setup=True)
        print("很好，进入到了正常处理流程")
# Add new entities to the modelspace:
        print("很好，定制新的版面,self.setSheetSize.textboxValue1==",self.x_of_nest,\
                "self.setSheetSize.textboxValue2==",self.y_of_nest)
        self.msp = self.doc.modelspace()
        # Add a rectangle: width=4, height = 2.5, lower left corner is WCS(x=2, y=3)
        #origin = Vec3(2, 3)
        self.origin = Vec3(0, 0)
        #origin_1= Vec3(0,0)
        self.msp.add_lwpolyline(
            forms.translate(forms.box(int(self.x_of_nest), int(self.y_of_nest)), self.origin),
            close=True
        )   
        
        self.mywindow.sheet_size_height=self.y_of_nest
        self.mywindow.sheet_size_width=self.x_of_nest
        #filename="new_template.dxf"
        self.filename="userdefine.dxf"
        self.doc.saveas(self.filename)
        self.mywindow.cad_window.open_template_file(self.filename)
        #except:
           # print("文件没有打开,进入异常处理")
            #return


    def set_nest_distance_func(self,q):
        print( q.text()+" is triggered")
        if(q.text()=="设置版面间隔"):
            try:
                #self.cad_viewer.resize(1000,3000)
                print("排版间隔设置")
                #self.sheet_size_app = QApplication(sys.argv)
                #set_sheet_size = sheet_size()
                #self.sheet_size_app.exit(self.sheet_size_app.exec_())
                #self.set_sheet_size=sheetsize()
                #self.setSheetSize=set_sheet_size()

                ##########相当于启动了一个新的窗口
                self.set_nest_gap_distance=set_nest_distance()
                ######问题在于这里的应用还没完成，在这里赋值不正确。
                self.set_nest_gap_distance._signal.connect(self.process_data)
                #self.mywindow.distance_of_nest=self.set_nest_gap_distance.textboxValue1
                print("排版间隔距离设置为==============",self.mywindow.distance_of_nest)
                
            except:
                print("没有设置排版间隔,默认为2mm")
    def process_data(self, str_data):
        #self.qlabel.setText(str_data)
        self.mywindow.distance_of_nest=str_data
        print("315,排版间隔距离设置为==============",str_data)

    def model_extract(self):
        print("model_extract函数用于提取单个模型")
        extractdxf(self.dxf_file)
        print("提取模型成功")
    
    def process_menu(self,q):
        print( q.text()+" is triggered")
        if(q.text()=='打开'):
            try:
                self.openfile()
            except:
                print("没有打开文件，请重新打开")
        if(q.text()=='导入总图'):

            try:
                #self.slot_open_image()
                self.import_all_dxf_model_from_directory()

            except:
                print("导入模型错误，请重新导入")
        if(q.text()=='导入模型'):
            try: 
                #self.import_all_dxf()
                self.import_all_dxf_file()
            except:
                print("打开文件出现异常，没有文件打开")
    def import_all_dxf(self):
        #print("打开文件夹下的所有模型")
        self.cur_dir = QDir.currentPath()  # 获取当前文件夹路径
        
        # 选择文件夹
        self.dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹', self.cur_dir)
        #dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹','', cur_dir)
        #include_extentions=['jpg','jpeg', 'bmp', 'png']
        print("当前的文件目录为",self.dir_path)
        # 读取文件夹文件
        self.file_list=self.get_all_files(self.dir_path)
        for file in self.file_list:
            print(file)
        self.number_of_dxf_model=len(self.file_list)
        #print("包含文件的数量为",number_of_dxf_model)
        #dxffile=self.dxf_to_png(dir_path)
        self.png_file_list=[]
        for index in range(0,self.number_of_dxf_model):
            self.png_file=self.dxf_to_png(self.file_list[index])
            self.png_file_list.append(self.png_file)
            print(len(self.png_file_list))
        
        #print("png_file_list[0]的文件名为",str(file_list[0]))
        #print("png_file_list[0]的文件名为",str(png_file_list[0]))
        #img=QtGui.QPixmap(png_file_list[0])
        self.img=self.read_img(self.png_file_list[0],150)
        self.mywindow.main_model.setPixmap(self.img)
        #number_of_dxf_model=len(png_file_list[0])
        
        
        #self.mywindow.dxf_model_number=len(file_list)
        for num in range(0,self.number_of_dxf_model):
            #print("应该被显示的文件名为",file_list[num])
            self.mywindow.set_single_dxf_model(num,self.png_file_list[num])
            print(self.png_file_list[num])
            #print(num)
        print("png_file_list[0]的文件名为",self.png_file_list[0])    
        for num in range(self.number_of_dxf_model,100):
            self.mywindow.set_single_dxf_model(num,'')
            print(num)
       # print("打开文件夹的所有模型")
        

    def import_all_dxf_file(self):
        #print("打开文件夹下的所有模型")
        self.cur_dir = QDir.currentPath()  # 获取当前文件夹路径
        
        # 选择文件夹
        self.dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹', self.cur_dir)
        #dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹','', cur_dir)
        #include_extentions=['jpg','jpeg', 'bmp', 'png']
        print("当前的文件目录为",self.dir_path)
        #####在这里赋值试试看，有什么不同
        #self.mywindow.distance_of_nest=int(self.set_nest_gap_distance.textboxValue1)
        #print("self.mywindow.distance_of_nest=self.set_nest_gap_distance.textboxValue1",\
        #self.set_nest_gap_distance.textboxValue1)
        # 读取文件夹文件
        self.file_list=self.get_all_files(self.dir_path)
        for file in self.file_list:
            print(file)
        self.number_of_dxf_model=len(self.file_list)
        
        #self.mywindow.dxf_model_number=len(file_list)
        for num in range(0,self.number_of_dxf_model):
            #print("应该被显示的文件名为",file_list[num])
            print("第",num,"个具体文件名为",self.file_list[num])
            self.mywindow.set_model_to_preview(num,self.file_list[num])
            
            #print(num)
        #print("png_file_list[0]的文件名为",file_list[0])    
        #for num in range(number_of_dxf_model,100):
           # self.mywindow.set_single_dxf_model(num,'')
            #print(num)
       # print("打开文件夹的所有模型")
       

    def import_all_dxf_model_from_directory(self):
        ####打开文件夹
        #self.mywindow.distance_of_nest=int(self.set_nest_gap_distance.textboxValue1)
        self.filename, self.filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'CAD files (*.dxf *.DXF *.plt)')
        if self.filename == '':
            return
        #print("小日本的东西写得成不？")
        print(self.filename)
        #self.dxf = ezdxf.readfile(filename)
        if(os.path.splitext(self.filename)[-1]==".plt"):
            print("打开的文件是plt文件",self.filename)
            self.array_list,self.maax_x,self.max_y,self.array_lines=parse_plt(self.filename)
            self.plt_convert_name=self.filename+".dxf"
            plt_to_dxf(self.array_lines,self.plt_convert_name)
    #plt_to_dxf_one_line(array_lines,"ts9.dxf")
            print("执行结束，看看能不能打开，并提取模型？")

        ############这里调用的模型的提取函数，将模型提取出来并保存到一定的目录。
        ########文件默认保存在"modle_dir"文件夹里面"
            self.dir_path=extractdxf(self.plt_convert_name)
        else:
            self.dir_path=extractdxf(self.filename)
        print(self.dir_path)

        # 读取文件夹文件
        self.file_list=self.get_all_files(self.dir_path)
        for file in self.file_list:
            print(file)
        self.number_of_dxf_model=len(self.file_list)
        
        #self.mywindow.dxf_model_number=len(file_list)
        for num in range(0,self.number_of_dxf_model):
            #print("应该被显示的文件名为",file_list[num])
            print(self.file_list[num])
            self.mywindow.set_model_to_preview(num,self.file_list[num])
            
            #print(num)
        print("png_file_list[0]的文件名为",self.file_list[0])    
        for num in range(self.number_of_dxf_model,100):
            self.mywindow.set_single_dxf_model(num,'')
            print(num)
       # print("打开文件夹的所有模型")
       


        


    def get_all_files(self,dir_path):
    #获取该目录下所有的文件名称和目录名称
    #dir_or_files = os.listdir(root_path)
        self.file_list=[]
        for self.root,self.dirs,self.files in os.walk(dir_path):
            for file in self.files:
                if(file.endswith(".dxf")):
                    #print(file)
                    ########需要绝对路径，不然显示不了
                        self.file_with_path=os.path.join(dir_path,file)
                        self.file_list.append(self.file_with_path)
        return self.file_list


    def process_nest_menu(self,q):
        print( q.text()+" is triggered")
        if(q.text()=='横向排版'):
            print("调用横向排版函数")
            try:
                nest_from_width_sample(self.dxf_file,5,0)
                print("调用函数nest_from_sample成功")
            except:
                print("没有文件")
                return 

            self.sc = MplCanvas(self, width=4, height=8, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
            self.sc.showdxf("D4.dxf")
            self.setCentralWidget(self.sc)
        if(q.text()=='竖向排版'):
            print("调用竖向排版函数")    
            #print("调用横向排版函数")
            nest_from_height_sample(self.dxf_file,5,1)
            print("调用函数nest_from_sample成功")
            self.sc = MplCanvas(self, width=4, height=8, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
            self.sc.showdxf("D4.dxf")
            self.setCentralWidget(self.sc)
 
#######菜单栏处理函数,注意处理函数里面包含了sc.showdxf()调用了这个函数实现了对dxf的显示和渲染。
    def openfile(self):
        print( "openfile函数 is triggered")
        '''openfile_name = QFileDialog.getOpenFileName(self,'请选择要添加的文件','','cad files(*.dxf , *.plt),All Files(*)')
        print(openfile_name[0])'''
        #print(openfile_name[0])
        '''print("文件openfile_name成功")'''
         
        self.mywindow.cad_window.view.open_file()
       
        '''png_file_path=self.dxf_to_png(openfile_name[0])
        print(openfile_name[0])
        print(png_file_path)
        #print(dxffile)
        scale=0.5       
        img=QtGui.QPixmap(png_file_path).scaled(self.mywindow.main_model.size(),aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)        
        

        self.mywindow.main_model.setScaledContents(True)
        self.mywindow.main_model.setPixmap(img)
        #self.mywindow.main_model.resize(img.size())
        self.mywindow.main_model.show()'''
        #png_file_path=self.dxf_to_png(openfile_name[0])
        '''if openfile_name is not None:
            # 还需要对图片进行重新调整大小
            img = QImageReader(png_file_path)
            scale = 700 / img.size().width()
            height = int(img.size().height() * scale)
            img.setScaledSize(QSize(700, height))
            img = img.read()
            # 打开设置好的图片
            pixmap = QPixmap(img)'''
        #pixmap=self.read_img(png_file_path,700)
        #print(pixmap)
        #self.mywindow.main_model.setPixmap(pixmap)
            #self.result.setText("车牌号放到这里")
        
        

        
        #Sself.mywindow.model.setPixmap(img)
        #self.mywindow.model.setPixmap(openfile_name[0])
        #self.mywindow.model.setPixmap(sc)
        #print(openfile_name)
    #dxf=dxfgrabber.readfile('126.dxf')
        #for layer in dxf.layers:
           # print(layer.name,layer.color,layer.linetype)
        #return openfile_name

    def read_img(self,img_path,show_width_pixes):
        if img_path is not None:
            # 还需要对图片进行重新调整大小
            img = QImageReader(img_path)
            scale = show_width_pixes/img.size().width()
            height = int(img.size().height() * scale)
            img.setScaledSize(QSize(show_width_pixes, height))
            img = img.read()
            # 打开设置好的图片
            pixmap = QPixmap(img)
            return pixmap
        else:  
            print("打开文件错误")
            return 


    def slot_open_image(self):
        print("slot_open_image 函数被调用")
        self.cwd = os.getcwd()
        #print("打开路径问题")
        #print(self.cwd)
        ###仅仅因为是一个多余的Names就导致我调试了3天，浪费3天的感情。
        self.file,self.filetype= QFileDialog.getOpenFileName(self,'打开多个图片',self.cwd,"*.jpg,*.png,*.JPG, *.JPEG,All Files(*)")
        #print("文件没有打开")
        #print("打开的文件数量为",len(files))
        '''for i in range(len(files)):
            jpg = QtGui.QPixmap(files[i]).scaled(self.labels[i].width(), self.labels[i].height())
            self.labels[i].setPixmap(jpg)'''
        #print(file)
        jpg=QPixmap(self.file).scaled(self.label_1.width(),self.label_1.height())
        #jpg=QPixmap(files).scaled(self.label_1.width(),self.label_1.height())
        #jpg = QtGui.QPixmap(files)
        #print("jpg打开",jpg)
        #image="1.jpg"
        self.label_1.setPixmap(jpg)
        '''pixmap = QPixmap("1.jpg").scaled(self.label_1.width(),self.label_1.height())
        self.label_1.setPixmap(pixmap)'''
        #self.label_1.show()
        #self.show()

    def dxf_to_png(self,filename):
        self.doc, self.auditor = recover.readfile(filename)
        if not self.auditor.has_errors:
        #matplotlib.qsave(doc.modelspace(), 'your.png')
            #pngnam
            
            matplotlib.qsave(self.doc.modelspace(),os.path.splitext(filename)[0]+".png")
            print("转化成png成功",os.path.splitext(filename)[0]+".png")
            return os.path.splitext(filename)[0]+".png"
        #return pngname
        
   #def nestdxf(self):
        #print("调用排版函数成功！！！")
        #nest_from_sample(dxf_file,n,concave_shape)
                
    def load_splash(self,sp):
        
    #QPixmap scaledPixmap = pixmap.scaled((600,600)), Qt::KeepAspectRatio);
        splash.setPixmap(QPixmap("6.jpg").scaled(600,400))
        #splash.resize(200,200)
        #splash.
        #splash.showMessage("加载...{0}%",QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom,QtCore.Qt.black)
        #splash.setFont(QFont('微软雅黑',10))
        splash.show()
        app.processEvents()
        for i in range(1,5):
            time.sleep(1)
            #sp.showMessage("加载...{0}%".format(i*10),QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom,QtCore.Qt.black)
            QtWidgets.qApp.processEvents() 

    def license_msg_of_out_data(self):
        QMessageBox.information(nestwindow,'许可证过期',"请联系供应商，获得许可证",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    def licene_msg_of_ok(self):
        QMessageBox.information(nestwindow,'许可证有效',"恭喜您，许可证在有效期内",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    nestwindow = MainWindow()

    splash=MySplashScreen()
    nestwindow.load_splash(splash)
    currentDateAndTime = datetime.now()

    print("The current date and time is", currentDateAndTime)
    day=currentDateAndTime.day
    
    if(day<10):
        day=str(0)+str(day)

    month=currentDateAndTime.month
    if(month<10):
        month=str(0)+str(month)
     
    year=currentDateAndTime.year
    date=[str(year),str(month),str(day)]
    ymd=''.join(date)
    #ymd=str(year).os.path.join(month,d)
    #print(ymd)
    #print(day,month,year)
    if(os.path.exists('License.dat')):
        license=check_license_file().license_check()
        #print(license[0])
        mac=check_license_file().get_mac_address()
        #mac='90:b1:1c:7a:20:70'
        nestwindow.show()
        splash.finish(nestwindow)
        splash.deleteLater()
        nestwindow.showMaximized()
        print("这是没有认证的版本")
        #sys.exit(app.exec_())

        if(license[0]==mac):
            print("验证通过")
            print(license[1],'ymd==========',ymd)
            if(ymd<license[1]):
                #print(license[1])
                #print(license[1])
                #print("产品还在正常许可期限内，请放心使用") 
                #nestwindow.licene_msg_of_ok()
                nestwindow.show()
                splash.finish(nestwindow)
                splash.deleteLater()
                nestwindow.showMaximized()
                #QApplication.processEvents()
             #睡眠一秒
                #time.sleep(1)
                sys.exit(app.exec_())
            else:
                nestwindow.license_msg_of_out_data()
                print("请联系供应商，获得许可证")
        ########开始处理dxf文件
            #sys.exit(app.exec_())
        else:

            nestwindow.license_msg_of_out_data()
            print("请联系供应商，获得许可证")

    else:
        nestwindow.license_msg_of_out_data()
        print("请联系供应商，获得许可证")
        
    
    '''splash.finish(nestwindow)
    splash.deleteLater()
    nestwindow.showMaximized()
    ########开始处理dxf文件
    sys.exit(app.exec_())'''


