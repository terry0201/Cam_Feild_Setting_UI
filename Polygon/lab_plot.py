import cv2 
import math
import numpy as np
import matplotlib.pyplot as plt
from utils import set_pyplot_marker_size

class DraggablePloygonMarker():
    def __init__(self, MainWindow, resizedPic):
        super().__init__()
        self.press = None
        self.pressInMarker = False
        self.whichMarker = None
        self.fig, self.ax = None, None
        self.markerSize = None
        self.radius = None

        # The parameters of Lab_UI are used in this class
        self.MainWindow = MainWindow
        self.resizedPic = resizedPic
        self.transformPolygonID = self.MainWindow.ui.transformPolygonID
        self.transformAttr = self.MainWindow.ui.transformAttr
        self.transformMatrix = self.MainWindow.ui.transformMatrix
        self.transformF = self.MainWindow.ui.transformF
        self.arrForPlotX = self.MainWindow.ui.arrForPlotX
        self.arrForPlotY = self.MainWindow.ui.arrForPlotY
        self.attribute =  self.MainWindow.ui.attribute
        self.resize = self.MainWindow.ui.resize
    
    def setup(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        maxx, minx, maxy, miny, xDiff, yDiff = self.get_beginning_xy_range()
        self.connect()
        self.set_beginning_info((minx - 20, maxx + 20),(miny - 20, maxy + 20), xDiff, yDiff)
        self.show()

    def set_beginning_info(self, xlim, ylim, xDiff, yDiff):
        """ Set some beginning pyplot-related data, radius, and marker size. """
        self.ax_dict = dict()
        self.ax_dict = {
            'xlim' : xlim,
            'ylim' : ylim,
            'figw' : self.ax.figure.get_figwidth(),
            'figh' : self.ax.figure.get_figheight(),
            'scale' : 1.0,
        }
        self.markerSize = 7
        # 測試其他範圍初始化=>同一圖片OK，換一張圖片隨便畫一個多邊形也OK
        self.radius = (xDiff * yDiff * (2.06155*(10 ** -5)) + 0.810779404)

    def connect(self):
        """ Connect to all the events we need. """
        self.cidScroll = self.fig.canvas.mpl_connect(
                'scroll_event', self.scroll_callback)   # zoom in zoom out
        self.cidPress = self.fig.canvas.mpl_connect(
                'button_press_event', self.press_callback)
        self.cidMotion = self.fig.canvas.mpl_connect(
                'motion_notify_event', self.motion_notify_callback)
        self.cidRelease = self.fig.canvas.mpl_connect(
                'button_release_event', self.release_callback)  
        self.cidy = self.ax.callbacks.connect(
                'ylim_changed', self.on_ylims_change)

    def on_ylims_change(self, event):
        self.markerSize, self.ax_dict = set_pyplot_marker_size(self.markerSize, self.ax_dict, self.fig, self.ax)
        print("After on_ylims_change() r: ", self.radius)
        print("After on_ylims_change() markerSize: ", self.markerSize)
        self.draw()
        
    def release_callback(self, event):
        """ Left mouse button is released. """
        if event.button == 1 and self.pressInMarker:
            self.pressInMarker = False
            # print(self.transformAttr)
            # print(self.attribute)
   
    def motion_notify_callback(self, event):
        """ If the left mouse clicks the default range of the marker and moves. """
        if self.pressInMarker: 
            (x0, y0), (xpress, ypress) = self.press
            if not event.xdata and not event.ydata : return
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            self.arrForPlotX[self.whichMarker], self.arrForPlotX[self.whichMarker + 4], self.transformAttr[self.whichMarker][0] = x0+dx, x0+dx, x0+dx
            self.arrForPlotY[self.whichMarker], self.arrForPlotY[self.whichMarker + 4], self.transformAttr[self.whichMarker][1] = y0+dy, y0+dy, y0+dy  
            for i, xy in enumerate(self.transformAttr):
                x, y = self.trans_point_position(xy[0],xy[1])
                self.attribute[self.transformPolygonID][i][0] = x
                self.attribute[self.transformPolygonID][i][1] = y
            self.MainWindow.ui.attribute =  self.attribute
            self.MainWindow.ui.ReDraw(update_for_tracking_pixmap = True)
            self.draw()

    def press_callback(self, event):
        """ Left mouse button is pressed. """
        self.pressInMarker = False
        # Avoid collision between toolbar and left-click move
        toolbarMode = plt.get_current_fig_manager().toolbar.mode
        print("CURRENT TOOL MODE: ", toolbarMode)
        if event.button == 1 and event.xdata and event.ydata and toolbarMode == "":
            for i, xy in enumerate(self.transformAttr):
                distance = math.sqrt(abs(xy[0] - event.xdata) ** 2 + abs(xy[1] - event.ydata) ** 2)
                print("Distance: ", distance)
                if distance <= self.radius:
                    print("In CIRCLE!")
                    self.pressInMarker = True
                    self.press = (xy[0], xy[1]), (event.xdata, event.ydata)
                    self.whichMarker = i
                    break

    def scroll_callback(self, event):
        """ User scrolls the mouse wheel. """
        # Restrict users from scrolling in non-picture spaces
        if not event.inaxes : return

        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        fanwei = (x_max - x_min) / 10
        fanwei2 = (y_max - y_min) / 10

        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei, x_max - fanwei),
                       ylim=(y_min + fanwei2, y_max - fanwei2))

        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei, x_max + fanwei),
                       ylim=(y_min - fanwei2, y_max + fanwei2))
    
    def trans_point_position(self, x, y):
        """
        Restore the coordinates on pyplot to their original positions.

        Params : 
            [array] matrix : The conversion matrix used in the original picture.
            [float] f : Zoom size value used in the original picture.
            [float] x : x-coordinate value in pyplot.
            [float] y : x-coordinate value in pyplot.
            
        Return :
            [float] new_x : The original x-coordinate value.
            [float] new_y : The original y-coordinate value.
        
        """
        _, IM = cv2.invert(self.transformMatrix)
        tmpx = x / self.transformF     
        tmpy = y / self.transformF
        coord = [tmpx, tmpy] + [1]
        P = np.float32(coord)

        x, y, z = np.dot(IM, P)
        #Divide x and y by z to get 2D in frame {A}
        new_x = (x / z) / self.resize
        new_y = (y / z) / self.resize
        return new_x, new_y  # original coordinates

    def show(self):
        """ 
        Show plot. 
        Users need to pay attention to the order of point creation and the order of point coordinates in the matching table.
        They must be the same.     
        """
        plt.xlim(self.ax_dict['xlim'])
        plt.ylim((self.ax_dict['ylim'][1],self.ax_dict['ylim'][0]))
        image = cv2.cvtColor(self.resizedPic, cv2.COLOR_BGR2RGB) # color the pic
        pixels = np.array(image)
        plt.imshow(pixels)
        plt.show(block = False)

    def get_beginning_xy_range(self):
        """
        Get the range and maximum and minimum values of the x-axis and y-axis at the beginning.
      
        Return :
            [float] maxx : The beginning x-axis maximum value.
            [float] minx : The beginning x-axis minimum value.
            [float] maxy : The beginning y-axis maximum value.
            [float] miny : The beginning y-axis minimum value.
            [float] xDiff : The difference of x-axis.
            [float] yDiff : The difference of y-axis.

        """
        for i, xy in enumerate(self.transformAttr):
            if i==0 : minx = xy[0]; maxx = xy[0]; miny = xy[1]; maxy = xy[1]
            else:
                minx = minx if minx < xy[0] else xy[0]
                maxx = maxx if maxx > xy[0] else xy[0]
                miny = miny if miny < xy[1] else xy[1]
                maxy = maxy if maxy > xy[1] else xy[1]
        xDiff = abs(maxx - minx)
        yDiff = abs(maxy - miny)
        print("xrange: ", maxx, " ", minx, " 差值: ", xDiff)
        print("yrange: ", maxy, " ", miny, " 差值: ", yDiff)
        print("圖片一開始所佔pixels： ", xDiff * yDiff)

        return maxx, minx, maxy, miny, xDiff, yDiff

    def draw(self):
        """ Drawing lines and markers for the plot. """
        if self.ax.lines : self.ax.lines.pop()
        self.fig.canvas.draw_idle()
        self.ax.plot(self.arrForPlotX, self.arrForPlotY, color="blue", alpha=0.5,
                             linewidth = 3, marker = "o", markersize = self.markerSize)
