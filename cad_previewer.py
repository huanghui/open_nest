# -*- coding: utf-8 -*-
import ezdxf
import sys
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.pyqt import PyQtBackend, CorrespondingDXFEntity, CorrespondingDXFParentStack
from ezdxf.addons.drawing.properties import is_dark_color
from ezdxf.lldxf.const import DXFStructureError
from ezdxf.addons.drawing.qtviewer import CADGraphicsViewWithOverlay
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*


#class cadWindow(QtWidgets.QMainWindow):
class cadPreViewer(QWidget):
    def __init__(self, parent=None):
        super(cadPreViewer, self).__init__(parent) 

        self.setWindowTitle('cadViewer')
        self.setGeometry(400,500,1000,500)
        #全局布局（2中）：这里选择水平布局
        ##########重新设计布局，因为不是centralwidget,但后期可以考虑将这个设计为centralwidget
        self.wlayout=QHBoxLayout()
        self.setLayout(self.wlayout)
        self.left_layout=QVBoxLayout()
        self.resize(800, 800)
        self.render_params = {'linetype_renderer': 'ezdxf'}
        #self.selectedInfo = SelectedInfo(self)
        #self.layers = new_layers(self)
        #self.logView = LogView(self)
       # self.logView =new_log_view(self)
        self.statusLabel = QtWidgets.QLabel()

        self.view=CADGraphicsViewWithOverlay()
        #self.view = CADGraphicsViewWithOverlay()
        self.view.setScene(QtWidgets.QGraphicsScene())
        #self.view.scale(0.1,0.1)
        #self.view.scale(0, 0)
        #self.view._zoom=0
        #self.view.setFixedSize(200,200)
        #self.view.scale()

        ###########预览的部分不需要放大缩小的功能，也暂时不需要
        ########那么多复杂的功能。
        self.view.setEnabled(False)
        self.wlayout.addWidget(self.view)
        #self.
        

    def open_file(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '', 'CAD files (*.dxf *.DXF)')
        if filename == '':
            return
        #print("小日本的东西写得成不？")
        print(filename)
        self.dxf = ezdxf.readfile(filename)
        
        #print("小日本的东西写得成不？")
        self.render_context = RenderContext(self.dxf)
        
        #self.backend = PyQtBackend(use_text_cache=True, params=self.render_params)
        self.backend = PyQtBackend(use_text_cache=True)
        print("成功读入")
        #self.layers.visible_names = None
        self.current_layout = None
        print("程序已经走到了这里")
        #self.select_layout_menu.clear()
        '''for layout_name in self.dxf.layout_names_in_taborder():
            action = self.select_layout_menu.addAction(layout_name)
            action.triggered.connect(self.change_layout)'''

        #self.layers.populate_layer_list( self.render_context.layers.values() )
        self.draw_layout('Model')
        self.setWindowTitle('CAD Viewer - ' + filename)


    def change_layout(self):
        layout_name = self.sender().text()
        self.draw_layout(layout_name)


############这个非常重要
    def draw_layout(self, layout_name):
        self.current_layout = layout_name
        self.view.begin_loading()
        new_scene = QtWidgets.QGraphicsScene()
        self.backend.set_scene(new_scene)
        layout = self.dxf.layout(layout_name)
        self.render_context.set_current_layout(layout)
        #if self.layers.visible_names is not None:
           # self.render_context.set_layers_state(self.layers.visible_names, state=True)
        try:
            frontend = MyFrontend(self.render_context, self.backend)
            #frontend.log_view = self.logView
            frontend.draw_layout(layout)
        except DXFStructureError as e:
            self.logView.append('DXF Structure Error')
            self.logView.append(f'Abort rendering of layout "{layout_name}": {str(e)}')
        finally:
            self.backend.finalize()
        
        self.view.end_loading(new_scene)
        self.view.buffer_scene_rect()
        #self.view.scale(1,1)
        self.view.fit_to_scene()
        #self.view.setFixedSize(100,100)
        self.view.setScene(new_scene)


class MyFrontend(Frontend):
    log_view = None
    def log_message(self, message):
        self.log_view.append(message)

if __name__ == '__main__':
    #app = QtWidgets.QApplication(sys.argv)
    app = QApplication(sys.argv)
    window = cadPreViewer()
    window.show()
    window.open_file()
    app.exec()