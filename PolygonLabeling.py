# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 17:15:24 2020
Use pyplot & TK to draw field info (polygon + descriptions)
@author: SSI
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from time import sleep
import matplotlib.patches as patches
import xml.etree.ElementTree as gfg  
        
def GenerateXML(dictionary, fileName="labelling.xml") : 
    """This funtion generate the required XML file"""   
    root = gfg.Element("annotation") 
     #the big section is called Annotation
    for key in dictionary:
        #for every polygon list in inside object witho subelement name and attributes and the type "polygon"
        objectElement = gfg.Element("object") 
        root.append(objectElement) 
        subElement1 = gfg.SubElement(objectElement,  "name:".strip(":"))
        subElement1.text = str(dictionary[key]["name"])
        subElement2 = gfg.SubElement(objectElement,  "attributes".strip(":"))
        subElement2.text = str(dictionary[key]["attributes"])
        subElement3 = gfg.SubElement(objectElement,  "polygon")
    
        for i in range(0, len(dictionary[key])-2):
            #for every vertex of the polygon list it's rounded x, y on xml
            SubInsidePolygon = gfg.SubElement(subElement3, "pt")
            sub_x = gfg.SubElement(SubInsidePolygon, "x")
            sub_y = gfg.SubElement(SubInsidePolygon, "y")
            sub_x.text = str(int(round(dictionary[key]["x_y_" + str(i)][0])))
            sub_y.text = str(int(round(dictionary[key]["x_y_" + str(i)][1])))
    tree = gfg.ElementTree(root) 
    #create the xml tree
    with open (fileName, "wb") as files : 
        tree.write(files) 
        #if xml does not exist create one otherwise rewrite to it

class TKInputDialog:
    #ref: https://www.python-course.eu/tkinter_entry_widgets.php
    def __init__(self, name='', attributes= '', win_size=(300, 200)):
        self.master = tk.Tk()
        self.entries = {}
        self.ret = None
        self.master.title("Enter Name and Attributes")
        
        firstLabel = tk.Label(self.master, text= "name")
        firstEntry = tk.Entry(self.master)
        #add rows to enter name 
        firstEntry.insert(0, name)
        #put the name that was enter last time back to the textbox
        #otherwise leave blank
        ent = firstEntry
        #Newly enter value
        self.entries["name"] = ent
        #Using self.entries to store the entered value
        secondLabel = tk.Label(self.master, text="attributes")
        secondEntry = tk.Entry(self.master)
        secondEntry.insert(0, attributes)
        ent = secondEntry
        self.entries["attributes"] = ent
        
            #confirm actions       
        btnDone = tk.Button(self.master, text='Ok', command=self.ok) #press OK button
        tk.Button(self.master, text='Ok', command=self.ok)
        
        firstLabel.grid(row=0, column=0, padx=15, pady=15)
        firstEntry.grid(row=0, column=1, padx=15, pady=15)
        #set size of the name textbox
        
        secondLabel.grid(row=1, column=0, padx=15, pady=15)
        secondEntry.grid(row=1, column=1, padx=15, pady=15, ipady=30, rowspan=2)
        #set size for the attribute textbox
        
        btnDone.grid(columnspan=3, padx=15, pady=15)
        #set size of the button 
        
        #adjust window position & size https://stackoverflow.com/a/14910894/10373104
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry('%dx%d+%d+%d' % (win_size[0], win_size[1], int(w/2), int(h/2)))
    
        self.master.focus_force() #move focus to this window https://stackoverflow.com/a/22751955/10373104
        self.master.mainloop()

    def ok(self, event=None):
        self.ret = {key: val.get() for key, val in self.entries.items()}
        #save the info
        self.master.quit()
        return self.ret
    
    def get(self):
        self.master.withdraw()
        #close Tk window
        return self.ret


