

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
#from readdxf import movexy
###########
#########这里只能处理2个多边形是否相交
def polyCrash(srcdxf):
    dxf=ezdxf.readfile(srcdxf)
    i=0
    points=[0,0]
    for e in dxf.entities:
        if(e.DXFTYPE== 'LWPOLYLINE' ):
            length=e.dxf.count
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
            if(length>75 and i==0):
                poly1 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
            elif(length>75 and i==1):
                print("进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])

            '''如果是比较复杂的非封闭多边线'''

        if(e.DXFTYPE== 'POLYLINE' ):
            length=e.__len__()
            #print(e.__len__())

            print("ployline的长度为",length,"当大于75时,系统认为这是一个模型")
            try:
    
            ################如果定点数大于75时，我们认为这是一个模型的外轮廓
                if(length>75 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                    i=i+1
                elif(length>75 and i==1):
                    print("进入到polyCrash的第二个循环")
                    poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            except:
                if(length>34 and i==0):
                    poly1 = Polygon([[p[0], p[1]] for p in e.points()])
                    i=i+1
                elif(length>34 and i==1):
                    print("进入到polyCrash的第二个循环")
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


############
###########如果模型大于2个，那么判断的是第一个模型最右边的模型和第二个模型
##########最左边的模型
def polyCrash2(srcdxf):
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
                print("进入到polyCrash2第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                print(i)
            elif(length>75 and i==2):
                i=i+1
                print("进入到polyCrash2第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            elif(length>75 and i==3):
                
                print("进入到polyCrash2第四个模型")
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
                  print("进入到polyCrash的第二个循环")
                  poly2 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>75 and i==2):
                  i=i+1
                  print("进入到polyCrash2第三个模型")
                  poly3 = Polygon([[p[0], p[1]] for p in e.points()])
              elif(length>75 and i==3):
                  print("进入到polyCrash2第四个模型")
                  poly4 = Polygon([[p[0], p[1]] for p in e.points()])

    crasharea=poly2.intersects(poly3)
    distance=poly2.exterior.distance(poly3)
    #distance2=poly1.exterior.distance(poly3)
    #distance3=poly1.exterior.distance(poly4)
    #distance4=poly2.exterior.distance(poly4)
    print("2个多边形的距离为",distance)
    print("2个多边形相交的面积为",crasharea)
    return distance

    #return poly1,poly2,poly3,poly4
###################
############计算重叠的面积




def polyCrash3(srcdxf):
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
                print("进入到第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.vertices()])
                i=i+1
                print(i)
            elif(length>75 and i==2):
                i=i+1
                print("进入到polyCrash3的第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.vertices()])
            elif(length>75 and i==3):
                
                print("进入到polyCrash3的第四个模型")
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
                print("进入到polyCrash的第二个循环")
                poly2 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==2):
                i=i+1
                print("进入到polyCrash3第三个模型")
                poly3 = Polygon([[p[0], p[1]] for p in e.points()])
            elif(length>75 and i==3):
                
                print("进入到polyCrash3第四个模型")
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
    return distance
    #return poly1,poly2,poly3,poly4

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



if __name__=="__main__":
    #data1,data2,data3=polyCrash_3("Dmix3.dxf")
    #data1,data2,data3=polyCrash_4("Piece11-S4.dxf")
    #data1,data2,=polyCrash("Piece11-S4.dxf")

    data1,data2,=polyCrash("edge.dxf")
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
    ax.xaxis.set_ticks_position('top')
    ax.invert_yaxis()
    plt.plot(*data1.exterior.xy)
    plt.plot(*data2.exterior.xy)
    #plt.plot(*data3.exterior.xy)
    #plt.plot(*data4.exterior.xy)
    plt.show()


