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

from fileinput import close
import ezdxf
import os
#
import math
from ezdxf.addons import Importer
import shutil

from ezdxf.addons import iterdxf
#from ezdxf import Importer
#from polycrash import polyCrash,polyCrash2,polyCrash3,polyCrash_3,polyCrash_4



 
def  make_dir(dir_name):
    folder=os.getcwd()[:-4]+dir_name
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("创建文件夹成功",folder)
        return folder
    else:
        print(folder,"文件夹存在")
        shutil.rmtree(folder)
        print(folder,"文件夹被移除")
        os.makedirs(folder)
        print("创建文件夹成功",folder)
        return folder
        #print("文件夹已经存在")
       # return 
   


def extractdxf_old(srcdxf):
    dxf=ezdxf.readfile(srcdxf)


    doc = iterdxf.opendxf(srcdxf)
    indexdxf=0
    j=0
    number_of_blocks=0
    #print(dxf.owner)
    model_path=make_dir("model_dir_test")
    msp=dxf.modelspace()
   # for e in dxf.modelspace():
      #  print(e,e.get_dxf_attrib('handle'))

    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    print("blocks的数量为",number_of_blocks)
    if(number_of_blocks==2 or number_of_blocks<10):

        #model_path=make_dir("model_dir")
        for e in dxf.entities:
           # indexdxf=0
            #print(e.DXFTYPE)
            
            if(e.DXFTYPE=="SPLINE"):
                print("模型的类型是spline")
            
               

                ##########为了将spline的点整理到列表里面，重新画成polyline。
                print(e.dxf.n_control_points)

                if(e.dxf.n_control_points>30):
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp.add_polyline2d(spline)
                #sprint(e.dxf.n_control_points)
                    print("多边线的定点数为",e)
                else:

                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp=newdoc.modelspace()
                                                    
                    msp.add_polyline2d(spline)
                                
               
            if(e.DXFTYPE=="LWPOLYLINE"):
                print("线段类型为LWPOLYLINE")
                for v in range (0,e.dxf.count):
                    print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                    i=i+1
                        
            if(e.DXFTYPE=='POLYLINE'):
                length=e.__len__()
                #print("线段类型为POLYLINE,polyline线段长度为",length)
                #if(e.is_closed==True):
                #print(e.doc)
                #print(e.dxf.handle)
            
                #print("多边线的定点数为",length)
                
                if(length>75):

                    print("线段类型为POLYLINE,polyline线段长度为",length)
                    #if(e):
                    #print("是否handle==202")
                    #print()
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                                            
                    msp.add_polyline2d(e.points())

                    large_start_x=e.__getitem__(0).dxf.location[0]
                    large_start_y=e.__getitem__(0).dxf.location[1]

                    large_end_x=e.__getitem__(length-1).dxf.location[0]
                    large_end_y=e.__getitem__(length-1).dxf.location[1]

                    large_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    large_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

                    large_rand_x=e.__getitem__(int(((length-1)*2)/3)).dxf.location[0]

                    large_rand_2_x=e.__getitem__(int(((length-1)*4)/5)).dxf.location[0]

                    large_rand_1_x=e.__getitem__(int(((length-1))/5)).dxf.location[0]
                    #print(name
                elif(length>19):
                    print("线段类型为POLYLINE,polyline线段长度为",length,"CHANGDU")
                    small_start_x=e.__getitem__(length-1).dxf.location[0]
                    small_start_y=e.__getitem__(length-1).dxf.location[1]

                    small_end_x=e.__getitem__(length-1).dxf.location[0]
                    small_end_y=e.__getitem__(length-1).dxf.location[1]

                    small_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    small_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

        
                    #if(((small_start_x>large_start_x and small_start_y>large_start_y)and (small_middle_x>large_middle_x and small_middle_y>large_middle_y) )or( (small_start_x<large_start_x and small_start_y<large_start_y)and (small_middle_x<large_middle_x and small_middle_y<large_middle_y))):
                    #####搞反了，应该是小的比较大的。
                    ####整个逻辑都错了。
                    #error=1
                    if((small_start_x<large_start_x) and (small_start_x<large_middle_x) and small_start_x<large_rand_x and small_start_x<large_rand_2_x and  small_start_x<large_rand_1_x):
                        print(e.__getitem__(0).dxf.location[0])
                        indexdxf=indexdxf+1
                                #name=e.get_dxf_attrib('handle')+".dxf"
                        name="mode"+str(indexdxf)+".dxf"
                                    #polyline_exporter = doc.export(name)
                        newdoc= ezdxf.new("R2010")
                                    #name="mode"+str(indexdxf)+".dxf"
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())

                    else:
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())
                                
                        

                            
                else:
                    msp=newdoc.modelspace()
                                        
                    msp.add_polyline2d(e.points())
              
                            #print("这是一个新的dxf模型文件的图形文件")       
                
            newdoc.saveas(os.path.join(model_path,name))
                #print("模型",name,"建立好了")'''
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
                    #newdoc.saveas(name)
                    newdoc.saveas(os.path.join(model_path,name))
    return model_path
            