class MousePointsReactor:
    '''return desired mouse click points on frame get_mouse_points'''
    def __init__(self, img, num, labels:list=None, defaults:list=None, output_xml='default.xml'):
        self.img = img
        self.num = num
        self.labels = labels
        self.defaults = defaults
        self.pts = {} #final results
        self.circles = [] #double click positions
        self.texts = [] #show text for circles
        self.l = None #temporary line patch
        self.ax = None #pyplot canvas
        self.clicked_circle = None #save the clicked circle
        self.clicked_point = None #save the clicked point
        self.c = None #get circle appears when mouse pass the circles
        self.point = None #the point clicked on at first to move
        self.kayma = None #the change vector
        self.press = False #if the circle pressed
        self._start = False #start to move
        self.newline = [] #for drawing a line
        self.circles = [] #all circles
        self.polygons = []#all poly
        self.move_patch = [] #the patch to move
        self.current_items = {"circle": [], "line": [], "polygon": []} #The items that are being drawing now (they are linked)
        self.all_patches = [] #all the items drawn
        self.poly_info = {} #store name, attribute and x,y(value) of a polygon(key)
        self.output_xml = output_xml
        
    def onClick(self, event):
        def get_xy_min_max(list_verteces):
            x_min = 10000 
            x_max = -1000
            y_min = 10000 
            y_max = -10000
            for pt in list_verteces:
                if pt[0] <= x_min:
                    x_min = pt[0]
                if pt[0] >= x_max:
                    x_max = pt[0]
                if pt[1] <= y_min:
                    y_min = pt[1]
                if pt[1] >= y_max:
                    y_max = pt[1]
            return (x_min, x_max, y_min, y_max) 
        #Use this function to find the x,y's max and min out of all vertices 

        if not event.xdata or not event.ydata: #click outside image
            return
        pos = (event.xdata, event.ydata) #set mouse data to pos
        if event.button == MouseButton.LEFT: #click left button: 
            click_on_circle = False 
            click_on_polygon = False 
            for i_c, c in enumerate(self.circles): #check if in every exist circule
                contains, attrd = c.contains(event)
                if contains:
                    click_on_circle = True
                    if self.current_items["circle"] and not self.current_items["polygon"]: 
                        #check if already drawing lines/circles and not yet close so no polygon 
                        if self.current_items["circle"][0].contains(event): 
                        #if so then, check if click back to the first point => if yes then draw polygon(the shape is closed now)
                            vertex = []
                            for c in self.current_items["circle"]:
                                vertex.append(c.center)
                            #set the ceter of the circles as the vertex of the polygon
                            p = Polygon(vertex,alpha=0.5)
                            #transparent polygon
                            self.ax.add_patch(p)
                            #add on to the canvas (they are alias)
                            self.current_items["polygon"].append(p)
                            #add to current item (they are alias)
                            self.polygons.append(p)
                            #add to all polygonds (they are alias)
                            self.current_items["line"].append(self.l)
                            # self.ax.add_line(self.l)
                            self.newline = []
                            self.l = None
                            #add drawn line and reset the drawing system
                            self.all_patches.append(self.current_items)
                            #add current item to all drawn items
                            for i, c_ in enumerate(self.current_items["circle"]):
                                if i>0:
                                    self.ax.patches.remove(c_)
                                #remove the drawn circles on the canva (still stored in all_patches) 
                            self.current_items = {"circle": [], "line": [], "polygon": []}
                            #reset current item

                    elif not self.current_items["circle"]: 
                        #check if to move the polygon (haven't started to draw anything)
                        for patch in self.all_patches:
                            #get which patch click on 
                            if c == patch["circle"][0]: 
                                self.press = True
                                self.clicked_circle = c
                                self.clicked_point = pos
                                self.move_patch.append(patch)
                                click_on_polygon = False
                                #set back to default
 
            if not click_on_circle: #not click on any circle
                for polygon in self.polygons:
                    #check if click on polygon
                    v = get_xy_min_max(polygon.get_xy())
                    if (v[0] <= pos[0] <= v[1]) and (v[2] <= pos[1] <= v[3]):
                        click_on_polygon = True
                        try:
                            name = self.poly_info[str(polygon)]["name"]
                            attributes = self.poly_info[str(polygon)]["attributes"]
                            a = TKInputDialog(name, attributes).get()
                        #get previous value if exists
                        except:
                            a = TKInputDialog().get()   
                        #get entered poly info
                        self.poly_info[str(polygon)]  = a
                        #store polygon info
                        
            if not click_on_circle and not click_on_polygon:
                #if not click on both 
                    c = patches.Circle(pos, 7, color='blue', zorder=100) #draw a circle
                    self.circles.append(c) #add to circles
                    self.current_items["circle"].append(c) #add to current items 
                    self.ax.add_patch(c) #add to canva
                    if not self.newline: #add line start point
                        self.newline = [pos]
                    else:
                        self.current_items["line"].append(self.l) #draw linked line
                        self.newline = [pos]
                        self.l = None
            # self.show_intersections()
            click_on_circle = False
            click_on_polygon = False
            #set back to default 
            
        elif event.button == MouseButton.RIGHT:
            #right click
            #check click-on-circle event
            remove_index = []
            #the index of itmes to remove
            def dist(x, y):
                """
                Return the distance between two points.
                """
                dx = x[0] - y[0]
                dy = x[1] - y[1]
                ans = dx**2 + dy**2
                ans = ans**(0.5)
                return ans
            
            for ip, patch in enumerate(self.all_patches):
                #check every patch
                if dist(patch["circle"][0].center , pos) <= patch["circle"][0].radius:
                    remove_index.append(ip)
                    c = patch["circle"][0]
                    self.ax.patches.remove(c)
                    self.circles.remove(c)
                    #remove the circle that is clicked on 
                    for poly in patch["polygon"]:
                        self.ax.patches.remove(poly)
                        self.polygons.remove(poly) #find and delet the polygon associated with the clicked circle
                    for line in patch["line"]:
                        self.ax.lines.remove(line)
                        #find and delet the polygon associated with the clicked circle
            for i in remove_index:
                self.all_patches.pop(i)
                #remove the clicked items from all patches 
            # for i_c, c in enumerate(self.circles):
            #     ## check every exist circle 
            #     contains, attrd = c.contains(event)
            #     if contains:
            #         click_on_circle = True
            #         self.ax.patches.remove(c)
            #         self.circles.remove(c)
            #         for item in self.total_item:
            #             if c in item["c"]:
            #                 for p in item["p"]:
            #                     self.polygon.remove(p)
            #                     self.ax.patches.remove(p)
            #                 self.total_item.remove(item)
                    
    def onMove(self, event):
        if not event.xdata or not event.ydata: #click outside image
            return
        pos = (event.xdata, event.ydata)
        def dist(x, y):
            """
            Return the distance between two points.
            """
            dx = x[0] - y[0]
            dy = x[1] - y[1]
            ans = dx**2 + dy**2
            ans = ans**(0.5)
            return ans
        
        if self.press:
            #if pressed 
            self._start = True 
             ## click point (move)
            self.kayma = (pos[0] - self.clicked_point[0] , pos[1] - self.clicked_point[1])
            #get how much the mouse move
            self.clicked_point = pos[0], pos[1]
            #update the clicked pt
            for i, patch in enumerate(self.move_patch):
                for c in patch["circle"]:
                    c.set_center((c.center[0]  + self.kayma[0], c.center[1] + self.kayma[1])) 
                    #move circles
                for i_p, p in enumerate(patch["polygon"]):
                    new_ver = []
                    for vertex in p.get_xy():
                        new_position = vertex[0] + self.kayma[0], vertex[1] + self.kayma[1]
                        new_ver.append(new_position)
                    i = self.ax.patches.index(p)
                    self.ax.patches[i].set_xy(new_ver)
                    #move the polygons
                for i_l, l in enumerate(patch["line"]):
                    new_xdata = [l.get_xdata()[0] + self.kayma[0], l.get_xdata()[1] + self.kayma[0]]
                    new_ydata = [l.get_ydata()[0] + self.kayma[1], l.get_ydata()[1] + self.kayma[1]]
                    l.set_xdata(new_xdata)
                    l.set_ydata(new_ydata)
                    i = self.ax.lines.index(l)
                    self.ax.lines[i].set_xdata(new_xdata)
                    self.ax.lines[i].set_ydata(new_ydata)
                    #move the lines
                    # self.ax.figure.canvas.draw_idle()
        else:
            #if not pressed
            in_circle = False
            for i_c, c in enumerate(self.circles):
                try:
                    distance = dist(pos, c.center)
                    if distance <= c.get_radius():
                        in_circle = True
                        try:
                            self.ax.patches.remove(self.c)
                            self.c = None
                        except:
                            pass
                        self.c = patches.Circle(c.center, 7, color='red', zorder=100)
                        self.ax.add_patch(self.c)
                except:
                    pass
            #change color if pass by a circle
            if not in_circle:
                    try:
                        self.ax.patches.remove(self.c)
                        self.c = None
                    except:
                        pass
            in_circle = False    
            #move outside the circle then change color back
            if self.newline: #has start point
                try:
                    self.ax.lines.remove(self.l)
                except:
                    pass
                #Line2D https://stackoverflow.com/a/36488527/10373104
                self.l = Line2D([self.newline[0][0], pos[0]], [self.newline[0][1], pos[1]], color='red')
                self.ax.add_line(self.l)
                #drawing line features
        self.ax.figure.canvas.draw_idle() #update canvas   
        
    def release(self, event):
        #the release mouise event 
        if self.press and self._start: 
            self.press = False
            self._start = False
            self.move_patch = []
            self.clicked_point = None
            #reset 
            
    def onKyePress(self, event):
        #link keyboard with certain events
        self.leave = event.key in ['l', 'L', 'Q','q']
        # if event.key in ['y', 'Y']:
        #     self.newline = []
        #     self.l.remove()
        #     self.all_patches.append(self.current_items)
        #     self.current_items = {"circle": [], "line": [], "polygon": []}
        # self.ax.figure.canvas.draw_idle()
        if event.key in ['x', "X"]:
            dictionary = {}
            for poly in self.polygons:
                dictionary[str(poly)] = {}
                try:
                    for key in self.poly_info[str(poly)]:
                        dictionary[str(poly)][key] = self.poly_info[str(poly)][key]
                except:
                    dictionary[str(poly)]["name"] = ''
                    dictionary[str(poly)]["attributes"] = ''
                for i, x_y in enumerate(poly.get_xy()):
                    dictionary[str(poly)]["x_y" + "_" + str(i)] = x_y
            GenerateXML(dictionary, self.output_xml)
        
    def start(self):
        self.loop = True
        self.leave = False
        fig, self.ax = plt.subplots(1)
        plt.imshow(self.img[:,:,::-1]) #or self.ax.imshow(self.img[:,:,::-1])
        fig.canvas.mpl_connect('button_press_event', self.onClick)
        fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        fig.canvas.mpl_connect('key_press_event', self.onKyePress)
        fig.canvas.mpl_connect('button_release_event', self.release)            
        plt.title('press L or Q to leave\npress X to output xml file.')
        plt.get_current_fig_manager().window.showMaximized() #maximize window https://stackoverflow.com/a/18824814/10373104
        plt.show()
        #set up the screen
        # auto close version
        plt.show(block=False) #https://github.com/matplotlib/matplotlib/issues/8560/#issuecomment-397254641
        while (len(self.pts) < self.num) & self.loop :
            if self.leave:
                self.loop = False
            if cv2.waitKey(1) in [ord('q'), ord('Q'), 27]:
                return self.polygons, self.poly_info
        sleep(1)
        plt.close(fig)
        return self.polygons, self.poly_info
    
    def get_pts(self):
        return self.pts

