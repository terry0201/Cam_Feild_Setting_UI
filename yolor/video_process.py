#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import shutil
import argparse

def config_image_path():
    video_image_path = "./inference/images/video_image/"
    if os.path.exists(video_image_path)==False:
        os.mkdir(video_image_path)
    return video_image_path

if __name__ == "__main__":

    config_image_path()

    parser = argparse.ArgumentParser()
    parser.add_argument('--video_name', type=str, default='street1.mp4', help='要處理的影片名稱(含附檔名)')
    opt = parser.parse_args()

    video_path = "./inference/images/"+opt.video_name

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('frame', frame)
        cv2.imwrite('./inference/images/video_image/'+opt.video_name[:-4]+'.jpg',frame)
        print(opt.video_name[:-4]+'.jpg'+' 存放在 '+'./inference/images/video_image/'+' 資料夾下')
        break
        # if cv2.waitKey(1) == ord('q'):
        #     break
        cap.release()
        cv2.destroyAllWindows()