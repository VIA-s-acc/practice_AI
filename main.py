import ultralytics
ultralytics.checks()

#yolo task=detect mode=train model=yolov8m.pt data="path to dataset.yaml" epochs=10 imgsz=640 batch=8 project=(path to result) name=tbox  
#train

#yolo task=detect mode=predict model=C:\practice\result\tbox\weights\best.pt conf=0.59 source=C:\practice\Train\images\0043.jpg line_width=5 save_txt=true       
#predict