if __name__ == "__main__":   
    def open_file():
        openfilename=fd.askopenfilename(initialdir="/",title="Select file",\
                     filetypes = [("photo files",".jpg .png"), ("video files",".mp4 .avi")])
        print(openfilename)
        #select file
        try:
            src = r""+openfilename
            flag_reset = True
            cap = cv2.VideoCapture(src)
            ret, img = cap.read()  
            points = [[[10,0],  [570,954]],
                      [[20,0],  [340,1010]],
                      [[30,0],  [247,1030]],
                      [[40,0],  [203,1043]],
                      [[50,0],  [177,1050]],
                      [[60,0],  [155,1052]],
                      [[70,0],  [147,1054]],
                      [[10,6],  [462,359]],
                      [[20,6],  [282,659]],
                      [[30,6],  [213,784]],
                      [[40,6],  [177,855]],
                      [[50,6],  [154,896]],
                      [[60,6],  [140,923]],
                      [[70,6],  [130,944]],
                      [[10,10], [396,23]],
                      [[20,10], [250,479]],
                      [[30,10], [197,642]],
                      [[40,10], [167,740]],
                      [[50,10], [145,806]],
                      [[60,10], [132,836]],
                      [[70,10], [125,865]],]
            image_points = np.array(points)[:,1,:]
            world_points = np.array(points)[:,0,:]
            path_image_npz = os.path.join(os.getcwd(),'transformer/points_image.npz')
            if os.path.exists(path_image_npz ) & ~flag_reset:
                print('read npy')
                points = np.load(path_image_npz )
                image_points, world_points = points['arr_0'], points['arr_1']
            else:
                print('redraw point')
                
                get_points = MousePointsReactor(img, len(world_points), ['x', 'y'], world_points)
                get_points.start()        
                world_points = np.array(list(points.values()))
                image_points = np.array([np.array(x) for x in points.keys()])
                np.savez(path_image_npz , image_points, world_points)
        except:
            print("檔案不存在!") 
        root.destroy()
        #close window 
    root=tk.Tk()
    root.title("檔案開啟")
    ttk.Button(root, text="開啟檔案", command=open_file).pack()          
    #open file option
    root.mainloop()
