import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from math import ceil
from shapely import geometry
import pickle
import cv2
import time
import os


def capture(frame_count=8, input_address=0):        #frame_counter=> how many frames in total
    
    #type-in file name
    timetup = time.localtime()
    file_name = time.strftime('%Y%m%d%H%M%S', timetup)
    
    os.makedirs('Polygon/calibration_parameter/{}'.format(file_name), exist_ok=True)
    
    counter=0
    corner_x = 7   # pattern is 7*7
    corner_y = 7
    objp = np.zeros((corner_x*corner_y, 3), np.float32)
    objp[:, :2] = np.mgrid[0:corner_x, 0:corner_y].T.reshape(-1, 2)#[0 0 0],[1 0 0],[2 0 0]........[6 6 0]
    _width = 0
    _height = 0
    setting = 0

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    cap = cv2.VideoCapture(input_address)

    start_time = time.time()
    print("a frame will be captured in three seconds")
    while True:         #using infinite loop with timer to do the realtime capture and calibrate
        cur_time = time.time()
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if cur_time-start_time > 3:
            if ret: #capture success
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, (corner_x, corner_y), None)  #find if the image have chessboard inside
                if ret == True: #chessboard is found in this frame
                    counter += 1
                    print("capture success and chessboard is founded, {}/{}".format(counter,frame_count))
                    objpoints.append(objp)
                    imgpoints.append(corners)
                    cv2.imwrite('Polygon/calibration_parameter/{}/output{}.jpg'.format(file_name, counter), gray)
                    #above part for finding chessboard, append points, save picture

                    if setting == 0:
                        print("! setting !")
                        _width = frame.shape[1]
                        _height = frame.shape[0]
                        img_size = (_width, _height)
                        side_num1, side_num2, block_length1, block_length2, block = show_block(_width, _height)
                        print("(width, height) = ({}, {})".format(_width, _height))
                        block_num = side_num1*side_num2
                        print("side length of block = {} x {}".format(block_length1, block_length2))
                        print("number of block = {} x {} = {}".format(side_num1, side_num2, block_num))
                        #print("block[x左,x右,y上,y下]: ", block)    
                        pixel = _pixel(_width, _height)
                        pixel_number = len(pixel)   #trim
                        print("number of pixel = {}".format(len(pixel)))  # pixel_width*pixel_height=len(pixel)
                        initial_pixel = []
                        for i in range(len(block)):
                            count_pixel = check_pixel(pixel, block[i][0], block[i][1], block[i][2], block[i][3])
                            print("block {} : {}    initial pixel number : {}".format(i, block[i], count_pixel))
                            initial_pixel.append(count_pixel)
                        setting = 1
                    
                    imgpoints, objpoints, packed_tmp, ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp, all_error_tmp, reprojection_error_tmp \
                        = calculate_parameters(objpoints, imgpoints, img_size, counter, frame_count, eliminate=False)
                    if counter>=2:
                        p_imgpoints = parse_imgpoints(imgpoints)    #resize from (n, 49, 1, 2) <class 'list'> to (49n, 2) <class 'list'>
                        all_corner, uncovered_pixel = pick_corner_find_uncovered_pixel(p_imgpoints, counter, pixel)
                        #print("imgpoints:\n{}".format(imgpoints))   
                        #print(np.shape(imgpoints), type(imgpoints))    #(2, 49, 1, 2)
                        #print("p_imgpoints:\n{}".format(p_imgpoints))   
                        #print(np.shape(p_imgpoints), type(p_imgpoints))    #(98, 2)

                        #print("ret_tmp:{}\n mtx_tmp:\n{}\n dist_tmp:\n{}\n rvecs_tmp:\n{}\n tvecs_tmp:\n{}".format(ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp))
                        print("error for each frame:{}".format(all_error_tmp))
                        print("reprojection_error:{}".format(reprojection_error_tmp))
                        
                        for i in range(len(block)):
                            count_pixel = check_pixel(uncovered_pixel, block[i][0], block[i][1], block[i][2], block[i][3])
                            print("block {} : {}     coverage : {}/{} = {}".format(i, block[i], initial_pixel[i]-count_pixel, initial_pixel[i], round((initial_pixel[i]-count_pixel)/initial_pixel[i], 3)))

                        #print(all_corner)
                        uncovered_pixel_num = len(uncovered_pixel)
                        coverage_tmp = (pixel_number-uncovered_pixel_num)/pixel_number
                        #print("uncovered pixel number: {}".format(uncovered_pixel_num))
                        print("整體覆蓋率: {}".format(coverage_tmp))
                        pixel = uncovered_pixel
                        nosample_block_tmp = no_sample_block(block, imgpoints)
                else:
                    print("No chessboard is found in this frame")
                
                #print("相機資料數(imgpoints):",len(imgpoints))
                #print("空間資料數(objpoints):",len(objpoints))
                
                """ 
                if counter>3:
                    nosample = no_sample_block(_width, _height, imgpoints)
                
                    if len(nosample) == 0:
                        print('final error:',err)
                        cv2.destroyAllWindows()
                        break
                """
                if counter == frame_count:  #meet the number of frames defined in the begining
                    print("\n\n end \n\n")
                    cap.release()           #release the camera
                    cv2.destroyAllWindows()
                    break
            
            start_time=cur_time
            print("\na frame will be captured in three seconds\n")

    # scatter_hist(imgpoints, _width, _height)
    fixed_param = {'ret':ret_tmp, 'mtx': mtx_tmp, 'dist': dist_tmp, 'rvecs':rvecs_tmp, 'tvecs':tvecs_tmp,
     'error':all_error_tmp, 'reprojection error': reprojection_error_tmp, 
     'pixel number': pixel_number, 'uncovered pixel number': uncovered_pixel_num, 'coverage': coverage_tmp
     , 'no sample block': nosample_block_tmp, 'no sample block number': len(nosample_block_tmp)}
    
    return fixed_param
    #print("fixed_param:\n",fixed_param)
    # file = open('Polygon/calibration_parameter/{}.pickle'.format(file_name),'wb')
    # pickle.dump(fixed_param,file)   #save parameters
    # file.close()