def extractdxf_old_2(srcdxf):
    dxf=ezdxf.readfile(srcdxf)


    doc = iterdxf.opendxf(srcdxf)
    indexdxf=0
    j=0
    number_of_blocks=0
    #print(dxf.owner)
    model_path=make_dir("model_dir_test")
    msp=dxf.modelspace()
   # for e in dxf.modelspace():
      #  print(e,e.get_dxf_attrib('handle'))
    
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    print("blocks的数量为",number_of_blocks)
    max_len_of_entity=0
    if(number_of_blocks==2 or number_of_blocks<10 ):
        #if(e.DXFTYPE=='POLYLINE'):

        #list_of_line=[]
        
        #d#xf.entities.sort(dxf.entities.__len__())
        print("开始寻找最大的模型长度")
        
        #max_len_of_entity=0
        for e in dxf.entities:
            print("进入到for循环里面，到底是哪里出了问题？")
            print("这句话出了错误？线段类型为",e.DXFTYPE)
            #sprint(e.__len__())
            if(e.DXFTYPE=='POLYLINE'):
                #length=e.__len__() 
                #print())
            
                if(max_len_of_entity<e.__len__()):
                    max_len_of_entity=e.__len__()
            else:
                print("e.DXTTYPE的类型为",e.DXFTYPE)
            #list_of_line.append(e)'''
            #e.sort(len(e.__len__()))
        #list_of_line.sort(e.__len__())


        #max_len=max(len(dxf.entities))

        print("max_len_of_entity实体最大的长度为",max_len_of_entity)

    if(max_len_of_entity>600 ):
        for e in dxf.entities:
        #print("max_len_of_entity实体最大的长度为",max_len_of_entity)
            if(e.DXFTYPE=='POLYLINE' and e.__len__()>600):
            #for e in dxf.entities:
                print("由于多边形的点数太大，直接提取模型",e.__len__())
                indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                msp=newdoc.modelspace()
                                            
                msp.add_polyline2d(e.points())
            #msp=newdoc.modelspace()
            #msp.add_polyline2d(e.points())
                
                                #print("这是一个新的dxf模型文件的图形文件")       
                    
                newdoc.saveas(os.path.join(model_path,name))
    elif(number_of_blocks==2 or number_of_blocks<10):

        #model_path=make_dir("model_dir")
        print("block太少,在这提取模型")
        for e in dxf.entities:
           # indexdxf=0
            #print(e.DXFTYPE)
            
            
            if(e.DXFTYPE=="SPLINE"):
                print("模型的类型是spline")
            
               

                ##########为了将spline的点整理到列表里面，重新画成polyline。
                print(e.dxf.n_control_points)

                if(e.dxf.n_control_points>30):
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp.add_polyline2d(spline)
                #sprint(e.dxf.n_control_points)
                    print("多边线的定点数为",e)
                else:

                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp=newdoc.modelspace()
                                                    
                    msp.add_polyline2d(spline)
                                
               
            if(e.DXFTYPE=="LWPOLYLINE"):
                print("线段类型为LWPOLYLINE")
                for v in range (0,e.dxf.count):
                    print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                    i=i+1
                        
            if(e.DXFTYPE=='POLYLINE'):
                length=e.__len__()
                #print("线段类型为POLYLINE,polyline线段长度为",length)
                #if(e.is_closed==True):
                #print(e.doc)
                #print(e.dxf.handle)


                #for e in dxf.entities:


                #print("多边线的定点数为",length)\
                #if()
                
                if(length>75):

                    print("线段类型为POLYLINE,polyline线段长度为",length)
                    #if(e):
                    #print("是否handle==202")
                    #print()
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                                            
                    msp.add_polyline2d(e.points())

                    large_start_x=e.__getitem__(0).dxf.location[0]
                    large_start_y=e.__getitem__(0).dxf.location[1]

                    large_end_x=e.__getitem__(length-1).dxf.location[0]
                    large_end_y=e.__getitem__(length-1).dxf.location[1]

                    large_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    large_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

                    large_rand_x=e.__getitem__(int(((length-1)*2)/3)).dxf.location[0]

                    large_rand_2_x=e.__getitem__(int(((length-1)*4)/5)).dxf.location[0]

                    large_rand_1_x=e.__getitem__(int(((length-1))/5)).dxf.location[0]
                    #print(name
                elif(length>19):
                    print("线段类型为POLYLINE,polyline线段长度为",length,"CHANGDU")
                    small_start_x=e.__getitem__(length-1).dxf.location[0]
                    small_start_y=e.__getitem__(length-1).dxf.location[1]

                    small_end_x=e.__getitem__(length-1).dxf.location[0]
                    small_end_y=e.__getitem__(length-1).dxf.location[1]

                    small_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    small_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

        
                    #if(((small_start_x>large_start_x and small_start_y>large_start_y)and (small_middle_x>large_middle_x and small_middle_y>large_middle_y) )or( (small_start_x<large_start_x and small_start_y<large_start_y)and (small_middle_x<large_middle_x and small_middle_y<large_middle_y))):
                    #####搞反了，应该是小的比较大的。
                    ####整个逻辑都错了。
                    #error=1
                    if((small_start_x<large_start_x) and (small_start_x<large_middle_x) and small_start_x<large_rand_x and small_start_x<large_rand_2_x and  small_start_x<large_rand_1_x):
                        print(e.__getitem__(0).dxf.location[0])
                        indexdxf=indexdxf+1
                                #name=e.get_dxf_attrib('handle')+".dxf"
                        name="mode"+str(indexdxf)+".dxf"
                                    #polyline_exporter = doc.export(name)
                        newdoc= ezdxf.new("R2010")
                                    #name="mode"+str(indexdxf)+".dxf"
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())

                    else:
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())
                                
                        

                            
                else:
                    msp=newdoc.modelspace()
                                        
                    msp.add_polyline2d(e.points())
              
                            #print("这是一个新的dxf模型文件的图形文件")       
                
            newdoc.saveas(os.path.join(model_path,name))
                #print("模型",name,"建立好了")'''
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
                    #newdoc.saveas(name)
                    newdoc.saveas(os.path.join(model_path,name))
    return model_path
            
