import ezdxf
import numpy as np

import time
#import ezdxf
from shapely.geometry import Polygon ###多边形

from shapely.geometry import Polygon,MultiPoint

import matplotlib.pyplot as plt
import scipy.io as io

import point_in_poly

dxf = ezdxf.readfile('Piece11-S6.dxf')
#dxf = ezdxf.readfile('merge.dxf')
msp = dxf.modelspace()
'''for b in dxf.blocks:
    print(b.name)
    for e in b:
        if e.DXFTYPE=="POLYLINE":
            for p in e.points():
            #print(e.DXFTYPE)
                Polygon.add(p)
poly=Polygon'''
point=(0,0)
Points=[]

#polyline=
poly_lines=[]
# get all POLYLINE entities from model space
polylines = msp.query('POLYLINE')
print(len(polylines))
#for polyline in polylines:
   # print('Polyline #{}'.format(polyline.dxf.handle))
  #print(polyline.is_closed)
    #for p in polyline.points():
       # print(p[0],p[1])
      #poly= Polygon达会好看很多
doc2 = ezdxf.new("R2000")
msp2 = doc2.modelspace()
for polyline in polylines:
    poly_lines.append(polyline)
    #msp.addlwpoline()
    msp2.add_lwpolyline(polyline.points())
    for p  in polyline.points():
        point=(p[0],p[1])
       # msp.addlwpoline(point)
        Points.append(point)

#for p in Points:
   # if point_in_poly.is_in_poly2(p,points):
poly=Polygon(Points)
#poly=Polygon([[p[0], p[1]] for polyline in polylines  for p in polyline.points()])
    #for i, location in enumerate(polyline.points()):
        #print('Point at index {}: {}'.format(i, location))





# point format = (x, y, [start_width, [end_width, [bulge]]])
# set start_width, end_width to 0 to be ignored (x, y, 0, 0, bulge).

#points = [(0, 0, 0, .05), (3, 0, .1, .2, -.5), (6, 0, .1, .05), (9, 0)]
#msp2.add_lwpolyline(Points)

doc2.saveas("lwpolyline5.dxf")
print("文件保存成lwpolyline成功")


#from shapely.geometry import Polygon'''
#poly=Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

ax=plt.gca()
ax.xaxis.set_ticks_position('top')
#ax.invert_yaxis()
plt.plot(*poly.exterior.xy)
    #plt.plot(*data2.exterior.xy)
    #plt.plot(*data3.exterior.xy)
    #plt.plot(*data4.exterior.xy)
plt.show()




