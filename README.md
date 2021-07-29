# Cam_Feild_Setting_UI
an UI that can do
1. camera distortion calibration
2. camera-to-real_world projection by perspective tramsform
3. polygon painting on camrea view

## Calibration
> `python realtime.py`

每三秒擷取一張frame，且用累計下來的frame去做calibration

## GUI
> `python lab_main.py`
- 完成: 讀檔、存檔、新增 | 編輯 | 刪除 多邊形、transform、多邊形 <-> table 雙向 Highlight、
- TODO: Camera 相關功能

### env:
> `pip install PySide2`  
> `pip install opencv-python`  
> `pip install Shapely`  
> `pip install numpy`
> `pip install matplotlib`

備註: .xml(多邊形資料) / .npy(transform 矩陣) 會儲存在與圖片相同資料夾底下

## Reference
- [PySide2教學](https://medium.com/bucketing/pyside2-pyqt-tutorial-3c2be590bc6a)
- [OpenCV Camera Calibration](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html)

## Contributors
[詹家欣 Chia-Hsin Chan](https://sites.google.com/site/terry0201/)、

## Meeting markdown document
[link](https://hackmd.io/1zHg7h21TXWCPbuK0SQ4MA?both)
