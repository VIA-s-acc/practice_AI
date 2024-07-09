import os 
import shutil
import random
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image

train_path_img = './Train/images'
train_path_label = './Train/labels'
val_path_img = './Val/images'
val_path_label = './Val/labels'
test_path_img = './Test'

'''
Split the dataset into train and test and creates the train.txt and test.tx with
the respective path of the images in each folder
'''

def train_test_split(path,neg_path=None, split = 0.2, train_path_img=train_path_img, train_path_label=train_path_label, val_path_img=val_path_img, val_path_label=val_path_label, test_path_img=test_path_img):
    print("------ PROCESS STARTED -------")


    files = list(set([name[:-4] for name in os.listdir(path)])) ## removing duplicate names i.e. counting only number of images
    

    print (f"--- This folder has a total number of {len(files)} images---")
    random.seed(42)
    random.shuffle(files)

    test_size = int(len(files) * split)
    train_size = len(files) - test_size

    ##  создаем папки

    os.makedirs(train_path_img, exist_ok = True)
    os.makedirs(train_path_label, exist_ok = True)
    os.makedirs(val_path_img, exist_ok = True)
    os.makedirs(val_path_label, exist_ok = True)

    
    ### -----------  копируем обучающую выборку
    for filex in tqdm(files[:train_size]):
      if filex == 'classes':
          continue
      try:
        shutil.copy2(path + filex + '.jpg',f"{train_path_img}/" + filex + '.jpg' )
        shutil.copy2(path + filex + '.txt', f"{train_path_label}/" + filex + '.txt')
      except:
          pass  
    

    print(f"------ Training data created with 80% split {len(files[:train_size])} images -------")
    
    if neg_path:
        neg_images = list(set([name[:-4] for name in os.listdir(neg_path)])) ## removing duplicate names i.e. counting only number of images
        for filex in tqdm(neg_images):
            shutil.copy2(neg_path+filex+ ".jpg", f"{train_path_img}/" + filex + '.jpg')
            
        print(f"------ Total  {len(neg_images)} negative images added to the training data -------")
    
        print(f"------ TOTAL Training data created with {len(files[:train_size]) + len(neg_images)} images -------")
    


    ### ----------- копируем тестовую выборку
    for filex in tqdm(files[train_size:]):
      if filex == 'classes':
          continue
      try:
        shutil.copy2(path + filex + '.jpg', f"{val_path_img}/" + filex + '.jpg' )
        shutil.copy2(path + filex + '.txt', f"{val_path_label}/" + filex + '.txt')
      except:
          pass

    print(f"------ Testing data created with a total of {len(files[train_size:])} images ----------")
    
    print("------ TASK COMPLETED -------")

def convert_to_jpg(path):
    for filename in os.listdir(path):
        if filename.endswith('.tif') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.JPEG') or filename.endswith('.PNG') or filename.endswith('.JPEG'):
            img = Image.open(path+filename)
            img.save(path+filename.split('.')[0]+'.jpg', 'JPEG', quality=100) 
            os.remove(path+filename)
            
def move_all_ext_to(path, path_to, ext, to_gray=False):
    for filename in os.listdir(path):
        if filename.endswith(ext):
            if to_gray:
                img_path = path+'/'+filename
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(path_to+'/'+filename, img)
            else:
                shutil.copy2(path+'/'+filename, path_to+'/'+filename)

def resize_all(path, size):
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            img = cv2.imread(path+'/'+filename)
            img = cv2.resize(img, size)
            cv2.imwrite(path+'/'+filename, img)

def grayscale_all(path):
    for filename in os.listdir(path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.PNG'):
            img = cv2.imread(path+'/'+filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path+'/'+filename, img)


def cxcyhw_to_x1xn1x2yn2(path_to_labels):
    for file in os.listdir(path_to_labels):
        if file.endswith('.txt'):
            with open(os.path.join(path_to_labels, file), 'r+') as f:
                lines = f.readlines()
                new_lines = []
                for line in lines:
                    class_id, cx,cy,w,h = map(float, line.strip().split())
                    x1 = cx - w/2
                    y1 = cy - h/2
                    x2 = cx + w/2
                    y2 = cy - h/2
                    x3 = cx + w/2
                    y3 = cy + h/2
                    x4 = cx - w/2
                    y4 = cy + h/2
                    new_lines.append(f"{int(class_id)} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}\n")
                f.seek(0)
                f.writelines(new_lines)
                f.truncate()

            
def augment_data(patg):
    
    angles = [5, 10, 15, 20]
    files = os.listdir(patg)
    counter = 0
    coutn = len(files)//2
    for filename in files:
        if filename.endswith('.jpg'):
            counter += 1  
            print(f'{counter}/{coutn}')
 
            for angle in angles:
                img = cv2.imread(patg+'/'+filename)
                img, rot_mat = rotate_image(img, angle)
                cv2.imwrite(patg+'/'+filename.split('.')[0]+'_'+str(angle)+'.jpg', img)
                text_file = open(patg+'/'+filename.split('.')[0]+'.txt')
                with open(patg+'/'+filename.split('.')[0] + '.txt', "r") as text_file:
                    lines = text_file.readlines()             
                append = []
                with open(patg+'/'+filename.split('.')[0] + '_' + str(angle) + '.txt', "a") as text_file:
                    for line in lines:
                        class_id, x1, y1, x2, y2, x3, y3, x4, y4 = map(float, line.strip().split())
                        class_id = int(class_id)
                        rx1, ry1 = rotate_point(x1 * img.shape[1], y1 * img.shape[0], rot_mat)
                        rx2, ry2 = rotate_point(x2 * img.shape[1], y2 * img.shape[0], rot_mat)
                        rx3, ry3 = rotate_point(x3 * img.shape[1], y3 * img.shape[0], rot_mat)
                        rx4, ry4 = rotate_point(x4 * img.shape[1], y4 * img.shape[0], rot_mat)
                        # normalize
                        rx1 = rx1 / img.shape[1]
                        ry1 = ry1 / img.shape[0]
                        rx2 = rx2 / img.shape[1]
                        ry2 = ry2 / img.shape[0]
                        rx3 = rx3 / img.shape[1]
                        ry3 = ry3 / img.shape[0]
                        rx4 = rx4 / img.shape[1]
                        ry4 = ry4 / img.shape[0]
                        
                        append.append(f"{class_id} {rx1} {ry1} {rx2} {ry2} {rx3} {ry3} {rx4} {ry4}\n")
                    text_file.writelines(append)
                    text_file.close()       
                    append.clear()
                 
                    
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result, rot_mat

                
                
def rotate_point(x, y, rot_mat):
    point = np.array([x, y, 1]).reshape((3, 1))
    rotated_point = np.dot(rot_mat, point)
    return rotated_point[0, 0], rotated_point[1, 0]

def blur_all(path):
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            img = cv2.imread(path+'/'+filename)
            img = cv2.GaussianBlur(img, (5, 5), 0)
            cv2.imwrite(path+'/'+filename, img)
            


if __name__ == '__main__':
    pass
    # cxcyhw_to_x1xn1x2yn2('data/')
    # print("------ CXCYHW TO X1XN1X2YN2 STARTED -------")
    # cxcyhw_to_x1xn1x2yn2('data/')
    # print("------ CXCYHW TO X1XN1X2YN2 ENDED -------")
    # print("------ RESIZE STARTED -------")
    # resize_all('data/', (640, 640))
    # print("------ RESIZE ENDED -------")
    # print("------ AUGMENTATION STARTED -------")
    # augment_data('data/')
    # print("------ AUGMENTATION ENDED -------")
    # train_test_split('data/')