#import dxfgrabber
#######################实现部分dxf文件的部分移位
##########实现了文件的绝对移位和原有文件的合并。

#########初步实现了指定数量的排版和dx,dy 的位移，但尚未实现给定长度和宽度的数量计算和给定文件的旋转。
#######readdxf0.6版本实现了旋转和平移以及dx,dy的位移功能，向前跨越了一大步。但这个离我们需要的功
######能还有很大一步 readdxf0.7主要解决图形边界计算的问题。
###################
#############readdxf0.7主要解决了提取图形速度的问题，由1个小时的提取速度现在变成了1分钟，
#############readdxf0.7同时解决了模型提取的问题，在一个很多模型的dxf文件中提取合适的模型
##########虽然提取的模型用了非常简单的算法，但是work即好。

#################接下来进入到最关键的算法了，就是判断2个模型的边界问题。


##################\
#################0.8解决了很多问题，比如模型边界和1，7两类模型的智能排版问题，
#################至于其他的模型会不会有什么问题
###################0.9模型主要解决的是竖直模型排版的问题的问题。
###################
############0.9版本解决了部分竖直的问题
##################


########
#########这个可以提取发过来的4个模型，第二种提取办法和第一种提取办法不太一样，现在新的函数
##########可以兼容

import ezdxf
import os
#
import math
from ezdxf.addons import Importer
#from ezdxf import Importer
#from polycrash import polyCrash,polyCrash2,polyCrash3,polyCrash_3,polyCrash_4



def extractdxf(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    indexdxf=0
    j=0
    number_of_blocks=0
    #print(dxf.owner)
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    if(number_of_blocks==2):
        for e in dxf.entities:
           # indexdxf=0
                
                #@print("共有",i,"个insert")
                #print(e.DXFTYPE,e.dxf.flags)
            if(e.DXFTYPE=="LWPOLYLINE"):
                for v in range (0,e.dxf.count):
                    print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                    i=i+1
                        
            if(e.DXFTYPE== 'POLYLINE'):
                    #print(e.get_mode())
                length=e.__len__()
                
                print(length)
                  
                    
                if(length>75):
                    indexdxf=indexdxf+1
                       
                            #name=b.dxf.name+".dxf"
                      
                    newdoc= ezdxf.new("R2010")
                    name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                            
                    msp.add_polyline2d(e.points())
                       
                ###########如果points()小于100，我们认为是内嵌图形，不能作为一个模型，不新建dxf，直接写入现有的msp中
                elif(length<75):
                    print("模型文件的内部图形文件")
                        #for vtex in e.vertices:
                    msp.add_polyline2d(e.points())
                        #@msp.add_polyline(e)
                            #print("这是一个新的dxf模型文件的图形文件")
                    
                newdoc.saveas(name)
                print("模型",name,"建立好了")
    else:
        for b in dxf.blocks:
            print(b.name)
             #print(b.name,i)
            #points=[]
            j=j+1
             #######每一个块对应一个模型。
            newdoc= ezdxf.new()
            if(b.dxf.name!="*Model_Space" and b.dxf.name!="*Paper_Space"):
                
                    name=b.dxf.name+".dxf"
                    msp=newdoc.modelspace()
                    for e in b: 
                 #print(e.DXFTYPE,j)
                        if(e.DXFTYPE=="POLYLINE"):
                            #print(e.DXFTYPE,j)
                            msp.add_polyline2d(e.points())
                        if(e.DXFTYPE=="ARC"):
                            msp=newdoc.modelspace()
                            msp.add_arc(e.dxf.center,e.dxf.radius,e.dxf.start_angle,e.dxf.end_angle)           
            
            #name=str(j)+".dxf"
                    newdoc.saveas(name)
            

###################


if __name__=="__main__":
    #
    
    #rotate_zdxf("Drawing.dxf",(-math.pi)/24,"2.dxf")
    #rotate_zdxf("Drawing10.dxf",(-math.pi)/24,"3.dxf")
    #rotate_zdxf("Drawing31.dxf",(-math.pi)/36 ,"3.dxf")
    #movenest(5,"rotate1.dxf")
    #edge("Drawing2.dxf")
    #edge("2.dxf")
    #extractdxf("12-30 ZAOG042221504 #22.dxf")
    #extractdxf("6-10 204422140110 男款 #22 奕翔转单切割档.dxf")
     #22
    #extractdxf("126.dxf")
    extractdxf("12-30 ZAOG042221504 #22.dxf")
   


