import cv2 
import math
import numpy as np
import matplotlib.pyplot as plt

class DraggablePloygonMarker():
    MarkerSize = 7
    Radius = 3
    # TODO: ? Marker現在會因為縮放而造成放大較精準，縮小容易在圈內但不會移動
    def __init__(self, MainWindow, resizedPic):
        super().__init__()
        self.press = None
        self.pressInMarker = False
        self.whichMarker = None
        self.fig, self.ax = None, None

        # The parameters of Lab_UI are used in this class
        self.MainWindow = MainWindow
        self.resizedPic = resizedPic
        self.transformPolygonID = self.MainWindow.ui.transformPolygonID
        self.transformAttr = self.MainWindow.ui.transformAttr
        self.transformmatrix = self.MainWindow.ui.transformmatrix
        self.transformf = self.MainWindow.ui.transformf
        self.arrForPlotX = self.MainWindow.ui.arrForPlotX
        self.arrForPlotY = self.MainWindow.ui.arrForPlotY
        self.attribute =  self.MainWindow.ui.attribute
        self.resize = self.MainWindow.ui.resize
    
    def setup(self):
        plt.close('all')
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.connect()
        self.show()

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
    #     self.cidx = self.ax.callbacks.connect(
    #             'xlim_changed', self.on_xlims_change)
    #     self.cidy = self.ax.callbacks.connect(
    #             'ylim_changed', self.on_ylims_change)

    # def on_xlims_change(self, event_ax):
    #     print("updated xlims: ", event_ax.get_xlim())

    # def on_ylims_change(self, event_ax):
    #     print("updated ylims: ", event_ax.get_ylim())

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
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            # self.arrForPlotX[self.whichMarker] = self.arrForPlotX[self.whichMarker + 4] = self.transformAttr[self.whichMarker][0] = x0+dx
            # self.arrForPlotY[self.whichMarker] = self.arrForPlotY[self.whichMarker + 4] = self.transformAttr[self.whichMarker][1] = y0+dy
            self.arrForPlotX[self.whichMarker], self.arrForPlotX[self.whichMarker + 4], self.transformAttr[self.whichMarker][0] = x0+dx, x0+dx, x0+dx
            self.arrForPlotY[self.whichMarker], self.arrForPlotY[self.whichMarker + 4], self.transformAttr[self.whichMarker][1] = y0+dy, y0+dy, y0+dy  
            for i, xy in enumerate(self.transformAttr):
                x, y = self.trans_point_position(xy[0],xy[1])
                self.attribute[self.transformPolygonID][i][0] = x
                self.attribute[self.transformPolygonID][i][1] = y
            self.MainWindow.ui.attribute =  self.attribute
            self.MainWindow.ui.ReDraw(update_for_tracking_pixmap = True)
            self.ax.lines.pop()
            self.fig.canvas.draw_idle()
            self.draw()

    def press_callback(self, event):
        """ Left mouse button is pressed. """
        self.pressInMarker = False
        # Avoid collision between toolbar and left-click move
        toolbarMode = plt.get_current_fig_manager().toolbar.mode
        print("CURRENT TOOL MODE: ", toolbarMode)
        if event.button == 1 and event.xdata and event.ydata and toolbarMode == "":
            for i, xy in enumerate(self.transformAttr):
                distance = math.sqrt(abs(xy[0]-event.xdata) ** 2 + abs(xy[1]-event.ydata) ** 2)
                # print("Distance: ", distance)
                if distance <= self.Radius:
                    print("In CIRCLE!")
                    self.pressInMarker = True
                    self.press = (xy[0], xy[1]), (event.xdata, event.ydata)
                    self.whichMarker = i
                    break

    # for ToTrans matplot window 
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

        self.fig.canvas.draw_idle()
    
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
        _, IM = cv2.invert(self.transformmatrix)
        tmpx = x / self.transformf     
        tmpy = y / self.transformf
        coord = [tmpx, tmpy] + [1]
        P = np.float32(coord)

        x, y, z = np.dot(IM, P)
        #Divide x and y by z to get 2D in frame {A}
        new_x = (x / z) / self.resize
        new_y = (y / z) / self.resize
        return new_x, new_y  # original coordinates

    def show(self):
        """ Show plot. """
        for i, xy in enumerate(self.transformAttr):
            if i==0 : minx = xy[0]; maxx = xy[0]; miny = xy[1]; maxy = xy[1]
            else:
                minx = minx if minx < xy[0] else xy[0]
                maxx = maxx if maxx > xy[0] else xy[0]
                miny = miny if miny < xy[1] else xy[1]
                maxy = maxy if maxy > xy[1] else xy[1]
        # print(minx," ",maxx," ",miny," ",maxy)
        # Users need to pay attention to the order of point creation and the order of point coordinates in the matching table.
        # They must be the same
        plt.xlim(minx - 10, maxx + 10)
        plt.ylim(maxy + 10, miny - 10)
        image = cv2.cvtColor(self.resizedPic, cv2.COLOR_BGR2RGB)
        pixels = np.array(image)
        plt.imshow(pixels) #, interpolation = "nearest")
        self.draw()
        plt.show(block = False)
        
    def draw(self):
        """ Drawing lines and markers for the plot. """
        self.ax.plot(self.arrForPlotX, self.arrForPlotY, color="blue", alpha=0.5,
                             linewidth = 3, marker = "o", markersize = self.MarkerSize)
