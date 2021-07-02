import cv2
from time import sleep,time
import os
import numpy as np
from utils import cal_reproject_error, dim_statistic, dim_stat_xy, sliding_window_calibrate, scatter_hist

def capture(frame_count=20):
    counter=0
    corner_x = 7   # pattern is 7*7
    corner_y = 7
    objp = np.zeros((corner_x*corner_y, 3), np.float32)
    objp[:, :2] = np.mgrid[0:corner_x, 0:corner_y].T.reshape(-1, 2)#[0 0 0],[1 0 0],[2 0 0]........[6 6 0]

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
            if ret: #capture success
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, (corner_x, corner_y), None)
                if ret == True:
                    counter += 1
                    print("capture success and chessboard is founded, {}/{}".format(counter,frame_count))
                    objpoints.append(objp)
                    #corners_with_three_d = np.c_[corners , np.zeros((49, 1, 1))]  # append zero to last dimension
                    imgpoints.append(corners)  
                    #above part for finding chessboard
                    img_size = (frame.shape[1], frame.shape[0])

                    if counter>10:  #choosing when to do the sliding window
                        ret, mtx, dist, rvecs, tvecs, imgpoints, objpoints, err = sliding_window_calibrate(objpoints, imgpoints, img_size, counter, frame_count)
                    else:
                        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)
                        err = cal_reproject_error(imgpoints,objpoints,rvecs,tvecs,mtx,dist)

                    print("error:{}".format(err))
                    #if counter>1:
                        #dim_statistic(imgpoints, frame.shape[1], frame.shape[0])
                    #    dim_stat_xy(imgpoints, frame.shape[1], frame.shape[0])
                else:
                    print("No chessboard is found in this frame")
                print('\n')
                if counter == frame_count:  #meet the number of frames defined before
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