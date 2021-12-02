import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from math import ceil
from shapely import geometry
import pickle
import time
import os


def capture(frame_count=20, input_address=0):        #frame_counter=> how many frames in total
    
    #type-in file name
    # timetup = time.localtime()
    # file_name = time.strftime('%Y%m%d%H%M%S', timetup)
    
    os.makedirs('Polygon/calibration_parameter/', exist_ok=True)
    
    counter=0
    corner_x = 7   # pattern is 7*7
    corner_y = 7
    objp = np.zeros((corner_x*corner_y, 3), np.float32)
    objp[:, :2] = np.mgrid[0:corner_x, 0:corner_y].T.reshape(-1, 2)#[0 0 0],[1 0 0],[2 0 0]........[6 6 0]
    setting = False
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.
    block = []
    del_history = []
    pic_del = 0

    cap = cv2.VideoCapture(input_address)
    start_time = time.time()
    while True:         #using infinite loop with timer to do the realtime capture and calibrate
        cur_time = time.time()
        ret, frame = cap.read()
        if setting == True and cur_time-start_time < 2.9:
            text = "{}".format(int(round( 3-(cur_time-start_time),0)) )
            cv2.putText(frame, text, (285, 270), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 2, cv2.LINE_AA)
            draw_block(frame, block, block_coverage)
        if setting == False:
            cv2.putText(frame, "setting", (260, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if cur_time-start_time > 3:
            if ret: #capture success
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, (corner_x, corner_y), None)  #find if the image have chessboard inside
                if ret == True: #chessboard is found in this frame
                    if setting == False:
                        print("! setting !")
                        _width = frame.shape[1]
                        _height = frame.shape[0]
                        img_size = (_width, _height)
                        side_num1, side_num2, block_length1, block_length2, block = show_block(_width, _height)
                        print("(width, height) = ({}, {})".format(_width, _height))
                        block_num = len(block)
                        print("side length of block = {} x {}".format(block_length1, block_length2))
                        print("number of block = {} x {} = {}".format(side_num1, side_num2, block_num))
                        block_coverage = [0]*block_num   
                        pixel = _pixel(0, _width, 0, _height)
                        init_pixel_number = len(pixel) 
                        print("number of pixel = {}".format(init_pixel_number))  # pixel_width*pixel_height=len(pixel)
                        initial_pixel = []
                        for i in range(len(block)):
                            count_pixel = check_pixel(pixel, block[i][0], block[i][1], block[i][2], block[i][3])
                            print("block {} : {}    initial pixel number : {}".format(i, block[i], count_pixel))
                            initial_pixel.append(count_pixel)
                        setting = True
                        start_time=cur_time
                        continue
                    counter += 1
                    print("capture success and chessboard is founded, {}/{}".format(counter,frame_count))
                    objpoints.append(objp)
                    imgpoints.append(corners)
                    #cv2.imwrite('./{}/output{}.jpg'.format(file_name,counter), gray)
                    #above part for finding chessboard, append points, save picture

                    imgpoints, objpoints, packed_tmp, ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp, all_error_tmp, mean_error_tmp \
                        = calculate_parameters(objpoints, imgpoints, img_size, counter-pic_del, frame_count, eliminate=False)

                    p_imgpoints = parse_imgpoints(imgpoints)    #resize from (n, 49, 1, 2) <class 'list'> to (49n, 2) <class 'list'>
                    uncovered_pixel, discard = pick_corner_find_uncovered_pixel(p_imgpoints, counter, pic_del, pixel) 
                    del_history.append(discard)

                    print("error for each frame:{}".format(all_error_tmp))
                    error_avg = np.average(all_error_tmp)
                    error_std = np.std(all_error_tmp)
                    print("average:", error_avg)     
                    print("standard:", error_std)
                    pixel = uncovered_pixel

                    if counter == 10:
                        print("check")
                        for i in range(counter-1, -1, -1):
                            if all_error_tmp[i] >= error_avg + 2*error_std:
                                imgpoints.pop(i)
                                objpoints.pop(i)
                                all_error_tmp.pop(i)
                                for j in range(len(del_history[i])):
                                    pixel.append(del_history[i][j])
                                del_history.pop(i)
                                print("delete")
                                pic_del += 1
                        print("error for each frame (deleted):{}".format(all_error_tmp))
                    if counter >10:
                        if all_error_tmp[-1] >= error_avg + 2*error_std:
                            imgpoints.pop(-1)
                            objpoints.pop(-1)
                            all_error_tmp.pop(-1)
                            for j in range(len(del_history[-1])):
                                pixel.append(del_history[-1][j])
                            del_history.pop(-1)
                            print("delete")
                            pic_del += 1
                            print("error for each frame (deleted):{}".format(all_error_tmp))
                    print("picture deleted: ", pic_del)

                    for i in range(len(block)):
                        count_pixel = check_pixel(pixel, block[i][0], block[i][1], block[i][2], block[i][3])
                        block_coverage[i] = round((initial_pixel[i]-count_pixel)/initial_pixel[i], 3)
                        #print("block {} : {}     coverage : {}/{} = {}".format(i, block[i], initial_pixel[i]-count_pixel, initial_pixel[i], block_coverage[i]))
                    pixel_num = len(pixel)
                    coverage_tmp = (init_pixel_number - pixel_num)/init_pixel_number

                    qualify = 0
                    for i in range(len(block_coverage)):
                        if block_coverage[i] > 0.3:
                            qualify += 1
                    print("block>0.3:", qualify, "/", len(block)) 
                    if counter >= 10:
                        if qualify == len(block_coverage):
                            print("\n\n end \n\n")
                            cap.release()       #release the camera
                            cv2.destroyAllWindows()
                            break
                    if counter == frame_count:  #meet the number of frames defined in the begining
                        print("\n\n end \n\n")
                        cap.release()           #release the camera
                        cv2.destroyAllWindows()
                        break
                else:
                    print("No chessboard is found in this frame")
            start_time=cur_time
            #print("\na frame will be captured in three seconds\n")

    # scatter_hist(imgpoints, _width, _height)
    fixed_param = {'img_points':imgpoints, 'ret':ret_tmp, 'mtx':mtx_tmp, 'dist':dist_tmp, 'rvecs':rvecs_tmp, 'tvecs':tvecs_tmp, \
        'error':all_error_tmp, 'mean_error':mean_error_tmp, 'block_coverage':block_coverage, 'coverage':coverage_tmp}
    #print("fixed_param:\n",fixed_param)

    return fixed_param



def open_camera_pickle(filename):
    file = open('Polygon/calibration_parameter/{}'.format(filename),'rb')
    fixed_param = pickle.load(file)
    file.close()
    return fixed_param

def get_new_calibrate_img(img, fixed_param):
    
    mtx = fixed_param['mtx']
    dist = fixed_param['dist']
    # reprojection_error = fixed_param['reprojection_error']
    # print("file name: ", file_name)
    # print(fixed_param)


    h,  w = img.shape[:2]

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    return dst

def parse_imgpoints(imgpoints):     #sub_function used by dimension statistic
    # print("before:",np.array(imgpoints).shape)
    pts = np.array(imgpoints).squeeze(axis=None)
    # print("after:",pts.shape)
    if len(imgpoints) == 1:
        a = 1
        b, _ = pts.shape
    else:
        a, b, _ = pts.shape
    pts = np.resize(pts,(a*b,2)).tolist()    #resize to the format we want
    # print(np.array(pts))
    # print(type(pts))
    return pts

"""
#use parameters to calculate reprojection error
def cal_reproject_error(imgpoints, objpoints, rvecs, tvecs, mtx, dist):
    sum_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        sum_error += error
    #print( "reprojection error: {}".format(sum_error/len(objpoints)))
    reprojection_error = sum_error/len(objpoints)
    return reprojection_error
"""

#use frames to calculate every parameters
def calculate_parameters(objpoints, imgpoints, img_size, cur_count, total, eliminate=False):
    #reprojection_error = None
    packed_tmp = ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp = cv2.calibrateCamera(objpoints[:], imgpoints[:], 
                                                                                        img_size, None, None)
    all_error_tmp=[]
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs_tmp[i], tvecs_tmp[i], mtx_tmp, dist_tmp)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        all_error_tmp.append(error) # all_error: 由每張frame各自的error所組成的array

    mean_error_tmp = sum(all_error_tmp)/len(all_error_tmp)

    return imgpoints[:], objpoints[:], packed_tmp, ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp, all_error_tmp, mean_error_tmp


