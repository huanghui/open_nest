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

from this import d
import ezdxf
import os
#
import math
from ezdxf.addons import Importer
import shutil
#from ezdxf import Importer
#from polycrash import polyCrash,polyCrash2,polyCrash3,polyCrash_3,polyCrash_4

from maxminpoint02 import*

from readdxf15 import *

from polycrash03 import test_of_2_model_crash

#from readdxf15 import rotate_zdxf

###################

def copy_dxf(srcdxf,x,y,copy_dxf):
    dxf=ezdxf.readfile(srcdxf)
    msp=dxf.modelspace()
    b=[]
    for e in dxf.entities:
        #print(e)
        body=e.copy()
        b.append(body)
        e.translate(x,y,0)
    for index in b:
        msp.add_entity(index)
      #print(index)
    dxf.saveas(copy_dxf)

##########实现copy n个模型排列
def copy_num_dxf(srcdxf,dx,dy,number_of_copy,targetdxf):

    dxf=ezdxf.readfile(srcdxf)
    msp=dxf.modelspace()
    dxf2=ezdxf.new()

    msp2=dxf2.modelspace()
    #dxf2=dxf.
    b=[]
    #Eother_dxf=[]*number_of_copy
    #other_dxf=[[]]*number_of_copy
    #for num in range(0,number_of_copy):
        #dx=dx*num
        ######取有个最开始的值
        #dxf=dxf2
        #other_dxf[num]=[]
    #last_dxf
    for i in range(0,number_of_copy):
        for e in dxf.entities:
           
            body=e.copy()
                #body2=e.copy()
            #b.append(body)
            #other_dxf[i].b
            msp2.add_entity(body)
            e.translate(dx,dy,0)

        #for entity in b:
          #  msp2.add_entity(entity)
        #other_dxf.append(b)
    
    '''for i in range(number_of_copy):
        for each_entitiy in other_dxf[i].entities:
           #for index in b:
            msp.add_entity(each_entitiy)'''
    

       # for index in b:
           # msp.add_entity(index)
            #print(body)
            #index.transalte(dx*num,0,0)
            #print(index)
        ############这个时候dxf.entities的量比现在大很多。

    dxf2.saveas(targetdxf)



def rotate_dxf(srcdxf,angle,savename):
    ##########dx,dy 代表要移动的量。
    #dx=100
    dxf=ezdxf.readfile(srcdxf)
    i=0
    for e in dxf.entities:
        #e.scale(2,2,1)       
        try:
            #lay_out=e.get_layout()
            e.rotate_z(angle)
           
        except:
            print("无法调用getlyaout") 
    dxf.saveas(savename)
    return dxf



def rotate_dxf_ai(srcdxf,angle,savename):
    ##########dx,dy 代表要移动的量。
    #dx=100
    dxf=ezdxf.readfile(srcdxf)
    i=0
    for e in dxf.entities:
        #e.scale(2,2,1)       
        try:
            #lay_out=e.get_layout()
            e.rotate_z(angle)
           
        except:
            print("无法调用getlyaout") 
    dxf.saveas(savename)
    return dxf



######
def movexy(srcdxf,x,y):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,y,0)
     dxf.saveas(srcdxf)


def moveydxf(srcdxf,y):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(0,y,0)
     return dxf

def movexdxf(srcdxf,x):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,0,0)
     return dxf

####################
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
################

def mix_together(sdxf,tdxf,savename):
    base_dxf = ezdxf.readfile(tdxf)

#for filename in (inputdxf4,inputdxf3,inputdxf10):
    merge_dxf = ezdxf.readfile(sdxf)
    dxfimport(merge_dxf, base_dxf)

# base_dxf.save()  # to save as file1.dxf
    #base_dxf.saveas('nest.dxf#base_dxf.saveas("testrotate.dxf")
    base_dxf.saveas(savename)
    
    print("合并dxf文件成功") 
#base_dxf.show('merged.dxf')
#########################以下是dxf文件

    ###############高度设定和宽度的设定
