import xml.etree.ElementTree as ET
# import numpy as np

def xml2dict(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    polygonDict = {}
    # Find the coordinates and markers of the image from xml and store them in the Dict
    for obj in root.iter('object'):
        name = obj.find('name').text
        polygon_pos_list = []
        polygon = obj.find('polygon')
        for pt in polygon.iter('pt'):
            x = float(pt.find('x').text)
            y = float(pt.find('y').text)
            polygon_pos_list += [[x, y]]
        polygonDict[name] = polygon_pos_list
    return polygonDict


if __name__ == "__main__":
    print(xml2dict('TEST1.xml'))
# Find the key and value from Dict
# for i in polygonDict:
#     print("Key is", i, ",Value is", polygonDict[i])
#     for j in range(len(polygonDict[i])):
#         print(polygonDict[i][j][0])
#         print(polygonDict[i][j][1])