def open_camera_pickle(filename):
    file = open('Polygon/calibration_parameter/{}'.format(filename),'rb')
    fixed_param = pickle.load(file)
    file.close()
    return fixed_param

def get_new_calibrate_img(img, fixed_param):
    
    mtx = fixed_param['mtx']
    dist = fixed_param['dist']
    # reprojection_error = fixed_param['reprojection error']
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
    a, b, _ = pts.shape
    pts = np.resize(pts,(a*b,2)).tolist()    #resize to the format we want
    # print(np.array(pts))
    # print(type(pts))
    return pts


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

#use frames to calculate every parameters
def calculate_parameters(objpoints, imgpoints, img_size, cur_count, total, eliminate=False):
    #reprojection_error = None
    packed_tmp = ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp = cv2.calibrateCamera(objpoints[:], imgpoints[:], #using 1~last as new dataset, eliminate the first entry
                                                                                        img_size, None, None)
    all_error_tmp=[]
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs_tmp[i], tvecs_tmp[i], mtx_tmp, dist_tmp)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        all_error_tmp.append(error) # all_error: 由每張frame各自的error所組成的array

    reprojection_error_tmp = sum(all_error_tmp)/len(all_error_tmp)

    return imgpoints[:], objpoints[:], packed_tmp, ret_tmp, mtx_tmp, dist_tmp, rvecs_tmp, tvecs_tmp, all_error_tmp, reprojection_error_tmp

def _pixel(_width, _height):
    spacing = 4
    pixel_width = math.floor((_width+spacing/2)/spacing) 
    pixel_height = math.floor((_height+spacing/2)/spacing)
    pixel=[]
    for m in range(pixel_width):
        for n in range(pixel_height):
            pixel.append([(m+0.5)*spacing, (n+0.5)*spacing])
    #print(np.shape(pixel), len(pixel))  #(3072, 2) 3072
    return pixel

def check_pixel(pixel, x_left, x_right, y_top, y_bot):
    counter = 0
    for i in range(len(pixel)):
        if (pixel[i][0] > x_left) and (pixel[i][0] < x_right) and (pixel[i][1] > y_top) and (pixel[i][1] <y_bot):
            counter += 1
    return counter

def pick_corner_find_uncovered_pixel(p_imgpoints, counter, pixel):
    all_corner = []
    for i in range(counter):
        all_corner.append( [p_imgpoints[0+49*i], p_imgpoints[6+49*i], p_imgpoints[48+49*i], p_imgpoints[42+49*i]] )
    
    poly = all_corner[counter-1]
    line = geometry.LineString(poly)
    polygon = geometry.Polygon(line)
    for k in range(len(pixel)):
        point= geometry.Point(pixel[k])
        if polygon.contains(point) == True:
            pixel[k] = -1
    new_pixel = []
    for n in range(len(pixel)):
        if pixel[n] != -1:
            new_pixel.append(pixel[n])
    
    if counter==2:
        pixel = new_pixel
        poly = all_corner[0]
        line = geometry.LineString(poly)
        polygon = geometry.Polygon(line)
        for k in range(len(pixel)):
            point= geometry.Point(pixel[k])
            if polygon.contains(point) == True:
                pixel[k] = -1
        new_pixel = []
        for n in range(len(pixel)):
            if pixel[n] != -1:
                new_pixel.append(pixel[n])        
    
    return all_corner, new_pixel

def show_block(_width, _height):
    side_num1 = 6                                      #長邊(預設x)切成幾塊
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


def no_sample_block(block, imgpoints):
    pts = parse_imgpoints(imgpoints)
    dot_num = len(pts)
    nosample=[]
    for m in range(len(block)):
        c=0     #count
        for n in range(dot_num):
            if pts[n][0]>=block[m][0] and pts[n][0]<=block[m][1] and pts[n][1]>=block[m][2] and pts[n][1]<=block[m][3]:   #a[n,0]=x值 a[n,1]=y值
                break
            else:
                c+=1
        if c == dot_num:    #no dot in this block
            nosample.append(block[m])
        else:
            continue
    
    print('nosample block[x左,x右,y上,y下]: ', nosample)
    print('number of nosample block: ', len(nosample)) 
    return nosample


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
