import os
import xml.etree.ElementTree as ET

class XMLToYOLOConverter:
    def __init__(self, xml_folder, output_folder, find = 'bndbox', obj_class = "Text_Box"):
        self.xml_folder = xml_folder
        self.output_folder = output_folder
        self.find = find
        self.obj_class = obj_class
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def convert(self):
        for xml_file in os.listdir(self.xml_folder):
            if xml_file.endswith('.xml'):
                xml_path = os.path.join(self.xml_folder, xml_file)
                self.convert_xml_to_yolo(xml_path)

    def convert_xml_to_yolo(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        img_folder = root.find('folder').text
        img_filename = root.find('filename').text
        img_path = os.path.join(img_folder, img_filename)

        img_width = int(root.find('size').find('width').text)
        img_height = int(root.find('size').find('height').text)

        txt_filename = os.path.splitext(img_filename)[0] + '.txt'
        txt_path = os.path.join(self.output_folder, txt_filename)

        with open(txt_path, 'w') as txt_file:
            for obj in root.findall('object'):
                obj_class = obj.find('name').text
                if obj_class != self.obj_class:
                    continue

                xmin = int(obj.find(self.find).find('xmin').text)
                ymin = int(obj.find(self.find).find('ymin').text)
                xmax = int(obj.find(self.find).find('xmax').text)
                ymax = int(obj.find(self.find).find('ymax').text)

                x_center = (xmin + xmax) / 2.0 / img_width
                y_center = (ymin + ymax) / 2.0 / img_height
                box_width = (xmax - xmin) / img_width
                box_height = (ymax - ymin) / img_height

                txt_file.write(f"0 {x_center} {y_center} {box_width} {box_height}\n")

        print(f"Converted {xml_path} to {txt_path}")


# Пример использования:
xml_folder = 'Dataset'
output_folder = 'Data'

converter = XMLToYOLOConverter(xml_folder, output_folder, obj_class='line')
converter.convert()
