import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil



# 这里是将左上角和右下角的坐标转化为中心点和宽高
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(wd,image_id):
    try:
        in_file = open(wd+'/Annotations2/%s.xml'%(image_id))
        out_file = open( wd + '/labels/%s.txt'%(image_id), 'w')
        tree=ET.parse(in_file) # 导入xml数据
        root = tree.getroot() # 得到跟节点
        size = root.find('size') # 找到根节点下面的size节点
        w = int(size.find('width').text) # 得到图片的尺寸
        h = int(size.find('height').text)
        for obj in root.iter('object'): # 对根节点下面的'object’节点进行遍历
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes:
                classes.append(cls)
            if int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    except Exception as e:
        print(str(e))
        print(image_id)




def convert_ImgaSets(path):
    image_file=os.listdir(path)
    f = open(('train.txt'), 'w+')  # 写入图片名字
    f1 = open(('train_full.txt'), 'w+')  # 写入图片名字
    f2 = open(('val.txt'), 'w+')  # 写入图片名字
    count=0
    for file in image_file:
        f.write(file[:-4]+'\n')
        if count%10==0:
            f2.write(path+file+'\n')
        else:
            f1.write(path+file+'\n')
        count=count+1

    f.close()




if __name__=='__main__':
    wd = getcwd() # 获取当前文件的路径
    wd = wd.replace('\\', '/')

    classes = []  # 这里是你要处理的数据的类别总数

    if os.path.exists(wd + '/labels/'): # 创建一个label文件夹来存放图片对应的类别和坐标
        shutil.rmtree(wd + '/labels/')
    os.makedirs(wd + '/labels/')
    convert_ImgaSets(wd+'/JPEGImages2/')
    image_ids = open('train.txt').read().strip().split()
    k=0
    for image_id in image_ids:
        convert_annotation(wd,image_id)
        k=k+1
    print(classes)
    # for cls in classes:
    #     exec(str(cls)+"_num=0")
    # test_file = os.listdir(wd + '/labels/')
    # for file in test_file:
    #     infile=open(wd +"/labels/"+ file)
    #     line=infile.readline()
    #     # print(list(line)[0])
    #     try:
    #         exec(str(classes[int(list(line)[0])])+"_num+=1")
    #     except Exception as e:
    #         print(str(e))
    # for i in range(len(classes)):
    #     print(classes[i],eval(str(classes[i])+"_num"))
