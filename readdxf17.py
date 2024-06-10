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

##############
############1.2版本可能要开始设计界面了，因为基本的排版已经基本解决了， 
import ezdxf
import os
#
from math import *
import math
from ezdxf.addons import Importer
#from ezdxf import Importer
from polycrash02 import polyCrash,polyCrash2,polyCrash3,polyCrash_3,polyCrash_4

from maxminpoint02 import findMaxXVertex,findMaxYVertex,findMinXVertex,findMinYVertex



def maxNum(array):
    maxNumber=array[0]
    for item in array:
        if item>maxNumber:
            maxNumber=item
    print("该数列的最大值为",maxNumber)
    return maxNumber

def minNum(array):
    minNumber=array[0]
    for item in array:
        if item<minNumber:
            minNumber=item
    print("该数列的最小值为",maxNumber)
    return minNumber







def movexdxf(srcdxf,x):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,0,0)
     return dxf

############移动后保存到源文件
def movexy(srcdxf,x,y):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,y,0)
     dxf.saveas(srcdxf)


###############移动后保存到另外一个文件
def copytomove(srcdxf,x,y,targetdxf):
    dxf=ezdxf.readfile(srcdxf)
    for e in dxf.entities:
        e.translate(x,y,0)
    dxf.saveas(targetdxf)
    

#############以下是旋转方法函数，表示对dxf文件图像的旋转。


def moveydxf(srcdxf,y):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(0,y,0)
     return dxf



def rotate_zdxf(srcdxf,angle,savename):
    ##########dx,dy 代表要移动的量。
    #dx=100
    dxf=ezdxf.readfile(srcdxf)
    i=0
    for e in dxf.entities:
        #e.scale(2,2,1)       
        try:
            #lay_out=e.get_layout()
            e.rotate_z(angle)
            #print("进入到角度旋转")
        ##########这里只做旋转，不做平移。
            #e.translate(239,191,0)
            #print("lay_out版图为",lay_out)
            #print("get_layout(),能够调用成功")
        except:
            print("无法调用getlyaout") 
    dxf.saveas(savename)
    return dxf

#########################以下是dxf文件合并函数


def dxfimport(source, target):
    importer = Importer(source, target)
    #importer=ezdxImporter(source,target)
    # import all entities from source modelspace into target modelspace
    #importer.import_all(table_conflict='discard', block_conflict='discard')
    #target.move(100,100)
    importer.import_modelspace()
    
    # import all required resources and dependencies
    importer.finalize()

    target.saveas("mergex.dxf")

    #return target
######################合并文件必须同时打开2个文件。
def mix(sdxf,tdxf,savename):
    base_dxf = ezdxf.readfile(tdxf)

#for filename in (inputdxf4,inputdxf3,inputdxf10):
    merge_dxf = ezdxf.readfile(sdxf)
    dxfimport(merge_dxf, base_dxf)

# base_dxf.save()  # to save as file1.dxf
    #base_dxf.saveas('nest.dxf#base_dxf.saveas("testrotate.dxf")
    base_dxf.saveas(savename)
    
    print("合并dxf文件成功") 
#base_dxf.show('merged.dxf')
#mix(inputdxf2,inputdxf3)


#######################
    #################
    #################重新定义一个合并函数，并显示合并后的多边形之间的距离
def mergeDxf(sdxf,tdxf,savename):
    base_dxf = ezdxf.readfile(tdxf)

#for filename in (inputdxf4,inputdxf3,inputdxf10):
    merge_dxf = ezdxf.readfile(sdxf)
    dxfimport(merge_dxf, base_dxf)

# base_dxf.save()  # to save as file1.dxf
    #base_dxf.saveas('nest.dxf#base_dxf.saveas("testrotate.dxf")
    base_dxf.saveas(savename)
    print(polyCrash(savename))
    print("合并dxf文件成功") 
#base_dxf.show('merged.dxf')


###############以下是排版方法，可以实现n*n的排版。
def movenest(n,srcdxf):
   
############横向排版
    movexdxf(srcdxf,150).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    os.remove("D2.dxf")
    for  i in range(1,n):
        movexdxf(srcdxf,i*150).saveas("D2.dxf")
#saveas("D2.dxf")
        mix("D0.dxf","D2.dxf","D0.dxf")
        os.remove("D2.dxf")

############对其进行竖直排版
    ydxf = ezdxf.readfile("D0.dxf")
    ydxf.saveas("Dy.dxf")
    #moveydxf("Dy.dxf",100).saveas("D3.dxf")
#saveas("D2.dxf")
    
    #mix("Dy.dxf","D3.dxf")
    #os.remove("D3.dxf")

    ##########
    ############
    #import ezdxf
    doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
    msp = doc.modelspace() # 获取模型空间
    #msp.add_text("Hello World") # 添加文字
    doc.saveas("D4.dxf") # 保存图形
    
    for j in range(1,2*n):
        moveydxf("Dy.dxf",j*90).saveas("D3.dxf")
#saveas("D2.dxf")
        mix("D4.dxf","D3.dxf","D4.dxf")
        #mix("D4.dxf","D3.dxf","D4.dxf")
        os.remove("D3.dxf")


###########################
        ###################
        #################z上一个排序函数只是写死了模型的高度和宽度
        ###############以下的函数将通过运算来实现。
        #################

def nestHeightWidth(n,srcdxf,height,width):
   
############横向排版
    movexdxf(srcdxf,2*width).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    os.remove("D2.dxf")
    for  i in range(1,n):
        movexdxf(srcdxf,i*2*width).saveas("D2.dxf")
#saveas("D2.dxf")
        mix("D0.dxf","D2.dxf","D0.dxf")
        os.remove("D2.dxf")

############对其进行竖直排版
    ydxf = ezdxf.readfile("D0.dxf")
    ydxf.saveas("Dy.dxf")
    #moveydxf("Dy.dxf",100).saveas("D3.dxf")
#saveas("D2.dxf")
    
    #mix("Dy.dxf","D3.dxf")
    #os.remove("D3.dxf")

    ##########
    ############
    #import ezdxf
    doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
    msp = doc.modelspace() # 获取模型空间
    #msp.add_text("Hello World") # 添加文字
    doc.saveas("D4.dxf") # 保存图形
    
    for j in range(1,2*n):
        moveydxf("Dy.dxf",j*height).saveas("D3.dxf")
#saveas("D2.dxf")
        mix("D4.dxf","D3.dxf","D4.dxf")
        #mix("D4.dxf","D3.dxf","D4.dxf")
        os.remove("D3.dxf")


