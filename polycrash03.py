

############
############
#############实现了多边形的碰撞检验，如果是出现2个多边形重叠，那么返回TRUE
###########
#######如果2个多边形不重叠，返回时Fasle
import numpy as np

import time
import ezdxf
from shapely.geometry import Polygon ###多边形

from shapely.geometry import Polygon,MultiPoint

import matplotlib.pyplot as plt
import scipy.io as io

import os

from ezdxf.addons import Importer

from maxminpoint02 import*
#from readdxf import movexy
###########
#########这里只能处理2个多边形是否相交
def polyCrash(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    j=0
    points=[0,0]
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            try:
                if(length>75 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                    i=i+1
                elif(length>75 and i==1):
                    print("进入到polyCrash的第二个循环")
                    poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
            except:
                
                if(length>34 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                    i=i+1
                elif(length>34 and i==1):
                    print("进入到polyCrash的第二个循环")
                    poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
            '''如果是比较复杂的非封闭多边线'''

        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())

            #print("ployline的长度为",length,"当大于75时,系统认为这是一个模型")
            #try:
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                print("进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])

        ########这个是保守的做法，其实这个做法是不对的，因为34的模型很容易出先错误的。
                #####一旦模型大一点，里面的东西就会出来。不过也不一定，因为里面的
                #######模型也是没什么问题了。

    
            #except:
            if(length>34 and i==0 and j==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
                j=j+1
            elif(length>34 and i==1 and j==1):
                print("length小于75时，进入到polyCrash的第二个循环")
                j=j+1
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
           #for p  in polyline.points():
                #point=(p[0],p[1])
               # points.append(point) 
        
        #for p in points:
           # if point_in_poly.is_in_poly2(p,points):
          #  poly=Polygon(points)
        

    crash=poly1.intersects(poly2)
    distance=poly1.exterior.distance(poly2)
    print("polyCrash,2个多边形的距离为",distance)
    return distance
    #return poly1,poly2



def polyCrash_return_2_model(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    j=0
    points=[0,0]
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            try:
                if(length>75 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                    i=i+1
                elif(length>75 and i==1):
                    print("进入到polyCrash的第二个循环")
                    poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
            except:
                
                if(length>34 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                    i=i+1
                elif(length>34 and i==1):
                    print("进入到polyCrash的第二个循环")
                    poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
            '''如果是比较复杂的非封闭多边线'''

        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())

            #print("ployline的长度为",length,"当大于75时,系统认为这是一个模型")
            #try:
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                print("进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])

        ########这个是保守的做法，其实这个做法是不对的，因为34的模型很容易出先错误的。
                #####一旦模型大一点，里面的东西就会出来。不过也不一定，因为里面的
                #######模型也是没什么问题了。

    
            #except:
            if(length>34 and i==0 and j==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
                j=j+1
            elif(length>34 and i==1 and j==1):
                print("进入到polyCrash的第二个循环")
                j=j+1
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
           #for p  in polyline.points():
                #point=(p[0],p[1])
               # points.append(point) 
        
        #for p in points:
           # if point_in_poly.is_in_poly2(p,points):
          #  poly=Polygon(points)
        

    crash=poly1.intersects(poly2)
    distance=poly1.exterior.distance(poly2)
    print("polyCrash,2个多边形的距离为",distance)
    #return distance
    return poly1,poly2




############
###########如果模型大于2个，那么判断的是第一个模型最右边的模型和第二个模型
##########最左边的模型
def polyCrash2(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    j=0
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                #print("进入到polyCrash2第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                print(i)
            elif(length>75 and i==2):
                i=i+1
                #print("进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            elif(length>75 and i==3):
                i=i+1
               # print("进入到polyCrash2第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.vertices()])

        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
             #print(e.__len__())
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                #print("进入到polyCrash的第一个循环,获取第一个模型")
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                i=i+1
                #print("进入到polyCrash的第二个循环,获取第二个模型")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==2):
                i=i+1
               # print("进入到polyCrash2第三个模型,获取第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==3):
                i=i+1
               # print("进入到polyCrash2第四个模型,获取第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])

            
            if(length>34 and j==0 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                #i=i+1
                j=j+1
            elif(length>34 and j==1 and i==0):
                #i=i+1
                j=j+1
                #print(",length>34,进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>34 and j==2 and i==0):
                #i=i+1
                j=j+1
                #print(",length>34,进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>34 and j==3 and i==0):
                #i=i+1
                #print(",length>34,进入到polyCrash2第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])

    crasharea=poly2.intersects(poly3)
    distance1=poly2.exterior.distance(poly3)

    distance2=poly1.exterior.distance(poly3)

    distance3=poly2.exterior.distance(poly4)

    distance4=poly1.exterior.distance(poly4)

    distance=min(distance1,distance2,distance3,distance4)
    #distance2=poly1.exterior.distance(poly4)
    #distance3=poly2.exterior.distance(poly3)
    #distance4=poly2.exterior.distance(poly4)
    #distance=max(distance1,distance2,distance3,distance4)

    #distance=max(distance1,distance2)    print("2个多边形的距离为",distance)
    print("2个多边形相交的面积为",crasharea)
    #return distance,crasharea
    return distance

    #return poly1,poly2,poly3,poly4
###################
############计算重叠的面积


def polyCrash2_ploy(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    j=0
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
            print("e.DXFTYPE的类型为LWPLOYLINE")
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                print("进入到polyCrash2第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                print(i)
            elif(length>75 and i==2):
                i=i+1
                print("进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            elif(length>75 and i==3):
                i=i+1
                
                print("进入到polyCrash2第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.vertices()])

        if(e.DXFTYPE== 'POLYLINE' ):
              length=e.__len__()
             #print(e.__len__()
              #print("e.DXFTYPE的类型为PLOYLINE")
              #i=0
                ################如果定点数大于75时，我们认为这是一个模型的外轮廓
              if(length>75 and i==0):
                #print("进入到polyCrash的第一个个循环,获取第一个模型")
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                print("length>75,poly1生成")
                i=i+1
              elif(length>75 and i==1):
                print("length>75,poly2生成")
                i=i+1
                #print("进入到polyCrash的第二个循环,获取第二个模型")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>75 and i==2):
                print("length>75,poly3生成")
                i=i+1
                #print("进入到polyCrash2第三个模型,获取第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>75 and i==3):
                print("length>75,poly4生成")
                i=i+1
                #print("length>75,进入到polyCrash2第四个模型，获取第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])


                ########模型提取出现问题，重新设计i
              
              #j=0
              if(length>34 and j==0 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                #i=i+1
                j=j+1
                print("length>34,poly1生成")
              elif(length>34 and j==1 and i==0):
                #i=i+1
                j=j+1
                print("length>34,poly2生成")
                print(",length>34,进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>34 and j==2 and i==0):
                #i=i+1
                j=j+1
                print("length>34,poly3生成")
                print(",length>34,进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>34 and j==3 and i==0):
                #i=i+1
                print(",length>34,进入到poly4")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])


    crasharea=poly2.intersects(poly3)
    distance=poly2.exterior.distance(poly3)
    #distance2=poly1.exterior.distance(poly3)
    #distance3=poly1.exterior.distance(poly4)
    #distance4=poly2.exterior.distance(poly4)
    print("2个多边形的距离为",distance)
    print("2个多边形相交的面积为",crasharea)
    #return distance

    return poly1,poly2,poly3,poly4




def polyCrash3(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    j=0
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                #print("进入到第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                print(i)
            elif(length>75 and i==2):
                i=i+1
                #print("进入到polyCrash3的第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            elif(length>75 and i==3):
                
                #print("进入到polyCrash3的第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.vertices()])


        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                i=i+1
               # print("进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==2):
                i=i+1
               # print("进入到polyCrash3第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==3):
                
                #print("进入到polyCrash3第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])   




            if(length>34 and j==0 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                #i=i+1
                j=j+1
            elif(length>34 and j==1 and i==0):
                #i=i+1
                j=j+1
                #print(",length>34,进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>34 and j==2 and i==0):
                #i=i+1
                j=j+1
                #print(",length>34,进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>34 and j==3 and i==0):
                #i=i+1
               # print(",length>34,进入到polyCrash2第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.points()])


    
    crasharea23=poly2.intersects(poly3)
    crasharea13=poly1.intersects(poly3)
    crasharea14=poly1.intersects(poly4)
    crasharea24=poly2.intersects(poly4)
    
    distance1=poly2.exterior.distance(poly3)
    distance2=poly1.exterior.distance(poly3)
    distance3=poly1.exterior.distance(poly4)
    distance4=poly2.exterior.distance(poly4)
    distance=min(distance1,distance2,distance3,distance4)
    crasharea=max(crasharea23,crasharea13,crasharea14,crasharea24)
    print("2个多边形的距离为",distance)
    print("2个多边形相交的面积为",crasharea)
    #return distance
    return poly1,poly2,poly3,poly4

def polyCrash_3(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                print("polyCrash_3第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                #print(i)
            elif(length>75 and i==2):
                i=i+1
                print("polyCrash_3的第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            '''elif(length>75 and i==3):
                
                print("进入到polyCrash3的第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.vertices()])'''

        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                i=i+1
                print("进入到polyCrash_3的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==2):
                print("进入到polyCrash_3第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
           

    


    
    crasharea23=poly2.intersects(poly3)
    crasharea13=poly1.intersects(poly3)
    crasharea12=poly1.intersects(poly2)
    '''crasharea14=poly1.intersects(poly4)
    crasharea24=poly2.intersects(poly4)'''
    
    distance1=poly2.exterior.distance(poly3)
    distance2=poly1.exterior.distance(poly3)
    distance3=poly1.exterior.distance(poly2)
    '''distance3=poly1.exterior.distance(poly4)
    distance4=poly2.exterior.distance(poly4)'''
    distance=min(distance1,distance2,distance3)
    crasharea=max(crasharea23,crasharea13,crasharea12)
    print("2个多边形的距离为",distance)
    print("2个多边形相交的面积为",crasharea)
    return distance
    #return poly1,poly2,poly3

def polyCrash_4(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                print("polyCrash_4第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                #print(i)
            elif(length>75 and i==2):
                i=i+1
                print("polyCrash_4的第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            '''elif(length>75 and i==3):
                
                print("进入到polyCrash3的第四个模型")
                poly4 = Polygon([[p[0], p[1]] for p in e.vertices()])'''
        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                i=i+1
            elif(length>75 and i==1):
                i=i+1
                print("进入到polyCrash_4的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==2):
                print("进入到polyCrash_4第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])

    


    
    crasharea23=poly2.intersects(poly3)
    crasharea13=poly1.intersects(poly3)
    crasharea12=poly1.intersects(poly2)
    '''crasharea14=poly1.intersects(poly4)
    crasharea24=poly2.intersects(poly4)'''
    
    distance1=poly2.exterior.distance(poly3)
    distance2=poly1.exterior.distance(poly3)
    distance3=poly1.exterior.distance(poly2)
    '''distance3=poly1.exterior.distance(poly4)
    distance4=poly2.exterior.distance(poly4)'''
    distance_max=max(distance1,distance2,distance3)
    distance_min=min(distance1,distance2,distance3)
    crasharea=max(crasharea23,crasharea13,crasharea12)
    print("2个多边形的最小距离为",distance_min)
    print("2个多边形的最大距离为",distance_max)
    print("2个多边形相交的面积为",crasharea)
    return distance_max
    #return poly1,poly2,poly3



def Cal_area_2poly(data1,data2):
    #poly1=Polygon(data1).convex_hull
    poly1=Polygon(data1)
    #poly2=Polygon(data2).convex_hull
    poly2=Polygon(data2)

    if not poly1.intersects(poly2):
        inter_area=0
    else:
        inter_area=poly1.intersection(poly2).area

    return inter_area


def movexy(srcdxf,x,y):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,y,0)
     dxf.saveas(srcdxf)


def movexdxf(srcdxf,x):
     dxf=ezdxf.readfile(srcdxf)
     for e in dxf.entities:
         e.translate(x,0,0)
     return dxf


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

def mix(sdxf,tdxf,savename):
    base_dxf = ezdxf.readfile(tdxf)

#for filename in (inputdxf4,inputdxf3,inputdxf10):
    merge_dxf = ezdxf.readfile(sdxf)
    dxfimport(merge_dxf, base_dxf)

# base_dxf.save()  # to save as file1.dxf
    #base_dxf.saveas('nest.dxf#base_dxf.saveas("testrotate.dxf")
    base_dxf.saveas(savename)
    
    print("合并dxf文件成功") 

def test_of_2_model(srcdxf,width):
    
    distance=polyCrash("edge.dxf")
    if(os.path.exists("Dpolycrash.dxf")):

        os.remove("Dpolycrash.dxf")
    #########这里做while循环有点傻吧？
    movexdxf(srcdxf,width).saveas("Dpolycrash.dxf")
    #####好像也不太傻，因为这里涉及到细节操作，因为上面做的模型并不能代表这个模型就
    #####一定完全满足需求，需要微调。
    while(distance==0):
       
        movexy("Dpolycrash.dxf",distance,0)
     
        mix(srcdxf,"Dpolycrash.dxf","Dpolycrash.dxf")
        distance=polyCrash("Dpolycrash.dxf")
    data1,data2=polyCrash_return_2_model("Dpolycrash.dxf")

    return data1,data2



def test_of_crash(srcdxf,width):
    if(os.path.exists("D2.dxf")):

        os.remove("D2.dxf")
############这里只是做初步的碰撞组合
    movexdxf(srcdxf,2*width).saveas("D2.dxf")
    #movexdxf(srcdxf,width).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    
    ###########微调，如果distance为真
    #distance=polyCrash2("D0.dxf")

    distance,crasharea=polyCrash2("D0.dxf")
    print("两个模型的距离",distance)

    #errorDistance=distance
    #############
    #############需要进行反复修正2组模型之间的距离,注意是2组
    while(distance>1):
        #errorDistance+=distance
        os.remove("D0.dxf")
        movexy("D2.dxf",-distance,0)
        mix(srcdxf,"D2.dxf","D0.dxf")
        distance,crasharea=polyCrash2("D0.dxf")

    
def test_poly2_crash(srcdxf):
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    width=maxx[0]-minx[0]

    print("在nestwidth3中第1533行中，width的值为",width)
############横向排版
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
    while(distance>0.5):
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

    print("nestwidth3 第1563行中,求的的width值为,",width)


def test_of_2_model_crash(srcdxf,export_name,dx):
    minx=findMinXVertex(srcdxf)
    maxx=findMaxXVertex(srcdxf)
    width=maxx[0]-minx[0]

    #print("在nestwidth3中第1533行中，width的值为",width)
############横向排版
    if(os.path.exists("D2.dxf")):

        os.remove("D2.dxf")
############这里只是做初步的碰撞组合
    movexdxf(srcdxf,2*width).saveas("D2.dxf")
    #movexdxf(srcdxf,width).saveas("D2.dxf")
#saveas("D2.dxf")
    mix(srcdxf,"D2.dxf","D0.dxf")
    
    ###########微调，如果distance为真
    distance=polyCrash("D0.dxf")
    errorDistance=distance
    #############
    #############需要进行反复修正2组模型之间的距离,注意是2组
    while(distance-dx>0.001):
        errorDistance+=distance
        os.remove("D0.dxf")
        movexy("D2.dxf",dx-distance,0)
        mix(srcdxf,"D2.dxf","D0.dxf")
        distance=polyCrash("D0.dxf")
        #if((distance-2)<0.001):
            #break
        

    #MaxX=findMinXVertex("D2.dxf")
    #MinX=findMinXVertex(srcdxf)
    mix(srcdxf,"D2.dxf",export_name)
    width_of_2model=findMaxXVertex("D0.dxf")[0]-findMinXVertex("D0.dxf")[0]
    #mix(srcdxf,"D2.dxf",export_name)

    if(os.path.exists("D2.dxf")):
        os.remove("D2.dxf")
    if(os.path.exists("D0dxf")):
        os.remove("D0.dxf")
###########我觉得放这里判断是不是很不好？但是动了这个，怕有其他问题。
    #######这个是才是实际的宽度
    #width_of_2model=MaxX[0]-MinX[0]
    #width_of_2model

    print("在不旋转的情况下，经过碰撞最适合的宽度为,",width_of_2model)

    
    return width_of_2model


if __name__=="__main__":
    #data1,data2,data3=polyCrash_3("Dmix3.dxf")
    #data1,data2,data3=polyCrash_4("Piece11-S4.dxf")
    #data1,data2,=polyCrash("Piece11-S4.dxf")

    #width=find_maxx_vertex("3.dxf")[0]-find_minx_vertex("3.dxf")[0]
    
   # test_of_crash("edge.dxf",width)

    #data1,data2,=polyCrash_return_2_model("edge.dxf")
    if(os.path.exists("edge.dxf")):
        os.remove("edge.dxf")
    #test_of_2_model_crash("3.dxf","edge.dxf")
    #data1,data2,=polyCrash_return_2_model("edge.dxf")

    data1,data2,data3,data4=polyCrash2_ploy("D0.dxf")


    
    #data1,data2=test_of_2_model("3.dxf",width)

    #data1,data2=polyCrash_return_2_model("D.dxf")
    #poly1=[0]*2
    #poly=[0]*2
    #for i in range(0,):
       # print("获取的坐标值",data[0],data[1])
    #    poly1[
   # print("这是第二个个多边形")
    #for data in data2:
       # print("获取的坐标值",data[0],data[1])
    #area=Cal_area_2poly(data1,data2)
    #print("两多边形相交的面积等于",area)
    #poly1=Polygon([(0,0),(1,1),(2,0),(2,2),(0,2)])
   # poly2=Polygon([(0,0),(2,2),(3,0),(3,3),(0,3)])
    
    #print(area)
    
    #print(poly.bounds)
    #print(poly1.intersects(poly2))
    #@print(polyIsCrash("edge24.dxf"))
    #print(polyIsCrash("edge25.dxf"))
    ax=plt.gca()
    #ax.xaxis.set_ticks_position('top')
    #ax.invert_yaxis()
    plt.plot(*data1.exterior.xy)
    plt.plot(*data2.exterior.xy)
    plt.plot(*data3.exterior.xy)
    plt.plot(*data4.exterior.xy)
    plt.show()


