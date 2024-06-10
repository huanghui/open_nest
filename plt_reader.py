from io import StringIO
import numpy as np

import ezdxf
#data_2 = np.genfromtxt('bp27-36.plt', delimiter=' ', skip_header=3)
#for data in data_2:
    
#from hpgl import parse_hpgl

#    print("data_2==============",data)

def parse_plt(gl_file):



    border = 10

    pen_down = False
    cur_pen = 1
    cur_x = 0
    cur_y = 0
    cto_x = 0 # text offset
    cto_y = 0

    std_font = 48
    alt_font = 48
    cur_font = 48

    char_rel_width = 0.0075
    char_rel_height = 0.0075

    char_abs_width = 0
    char_abs_height = 0

    pen_width = 1
    stroke_weight = 0

    label_term = chr(3)
    label_term_print = False

    paths = []
    labels = []
    if type(gl_file) == str:
        glf = open(gl_file,'r')
        print("gl_file的数据类型为",type(gl_file))
        #glf = gl_file
    else:
        print("gl_file的数据类型为",type(gl_file))
        glf = gl_file

    #array_points=[]

    #######建立polyline的东西
    ######建立线段列表
    array_lines=[]
    #point=[0,0]
    array_points=[]
    
    #glf=glf.decode("utf-8")

    #all_file=(glf.read()).decode("utf-8")
    #glf=all_file
    plot_time=0
    #######开始读入指令了
    while True:

        ####建立线段点数组
        #array_points=[]

        ########从标点符号开始读入
        c = glf.read(1)
        #c=c.decode("utf-8")
        while c == ';' or c == ' ' or c == '\r' or c == '\n':
            c = glf.read(1)
            #print("c99009999999999999999999999",c)
        #print("cmd++++++++++++++",glf.read(2),"c+++++++++++++++++",c)

        #print("foi9w[ejfwo3envoiwenvoiwenviowenjvwe",glf.read(0),"jifnweofnwoeinfweoinfweofhnweoihn",glf.read(100))
        #c=c.decode("utf-8")
        #print(type(c),type((glf.read(1)).decode("utf-8")))
        #md=(glf.read(1)).decode("utf-8")
        #c=c.decode("utf-8")
        #c=
        #print(c,type(c))
        cmd = c + glf.read(1)
        #cmd = c + md
        cmd = cmd.upper()
        #cmd = cmd.decode("utf-8")
        #print("cmd++++++++++++++====================",cmd)
        #print(glf.read(100))
        if cmd=='':
            print("数据或者指令为空")
            break
        if len(cmd)  < 2:
            print("数据或者指令为空<2")
            break
        #######如果实现了PU和PD,那么现在的办法就是
        #if cmd=='IN':
          #  pass
        
        if cmd == 'PU':
            # pen up
            pen_down = False
            ####不能随便read
            data=''
            letter=glf.read(1)
            while(letter!=';'):
              data=data+letter
              letter=glf.read(1)

            #print("data的数值等于================",data)
            point=[0,0]
            point[0]=float((data.split(','))[0])/40
            point[1]=float(((data.split(',')[1]).split(';'))[0])/40
            #print("获取的点坐标为",point[0],point[1])
            #array_points.append(point)
            plot_time=plot_time+1
            print("命令为PU","坐标为",point,"提笔次数============",plot_time)
            #print("array_points点的坐标为",array_points)
            #array_points.append(point)
            array_points.append(tuple(point))
            ####当碰到pu时，该抬刀了，这个时候,需要重新建立array_points了。
            #print(array_points)
            '''if len(array_points)>0: 
                array_lines.append(array_points)
            #array_points.clear()
            array_points=[]'''
            #continue



        elif cmd == 'PD':
            # pen down
            pen_down = True

            data=''
            letter=glf.read(1)
            while(letter!=';'):
              data=data+letter
              letter=glf.read(1)

            #print("data的数值等于================",data)
            point=[0,0]

            #point=(0,0)
            point[0]=float((data.split(','))[0])/40
            point[1]=float(((data.split(',')[1]).split(';'))[0])/40
            #print("获取的点坐标为",point[0],point[1])
            #print(point)

            array_points.append(tuple(point))
            #print(array_points)
            #print("array_points点的坐标为",array_points)
            #continue 

        elif cmd == 'SP':
            # select pen
            c = glf.read(1)
            if c == ';':
                continue
            elif c=='':
                print("数据已经到头了")
            
                break
            cur_pen = int(c)
            if(cur_pen==0):
                print("cur_pen==============",cur_pen,"文件已到末尾")
                if len(array_points)>0: 
                    array_lines.append(array_points)

            
            #continue
        elif cmd == 'LT':
            if len(array_points)>0: 
                array_lines.append(array_points)
            #array_points.clear()
            array_points=[]
            #pass
        ################字体命令的更改
        elif cmd == 'SA':
            # select alternate
            cur_font = alt_font
        elif cmd == 'SS':
            # select standard
            cur_font = std_font

        elif cmd == 'SR':
            # specify relative character sizes
            s = ''
            c = glf.read(1)
            while c != ',':
                s += c
                c = glf.read(1)
            char_rel_width = float(s)/100.0
            s = ''
            c = glf.read(1)
            while c != ';':
                s += c
                c = glf.read(1)
            char_rel_height = float(s)/100.0
        elif cmd == 'SI':
            # specify absolute character sizes
            s = ''
            c = glf.read(1)
            while c != ',':
                s += c
                c = glf.read(1)
            char_abs_width = float(s)
            s = ''
            c = glf.read(1)
            while c != ';':
                s += c
                c = glf.read(1)
            char_abs_height = float(s)

        elif cmd == 'PA':
            # plot absolute

            c = ''
            pts = [(cur_x, cur_y, cto_x, cto_y)]

            while c != ';':
                s = ''
                c = glf.read(1)
                if c == ';':
                    cur_x = 0
                    cur_y = 0
                    cto_x = 0
                    cto_y = 0
                    pts.append((0,0,0,0))
                    break
                while c == '-' or ord(c) >= 48 and ord(c) <= 57:
                    s += c
                    c = glf.read(1)

                cur_x = int(s)

                s = ''
                c = glf.read(1)
                while c == '-' or ord(c) >= 48 and ord(c) <= 57:
                    s += c
                    c = glf.read(1)

                cur_y = int(s)

                cto_x = 0
                cto_y = 0

                pts.append((cur_x, cur_y, 0, 0))

            if pen_down:
                paths.append((cur_pen, pen_width, pts))
        elif cmd == 'LB':
            # label

            c = glf.read(1)
            x = cur_x
            y = cur_y
            tx = cto_x
            ty = cto_y
            while label_term_print or c != label_term:
                if ord(c) == 8:
                    cto_x -= char_rel_width * 3/2
                elif ord(c) == 10:
                    cto_x = tx
                    cto_y -= char_rel_height * 2
                elif ord(c) < 32:
                    pass
                else:
                    labels.append((cur_x, cur_y, cto_x, cto_y, char_rel_width, char_rel_height, cur_pen, cur_font, c))
                    cto_x += char_rel_width * 3/2
                    if c == label_term:
                        break
                c = glf.read(1)
        elif cmd == 'DI':
            # absolute direction
            s = ''
            c = glf.read(1)
            if c == ';':
                #run = 1
                #rise = 0
                continue
            while c != ',':
                s += c
                c = glf.read(1)
            #run = float(s)
            s = ''
            c = glf.read(1)
            while c != ';':
                s += c
                c = glf.read(1)
            #rise = float(s)
        elif cmd == 'DF':
            # defaults
            pen_down = False
            cur_pen = 1
            cur_x = 0
            cur_y = 0
            cto_x = 0
            cto_y = 0

            std_font = 48
            alt_font = 48
            cur_font = 48

            char_rel_width = 0.0075
            char_rel_height = 0.0075

            label_term = chr(3)
            label_term_print = False
        elif cmd == 'IN':
            # init
            print("这里就是处理IN指令的内容")
            pen_down = False
            cur_pen = 1
            cur_x = 0
            cur_y = 0
            cto_x = 0
            cto_y = 0

            std_font = 48
            alt_font = 48
            cur_font = 48

            char_rel_width = 0.0075
            char_rel_height = 0.0075

            label_term = chr(3)
            label_term_print = False
        elif cmd == 'OP':
            # output P1 and P2 - ignored
            pass

        elif cmd=='PG':
            break
        elif cmd=='VS' or cmd=='32':
            vsstr=glf.read(4)
            print("vsstr==================",vsstr)
            continue
        elif cmd=='WU':
            wustr=glf.read(1)
            print("vsstr==================",wustr)
            continue
        elif cmd=='PW':
            wustr=glf.read(7)
            print("vsstr==================",wustr)
            continue


        else:
            #print("cmd+++++++++++++++++++++++",cmd)
            raise Exception("Unknown HPGL command (%s)" % cmd)
            #print("cmd+++++++++++++++++++++++",cmd)

    # determine size
    max_x = 0
    max_y = 0

    # max extent of vector graphics
    for path in paths:
        pen, width, pts = path
        for p in pts:
            max_x = max(p[0], max_x)
            max_y = max(p[1], max_y)

    # max extent of text
    for lb in labels:
        max_x = max(lb[0]/(1-(lb[2]+lb[4])), max_x)
        max_y = max(lb[1]/(1-(lb[3]+lb[5])), max_y)

    max_x = round(max_x+0.5)
    max_y = round(max_y+0.5)

    # add text offsets
    paths2 = []
    for path in paths:
        pen, width, pts = path
        pts2 = []
        for p in pts:
            pts2.append((p[0] + p[2]*max_x, p[1] + p[3]*max_y))
        paths2.append((pen, width, pts2))
    paths = paths2

    # render text
    for lb in labels:
        x, y, tx, ty, cw, ch, pen, font, c = lb
        width = cw*max_x
        height = ch*max_y
        x += tx*max_x
        y += ty*max_y
        if stroke_weight < 9999:
            pw = 0.1 * min(height, 1.5*width) * 1.13**stroke_weight
        else:
            pw = pen_width
        if c in stick_font:
            chr_paths = stick_font[c]
            for pts in chr_paths:
                path = []
                for p in pts:
                    path.append((p[0]/4*width+x, p[1]/8*height+y))
                paths.append((pen, pw, path))

    max_x += border*2
    max_y += border*2

    # flip y axis and shift
    paths2 = []
    for path in paths:
        pen, width, pts = path
        pts2 = []
        for p in pts:
            pts2.append((p[0]+border, max_y-p[1]-border))
        paths2.append((pen, width, pts2))

    return paths2, max_x, max_y,array_lines



