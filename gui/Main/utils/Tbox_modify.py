#### DONT USE THIS CODE #### 


import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import namedtuple
class TboxGenerator:
    def __init__(self, path_to_img, path_to_labels, path_to_save, mode = 'OBB'):
        self.path_to_img = path_to_img
        self.path_to_labels = path_to_labels
        self.path_to_save = path_to_save
        self.mode = mode
        if mode.lower() not in ['obb', 'detect']:
            raise ValueError('mode should be obb or detect')
        
    def generate(self) -> str | bool:
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)        

        img = cv2.imread(self.path_to_img)
        labels = open(self.path_to_labels).read().strip().split('\n')
        if labels[0] == "No labels found":
            cv2.imwrite(os.path.join(self.path_to_save, f'tbox.jpg'), img)
            return self.path_to_save
        
        for i in range(len(labels)):
            labels[i] = labels[i][2:]
                    
        height, width, _ = img.shape
        def relative_to_absolute(rel_coords, img_width, img_height):
            x_center_rel, y_center_rel, width_rel, height_rel = map(float, rel_coords.split())
            x_center = int(x_center_rel * img_width)
            y_center = int(y_center_rel * img_height)
            box_width = int(width_rel * img_width)
            box_height = int(height_rel * img_height)
            x1 = int(x_center - box_width / 2)
            y1 = int(y_center - box_height / 2)
            x2 = int(x_center + box_width / 2)
            y2 = int(y_center + box_height / 2)

            return x1, y1, x2, y2
        if self.mode.lower() == 'detect':
            for i, coord in enumerate(labels):
                x1, y1, x2, y2 = relative_to_absolute(coord, width, height)
                cropped_image = img[y1:y2, x1:x2]
                cv2.imwrite(os.path.join(self.path_to_save, f'tbox_{i}.jpg'), cropped_image)
        
        elif self.mode.lower() == 'obb':
            for i, coord in enumerate(labels):
                x1, y1, x2, y2, x3, y3, x4, y4 = map(float, coord.split())
                x1, x2, x3, x4 = x1 * width, x2 * width, x3 * width, x4 * width
                y1, y2, y3, y4 = y1 * height, y2 * height, y3 * height, y4 * height
                mask = np.zeros(img.shape, dtype=np.uint8)
                roi_corners = np.array([[(x1, y1), (x2, y2), (x3, y3), (x4, y4)]], dtype=np.int32)
                channel_count = img.shape[2]
                ignore_mask_color = (255,)*channel_count
                cv2.fillConvexPoly(mask, roi_corners, ignore_mask_color)
                masked_image = cv2.bitwise_and(img, mask)
                masked_image = self.rotate_crop(masked_image, (x1, y1), (x2, y2))
                cv2.imwrite(os.path.join(self.path_to_save, f'tbox_{i}.jpg'), masked_image)
                cropped = Image.fromarray(masked_image[:, :, ::-1])
                bbox = cropped.getbbox()
                croppeed_image = cropped.crop(bbox)
                croppeed_image.save(os.path.join(self.path_to_save, f'tbox_{i}.jpg'))
                
        return self.path_to_save        
        

                
    def rotate_crop(self, image, pt1, pt2):
        vec = namedtuple('Point', ['x', 'y'])
        vec.x, vec.y = pt2[0] - pt1[0], pt2[1] - pt1[1]
        theta = math.atan2(vec.y, vec.x)
        theta = math.degrees(theta)
        if theta > 45:
            theta = theta - 90
        elif theta < -45:
            theta = theta + 90  
        image = self.rotate_image(image, theta)
        
        return image                 
              
                
    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result
            





                
                

                