##########
        ##########将模型旋转并实现合并
        #############
def rotatenest():   
#nest(10,"Drawing2.dxf")
    rotate_zdxf("Drawing2.dxf",math.pi,"rotate1.dxf")
    mix("Drawing2.dxf","rotate.dxf","rotate1.dxf")
    print("将源文件和旋转好的移动到文件都保存到rotate1.dxf文件中")
     #for i in range(1,n)
       # rotate_zdxf(srcdxf,math.pi)
       # mix(srcdxf,"rotate.dxf")
###############
       ##########
       ##########
       # mix(srcdxf,"rotate.dxf")



def classifyForDxf(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"

    #############寻找实体中x值最大的和y值最大的
    for e in dxf.entities:
        
        #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
               ########如果大于75则可以主张为轮廓比较大，归属到单个模型
           # for v in range (0,e.dxf.count):
                   # print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1]            #i=i+1
            
            for vtex  in e.vertices():
                    #maxnumber=e.find(max(e.vertices))
                  print(vtex)
                    #print(vtex[0])
                    #maxvalue=max(vtex[0])
            #return
    miny=findMinYVertex(srcdxf)
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    print("多边形竖直方向最小为",miny)
    print("多边形竖直方向最大为",maxy)
    print("多边形X方向最小为",minx)
    print("多边形X方向最小为",maxx)
    


################
                  ########
                  ###########
                  ########根据不同形状进行组合，并通过组合形成排版单元
                  ###########再通过单元组合成整图。


def egdeset(srcdxf,savename,dx,concave):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #rint("开始判断2个模型是否交叉")
    #先将模型旋转180度，

    ##############
    ##############
    ##############先把模型手动调整好位置
    #rotate_zdxf(srcdxf,(1/24)*(math.pi),srcdxf)
    

    ##############再开始找靶点和调整位置
    miny=findMinYVertex(srcdxf)
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    height=maxy[1]-miny[1]
    movex=maxx[0]-minx[0]
    #width=maxx[0]-minx[0]
    #########
    #########如果模型的形状不是上大下小的情况的，属于中间凹陷的，那么
    #########点的情况需要额外处理，
    if(concave==1):
        print("判断是右凹形多边形")
        rotatename="copytomove.dxf"
        #findMinYVertex(rotatename)
        #findMinXVertex(rotatename)
       #findMaxXVertex(rotatename)
       #findMaxYVertex(rotatename)

        ###############
        ###########如果是凹面多边形，那么宽度需要调整
        movex=maxx[0]-minx[0]
        width=(4/5)*movex
        movey=0
        copytomove(srcdxf,movex*(4/5),movey,rotatename)
        #movexy(srcdxf,movex+dx,movey)
    elif (concave==0):
        ####
        width=movex*(7/10)
        print("判断是凸面形多边形")
        rotatename="rotatename.dxf"
        rotate_zdxf(srcdxf,math.pi,rotatename)
        findMinYVertex(rotatename)
        findMinXVertex(rotatename)
        findMaxXVertex(rotatename)
        findMaxYVertex(rotatename)
    #k=findMaxYVertex(rotatename)-findMinYVertex(rotatename)

    ##########
    ##########具体执行时调和的结果，综合的结果该结果比较理想
        movey=(findMaxYVertex(srcdxf))[1]-(findMaxYVertex(rotatename))[1]
        movex=(findMaxXVertex(srcdxf))[0]-((findMaxYVertex(rotatename))[0]+(findMinXVertex(rotatename))[0])/2

        move_x=(findMaxXVertex(srcdxf))[0]-(findMinXVertex(rotatename))[0]
        print("两图像之间的Y轴距离为",movey)
    #distancex=(movex+move_x)/2
        movexy(rotatename,movex+dx,movey)
    #dxf.saveas(savename)
    #######将模型合并并且写入到指定的文件中
    mix(srcdxf,rotatename,savename)
    '''distance=polyCrash(savename)
    print(distance)
    if(distance):
        os.remove(savename)
        movexy(rotatename,movex+dx-distance,movey)
        mix(srcdxf,rotatename,savename)'''
    
    ##########
    #########
    #######计算模型的高度
    
    print("最新合并的图像是怎么样的？")
    return height,width

    

def distanceSet(srcdxf,savename,dx,concave):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #rint("开始判断2个模型是否交叉")
    #先将模型旋转180度，

    ##############
    ##############
    ##############先把模型手动调整好位置
    #rotate_zdxf(srcdxf,(1/24)*(math.pi),srcdxf)
    

    ##############再开始找靶点和调整位置
    miny=findMinYVertex(srcdxf)
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    height=maxy[1]-miny[1]
    movex=maxx[0]-minx[0]
    #width=maxx[0]-minx[0]
    #########
    #########如果模型的形状不是上大下小的情况的，属于中间凹陷的，那么
    #########点的情况需要额外处理，
    if(concave==1):
        print("判断是右凹形多边形")
        rotatename="copytomove.dxf"
        #findMinYVertex(rotatename)
        #findMinXVertex(rotatename)
       #findMaxXVertex(rotatename)
       #findMaxYVertex(rotatename)

        ###############
        ###########如果是凹面多边形，那么宽度需要调整
        movex=maxx[0]-minx[0]
        width=(4/5)*movex
        movey=0
        copytomove(srcdxf,movex*(4/5),movey,rotatename)
        #movexy(srcdxf,movex+dx,movey)
    elif (concave==0):
        ####
        width=movex*(5.5/10)
        print("判断是凸面形多边形")
        rotatename="rotatename.dxf"
        rotate_zdxf(srcdxf,math.pi,rotatename)
        findMinYVertex(rotatename)
        findMinXVertex(rotatename)
        findMaxXVertex(rotatename)
        findMaxYVertex(rotatename)
    #k=findMaxYVertex(rotatename)-findMinYVertex(rotatename)

    ##########
    ##########具体执行时调和的结果，综合的结果该结果比较理想
        movey=(findMaxYVertex(srcdxf))[1]-(findMaxYVertex(rotatename))[1]
        movex=(findMaxXVertex(srcdxf))[0]-((findMaxYVertex(rotatename))[0]+(findMinXVertex(rotatename))[0])/2

        move_x=(findMaxXVertex(srcdxf))[0]-(findMinXVertex(rotatename))[0]
        print("两图像之间的Y轴距离为",movey)
    #distancex=(movex+move_x)/2
        movexy(rotatename,movex,movey*1.04)
        #movexy(rotatename,movex,movey)
    #dxf.saveas(savename)
    #######将模型合并并且写入到指定的文件中,并进行修正，polyCrash就是可以修正的量
    mix(srcdxf,rotatename,savename)
    distance=polyCrash(savename)
    #print("2个模型之间的距离为",distance)
    errorDistance=distance
    while(distance>0.1):
        errorDistance+=distance
        os.remove(savename)
        movexy(rotatename,-distance,0)
        mix(srcdxf,rotatename,savename)
        distance=polyCrash(savename)

    #width=width-errorDistance
    #width=movex
    ##########
    #########
    #######计算模型的高度
    
    print("最新合并的图像是怎么样的？")
    return height,width


 

   ##############
#############建立能够自动识别宽度的排版函数#################

def nestWidth2(n,srcdxf,height,concave):

    #########
    ##########第一步大致调整到合适的位置
    
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    width=maxx[0]-minx[0]
############横向排版
    movexdxf(srcdxf,2*width).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    
    ###########微调，如果distance为真
    distance=polyCrash2("D0.dxf")
    errorDistance=distance
    #############
    #############需要进行反复修正2组模型之间的距离
    while(distance>0.1):
        errorDistance+=distance
        os.remove("D0.dxf")
        movexy("D2.dxf",-distance,0)
        mix(srcdxf,"D2.dxf","D0.dxf")
        distance=polyCrash2("D0.dxf")
    '''#errorDistance=distance
    os.remove("D0.dxf")
    os.remove("D2.dxf")
    copytomove(srcdxf,-distance,0,"D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    distance=polyCrash2("D0.dxf")'''
    #width=
    MaxX=findMinXVertex("D2.dxf")
    MinX=findMinXVertex(srcdxf)
    width=MaxX[0]-MinX[0]
    print("2组合模型的整体宽度为",width)


    ###########
    ###########在正式开始排版前还需要就竖直方向测试高度
    moveydxf("D2.dxf",height).saveas("Dheight.dxf")
    mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
    distanceH=polyCrash3("Dhtest.dxf")
    while(distanceH==0):
        os.remove("Dhtest.dxf")
        height=height+1
        moveydxf("D2.dxf",height).saveas("Dheight.dxf")
        mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
        distanceH=polyCrash3("Dhtest.dxf")
    
    print("最合适的高度为",height)
    ##############
    ################如果这个模型的最右边的点位于该模型的中间部分
    ################那么就要特殊处理了
    #if(concave==1)
    #os.remove("Dhtest.dxf")
###########开始横向排版
    #os.remove("D2.dxf")
    for  i in range(1,n-1):
        movexdxf(srcdxf,(i+1)*width).saveas("D2.dxf")
#saveas("D2.dxf")
        mix("D0.dxf","D2.dxf","D0.dxf")
        os.remove("D2.dxf")

############对其进行竖直排版
        ########竖直方向不能碰撞，所以需要设置
    ydxf = ezdxf.readfile("D0.dxf")
    ydxf.saveas("Dy.dxf")
    #moveydxf("Dy.dxf",100).saveas("D3.dxf")
#saveas("D2.dxf")
    
    #mix("Dy.dxf","D3.dxf")
    #os.remove("D3.dxf")

    ##########
    ############
    #import ezdxf
    doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
    msp = doc.modelspace() # 获取模型空间
    #msp.add_text("Hello World") # 添加文字
    doc.saveas("D4.dxf") # 保存图形

    #moveydxf("Dy.dxf",height).saveas("D3.dxf")

    #mix("D4.dxf","D3.dxf","D4.dxf")
  #  distanceH=
    #########
    #while(distance==0)
        
    
    
    for j in range(0,2*n):
        moveydxf("Dy.dxf",j*height).saveas("D3.dxf")
        ##################
        ##################当模型是均匀的并且是中间窄，两端大的时候
        #if(concave==1)
                        
#saveas("D2.dxf")
        mix("D4.dxf","D3.dxf","D4.dxf")
        #mix("D4.dxf","D3.dxf","D4.dxf")
        os.remove("D3.dxf")


#######################
        ######################先纵向排版，然后再横向排版
def nestHeightFirst(n,srcdxf,width,height):



    ##########
    #########'''
    '''由于是从一列开始排，所以基本的排版是从列开始'''
    miny=findMinYVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    Height=maxy[1]-miny[1]
    #########
    #print("进入到nestHeight的高度和宽度",height)
    #movexy(srcdxf,0,height)
    ##########第一步大致调整到合适的位置
    copytomove(srcdxf,0,-2*Height,"D2.dxf")
    #minx=findMinXVertex(srcdxf)
    #maxx=findMaxXVertex(srcdxf)
    #width=maxx[0]-minx[0]
############横向排版
    #movexdxf(srcdxf,2*width).saveas("D2.dxf")
    

    #############@###该模板是从纵向开始排版
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    print("先测试第一个合并的效果")
    ###########微调，如果distance为真
    distance=polyCrash2("D0.dxf")
    errorDistance=distance
    #############
    #############需要进行反复修正2组模型之间的距离
    while(distance>0.1):
        errorDistance+=distance
        os.remove("D0.dxf")
        movexy("D2.dxf",0,distance)
        mix(srcdxf,"D2.dxf","D0.dxf")
        distance=polyCrash2("D0.dxf")
    #errorDistance=distance
    '''os.remove("D0.dxf")
    os.remove("D2.dxf")
    copytomove(srcdxf,-distance,0,"D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    distance=polyCrash2("D0.dxf")'''
    #width=

    ###############以上是处理模型的竖直排列的问题
    ##########得到2个模型的距离。
    MaxY1=findMaxYVertex("D2.dxf")
    MaxY2=findMaxYVertex(srcdxf)
    actual_Height=MaxY2[1]-MaxY1[1]
    print("2组合模型的整体高度为",actual_Height)


    ###########
    ###########在正式开始排版前还需要就竖直方向测试高度
    '''moveydxf("D2.dxf",height).saveas("Dheight.dxf")
    mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
    distanceH=polyCrash3("Dhtest.dxf")
    while(distanceH==0):
        os.remove("Dhtest.dxf")
        height=height+1
        moveydxf("D2.dxf",height).saveas("Dheight.dxf")
        mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
        distanceH=polyCrash3("Dhtest.dxf")'''
    
    # print("最合适的高度为",height)
    #os.remove("Dhtest.dxf")
###########开始横向排版
    os.remove("D2.dxf")
    for  i in range(1,n):
        #moveydxf(srcdxf,-(i+1)*actual_Height).saveas("D2.dxf")
        copytomove(srcdxf,0,-i*actual_Height,"D2.dxf")
#saveas("D2.dxf")
        mix("D0.dxf","D2.dxf","D0.dxf")
        #os.remove("D0.dxf")

        os.remove("D2.dxf")

############对其进行竖直排版
########竖直方向不能碰撞，所以需要设置
    ydxf = ezdxf.readfile("D0.dxf")
    ydxf.saveas("Dy.dxf")
    #moveydxf("Dy.dxf",100).saveas("D3.dxf")
#saveas("D2.dxf")
    
    #mix("Dy.dxf","D3.dxf")
    #os.remove("D3.dxf")

    ##########
    ############
    #import ezdxf
    doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
    msp = doc.modelspace() # 获取模型空间
    #msp.add_text("Hello World") # 添加文字
    doc.saveas("D4.dxf") # 保存图形

    #moveydxf("Dy.dxf",height).saveas("D3.dxf")

    #mix("D4.dxf","D3.dxf","D4.dxf")
  #  distanceH=
    #########
    #while(distance==0)
    movexdxf(srcdxf,width).saveas("Dcrash.dxf")
        ##################
        ##################当模型是均匀的并且是中间窄，两端大的时候
        #if(concave==1)
                        
#saveas("D2.dxf")
    mix(srcdxf,"Dcrash.dxf","Dcrash.dxf")
    distance=polyCrash3("Dcrash.dxf")
    '''while(distance==0):
        os.remove("Dcrash.dxf")
        width=width+1
        movexdxf(srcdxf,width).saveas("Dcrash.dxf")
        mix(srcdxf,"Dcrash.dxf","Dcrash.dxf")
        distance=polyCrash3("Dcrash.dxf")'''
    
    
    for j in range(0,2*n):
        movexdxf("Dy.dxf",j*width).saveas("D3.dxf")
        ##################
        ##################当模型是均匀的并且是中间窄，两端大的时候
        #if(concave==1)
                        
#saveas("D2.dxf")
        mix("D4.dxf","D3.dxf","D4.dxf")
        #mix("D4.dxf","D3.dxf","D4.dxf")
        os.remove("D3.dxf")
    





##################
        ##################
        ############2个模型拼合的精细调整
def distanceSet2(srcdxf,savename,dx,concave):
    
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #rint("开始判断2个模型是否交叉")
    #先将模型旋转180度，

    ##############
    ##############
    ##############先把模型手动调整好位置
    #rotate_zdxf(srcdxf,(1/24)*(math.pi),srcdxf)
    

    ##############再开始找靶点和调整位置
    miny=findMinYVertex(srcdxf)
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    height=maxy[1]-miny[1]
    movex=maxx[0]-minx[0]
    width=maxx[0]-minx[0]
    #########
    #########如果模型的形状不是上大下小的情况的，属于中间凹陷的，那么
    #########点的情况需要额外处理，
    if(concave==1):
        print("判断是右凹形多边形")
        rotatename="copytomove.dxf"
        #findMinYVertex(rotatename)
        #findMinXVertex(rotatename)
       #findMaxXVertex(rotatename)
       #findMaxYVertex(rotatename)

        ###############
        ###########如果是凹面多边形，那么宽度需要调整
        movex=maxx[0]-minx[0]
        width=(4/5)*movex
        movey=0
        copytomove(srcdxf,movex*(4/5),movey,rotatename)
        #movexy(srcdxf,movex+dx,movey)
    elif (concave==0):
        ####
        #width=movex*(5.5/10)
        print("判断是凸面形多边形")
        rotatename="rotatename.dxf"
        rotate_zdxf(srcdxf,math.pi,rotatename)
        findMinYVertex(rotatename)
        findMinXVertex(rotatename)
        findMaxXVertex(rotatename)
        findMaxYVertex(rotatename)
    #k=findMaxYVertex(rotatename)-findMinYVertex(rotatename)

    ##########
    ##########具体执行时调和的结果，综合的结果该结果比较理想
        movey=(findMaxYVertex(srcdxf))[1]-(findMaxYVertex(rotatename))[1]
        movex=(findMaxXVertex(srcdxf))[0]-((findMaxYVertex(rotatename))[0]+(findMinXVertex(rotatename))[0])/2

        move_x=(findMaxXVertex(srcdxf))[0]-(findMinXVertex(rotatename))[0]
        print("两图像之间的Y轴距离为",movey)
    #distancex=(movex+move_x)/2
        if((minx[1]>(miny[1]+maxy[1])/2)):
           #############如果模型的形状是上宽下窄的
            print("模型是上大下小的")
            if(miny[0]>minx[0]+(maxx[0]-minx[0])*2/3 or miny[0]<minx[0]+(maxx[0]-minx[0])*1/3):
                print("在上大下小的模型中，该模型的相对宽度比较均匀")
                movexy(rotatename,movex,movey)
            else:
                print("该模型并不均匀")
                movexy(rotatename,movex,movey*0.975)
        else:
            ############否则就需要往上移动一点，以满足更好的配合，
            #################但这个并不是理想化的模型
            print("模型是上小下大的")
            if(maxy[0]>minx[0]+(maxx[0]-minx[0])*2/3 or maxy[0]<minx[0]+(maxx[0]-minx[0])*1/3):
                print("在上小下的模型中，该模型的相对宽度比较均匀")
                movexy(rotatename,movex,movey)
            else:
                print("该模型并不均匀")
                movexy(rotatename,movex,movey*1.025)
                
            
    #dxf.saveas(savename) 
    #######将模型合并并且写入到指定的文件中,并进行修正，polyCrash就是可以修正的量
    mix(srcdxf,rotatename,savename)

    #######这里是2合并后2个模型的组合宽度
    
    
    #print("2个模型的宽度为",Width2model)
    
    distance=polyCrash(savename)
    while(distance==0):
        os.remove(savename)
        movexy(rotatename,1,0)
        mix(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    #print("2个模型之间的距离为",distance)
    errorDistance=distance
    while(distance>0.1):
        errorDistance+=distance
        os.remove(savename)
        movexy(rotatename,-distance,0)
        mix(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    #########

    
    #width_2modle=(findMaxXVertex(savename))[0]-(findMinXVertex(savename))[0]
    #movexy(rotatename,movex,movey)

  
    #print("2个模型的宽度为",Width2model)
    #width=width-errorDistance
    #width=movex
    ##########
    #########
    #######计算模型的高度
    
    print("最新合并的图像是怎么样的？")
    return height,width


#def BestSet2Modle(srcdxf1,srcdxf2)
    
def heightSet(srcdxf,savename,dx,concave):
    
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    ##############再开始找靶点和调整位置
    miny=findMinYVertex(srcdxf)
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    maxy=findMaxYVertex(srcdxf)
    height=maxy[1]-miny[1]
    movex=maxx[0]-minx[0]

    ##########这里定义的实际宽度和高度都不太对。
    actual_width=maxx[0]-minx[0]
    #########
    #########如果模型的形状不是上大下小的情况的，属于中间凹陷的，那么
    #########点的情况需要额外处理，
    if(concave==1):
        print("判断是右凹形多边形")
        rotatename="nextRow.dxf"
        print("到底有没有进入到这个循环？")
        rotate_zdxf(srcdxf,(math.pi),rotatename)
        ##########
        ###########先旋转，然后再将旋转后的模型移动到下方。

        ############应该是先将模型copy一份到右边，然后再旋转移动到下方？其
        ########其实区别不大。
        ###############
        ###########如果是凹面多边形，那么宽度需要调整
        rotatemaxx=findMaxXVertex(rotatename)
        #movex=maxx[0]-minx[0]
        width=maxx[0]-rotatemaxx[0]  ##########这个宽度实际上是一个相对宽度，
        #############只要模型不碰撞就这个宽度并不精确。
        #movey=0
        actual_height=miny[1]
        movexy(rotatename,width,actual_height)
        #movexy(srcdxf,movex+dx,movey)
        mix(srcdxf,rotatename,savename)


        ############由于涉及到X轴的干涉，所以需要增加一个mix
        #############2022年6月14日
        #gap=0
        ############
        ##############再来测试2个模型之间的垂直距离
        distance=polyCrash(savename)
        #actual_width=actual_width-distance
        while(distance>0.1):
                #errorDistance+=distance
                os.remove(savename)
                movexy(rotatename,0,distance)
                mix(srcdxf,rotatename,savename)
                distance=polyCrash(savename)
                #gap=gap+1
        #############
                ######单独设置X的宽度有可能存在间隙
        #acutal_gap=polyCrash()
        copytomove(srcdxf,actual_width,0,"Dwidthset.dxf")
        mix(srcdxf,"Dwidthset.dxf","Dw.dxf")
        distance=polyCrash("Dw.dxf")
        while(distance>0.1):
            os.remove("Dwidthset.dxf")
            os.remove("Dw.dxf")
            actual_width=actual_width-distance
            copytomove(srcdxf,actual_width,0,"Dwidthset.dxf")
            mix(srcdxf,"Dwidthset.dxf","Dw.dxf")
            distance=polyCrash("Dw.dxf")
             
            
        ########这个distance属于最远的距离，但是这里的出来的是最小距离
        #########这里是有误差的。
        ###########
        #############还要再做一次碰撞，因为怕撞到右边的模型
        #os.remove("Dw.dxf")
        #os.remove("Dw.dxf")
        
        copytomove(srcdxf,actual_width,0,"Dwidthset.dxf")
        #mix(srcdxf,"Dwidthset.dxf","Dw.dxf")
        mix(savename,"Dwidthset.dxf","Dmix3.dxf")

            #########先把距离好好判断一下

        #########
        #########上下的模型是非常紧凑的,这个时候还需要调整新Dmix3的距离
        distance4=polyCrash_4("Dmix3.dxf")
        #distance3=polyCrash_3("Dmix3.dxf")
        if(distance4>1 ):
            os.remove("Dmix3.dxf")
            os.remove(savename)
            #actual_height=actual_height+1 ######这个需要给后续排版作为参数使用。
            #actual_width= actual_width-1
            movexy(rotatename,-distance4/2,distance4/2)
            #movexy(rotatename,distance4,distance4/2)
        #movexy(srcdxf,movex+dx,movey)
            mix(srcdxf,rotatename,savename)
            mix(savename,"Dwidthset.dxf","Dmix3.dxf")
            distanc4=polyCrash_4("Dmix3.dxf")
            #distance3=polyCrash_3("Dmix3.dxf")


##########再来判断最小距离。

            #distance3=polyCrash2("Dmix3.dxf")
        #distance3=polyCrash_3("Dmix3.dxf")

        #########
        #########Dmix3.dxf是合并3个模型的情况。
        distance3=polyCrash_3("Dmix3.dxf")
        #distance=polyCrash("Dw.dxf")
        

        while(distance3==0):
            os.remove("Dmix3.dxf")
            os.remove(savename)
            #os.remove()
            
            actual_height=actual_height-1 ######这个需要给后续排版作为参数使用。
            #actual_width= actual_width-1
            movexy(rotatename,-1,-1)
        #movexy(srcdxf,movex+dx,movey)
            mix(srcdxf,rotatename,savename)
            mix(savename,"Dwidthset.dxf","Dmix3.dxf")
            
            #distance3=polyCrash2("Dmix3.dxf")
            distance3=polyCrash_3("Dmix3.dxf")

        
                
                
        best_height=findMaxYVertex(srcdxf)[1]-findMaxYVertex(rotatename)[1]
        height=best_height        
        
    elif (concave==0):
        ####
        #width=movex*(5.5/10)
        print("判断是凸面形多边形")
        rotatename="rotatename.dxf"
        rotate_zdxf(srcdxf,math.pi,rotatename)
        findMinYVertex(rotatename)
        findMinXVertex(rotatename)
        findMaxXVertex(rotatename)
        findMaxYVertex(rotatename)
    #k=findMaxYVertex(rotatename)-findMinYVertex(rotatename)

    ##########
    ##########具体执行时调和的结果，综合的结果该结果比较理想
        movey=(findMaxYVertex(srcdxf))[1]-(findMaxYVertex(rotatename))[1]
        movex=(findMaxXVertex(srcdxf))[0]-((findMaxYVertex(rotatename))[0]+(findMinXVertex(rotatename))[0])/2

        move_x=(findMaxXVertex(srcdxf))[0]-(findMinXVertex(rotatename))[0]
        print("两图像之间的Y轴距离为",movey)
    #distancex=(movex+move_x)/2
        if((minx[1]>(miny[1]+maxy[1])/2)):
           #############如果模型的形状是上宽下窄的
            print("模型是上大下小的")
            if(miny[0]>minx[0]+(maxx[0]-minx[0])*2/3 or miny[0]<minx[0]+(maxx[0]-minx[0])*1/3):
                print("在上大下小的模型中，该模型的相对宽度比较均匀")
                movexy(rotatename,movex,movey)
            else:
                print("该模型并不均匀")
                movexy(rotatename,movex,movey*0.975)
        else:
            ############否则就需要往上移动一点，以满足更好的配合，
            #################但这个并不是理想化的模型
            print("模型是上小下大的")
            if(maxy[0]>minx[0]+(maxx[0]-minx[0])*2/3 or maxy[0]<minx[0]+(maxx[0]-minx[0])*1/3):
                print("在上小下的模型中，该模型的相对宽度比较均匀")
                movexy(rotatename,movex,movey)
            else:
                print("该模型并不均匀")
                movexy(rotatename,movex,movey*1.025)
                
            
    #dxf.saveas(savename)
    #######将模型合并并且写入到指定的文件中,并进行修正，polyCrash就是可以修正的量
            mix(srcdxf,rotatename,savename)

    #######这里是2合并后2个模型的组合宽度
    
    
    #print("2个模型的宽度为",Width2model)
    
            distance=polyCrash(savename)
            while(distance==0):
                os.remove(savename)
                movexy(rotatename,1,0)
                mix(srcdxf,rotatename,savename)
                distance=polyCrash(savename)
    #print("2个模型之间的距离为",distance)
            errorDistance=distance
            while(distance>0.1):
                errorDistance+=distance
                os.remove(savename)
                movexy(rotatename,-distance,0)
                mix(srcdxf,rotatename,savename)
                distance=polyCrash(savename)
    #########

    
    #width_2modle=(findMaxXVertex(savename))[0]-(findMinXVertex(savename))[0]
    #movexy(rotatename,movex,movey)

  
    #print("2个模型的宽度为",Width2model)
    #width=width-errorDistance
    #width=movex
    ########## 
    #########
    #######计算模型的高度
    
    print("最新合并的图像是怎么样的？")
    return height,actual_width




def nest_from_height_sample(srcdxf,n,concave):
     #rotate_zdxf("Drawing.dxf",(-math.pi)/24,"2.dxf")
    #rotate_zdxf("Drawing10.dxf",(-math.pi)/24,"3.dxf")
    #rotate_zdxf("Piece14-S5.dxf",0 ,"3.dxf")
    rotate_zdxf(srcdxf,0 ,"3.dxf")
    #movenest(5,"rotate1.dxf")
    #edge("Drawing2.dxf")
    #edge("2.dxf")
    #extractdxf("2.dxf")
    try:
        #os.remove("D4.dxf")
        #os.remove("edge.dxf")
        #[Height,Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        [Height,Width]=heightSet("3.dxf","edge.dxf",1,concave)
        #nestWidth2(5,"edge.dxf",Height,1)
        nestHeightFirst(n,"edge.dxf",Width,Height)
        #os.remove("edge.dxf")
    except:
    #######分别对drawing2 ,drawing21进行大范围排版
    #[Height,Width]=egdeset("Drawing21.dxf","edge24.dxf",1,1)
   # [Height,Width]=egdeset("Drawing2.dxf","edge.dxf",1,0)
        #os.remove("edge.dxf")
        #[Height,Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        [Height,Width]=heightSet("3.dxf","edge.dxf",1,concave)
        nestHeightFirst(n,"edge.dxf",Width,Height)
        #nestWidth2(5,"edge.dxf",Height,1)


#def nestWidth2(n,srcdxf,height,concave):
def nestWidth3(nest_whole_number,x_number,y_number,srcdxf,height,concave):
    

    whole_number=int(nest_whole_number)

    #x_number=int(row_number_of_nest)

   # y_number=int(horizantal_number_of_nest)
    #########
    ##########第一步大致调整到合适的位置
    
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    width=maxx[0]-minx[0]
############横向排版

############这里只是做初步的碰撞组合
    movexdxf(srcdxf,2*width).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    
    ###########微调，如果distance为真
    distance=polyCrash2("D0.dxf")
    errorDistance=distance
    #############
    #############需要进行反复修正2组模型之间的距离
    while(distance>0.1):
        errorDistance+=distance
        os.remove("D0.dxf")
        movexy("D2.dxf",-distance,0)
        mix(srcdxf,"D2.dxf","D0.dxf")
        distance=polyCrash2("D0.dxf")
    '''#errorDistance=distance
    os.remove("D0.dxf")
    os.remove("D2.dxf")
    copytomove(srcdxf,-distance,0,"D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    distance=polyCrash2("D0.dxf")'''
    #width=
    MaxX=findMinXVertex("D2.dxf")
    MinX=findMinXVertex(srcdxf)
    width=MaxX[0]-MinX[0]
    print("2组合模型的整体宽度为",width)
    '''这里的整体模型宽度不能随便定义成2个，而要一起定义。'''

    ###########
    ###########在正式开始排版前还需要就竖直方向测试高度
    moveydxf("D2.dxf",height).saveas("Dheight.dxf")
    mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
    distanceH=polyCrash3("Dhtest.dxf")
    while(distanceH==0):
        os.remove("Dhtest.dxf")
        height=height+1
        moveydxf("D2.dxf",height).saveas("Dheight.dxf")
        mix("Dheight.dxf","D2.dxf","Dhtest.dxf")
        distanceH=polyCrash3("Dhtest.dxf")
    
    print("最合适的高度为",height)
    ##############
    ################如果这个模型的最右边的点位于该模型的中间部分
    ################那么就要特殊处理了
    #if(concave==1)
    #os.remove("Dhtest.dxf")
###########开始横向排版
    #os.remove("D2.dxf")
    ############如果横向排版的数量大则
    #####当需要排版的数量大于一行时
    if(whole_number>x_number):
        '''如果是奇数'''

        if(x_number%2):
            for  i in range(0,int((x_number-1)/2)):
                movexdxf(srcdxf,i*width).saveas("D2.dxf")
                #########由于这里是2个模型的宽度，所以要
            ##########会出现模型的如果是奇数的情况。
        #saveas("D2.dxf")
                mix("D0.dxf","D2.dxf","D0.dxf")
                os.remove("D2.dxf")
            '''等for循环完成了，需要做一个判断，也即最后还差一个模型'''
            '''这个3.dxf后期需要更改，有点太不上档次,D2.dxf文件是待合并文件，D0.dxf是合并的单排文件'''
            
            movexdxf("3.dxf",((x_number-1)/2)*width).saveas("D2.dxf")
            mix("D0.dxf","D2.dxf","D0.dxf")
            os.remove("D2.dxf")
        else:
            ####如果是偶数？
            for  i in range(0,int((x_number)/2)):
                movexdxf(srcdxf,i*width).saveas("D2.dxf")
                #########由于这里是2个模型的宽度，所以要
            ##########会出现模型的如果是奇数的情况。
        #saveas("D2.dxf")
                mix("D0.dxf","D2.dxf","D0.dxf")
                os.remove("D2.dxf")
            '''等for循环完成了，需要做一个判断，也即最后还差一个模型'''
            '''这个3.dxf后期需要更改，有点太不上档次,D2.dxf文件是待合并文件，D0.dxf是合并的单排文件''' 

        '''到这里是2*n'''
        ydxf = ezdxf.readfile("D0.dxf")
        ydxf.saveas("Dy.dxf")
        #os.remove("D0.dxf")
        '''doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
        msp = doc.modelspace() # 获取模型空间,这里莫名其妙的获取模型空间干什么。保存D4是做什么
    #msp.add_text("Hello World") # 添加文字
        doc.saveas("D4.dxf")''' # 保存图形
    ###########如果总排版数和恰好是一行，常见于上次排版的剩余空间。
    elif(whole_number==x_number):
        #os.remove("D4.dxf")
        doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
        msp = doc.modelspace() # 获取模型空间,这里莫名其妙的获取模型空间干什么。保存D4是做什么
    #msp.add_text("Hello World") # 添加文字
        doc.saveas("D4.dxf") # 保存图形
        #########这里重新组建了d4.dxf
        if(whole_number%2):
            for  i in range(0,int(whole_number/2)):
                movexdxf(srcdxf,i*width).saveas("D2.dxf")
        #saveas("D2.dxf")
                mix("D4.dxf","D2.dxf","D4.dxf")
                #os.remove("D2.dxf")
            '''需要单独的将模型再增加一个模型'''
            movexdxf("3.dxf",((whole_number-1)*width)/2).saveas("D2.dxf")
        #saveas("D2.dxf")
            mix("D4.dxf","D2.dxf","D4.dxf")
            #####
            os.remove("D2.dxf")
            print("剩下的排版只有1行，且1行未满")
            
        else:
            for  i in range(0,int(whole_number/2)):
                movexdxf(srcdxf,i*width).saveas("D2.dxf")
        #saveas("D2.dxf")
                mix("D4.dxf","D2.dxf","D4.dxf")
                os.remove("D2.dxf")
            

############对其进行竖直排版
        ########竖直方向不能碰撞，所以需要设置
    '''ydxf = ezdxf.readfile("D0.dxf")
    ydxf.saveas("Dy.dxf")
    #moveydxf("Dy.dxf",100).saveas("D3.dxf")
#saveas("D2.dxf")
    
    #mix("Dy.dxf","D3.dxf")
    #os.remove("D3.dxf")

    ##########
    ############
    #import ezdxf'''
    '''doc = ezdxf.new('AC1024') # 建立一个新的CAD2010文档
    #doc.encoding='gbk' # 设置编码为简体中文
    msp = doc.modelspace() # 获取模型空间,这里莫名其妙的获取模型空间干什么。保存D4是做什么
    #msp.add_text("Hello World") # 添加文字
    doc.saveas("D4.dxf")''' # 保存图形

        
    '''如果层数大于1，那么竖直方向排版列数'''
    if(y_number>1):
        for j in range(0,y_number-1):

            #if(j<horizantal_number_of_nest-1):
                moveydxf("Dy.dxf",j*height).saveas("D3.dxf")
                ##################
                ##################当模型是均匀的并且是中间窄，两端大的时候
                #if(concave==1)
                                
        #saveas("D2.dxf")
                mix("D4.dxf","D3.dxf","D4.dxf")
                #mix("D4.dxf","D3.dxf","D4.dxf")
                os.remove("D3.dxf")
    ############当模型只有1行时，
  #这里莫名其妙的获取模型空间干什么。保存D4是做什么
  ########如果y_number==1，那就不需要再考虑哦了，直接合并就可以了。
        #ms

            #else :   #(j==horizantal_number_of_nest-1):
            
    rest_number=whole_number-x_number*(y_number-1)
#######如果rest_number或者rest_number只需要排一行则
    #print("horizantal_number_of_nest也即竖排的数量为",horizantal_number_of_nest,)
    if(rest_number!=0 and rest_number!=whole_number):
        print("剩下需要排版的数量为",rest_number)
        #if(rest_number%2):
        for  i in range(0,int((rest_number)/2)):
            movexdxf(srcdxf,i*width).saveas("D2.dxf")
            moveydxf("D2.dxf",(y_number-1)*height).saveas("D3.dxf")
            mix("D4.dxf","D3.dxf","D4.dxf")
            #mix("Drest.dxf","D2.dxf","D0.dxf")
            #os.remove("D2.dxf")
        #saveas("D2.dxf")
            #mix("D0.dxf","D2.dxf","D0.dxf")
        if(rest_number%2):
            print("有可在这里面， D4.dxf文件应该是被污染了，不能随便访问D4.DXF文件的")
            movexdxf("3.dxf",((rest_number-1)/2)*width).saveas("D2.dxf")
            moveydxf("D2.dxf",(y_number-1)*height).saveas("D3.dxf")
            mix("D4.dxf","D3.dxf","D4.dxf")
            #mix("D0.dxf","D2.dxf","D0.dxf")
            #os.remove("D2.dxf")
                    ###########将最后一行排进去
        #moveydxf("D2.dxf",(y_number-1)*height).saveas("D3.dxf")
                ##################
                ##################当模型是均匀的并且是中间窄，两端大的时候
                #if(concave==1)
        os.remove("D0.dxf")
        os.remove("D2.dxf")
        
        #os.remove("D3.dxf")
        #os.remove("D")
        #saveas("D2.dxf")
        #mix("D4.dxf","D3.dxf","D4.dxf")
                    #mix("D4.dxf","D3.dxf","D4.dxf")
        #if(rest_number%2):

    #if(os.path.exists("D3.dxf")):
        #os.remove("D3.dxf")
############对其进行竖直排版
        ########竖直方向不能碰撞，所以需要设置
    #ydxf = ezdxf.readfile("D0.dxf")
    #ydxf.saveas("Dy.dxf")

    ###############
#################最后一行的数量是不确定的。
    



def nest_from_width_sample(srcdxf,n,concave):
     #rotate_zdxf("Drawing.dxf",(-math.pi)/24,"2.dxf")
    #rotate_zdxf("Drawing10.dxf",(-math.pi)/24,"3.dxf")
    #rotate_zdxf("Piece14-S5.dxf",0 ,"3.dxf")
    rotate_zdxf(srcdxf,0 ,"3.dxf")
    #movenest(5,"rotate1.dxf")
    #edge("Drawing2.dxf")
    #edge("2.dxf")
    #extractdxf("2.dxf")
    try:
        #os.remove("D4.dxf")
        #os.remove("edge.dxf")
        [Height,Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        #[Height,Width]=heightSet("3.dxf","edge.dxf",1,concave)
        nestWidth2(n,"edge.dxf",Height,0)
        #nestHeightFirst(n,"edge.dxf",Width,Height)
        #os.remove("edge.dxf")
    except:
    #######分别对drawing2 ,drawing21进行大范围排版
    #[Height,Width]=egdeset("Drawing21.dxf","edge24.dxf",1,1)
   # [Height,Width]=egdeset("Drawing2.dxf","edge.dxf",1,0)
        #os.remove("edge.dxf")
        [Height,Width]=distanceSet2("3.dxf","edge.dxf",1,0)
        #[Height,Width]=heightSet("3.dxf","edge.dxf",1,concave)
        #nestHeightFirst(n,"edge.dxf",Width,Height)
        nestWidth2(n,"edge.dxf",Height,0)



def nest_with_rectangle(dxf_model,number_for_nest,width,height):
    print("需要排版的模型名字为",dxf_model,"排版的数量为",number_for_nest,"版面的宽和长度为",width,height)
    ##########需要测量模型的长款和调整模型的位置，这是个大工程哦。
    ###先要调整模型的角度
    if(os.path.exists("3.dxf")):
        os.remove("3.dxf")
        rotate_zdxf(dxf_model,0 ,"3.dxf")
    else:
        rotate_zdxf(dxf_model,0 ,"3.dxf")
    ########计算模型的高度和最合适的宽度，注意，有些模型可以拼合起来得到最合适的宽度
    ##########必须要组合起来才能得知，单个模型算不出来的。
    if(os.path.exists("edge.dxf")):
       os.remove("edge.dxf")
       [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
    else:
        [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
    ######计算模型横向可以摆多少个

    
    num_of_width=int((1500)/model_Width)######这里的宽度是2个模型的平均宽度
    #######确定可以排多少行，比如排版100，每行12，那么就是100/12=8+1为9行。
    num_of_height=(int(int(number_for_nest)/num_of_width))+1
    print("模型的横排可以的值为",num_of_width,"模型的宽度为",model_Width)
    print("模型的竖排值为",num_of_height)
    nestWidth3(number_for_nest,num_of_width,num_of_height,"edge.dxf",model_Height,0)
    delt_x=findMinXVertex("D4.dxf")[0]
    delt_y=findMinYVertex("D4.dxf")[1]
    movexy("D4.dxf",0-delt_x,0-delt_y)
    #######将模型和外框整合并成1个模型，因为这里面部存在一个模型，整合起来让机器能够识别。
    mix("D4.dxf","xy.dxf","new_nest.dxf")
    print("最后mix成功")
    

def nest_with_rest(dxf_model,number_for_nest,width,height,model_Width,model_Height):
    print("需要排版的模型名字为",dxf_model,"排版的数量为",number_for_nest,"版面的宽和长度为",width,height)
    ##########需要测量模型的长款和调整模型的位置，这是个大工程哦。
    ###先要调整模型的角度
    #######如果该版面里面没有模型，那么我们就从0开始排版模型，如果
    #######版面里面有模型，那么就要从新的位置开始。
    #if()

    ###

    '''if(os.path.exists("3.dxf")):
        os.remove("3.dxf")
        rotate_zdxf(dxf_model,0 ,"3.dxf")
    else:
        rotate_zdxf(dxf_model,0 ,"3.dxf")
    ########计算模型的高度和最合适的宽度，注意，有些模型可以拼合起来得到最合适的宽度
    ##########必须要组合起来才能得知，单个模型算不出来的。
    if(os.path.exists("edge.dxf")):
       os.remove("edge.dxf")
       [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
    else:
        [model_Height,model_Width]=distanceSet2("3.dxf","edge.dxf",1,0)
    ######计算模型横向可以摆多少个'''
     
    
    num_of_width=int((1500)/model_Width)######这里的宽度是2个模型的平均宽度
    #######确定可以排多少行，比如排版100，每行12，那么就是100/12=8+1为9行。
    num_of_height=(int(int(number_for_nest)/num_of_width))+1

    print("模型排版的层数为",num_of_height)
    #print("模型的横排可以的值为",num_of_width,"模型的宽度为",model_Width)
   # print("模型的竖排值为",num_of_height)
    ##########
    ###########如果起始的排版点不等于0，那么问题大了，
    #if(start_x!=0):

    #@left_width=1500-start_x
    #start_nest_number=int(left_width/model_Width)

    nestWidth3(number_for_nest,num_of_width,num_of_height,"edge.dxf",model_Height,0)

    #next_start_x=findMaxXVertex("")
    #delt_x=findMinXVertex("D4.dxf")[0]
   # delt_y=findMinYVertex("D4.dxf")[1]
    
    
    ########获取模型的最大的Y值先
    #next_start_y=findMaxXVertex("D4.dxf")[1]-model_Height+old_start_y   ##需要加上上次的排版数据

    #next_start_x= (int(number_for_nest)-num_of_width*(num_of_height-1))*model_Width+old_start_x

    #movexy("D4.dxf",0-delt_x,0-delt_y)

    #copytomove("D4.dxf",0-delt_x,0-delt_y,"old_nest.dxf")
    ##########"old_nest.dxf"主要用于保存已经排版好的D4.dxf,
    #######将模型和外框整合并成1个模型，因为这里面部存在一个模型，整合起来让机器能够识别。
    #mix("D4.dxf","xy.dxf","new_nest.dxf")
    print("最后mix成功")

    #return next_start_x,next_start_y

    
    


#############实现了drawing2.dxf的密集排版，但是没还没有普适性。所以必须解决普适性的问题
if __name__=="__main__":
    
    #nest_from_width_sample("40.dxf",5,0)
        #os.remove("edge.dxf")
    #nest_from_height_sample("Piece18-S6.dxf",5,1)
   #classifyForDxf("Drawing21.dxf")
    nest_with_rectangle("mode15.dxf",10,1500,6000)
     
    
    #print(polyCrash("edge24.dxf"))
    #mergeDxf("Drawing21")


    