#array_list,maax_x,max_y,array_points=parse_plt("test2.plt")

#print("读入的文件为：",'test2.plt')

def  plt_to_dxf(points_lines,save_dxf_file):
    doc = ezdxf.new('R2010')
    #doc=modsapce
    msp = doc.modelspace()
    #new_line=[]
    #new_array_lines=[]
    ########这里是array_lines数组了，
    '''for line in points_lines:
        for  point in line:
            vec=(point[0],point[1])
            #sprint(vec)
            new_line.append(vec)
            
       #print("line的长度为",len(line))
        new_array_lines.append(new_line)'''
    print("第一次点坐标执行完毕。")
    #@pointsarray
    #for i in range (0,len(new_array_lines)-1):
       # print("line===========",i,"new_array_lines的长度为",len(new_array_lines[i]) )
    print("points_lines============的长度为",len(points_lines))
    for line in  points_lines:
        #for point in line:
           # print(point)
        msp.add_polyline2d(line)
        #i=i+1
        #print(i)
        #print(line,"该线段结束了")
        
    #msp.add_line((0, 0), (10, 0))
    doc.saveas(save_dxf_file)

#array_list=parse_plt("bp27-36.plt")
#array_list,maax_x,max_y,array_points=parse_plt('bp27-36.plt')