###################


def extractdxf(srcdxf):
    dxf=ezdxf.readfile(srcdxf)


    doc = iterdxf.opendxf(srcdxf)
    indexdxf=0
    j=0
    number_of_blocks=0
    #print(dxf.owner)
    model_path=make_dir("model_dir_test")
    msp=dxf.modelspace()
   # for e in dxf.modelspace():
      #  print(e,e.get_dxf_attrib('handle'))
    
    for b in dxf.blocks:
        number_of_blocks=number_of_blocks+1
    print("blocks的数量为",number_of_blocks)
    max_len_of_entity=0
    if(number_of_blocks==2 or number_of_blocks<10 ):
        #if(e.DXFTYPE=='POLYLINE'):

        #list_of_line=[]
        
        #d#xf.entities.sort(dxf.entities.__len__())
        print("开始寻找最大的模型长度")
        
        #max_len_of_entity=0
        for e in dxf.entities:
            print("进入到for循环里面，到底是哪里出了问题？")
            print("这句话出了错误？线段类型为",e.DXFTYPE)
            #sprint(e.__len__())
            if(e.DXFTYPE=='POLYLINE'):
                #length=e.__len__() 
                #print())
            
                if(max_len_of_entity<e.__len__()):
                    max_len_of_entity=e.__len__()
            else:
                print("e.DXTTYPE的类型为",e.DXFTYPE)
            #list_of_line.append(e)'''
            #e.sort(len(e.__len__()))
        #list_of_line.sort(e.__len__())


        #max_len=max(len(dxf.entities))

        print("max_len_of_entity实体最大的长度为",max_len_of_entity)

    if(max_len_of_entity>600 ):
        for e in dxf.entities:
        #print("max_len_of_entity实体最大的长度为",max_len_of_entity)
            if(e.DXFTYPE=='POLYLINE' and e.__len__()>600):
            #for e in dxf.entities:
                print("由于多边形的点数太大，直接提取模型",e.__len__())
                indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                msp=newdoc.modelspace()
                                            
                msp.add_polyline2d(e.points())
            #msp=newdoc.modelspace()
            #msp.add_polyline2d(e.points())
                
                                #print("这是一个新的dxf模型文件的图形文件")       
                    
                newdoc.saveas(os.path.join(model_path,name))
    elif(number_of_blocks==2 or number_of_blocks<10):

        #model_path=make_dir("model_dir")
        print("block太少,在这提取模型")
        for e in dxf.entities:
           # indexdxf=0
            #print(e.DXFTYPE)
            
            
            if(e.DXFTYPE=="SPLINE"):
                print("模型的类型是spline")
            
               

                ##########为了将spline的点整理到列表里面，重新画成polyline。
                print(e.dxf.n_control_points)

                if(e.dxf.n_control_points>30):
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp.add_polyline2d(spline)
                #sprint(e.dxf.n_control_points)
                    print("多边线的定点数为",e)
                else:

                    spline=[]
                    for vertex in range (0,e.dxf.n_control_points):
                        #print(e.control_points[vertex])
                        #@#msp.add_point(e.control_points[vertex])
                        spline.append(e.control_points[vertex])
                    msp=newdoc.modelspace()
                                                    
                    msp.add_polyline2d(spline)
                                
               
            if(e.DXFTYPE=="LWPOLYLINE"):
                print("线段类型为LWPOLYLINE")
                for v in range (0,e.dxf.count):
                    print("第",i,"条多边形的第",v,"个顶点坐标为","x=",e.__getitem__(v)[0],"y=",e.__getitem__(v)[1])
                    i=i+1
                        
            if(e.DXFTYPE=='POLYLINE'):
                length=e.__len__()
                #print("线段类型为POLYLINE,polyline线段长度为",length)
                #if(e.is_closed==True):
                #print(e.doc)
                #print(e.dxf.handle)


                #for e in dxf.entities:


                #print("多边线的定点数为",length)\
                #if()
                
                if(length>75):

                    print("线段类型为POLYLINE,polyline线段长度为",length)
                    #if(e):
                    #print("是否handle==202")
                    #print()
                    indexdxf=indexdxf+1
                    #name=e.get_dxf_attrib('handle')+".dxf"
                    name="mode"+str(indexdxf)+".dxf"
                            #polyline_exporter = doc.export(name)
                    newdoc= ezdxf.new("R2010")
                            #name="mode"+str(indexdxf)+".dxf"
                    msp=newdoc.modelspace()
                                            
                    msp.add_polyline2d(e.points())

                    large_start_x=e.__getitem__(0).dxf.location[0]
                    large_start_y=e.__getitem__(0).dxf.location[1]

                    large_end_x=e.__getitem__(length-1).dxf.location[0]
                    large_end_y=e.__getitem__(length-1).dxf.location[1]

                    large_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    large_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

                    large_rand_x=e.__getitem__(int(((length-1)*2)/3)).dxf.location[0]

                    large_rand_2_x=e.__getitem__(int(((length-1)*4)/5)).dxf.location[0]

                    large_rand_1_x=e.__getitem__(int(((length-1))/5)).dxf.location[0]
                    #print(name
                elif(length>19):
                    print("线段类型为POLYLINE,polyline线段长度为",length,"CHANGDU")
                    small_start_x=e.__getitem__(length-1).dxf.location[0]
                    small_start_y=e.__getitem__(length-1).dxf.location[1]

                    small_end_x=e.__getitem__(length-1).dxf.location[0]
                    small_end_y=e.__getitem__(length-1).dxf.location[1]

                    small_middle_x=e.__getitem__(int((length-1)/2)).dxf.location[0]
                    small_middle_y=e.__getitem__(int((length-1)/2)).dxf.location[1]

        
                    #if(((small_start_x>large_start_x and small_start_y>large_start_y)and (small_middle_x>large_middle_x and small_middle_y>large_middle_y) )or( (small_start_x<large_start_x and small_start_y<large_start_y)and (small_middle_x<large_middle_x and small_middle_y<large_middle_y))):
                    #####搞反了，应该是小的比较大的。
                    ####整个逻辑都错了。
                    #error=1
                    if((small_start_x<large_start_x) and (small_start_x<large_middle_x) and small_start_x<large_rand_x and small_start_x<large_rand_2_x and  small_start_x<large_rand_1_x):
                        print(e.__getitem__(0).dxf.location[0])
                        indexdxf=indexdxf+1
                                #name=e.get_dxf_attrib('handle')+".dxf"
                        name="mode"+str(indexdxf)+".dxf"
                                    #polyline_exporter = doc.export(name)
                        newdoc= ezdxf.new("R2010")
                                    #name="mode"+str(indexdxf)+".dxf"
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())

                    else:
                        msp=newdoc.modelspace()
                                                    
                        msp.add_polyline2d(e.points())
                                
                        

                            
                else:
                    msp=newdoc.modelspace()
                                        
                    msp.add_polyline2d(e.points())
              
                            #print("这是一个新的dxf模型文件的图形文件")       
                
            newdoc.saveas(os.path.join(model_path,name))
                #print("模型",name,"建立好了")'''
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
                        
                        #if(e.DXFTYPE=="POLYLINE" and e.__len__()>60):
                        if(e.DXFTYPE=="POLYLINE"):
                            #print(e.DXFTYPE,j)
                            msp.add_polyline2d(e.points())
                        if(e.DXFTYPE=="ARC"):
                            msp=newdoc.modelspace()
                            msp.add_arc(e.dxf.center,e.dxf.radius,e.dxf.start_angle,e.dxf.end_angle)           

            #name=str(j)+".dxf"
                    #newdoc.saveas(name)
                    newdoc.saveas(os.path.join(model_path,name))
    return model_path


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

    #extractdxf("5037#试板.dxf")
    #extractdxf("12-30 ZAOG042221504 #22.dxf")

    #extractdxf("E:\\test\\plt\\bp27-36_4.dxf")

    #extractdxf("E:\\test\\plt\\ts20.dxf")

    path=extractdxf("E:\\test\\text\\a.dxf")

    print(path)
   


