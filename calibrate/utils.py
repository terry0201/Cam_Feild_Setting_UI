import cv2
import numpy as np
from math import ceil
import matplotlib.pyplot as plt


def cal_reproject_error(imgpoints,objpoints,rvecs,tvecs,mtx,dist):  #calculate the reprojection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    #print( "total error: {}".format(mean_error/len(objpoints)) )
    return mean_error/len(objpoints)


"""
21
34
"""
def parse_imgpoints(imgpoints):     #sub_function used by dimension statistic
    pts=np.array(imgpoints).squeeze(axis=None)
    a,b,_ = pts.shape
    pts = np.resize(pts,(a*b,2)).tolist()    #resize to the format we want
    return pts

def dim_statistic(imgpoints,img_width,img_height):  #count the points with respect to four dimension
    half_width,half_height = img_height/2, img_height/2
    pts = parse_imgpoints(imgpoints)
    dim_list=np.zeros(shape=4,dtype=np.int8).tolist()   #divide into four dimension
    for item in pts:
        x,y = item
        if x > half_width and y > half_height:  #dim4
            dim_list[3] += 1
        elif x < half_width and y > half_height: #dim3
            dim_list[2] += 1
        elif x < half_width and y < half_height: #dim2
            dim_list[1] += 1
        elif x > half_width and y < half_height: #dim1
            dim_list[0] += 1
    _str='左上:{left_top}, 右上:{right_top}, 左下:{left_bottom}, 右下:{right_bottom}'.format(left_top=dim_list[1], right_top=dim_list[0],left_bottom=dim_list[2],right_bottom=dim_list[3])
    print(_str) 
    return 

def dim_stat_xy(imgpoints,img_width,img_height,div_num=10):    #project the points into x and y axis and do the further counting. Counting the distribution among x and y axis
    pts = parse_imgpoints(imgpoints)
    x_list , y_list = np.zeros(shape=div_num,dtype=np.int8).tolist() , np.zeros(shape=div_num,dtype=np.int8).tolist()
    width_per_div , height_per_div = ceil(img_width/div_num) , ceil(img_height/div_num)
    for item in pts:
        x,y = item
        x_list[int(x/width_per_div)] += 1
        y_list[int(y/height_per_div)] += 1  
    print("x axis(left to right):{}".format(str(x_list)))
    print("y axis(top to bottom): {}".format(str(y_list)))
    return


def sliding_window_calibrate(objpoints,imgpoints,img_size,cur_count,total): #if the newest data helps better performance, then discard the first. On the contary
    packed_tmp = ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp = cv2.calibrateCamera(objpoints[:], imgpoints[:], img_size, None, None)  #using 1~last as new dataset, eliminate the first entry
    packed_ori = ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints[:len(objpoints)-1], imgpoints[:len(imgpoints)-1], img_size, None, None)   #using 0~last-1
    ori = cal_reproject_error(imgpoints[:len(imgpoints)-1],objpoints[:len(objpoints)-1],rvecs,tvecs,mtx,dist)
    slided = cal_reproject_error(imgpoints[:],objpoints[:],rvecs_tmp,tvecs_tmp,mtx_tmp,dist_tmp)

    if ori < slided:
        print('new data doesn\'t help, eliminate it')
        return packed_ori + (imgpoints[:len(imgpoints)-1], objpoints[:len(objpoints)-1],ori)
    else:
        print("new data helps, add it to dataset")
        return packed_tmp + (imgpoints[:], objpoints[:],slided)
    #return ret, mtx, dist, rvecs, tvecs


def scatter_hist(imgpoints,_width,_height): #draw the scatter graph using imgpoints
    pt = parse_imgpoints(imgpoints)
    x=[]
    y=[]
    for item in pt:
        _x,_y = item
        x.append(_x)
        y.append(_y)

    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005


    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_axes(rect_scatter,xlim=(0,width),ylim=(0,height))     #axe is a sub-area in figure.
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    ax.set_xlim(0,_width)
    ax.set_ylim(0,_height)
    # the scatter plot:
    ax.scatter(x, y)

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')
    plt.show()