def _pixel(_wid0th, _width, _hei0ght, _height):
    spacing = 2
    pixel_width = math.floor(((_width-_wid0th)+spacing/2)/spacing) 
    pixel_height = math.floor(((_height-_hei0ght)+spacing/2)/spacing)
    pixel=[]
    for m in range(pixel_width):
        for n in range(pixel_height):
            pixel.append([(m+0.5)*spacing+_wid0th, (n+0.5)*spacing+_hei0ght])
    #print(np.shape(pixel), len(pixel))  #(3072, 2) 3072
    return pixel

def check_pixel(pixel, x_left, x_right, y_top, y_bot):
    counter = 0
    for i in range(len(pixel)):
        if (pixel[i][0] > x_left) and (pixel[i][0] < x_right) and (pixel[i][1] > y_top) and (pixel[i][1] <y_bot):
            counter += 1
    return counter

def pick_corner_find_uncovered_pixel(p_imgpoints, counter, t, pixel):
    all_corner = []
    save_discard = []
    for i in range(counter - t):
        all_corner.append( [p_imgpoints[0+49*i], p_imgpoints[6+49*i], p_imgpoints[48+49*i], p_imgpoints[42+49*i]] )
    poly = all_corner[-1]
    line = geometry.LineString(poly)
    polygon = geometry.Polygon(line)
    for k in range(len(pixel)):
        point= geometry.Point(pixel[k])
        if polygon.contains(point) == True:
            save_discard.append(pixel[k])
            pixel[k] = -1
    new_pixel = []
    for n in range(len(pixel)):
        if pixel[n] != -1:
            new_pixel.append(pixel[n])
            
    return new_pixel, save_discard      #這裡的new_pixel為還沒被任何一張覆蓋的pixel, save_discard為這張照片所覆蓋的pixel

