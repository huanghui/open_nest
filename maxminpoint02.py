import ezdxf
import os
#
import math



'''1.2的版本主要解决因为要引入block的问题，而产生了需要重构的问题'''
#################返回该图像X的最大值的坐标
def findMaxXVertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"

    #############寻找实体中x值最大的和y值最大的
    '''number_of_blocks=0
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    if(number_of_blocks==2):'''
    i=0
    max_x_points=[]
    for e in dxf.entities:
            
            #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
                    #for v in range (0,e.dxf.count):
                       # print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                        #i=i+1
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                       # print(vtex)
                        #print(vtex[0])
                        #maxvalue=max(vtex[0])

                ##########对单列数据进行排列，采用了lambda表达方法
                max_x_point=max(e.vertices(),key=(lambda x:x[0]))
                    
                    #max_y_value=min(e.vertices(),key=(lambda x:x[1]))
                    #ax_y_value=max(e.vertices()[1])
                    
                    
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                        #print(vtex[0],vtex[1])
                print("x的最大值的点坐标为",max_x_point)
                    #print("y的最大值为",max_y_value)
                return max_x_point
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            ralitive_max_x_point=max(e.points(),key=(lambda x:x[0]))
            max_x_points.append(ralitive_max_x_point)
            #print("y相对大的点坐标为min_y_points[",i,"]",ralitive_max_x_point)
    #print(len(min_y_points))
    max_x_point=max(max_x_points,key=(lambda x:x[0]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("X的最大值的点坐标为",max_x_point)

    return max_x_point
    #rotate_zdxf(srcdxf,math.pi,rotatename)
    
    #dxf.saveas(savename)
    #######将模型合并并且写入到指定的文件中
    #mix(srcdxf,rotatename,savename)
    #print("最新合并的图像是怎么样的？")
    #return dxf
def findMaxYVertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"

    #############寻找实体中x值最大的和y值最大的
    '''number_of_blocks=0
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    if(number_of_blocks==2):'''
    i=0
    max_y_points=[]
    for e in dxf.entities:
            
            #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
                    #for v in range (0,e.dxf.count):
                       # print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                        #i=i+1
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                       # print(vtex)
                        #print(vtex[0])
                        #maxvalue=max(vtex[0])

                ##########对单列数据进行排列，采用了lambda表达方法
                max_y_point=max(e.vertices(),key=(lambda x:x[1]))
                    
                    #max_y_value=min(e.vertices(),key=(lambda x:x[1]))
                    #ax_y_value=max(e.vertices()[1])
                    
                    
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                        #print(vtex[0],vtex[1])
                print("y的最大值的点坐标为",max_y_point)
                    #print("y的最大值为",max_y_value)
                return max_y_point
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            ralitive_max_y_point=max(e.points(),key=(lambda x:x[1]))
            max_y_points.append(ralitive_max_y_point)
            #print("y相对大的点坐标为min_y_points[",i,"]",ralitive_max_y_point)
    #print(len(min_y_points))
    max_y_point=max(max_y_points,key=(lambda x:x[1]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("y的最大值的点坐标为",max_y_point)

    return max_y_point

def findMinXVertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"

    #############寻找实体中x值最大的和y值最大的
    '''number_of_blocks=0
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    if(number_of_blocks==2):'''
    i=0
    min_x_points=[]
    for e in dxf.entities:
            
            #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
                    #for v in range (0,e.dxf.count):
                       # print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                        #i=i+1
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                       # print(vtex)
                        #print(vtex[0])
                        #maxvalue=max(vtex[0])

                ##########对单列数据进行排列，采用了lambda表达方法
                min_x_point=min(e.vertices(),key=(lambda x:x[0]))
                    
                    #max_y_value=min(e.vertices(),key=(lambda x:x[1]))
                    #ax_y_value=max(e.vertices()[1])
                    
                    
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                        #print(vtex[0],vtex[1])
                print("x的最小值的点坐标为",min_x_point)
                    #print("y的最大值为",max_y_value)
                return min_x_point
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            ralitive_min_x_point=min(e.points(),key=(lambda x:x[0]))
            min_x_points.append(ralitive_min_x_point)
            #print("x相对小的点坐标为min_y_points[",i,"]",ralitive_min_x_point)
    #print(len(min_y_points))
    min_x_point=min(min_x_points,key=(lambda x:x[0]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("X的最小值的点坐标为",min_x_point)

    return min_x_point
    #rotate_zdxf(srcdxf,math.pi,rotatename)
    
    #dxf.saveas(savename)
    #######将模型合并并且写入到指定的文件中
    #mix(srcdxf,rotatename,savename)
    #print("最新合并的图像是怎么样的？")
    #return dxf

def findMinYVertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"

    #############寻找实体中x值最大的和y值最大的
    '''number_of_blocks=0
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    if(number_of_blocks==2):'''
    i=0
    min_y_points=[]
    for e in dxf.entities:
            
            #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
                    #for v in range (0,e.dxf.count):
                       # print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                        #i=i+1
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                       # print(vtex)
                        #print(vtex[0])
                        #maxvalue=max(vtex[0])
                '''for v in e.vertices():
                    print(v)'''
                ##########对单列数据进行排列，采用了lambda表达方法
                min_y_point=min(e.vertices(),key=(lambda x:x[1]))
                    
                    #max_y_value=min(e.vertices(),key=(lambda x:x[1]))
                    #ax_y_value=max(e.vertices()[1])
                    
                    
                    #for vtex  in e.vertices():
                        #maxnumber=e.find(max(e.vertices))
                        #print(vtex[0],vtex[1])
                #print("y的最大值的点坐标为",min_y_point)
                    #print("y的最大值为",max_y_value)
                return min_y_point
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            ralitive_min_y_point=min(e.points(),key=(lambda x:x[1]))
            min_y_points.append(ralitive_min_y_point)
            #print("y相对大的点坐标为min_y_points[",i,"]",ralitive_min_y_point)
    #print(len(min_y_points))
    min_y_point=min(min_y_points,key=(lambda x:x[1]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("y的最大值的点坐标为",min_y_point)

    return min_y_point

        #############设置边界距离





##################
'''干脆重新写函数进行判断吧，原有的暂时不做太多改动，怕出现一些不必要的麻烦'''


def find_maxx_vertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"
    i=0
    max_x_points=[]
    #############寻找实体中x值最大的和y值最大的
    for e in dxf.entities:
        
        
        #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
               

            ##########对单列数据进行排列，采用了lambda表达方法
            max_x_point=max(e.vertices(),key=(lambda x:x[0]))
               
            #print("y的最小值的点坐标为",max_x_point)
            return max_x_point
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
            
            #print("该模型中含有polyline的线段")
            #for p in e.points():
                
            ##########对单列数据进行排列，采用了lambda表达方法
                #min_y_points[i]=min(p[1])
            ralitive_max_x_point=max(e.points(),key=(lambda x:x[0]))
            max_x_points.append(ralitive_max_x_point)
            #print("y相对大的点坐标为min_y_points[",i,"]",ralitive_max_x_point)
    #print(len(min_y_points))
    max_x_point=max(max_x_points,key=(lambda x:x[0]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("y的最大值的点坐标为",max_x_point)

            
    

    return max_x_point

    
    #return dxf
def find_maxy_vertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"
    i=0
    max_y_points=[]
    #############寻找实体中x值最大的和y值最大的
    for e in dxf.entities:
        
        
        #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
               

            ##########对单列数据进行排列，采用了lambda表达方法
            max_y_point=min(e.vertices(),key=(lambda x:x[1]))
               
            #print("y的最小值的点坐标为",max_y_point)
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
            
            #print("该模型中含有polyline的线段")
            #for p in e.points():
                
            ##########对单列数据进行排列，采用了lambda表达方法
                #min_y_points[i]=min(p[1])
            ralitive_max_y_point=max(e.points(),key=(lambda x:x[1]))
            max_y_points.append(ralitive_max_y_point)
            #print("y相对大的点坐标为min_y_points[",i,"]",ralitive_max_y_point)
    #print(len(min_y_points))
    max_y_point=max(max_y_points,key=(lambda x:x[1]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("y的最大值的点坐标为",max_y_point)

            
    

    return max_y_point

def find_minx_vertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    
    i=0
    min_x_points=[]
    #############寻找实体中x值最大的和y值最大的
    for e in dxf.entities:
        
        
        #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
               

            ##########对单列数据进行排列，采用了lambda表达方法
            min_y_point=min(e.vertices(),key=(lambda x:x[1]))
               
            #print("y的最小值的点坐标为",min_y_point)
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
            
            #print("该模型中含有polyline的线段")
            #for p in e.points():
                
            ##########对单列数据进行排列，采用了lambda表达方法
                #min_y_points[i]=min(p[1])
            ralitive_min_x_point=min(e.points(),key=(lambda x:x[0]))
            min_x_points.append(ralitive_min_x_point)
            #print("x相对小的点坐标为min_y_points[",i,"]",ralitive_min_x_point)
    #print(len(min_y_points))
    min_x_point=min(min_x_points,key=(lambda x:x[0]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("x的最小值的点坐标为",min_x_point)

            
    

    return min_x_point



def find_miny_vertex(srcdxf):
    #######读入基本的模型
    dxf=ezdxf.readfile(srcdxf)
    #print("开始判断2个模型是否交叉")
    #先将模型旋转180度，
    #rotatename="rotatename.dxf"
    i=0
    min_y_points=[]
    #############寻找实体中x值最大的和y值最大的
    for e in dxf.entities:
        
        
        #print(e.DXFTYPE,e.dxf.flags)
        if(e.DXFTYPE=="LWPOLYLINE"):
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
               
            
            ##########对单列数据进行排列，采用了lambda表达方法
            min_y_point=min(e.vertices(),key=(lambda x:x[1]))
               
            print("y的最小值的点坐标为",min_y_point)
        if(e.DXFTYPE=="POLYLINE"):
            i=i+1
            #if(e.__len__()>75):########如果大于75则可以主张为轮廓比较大，归属到单个模型
            
            #print("该模型中含有polyline的线段")
            #for p in e.points():
                
            ##########对单列数据进行排列，采用了lambda表达方法
                #min_y_points[i]=min(p[1])
            ralitive_min_y_point=min(e.points(),key=(lambda x:x[1]))
            min_y_points.append(ralitive_min_y_point)
            #print("y相对小的点坐标为min_y_points[",i,"]",ralitive_min_y_point)
    #print(len(min_y_points))
    min_y_point=min(min_y_points,key=(lambda x:x[1]))
            #min_y_point=min(min_y_points)
        #min_y_point=min(min_y_points,key=(lambda x:x[1]))
    print("y的最小值的点坐标为",min_y_point)

    return min_y_point

        #############设置边界距离
###############
###############
###############判断dxf的形状的算法，具体只能通过点来计算斜率。


if __name__=="__main__":
    #find_miny_vertex("Piece18-S6.dxf")
    
    #find_minx_vertex("Piece18-S6.dxf")
   # find_maxy_vertex("Piece18-S6.dxf")
    #find_maxx_vertex("Piece18-S6.dxf")
    #findMaxXVertex("Piece18-S6.dxf")
    #findMaxXVertex("Drawing11.dxf")
    #findMaxYVertex("Piece18-S6.dxf")
   # findMaxYVertex("Drawing11.dxf")
    #@findMinXVertex("Piece18-S6.dxf")
    #findMinXVertex("Drawing11.dxf")
    findMinYVertex("Piece18-S6.dxf")
    findMinYVertex("Drawing11.dxf")
    #Drawing11
