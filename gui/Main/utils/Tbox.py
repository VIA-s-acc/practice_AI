import cv2
import os
class TboxGenerator:
    def __init__(self, path_to_img, path_to_labels, path_to_save):
        self.path_to_img = path_to_img
        self.path_to_labels = path_to_labels
        self.path_to_save = path_to_save
        
    
    def generate(self) -> str | bool:
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)        
            
        img = cv2.imread(self.path_to_img)
        labels = open(self.path_to_labels).read().strip().split('\n')
        if labels[0] == "No labels found":
            return False
        
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
        
        for i, coord in enumerate(labels):
            x1, y1, x2, y2 = relative_to_absolute(coord, width, height)
            cropped_image = img[y1:y2, x1:x2]
            cv2.imwrite(os.path.join(self.path_to_save, f'tbox_{i}.jpg'), cropped_image)
        
        return self.path_to_save        
        


