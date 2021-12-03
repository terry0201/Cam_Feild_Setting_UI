from shapely.geometry import Polygon
from shapely.geometry import Point
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2
import shutil
from TEST_XML import xml2dict
import random

def detect_object_in_polygon(img_size,image_path,image_report_path,yolov5_point_dict,min_inter_area_ratio):
    
    # Display the bounding box and handcraft pologon through Matplotlib. 
    #---------------------------------
    #orangered --> bicycle
    #lime --> car
    #blue --> motorcycle
    #red --> bus
    #darkviolet --> train
    #peru --> truck
    #---------------------------------

    queryDict = np.load('./Test/TEST_dectect.npy',allow_pickle='TRUE').item()
    # print("queryDict:",queryDict)
    report_content = []
    
    Total_Label = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 
    'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    
    Car_Label_name = ['bicycle', 'car', 'motorcycle', 'bus', 'train', 'truck']
    Car_Label_color = ['orangered', 'lime', 'blue', 'red', 'darkviolet', 'peru']
    Car_name_color_dict = dict(zip(Car_Label_name,Car_Label_color))

    image_name = list(yolov5_point_dict.keys())[0]

    # print(yolov5_point_dict)
    # print("queryDict:", queryDict.keys())
    # print("queryDict['Bus']:",queryDict['Bus'])
    # print('Bus'.lower() in Car_Label_name)

    fig = plt.figure(figsize=(64,16))
    ax = fig.gca()
    for hand_polygon in list(queryDict.keys()):

        if hand_polygon.lower() in Car_Label_name:
            
            # human polygon point by 淨云畫的
            # handcraft_polygon = [(random.randint(0,img_size[1]),random.randint(0,img_size[0])) for x in range(10)]
            handcraft_polygon = list(map(tuple, queryDict[hand_polygon]))
            

            # print("handcraft_polygon:", handcraft_polygon)
        
            # handcraft polygon draw  
            handcraft_polygon = Polygon(handcraft_polygon).convex_hull
            handcraft_polygonX, handcraft_polygonY = handcraft_polygon.exterior.xy
            ax.plot(handcraft_polygonX, handcraft_polygonY, linewidth = 3, label = hand_polygon+' handcraft polygon')

            for index, bounding_box in enumerate(yolov5_point_dict[image_name]):
                object_polygon = Polygon([(bounding_box[0], bounding_box[1]), (bounding_box[0], bounding_box[3]), (bounding_box[2], bounding_box[1]),(bounding_box[2], bounding_box[3])]).convex_hull
                
                object_polygon_center_point = list(object_polygon.centroid.coords)
                object_polygon_center_point = Point(object_polygon_center_point)


                object_polygonX,object_polygonY = object_polygon.exterior.xy

                ax.plot(object_polygonX, object_polygonY, linewidth=3, color = Car_name_color_dict[Total_Label[bounding_box[4]]], label = Total_Label[bounding_box[4]])

                if not object_polygon.intersection(handcraft_polygon):
                    inter_area = 0 
                else:
                    inter_area = object_polygon.intersection(handcraft_polygon).area
                    # inter_area = inter_area/(img_size[0]*img_size[1])
                
 
                inter_area_ratio = inter_area/object_polygon.area

                if  (inter_area_ratio > min_inter_area_ratio) and handcraft_polygon.contains(object_polygon_center_point):
                    report_content.append([hand_polygon,Total_Label[bounding_box[4]],handcraft_polygon.area,object_polygon.area,inter_area,handcraft_polygon.contains(object_polygon_center_point),inter_area/handcraft_polygon.area,inter_area/object_polygon.area])
                    print("handcraft polygon {"+hand_polygon+"} area:", handcraft_polygon.area)
                    print("object polygon {"+Total_Label[bounding_box[4]]+"} area:", object_polygon.area)
                    print("object polygon center point {"+Total_Label[bounding_box[4]]+"} is in the handcraft region:", handcraft_polygon.contains(object_polygon_center_point))
                    print("handcraft polygon {"+hand_polygon+"} with object polygon {"+Total_Label[bounding_box[4]]+"} intersection area:", inter_area)
                    print("handcraft polygon {"+hand_polygon+"} with intersection area ratio:",inter_area/handcraft_polygon.area)
                    print("object polygon {"+Total_Label[bounding_box[4]]+"} with intersection area ratio:",inter_area/object_polygon.area)
                    print()

        else:
            print("It's not the car related label.")
        
    hand, labl = ax.get_legend_handles_labels()
    handout=[]
    lablout=[]
    for h,l in zip(hand,labl):
        if l not in lablout:
            lablout.append(l)
            handout.append(h)

    plt.title(image_name,fontsize=40)
    plt.xlabel("width",fontsize=40)
    plt.ylabel("height",fontsize=40)
    plt.xticks(fontsize=30)
    plt.xlim(0,img_size[1])
    plt.yticks(fontsize=30)
    plt.ylim(0,img_size[0])
    ax.legend(handout, lablout, loc=(1,0), fontsize=30)
    plt.grid(True)
    plt.savefig(image_path+image_name[:-4]+"_result.png")
    plt.close()
    
    polygon_report_content = pd.DataFrame(report_content,columns=['手繪框的Label','偵測物件框的Label','手繪框的面積','偵測物件框的面積','交集面積大小','偵測物件中心點是否有在手繪框裡面?','交集面積占手繪框面積的比率','交集面積占偵測物件框面積的比率'])
    polygon_report_content.to_csv(image_report_path+image_name[:-4]+'.csv',encoding='utf-8-sig')

def draw_handcraft_to_image(image, queryDict, line_thickness=3):

    # queryDict = np.load('./Test/TEST_dectect.npy', allow_pickle='TRUE').item()
    # queryDict = xml2dict('TEST.xml')
    Car_Label_name = ['bicycle', 'car', 'motorcycle', 'bus', 'train', 'truck']

    for hand_polygon in list(queryDict.keys()):
        #draw handcraft
        color = tuple(random.randint(0, 255) for _ in range(3))
        color = (29, 248, 63)
        # print("type:", type(queryDict[hand_polygon]), "queryDict[hand_polygon]:", queryDict[hand_polygon])
        points = np.array(queryDict[hand_polygon]).astype(np.int32)
        cv2.polylines(image, pts=[points], isClosed=True, color=color, thickness=line_thickness+10)
        # if hand_polygon.lower() in Car_Label_name:

def judge_object_in_handcraft(x, queryDict, min_inter_area_ratio):
    
    # queryDict = np.load('./Test/TEST_dectect.npy',allow_pickle='TRUE').item()

    Car_Label_name = ['bicycle', 'car', 'motorcycle', 'bus', 'train', 'truck']
    check = False

    for hand_polygon in list(queryDict.keys()):

        # if hand_polygon.lower() in Car_Label_name:
        handcraft_polygon = list(map(tuple, queryDict[hand_polygon]))
        handcraft_polygon = Polygon(handcraft_polygon).convex_hull

        object_polygon = Polygon([(x[0], x[1]), (x[0], x[3]), (x[2], x[1]),(x[2], x[3])]).convex_hull
        object_polygon_center_point = list(object_polygon.centroid.coords)
        object_polygon_center_point = Point(object_polygon_center_point)

        if not object_polygon.intersection(handcraft_polygon):
            inter_area = 0 
        else:
            inter_area = object_polygon.intersection(handcraft_polygon).area
        
        inter_area_ratio = inter_area/object_polygon.area
        if  (inter_area_ratio > min_inter_area_ratio) and handcraft_polygon.contains(object_polygon_center_point):
            check = True
    
    return check