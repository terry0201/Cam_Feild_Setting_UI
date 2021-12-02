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
- 完成: 讀檔、存檔、新增 | 編輯 | 刪除 多邊形、transform、多邊形 <-> table 雙向 Highlight
- TODO: Camera 相關功能

### exe
> `pip install pyinstaller`
> `pyinstaller -F lab_main.py [-n <Name> -c --icon=<Name.ico>]`
- Structure
```
Root/Polygon/exe/
                CameraFeild1014.exe     # 程式執行檔
                Polygon
                ├── name.txt            # 建立多邊形name的列表
                ├── address.txt         # 建立相機address的列表
                ├── sound               # 使用到的音效
                │   ├ clicked.wav 
                │   ├ error.wav
```

### env:
> `pip install PySide2`  
> `pip install opencv-python`  
> `pip install Shapely`  
> `pip install numpy`  
> `pip install matplotlib`

備註: .xml(多邊形資料) / .npy(transform 矩陣) 會儲存在與圖片相同資料夾底下

## Object detection

#### 切割video中的第一張frame:
> `python video_process.py --video_name street1.mp4` 


#### 判定封閉範圍內是否有交通工具:
> `python detect.py --source inference/images/street1.mp4 --weights yolor_p6.pt --min_inter_area_ratio 0.4 --handcraft_polygon_xml_path xml_dir/street1.xml`  


### env:
> `pip install -r requirements.txt`  
> `pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html`  
> `pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI`  


備註1: 需要在yolor資料夾路徑下pip install環境(在yolor資料夾內才有requirements.txt)  

備註2: 執行video_process.py前需將video放置在yolor/inference/images/資料夾下  

備註3: 執行detect.py前需將video放置在yolor/inference/images/路徑下，且xml需放置在yolor/xml_dir/資料夾下  

## Reference
- [PySide2教學](https://medium.com/bucketing/pyside2-pyqt-tutorial-3c2be590bc6a)
- [OpenCV Camera Calibration](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html)

## Contributors
[詹家欣 Chia-Hsin Chan](https://sites.google.com/site/terry0201/)、

## Meeting markdown document
[link](https://hackmd.io/1zHg7h21TXWCPbuK0SQ4MA?both)