def show_block(_width, _height):
    side_num1 = 4                                      #長邊(預設x)切成幾塊
    block_length1 = max(_width, _height)//side_num1 
    side_num2 = min(_width, _height)//block_length1+1  #短邊(預設y)切成幾塊
    block_length2 = min(_width, _height)//side_num2
    if _width < _height:
        hold_num = side_num1
        hold_length = block_length1
        side_num1 = side_num2
        block_length1 = block_length2
        side_num2 = hold_num
        block_length2 = hold_length

    block=[]
    for k in range(side_num2):
        for l in range(side_num1):
            if l == side_num1-1 and k == side_num2-1:
                block.append([l*block_length1, _width, k*block_length2, _height])
            elif l == side_num1-1:
                block.append([l*block_length1, _width, k*block_length2, (k+1)*block_length2])
            elif k == side_num2-1:
                block.append([l*block_length1, (l+1)*block_length1, k*block_length2, _height])
            else:
                block.append([l*block_length1, (l+1)*block_length1, k*block_length2, (k+1)*block_length2]) #append([x左,x右,y上,y下])
    #print('block[x左,x右,y上,y下]: ', block)    #由左至右由上至下
    return side_num1, side_num2, block_length1, block_length2, block


def scatter_hist(imgpoints, _width, _height, inverse=True): #draw the scatter graph using imgpoints
    pt = parse_imgpoints(imgpoints)
    x = []
    y = []
    values = []
    for item in pt:
        _x, _y = item
        x.append(_x)
        y.append(_y)

    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom+height+spacing, width, 0.2]
    rect_histy = [left+width+spacing, bottom, 0.2, height]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes(rect_scatter,xlim=(0, width),ylim=(0, height))     #axe is a sub-area in figure.
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    ax.set_xlim(0, _width)
    ax.set_ylim(0, _height)
    if inverse:     #due to the different coordinate between images and 2-D coordinate(mainly on Y axis), we have to inverse y axis to get the correct result
        ax.invert_yaxis()
    # the scatter plot:
    ax.scatter(x, y)

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth)+1) * binwidth

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')
    plt.show()

def draw_block(frame, block, block_cover):
    for i in range(len(block)):
        if block_cover[i] < 0.3:
            cv2.rectangle(frame, (block[i][0], block[i][3]), (block[i][1], block[i][2]), color = (0, 0, 255), thickness = 1)
        else:
            cv2.rectangle(frame, (block[i][0], block[i][3]), (block[i][1], block[i][2]), color = (0, 255, 0), thickness = 2)


def set_font_size(dpi, height, width):
    """
    In order to perform different font size under different resolutions and DPIs.

    Params : 
        [float] dpi : Zoom level. The user has set in the os preferences.
        [int] height : User-set resolution height. The user has set in the os preferences.
        [int] width : User-set resolution width. The user has set in the os preferences.
        
    Return :
        [int] basicSize : The sys basic font size.

    """
    print("Set font size...")
    basicSize = 20
    dpiF = dpi / 96.0
    # dpi never less than 1
    if dpiF > 1.0 :
        basicSize = basicSize // dpiF
    if height <= 900 :
        basicSize = basicSize - 2
    if width < 1500 :
        basicSize = basicSize - 2
    if height >= 1080 or width >= 1920:
        basicSize = basicSize + 2
    if width >= 2440 :
        basicSize = basicSize + 3
    print("Basic Font Sie: ", basicSize)
    return int(basicSize)

def set_pyplot_marker_size(markerSize, args, fig, ax):
    """
    Set marker size after scrolling.

    Params : 
        [float] markerSize : Zoom level. The user has set in the os preferences.
        [dict] args : The pyplot-related data saved at the beginning.
        [object] fig : The object of matplotlib.figure.Figure storing the top level container for all the plot elements.
        [object] ax : The object of matplotlib.axes._subplots.AxesSubplot.
        
    Return :
        [float] markerSize : The marker size after scrolling.
        [dict] args : Update scale value after scrolling.
    
    src: 
        https://stackoverflow.com/questions/48474699/marker-size-alpha-scaling-with-window-size-zoom-in-plot-scatter
        
    """
    fw = fig.get_figwidth()
    fh = fig.get_figheight()
    fac1 = min(fw/args['figw'], fh/args['figh'])

    xl = ax.get_xlim()
    yl = ax.get_ylim()
    fac2 = min(
        abs(args['xlim'][1]-args['xlim'][0])/abs(xl[1]-xl[0]),
        abs(args['ylim'][1]-args['ylim'][0])/abs(yl[1]-yl[0])
    )

    ##factor for marker size
    facS = (fac1*fac2)/args['scale']

    markerSize = markerSize*facS
    
    args['scale'] *= facS

    return markerSize, args