def find_best_width_height_old(srcdxf,savename,dx,concave):
    
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
        #print("判断是凸面形多边形")
        rotatename="rotatename.dxf"
        rotate_dxf(srcdxf,math.pi,rotatename)

        ##在这里增加代码搞定那个功能吧。



        #######需要把模型的搞定的。
        #########这4个调用是干什么的？
        #findMinYVertex(rotatename)
        #findMinXVertex(rotatename)
       ## findMaxXVertex(rotatename)
       # findMaxYVertex(rotatename)
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
    mix_together(srcdxf,rotatename,savename)

    #######这里是2合并后2个模型的组合宽度
    
    
    #print("2个模型的宽度为",Width2model)
    
    distance=polyCrash(savename)

    #########这里做while循环有点傻吧？

    #####好像也不太傻，因为这里涉及到细节操作，因为上面做的模型并不能代表这个模型就
    #####一定完全满足需求，需要微调。
    while(distance==0):
        os.remove(savename)
        movexy(rotatename,3,0)
        mix_together(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    #print("2个模型之间的距离为",distance)
    errorDistance=distance
    while(distance>0.2):
        errorDistance+=distance
        os.remove(savename)
        movexy(rotatename,-distance,0)
        mix_together(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    #########


    #width
    #height=findMaxYVertex(savename)[1]-findMaxYVertex(savename)[1]

    return height,width




def find_best_width_height(srcdxf,savename,dx,concave):
    
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #rint("开始判断2个模型是否交叉")
    #先将模型旋转180度，
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
    #########点的情况需要额外处理
    if(concave==0):
        ####
        #width=movex*(5.5/10)
        #print("判断是凸面形多边形")
        if(os.path.exists("edge.dxf")):
            os.remove("edge.dxf")
        rotatename="rotatename.dxf"
        rotate_dxf(srcdxf,math.pi,rotatename)

        
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
                print("在上小下大的模型中，该模型的相对宽度比较均匀")
                movexy(rotatename,movex,movey)
            else:
                print("该模型并不均匀")
                movexy(rotatename,movex,movey*0.975)
                
        
    mix_together(srcdxf,rotatename,savename)
    distance=polyCrash(savename)

    if(distance==0):
        print("两个模型的距离的为负时",distance)
        os.remove(savename)
        movexy(rotatename,1.5*width,0)
        mix_together(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    if(0<distance<dx-0.1):

        print("两个模型的距离的为正，但小于dx",distance)
        os.remove(savename)
        movexy(rotatename,dx,0)
        mix_together(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
    if(distance-dx>0.1):
        while(distance-dx>0.1):
            #errorDist=distance
            os.remove(savename)
            movexy(rotatename,dx-distance,0)
            mix_together(srcdxf,rotatename,savename)
            distance=polyCrash(savename)
            print("两个模型的距离的为",distance)
        os.remove(savename)
        movexy(rotatename,dx,0)
        mix_together(srcdxf,rotatename,savename)
        distance=polyCrash(savename)
        print("两个模型的距离的为",distance) 

   
    width_of_2_rotate_model=findMaxXVertex(savename)[0]-findMinXVertex(savename)[0]


    #width_of_2_rotate_model=test_of_2_model_crash(rotatename,"rotate.dxf",dx)
    #copy_num_dxf(srcdxf,width,0,1,"no_rotate.dxf")
    #####这里有个比较致命的错误，就是这个3/4比较要命，这样一搞，很多模型都会要比这个低。所以应该我刚刚写的
    #####那个循环就比较好，你先调整好2个模型的宽度，再来衡量比较好。
    print("模型旋转后的组合宽度为width_of_2_rotate_model",width_of_2_rotate_model)

    '''copy_num_dxf(srcdxf,(width*(3/4)),0,2,"no_rotate.dxf")
    width=(width*(3/4))
    width_of_2_model=findMaxXVertex("no_rotate.dxf")[0]-findMinXVertex("no_rotate.dxf")[0]'''

    width_of_2_model=test_of_2_model_crash(srcdxf,"no_rotate.dxf",dx)
    #copy_num_dxf(srcdxf,(width*(3/4)),0,2,"no_rotate.dxf")
    print("模型旋转后的组合宽度为width_of_2_rotate_model",width_of_2_rotate_model,"不旋转的组合最佳宽度为width_of_2_model",width_of_2_model)
    #width=(width*(3/4))
    #width_of_2_model=findMaxXVertex("no_rotate.dxf")[0]-findMinXVertex("no_rotate.dxf")[0]


    if(width_of_2_rotate_model>width_of_2_model):
        #avename="no_rotate.dxf"
        if(os.path.exists("edge.dxf")):
            os.remove("edge.dxf")
        dxf=ezdxf.readfile("no_rotate.dxf")
        dxf.saveas("edge.dxf")
        print("模型不需要旋转")
    else:
        print("  ")
        #######因为savename=="edge.dxf",所以不需要再重新保存成"edge""
        print("模型需要旋转")
        print("  ")
        #if(os.path.exists("edge.dxf")):
           # os.remove("edge.dxf")
        #dxf=ezdxf.readfile(savename)
       # dxf.saveas("edge.dxf")
    #width
    #height=findMaxYVertex(savename)[1]-findMaxYVertex(savename)[1]
    height=height+dx
    width=width+dx

    return height,width

    

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

   # movexdxf("mode1.dxf",100)
    #minx=find_minx_vertex("mode1.dxf")[0]
    #miny=find_miny_vertex("mode1.dxf")[1]

    #maxx=find_maxx_vertex("mode1.dxf")[0]-minx
    #movexy("mode1.dxf",0-minx,0-miny)
    #copy_dxf("mode1.dxf",maxx,0,"copy_model1.dxf")
    #copy_num_dxf("mode1.dxf",maxx,0,10,"copy_model1.dxf")

    #print("模型提取慢一点没问题，主要是模型的复制和合并才是问题")
    #extractdxf("12-30 ZAOG042221504 #22.dxf")
    dx=100
    h,w=find_best_width_height("mode13.dxf","edge.dxf",dx,0)
    print("测试完毕")



