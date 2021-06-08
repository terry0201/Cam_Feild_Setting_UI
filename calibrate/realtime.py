import cv2
from time import sleep,time
import os
import numpy as np

def cal_reproject_error(imgpoints,objpoints,rvecs,tvecs,mtx,dist):
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "calibrate finished, loss: {}".format(mean_error/len(objpoints)) )


def capture(frame_count=30):
    counter=0
    corner_x = 7   # pattern is 7*7
    corner_y = 7
    objp = np.zeros((corner_x*corner_y, 3), np.float32)
    objp[:, :2] = np.mgrid[0:corner_x, 0:corner_y].T.reshape(-1, 2)
    zero_arr = np.zeros(1)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d points in real world space
    imgpoints = [] # 2d points in image plane.

    cap = cv2.VideoCapture(0)

    start_time = time()
    print("a frame will be captured in three seconds")
    while True:
        cur_time = time()
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # 若按下 q 鍵則離開迴圈
            break
        if cur_time - start_time > 3:
            #start_time=cur_time
            if ret:
                print("capture success")
                counter += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, (corner_x, corner_y), None)
                if ret == True:
                    print("chessboard is founded")
                    objpoints.append(objp)
                    corners_with_three_d = np.c_[corners , np.zeros((49, 1, 1))]  # append zero to last dimension
                    imgpoints.append(corners)   # only one point?
                    #above part for find chessboard
                    img_size = (frame.shape[1], frame.shape[0])
                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
                    Vr = np.array(rvecs)
                    Tr = np.array(tvecs)
                    extrinsics = np.concatenate((Vr, Tr), axis=1).reshape(-1, 6)


                    #following part are used for undistort

                    h,  w = frame.shape[:2]
                    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
                    cal_reproject_error(imgpoints,objpoints,rvecs,tvecs,mtx,dist)



                if counter == frame_count:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            start_time=cur_time
            print("a frame will be captured in three seconds")
    cap.release()


if __name__ == '__main__':
  capture()
  
  cv2.destroyAllWindows()


  # 關閉所有 OpenCV 視窗
  #cv2.destroyAllWindows()