def  plt_to_dxf_one_line(points_lines,save_dxf_file):
    doc = ezdxf.new('R2010')
    #doc=modsapce
    msp = doc.modelspace()
    new_line=[]
    new_array_lines=[]
    ########这里是array_lines数组了，
    for line in points_lines:
        for  point in line:
            vec=(point[0],point[1])
            #sprint(vec)
            new_line.append(vec)
            
       #print("line的长度为",len(line))
        new_array_lines.append(new_line)
    print("第一次点坐标执行完毕。")
    #@pointsarray
    #for i in range (0,len(new_array_lines)-1):
       # print("line===========",i,"new_array_lines的长度为",len(new_array_lines[i]) )
    #i=0
    for polyline in new_array_lines:

        print(len(new_array_lines))
        #msp.add_lwpolyline(polyline)
        msp.add_polyline(polyline)
        #i=i+1
        #print(i)
        #print(line,"该线段结束了")
        
    #msp.add_line((0, 0), (10, 0))
    doc.saveas(save_dxf_file)



if __name__=="__main__":

    print("读入的文件为",'ts.plt')

    #print("array_points的长度为",len(array_points),"array_points===========",array_points)
    #for point in array_points:
    #  print(point)

    #plt_to_dxf(array_points,"bp27-36.dxf")

    print("执行结束，去查看plt_line.dxf是个什么怪物")

    #array_list,maax_x,max_y,array_lines=parse_plt('ts.plt')

    array_list,maax_x,max_y,array_lines=parse_plt("e:\\test\\plt\\ts.plt")

    plt_to_dxf(array_lines,"ts20.dxf")
    #plt_to_dxf_one_line(array_lines,"ts9.dxf")
    print("执行结束，去查看ts9.xf是个什么怪物")