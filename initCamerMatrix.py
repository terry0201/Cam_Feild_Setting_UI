# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:21:19 2019

@author: ystseng
"""

import numpy as np
import cv2
import glob
import time
import matplotlib.pyplot as plt

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)

#add 2.5 to account for 2.5 cm per square in grid
objp[:,:2] = np.mgrid[0:6,0:9].T.reshape(-1,2)*2.5




#%% A.read video stream
win_name='initaial camermatrix'
#cap = cv2.VideoCapture("rtsp://III-EITS:Iii12345678@10.22.22.150/MediaInput/h265")
# cap = cv2.VideoCapture("rtsp://III-EITS:Iii12345678@168.254.2.144/MediaInput/h265")
cap = cv2.VideoCapture("rtsp://192.168.0.100/media.amp?streamprofile=Profile1")

#%%%% a.take picture with space  key

count=0
while(1):
    ret,frame_raw = cap.read()
    if not ret:
        continue
    frame=cv2.resize(frame_raw,(1920,1080), interpolation=cv2.INTER_CUBIC)
    #    print('play')
    cv2.imshow("frame",cv2.resize(frame,(1080,720), interpolation=cv2.INTER_CUBIC))
    
    key = cv2.waitKey(1)#pauses for 3 seconds before fetching next image
    if key == 27:#if ESC is pressed, exit loop
        cv2.destroyAllWindows()
        break
    elif key ==32:
        print('shot')

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        flag_FCC=True
        while(flag_FCC):
            ret1, corners = cv2.findChessboardCorners(gray, (6,9), None)
        # If found, add object points, image points (after refining them)
            if ret1:
                
                cv2.imwrite('camera_calibration\img%d.jpg'%count, frame_raw)
                count+=1
                corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                objpoints.append(objp)
                imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(frame, (6,9), corners2, ret1)
                # cv2.imshow(win_name, frame)
                cv2.imshow(win_name,cv2.resize(frame,(1080,720), interpolation=cv2.INTER_CUBIC))
                flag_FCC=False
            else:
                continue

cv2.destroyAllWindows()
cap.release()

#%% B.varify the pictures 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('camera_calibration/*.jpg')

win_name="Verify"
cv2.namedWindow(win_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(win_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

print("getting images")
for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img,(1920,1080), interpolation=cv2.INTER_CUBIC)
    print(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (6,9), None)##77

    if ret == True:
        objpoints.append(objp)
        corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(img, (6,9), corners2, ret)
        cv2.imshow(win_name, img)
        cv2.waitKey(500)

    img1=img
    
cv2.destroyAllWindows()


#%% C.calculate crmera parameter
savedir=r'C:\GitHub\109_RadarFusion\iRSU_camera\\'
####calibrateCamera
ret, cam_mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
np.save(savedir+'cam_mtx.npy', cam_mtx)
np.save(savedir+'dist.npy', dist)

# frame = cv2.imread('C:\\GitHub\\P109_Panasonic\\C_ImageCalibration\\camera_calibration\\00.jpg')
frame = cv2.imread(r'C:\GitHub\109_EventEngine\camera_calibration\img0.jpg')
frame = cv2.resize(frame,(1920,1080), interpolation=cv2.INTER_CUBIC)
h, w = frame.shape[:2]
####getOptimalNewCameraMatrix
newcam_mtx, roi=cv2.getOptimalNewCameraMatrix(cam_mtx, dist, (w,h), 1, (w,h))
inverse = np.linalg.inv(newcam_mtx)
np.save(savedir+'roi.npy', roi)
np.save(savedir+'newcam_mtx.npy', newcam_mtx)

undst = cv2.undistort(frame, cam_mtx, dist, None, newcam_mtx)

frame_s=cv2.resize(frame,(1024,768), interpolation=cv2.INTER_CUBIC)
cv2.imshow('image', frame_s)
plt.figure();plt.imshow(frame_s[:,:,::-1])
undst_s=cv2.resize(undst,(1024,768), interpolation=cv2.INTER_CUBIC)
cv2.imshow('img1u', undst_s)
plt.figure();plt.imshow(undst_s[:,:,::-1])



plt.figure();plt.imshow(frame[:,:,::-1])
plt.figure();plt.imshow(undst[:,:,::-1])

map1, map2 = cv2.initUndistortRectifyMap(cam_mtx, dist, None, newcam_mtx, (w,h), cv2.CV_16SC2)
mapx, mapy = cv2.convertMaps(map1, map2,cv2.CV_16SC2)
plt.figure()
plt.subplot(221);plt.imshow(mapx[:,:,0])
plt.subplot(222);plt.imshow(mapx[:,:,1])
plt.subplot(223);plt.imshow(mapy[:,:])

disto2 = cv2.remap(frame, mapx, mapy, cv2.INTER_CUBIC)
plt.figure();plt.imshow(disto2[:,:,::-1])


map1[ 682, 184] 

undisto
(702-673,218-147)
undisto = cv2.undistortPoints(np.array([[682,184]], dtype=np.float32), cam_mtx, dist, None, newcam_mtx)

frame1 = frame.copy()
cv2.circle(frame1 , (682, 184), int(5), (255,255,255),-1)
plt.figure();plt.imshow(frame1[:,:,::-1])

undst1 = undst.copy()
cv2.circle(undst1 , tuple(undisto[0][0]) , int(5), (0,0,255),-1)
cv2.circle(undst1 , tuple(map1[ 184, 628] ) , int(5), (0,255,0),-1)
plt.figure();plt.imshow(undst1 [:,:,::-1])


#%%=======================Calculate Intr/Extr Parameter=========================
#%% A.load camera calibration
savedir="C:\\GitHub\\P109_Panasonic\\C_ImageCalibration\\panasonic_camera\\"
cam_mtx=np.load(savedir+'cam_mtx.npy')
dist=np.load(savedir+'dist.npy')
newcam_mtx=np.load(savedir+'newcam_mtx.npy')
inverse_newcam_mtx = np.linalg.inv(newcam_mtx)
roi=np.load(savedir+'roi.npy')

#load center points from New Camera matrix
cx=newcam_mtx[0,2]
cy=newcam_mtx[1,2]
fx=newcam_mtx[0,0]
print("cx: "+str(cx)+",cy "+str(cy)+",fx "+str(fx))

#%% B.Get real world point and image point

## 60cm
## -100cm
## 120cm
data=[[ 358,  96,   0,  0,  0],
      [ 600, 167,   1,  0,  0],
      [ 779, 220,   2,  0,  0],
      [ 912, 260,   3,  0,  0],
      [ 226, 190,   0,  1,  0],
      [ 445, 238,   1,  1,  0],
      [ 616, 274,   2,  1,  0],
      [ 749, 303,   3,  1,  0],
      [ 133, 258,   0,  2,  0],
      [ 328, 292,   1,  2,  0],
      [ 489, 315,   2,  2,  0],
      [ 622, 339,   3,  2,  0],
      [  67, 302,   0,  3,  0],
      [ 247, 326,   1,  3,  0],
      [ 395, 347,   2,  3,  0],
      [ 519, 363,   3,  3,  0],
#      [ 363, 648,   0,  0, -1.6 ],
#      [ 475, 644, 0.3,  0, -1.6 ],
#      [ 131, 623, 0.3,  3, -1.6 ],
#      [ 754, 625, 1.6,  0, -1.6 ],
#      [ 343, 616, 1.6,  3, -1.6 ],
#      [ 667, 608, 4.2,  3, -1.6 ],
#      [  18, 670,  -1,  0, -1.6 ],
#      [ 501, 610, 2.8,  3, -1.6 ],
#      [ 264, 607, 2.8,5.5, -1.6 ],
      [ 495, 436,   5,  6, 0 ],
      [ 555, 442, 5.8,  6, 0 ],
      [ 448, 459, 5.8,  8, 0 ],
      [ 690, 452,   8,  6, 0 ],
      
      ]
total_points_used=len(data)
#total_points_used=15
worldPoints = np.array([ [x[2],x[3],x[4]] for x in data[:total_points_used]]).astype('float32')
imagePoints = np.array([ [x[0],x[1]] for x in data[:total_points_used]]).astype('float32')


#%% C.calculate inter/extra matrix

ret, rvec1, tvec1=cv2.solvePnP(worldPoints,imagePoints,newcam_mtx,dist, flags=cv2.cv2.SOLVEPNP_ITERATIVE)

R_mtx, jac=cv2.Rodrigues(rvec1)
Rt=np.column_stack((R_mtx,tvec1))
P_mtx=newcam_mtx.dot(Rt)

#%%===========================Calculate project Points=================================
#%%%% case1
#detimagePoints=[]
#for i in range(0,total_points_used):
#    uv1, jco =cv2.projectPoints(worldPoints[i], rvec1, tvec1, newcam_mtx, dist) 
#    detimagePoints.append(uv1[0][0])
#%%%% case2
def W2I(worldPoints):
    XYZ1 = np.array([[worldPoints[0],worldPoints[1],worldPoints[2],1]], dtype=np.float32)
    XYZ1 = XYZ1.T
    suv1 = P_mtx.dot(XYZ1)
    s = suv1[2,0]    
    uv1 = suv1/s
    return(uv1[0:2])
    
s_arr=np.array([0], dtype=np.float32)
s_describe=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],dtype=np.float32)
detimagePoints=[]
for i in range(0,len(worldPoints)):
    XYZ1 = np.array([[worldPoints[i,0],worldPoints[i,1],worldPoints[i,2],1]], dtype=np.float32)
    XYZ1 = XYZ1.T
    suv1 = P_mtx.dot(XYZ1)
    s = suv1[2,0]    
    uv1 = suv1/s
    uv1 = uv1[0:2]
    detimagePoints.append(uv1)    
    
#%%===============================Varify==============================
#%%
img = cv2.imread('./camera_calibration/000.jpg')
img=cv2.resize(img,(1024,768), interpolation=cv2.INTER_CUBIC)
#img = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)
height, width, channels = img.shape
for ii in range(len(imagePoints)):
    cv2.circle(img,(imagePoints[ii][0],    imagePoints[ii][1]), 4, (0, 255, 255), -1)
    cv2.putText(img, '(%d)(%02.01f, %02.01f, %02.01f)'%(ii,worldPoints[ii][0],worldPoints[ii][1],worldPoints[ii][2]), (imagePoints[ii][0],    imagePoints[ii][1]), 
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
#    cv2.circle(img,(detimagePoints[ii][0], detimagePoints[ii][1]), 4, (255, 0, 255), -1)
#    cv2.putText(img, '(%d)'%(ii), (detimagePoints[ii][0],    detimagePoints[ii][1]), 
#                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
cv2.imshow('image',img)

#%%    
img = cv2.imread('./camera_calibration/000.jpg')
img=cv2.resize(img,(1024,768), interpolation=cv2.INTER_CUBIC)
#img = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)
height, width, channels = img.shape
for ii in range(len(imagePoints)):
    cv2.circle(img,(imagePoints[ii][0],    imagePoints[ii][1]), 4, (0, 255, 255), -1)
    cv2.putText(img, '(%d)(%02.01f, %02.01f, %02.01f)'%(ii,worldPoints[ii][0],worldPoints[ii][1],worldPoints[ii][2]), (imagePoints[ii][0],    imagePoints[ii][1]), 
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.circle(img,(detimagePoints[ii][0], detimagePoints[ii][1]), 4, (255, 0, 255), -1)
    cv2.putText(img, '(%d)'%(ii), (detimagePoints[ii][0],    detimagePoints[ii][1]), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('det',img)


#%%
img = cv2.imread('./camera_calibration/000.jpg')
img=cv2.resize(img,(1024,768), interpolation=cv2.INTER_CUBIC)
#img = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)
height, width, channels = img.shape
for ii in range(len(imagePoints)):
    cv2.circle(img,(imagePoints[ii][0],    imagePoints[ii][1]), 4, (0, 255, 255), -1)
    cv2.putText(img, '(%d)(%02.01f, %02.01f, %02.01f)'%(ii,worldPoints[ii][0],worldPoints[ii][1],worldPoints[ii][2]), (imagePoints[ii][0],    imagePoints[ii][1]), 
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.circle(img,(detimagePoints[ii][0], detimagePoints[ii][1]), 4, (255, 0, 255), -1)
    cv2.putText(img, '(%d)'%(ii), (detimagePoints[ii][0],    detimagePoints[ii][1]), 
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('imageori',img)
    uv_1  = np.array([[imagePoints[i,0],imagePoints[i,1],1]], dtype=np.float32)
    uv_1  = uv_1.T
    suv_1 = s*uv_1
    xyz_c = inverse_newcam_mtx.dot(suv_1)
    xyz_c = xyz_c-tvec1
    inverse_R_mtx = np.linalg.inv(R_mtx)
    XYZ = inverse_R_mtx.dot(xyz_c)

