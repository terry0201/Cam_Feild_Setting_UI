import cv2
import numpy as np
from math import ceil

def cal_reproject_error(imgpoints,objpoints,rvecs,tvecs,mtx,dist):  #calculate the reprojection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(objpoints)) )
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
    packed_tmp = ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp = cv2.calibrateCamera(objpoints[1:], imgpoints[1:], img_size, None, None)  #using 1~last as new dataset, eliminate the first entry
    packed_pri = ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints[:len(objpoints)-1], imgpoints[:len(imgpoints)-1], img_size, None, None)   #using 0~last-1
    ori = cal_reproject_error(imgpoints[:len(imgpoints)-1],objpoints[:len(objpoints)-1],rvecs,tvecs,mtx,dist)
    slided = cal_reproject_error(imgpoints[1:],objpoints[1:],rvecs_tmp,tvecs_tmp,mtx_tmp,dist_tmp)

    if ori < slided:
        print('original data is better\n')
        return packed_pri + (imgpoints[:len(imgpoints)-1], objpoints[:len(objpoints)-1])
    else:
        print("new data is better, eliminate the oldest one\n")
        return packed_tmp + (imgpoints[1:], objpoints[1:])
    #return ret, mtx, dist, rvecs, tvecs