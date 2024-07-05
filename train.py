import os
import argparse
import sys
from prepare_data import XMLToYOLOConverter
from split import train_test_split, resize_all, cxcyhw_to_x1xn1x2yn2, grayscale_all, convert_to_jpg
import shutil
from tqdm import tqdm
import torch
from loguru import logger
import os
logger.remove(0)
logger.add('train.log', level="DEBUG", rotation='10 MB')
logger.add(sys.stderr, level="INFO")


@logger.catch
def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='Trainer',
        description="Prepare data and train model",
    )
    parser.add_argument('-s', '-src','-source', type=str, help='path to data folder with images and labels', required=True)
    parser.add_argument('-t', '-train', type=str, required=False, default='Train', help='path to train folder (will used to save train images and labels)')
    parser.add_argument('-v', '-val', type=str, required=False, default='Val', help='path to val folder (will used to save val images and labels)')
    parser.add_argument('-m', '-model', type=str, required=True,help='path to .pt model')
    parser.add_argument('-ts', '-test', type=str, required=False, default=None, help='(Optional) path to test folder (will used to save test images and labels)')
    parser.add_argument('-b', '-batch', type=int, required=False, default=8, help='batch size')
    parser.add_argument('-ep', '-epochs', type=int, required=False, default=10, help='number of epochs')
    parser.add_argument('-d', '-device', type=str, required=False, default='default', help='device (cuda or cpu | default: cuda if available)')
    parser.add_argument('-w', '-workers', type=int, required=False, default=8, help='number of workers')
    parser.add_argument('-imgsz', type=int, required=False, default=640, help='image size')
    

    return parser.parse_args(args)

@logger.catch
def prepare_data(source, train, val, test, model, device, workers, imgsz, batch, epochs):
    train = os.path.abspath(train) + '\\'
    val = os.path.abspath(val) + '\\'
    source = os.path.abspath(source) + '\\'
    model = os.path.abspath(model)
    if device == 'default':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if test is not None:
        test = os.path.abspath(test) + '\\'
    actions = ['convert', 'convert_jpg', 'resize', 'grayscale', 'cxcyhw_to_x1xn1x2yn2', 'train_test_split', 'create_yaml','']
    
    for action, i in zip(actions, tqdm(range(7))):
        if action == 'convert':
            converter = XMLToYOLOConverter(source, source, obj_class='Text_Box') # FOR LINES USE obj_class='Text_line' and in .xml object_name = <Text_line>    
            converter.convert()
            if not os.path.exists(os.path.join(source, 'labels')):
                os.makedirs(os.path.join(source, 'labels'))
            for xml_file in os.listdir(source):
                if xml_file.endswith('.xml'):
                    shutil.move(os.path.join(source, xml_file), os.path.join(source, 'labels'))
        if action == 'convert_jpg':
            convert_to_jpg(source)
        if action == 'resize':
            resize_all(source, (imgsz, imgsz))
        if action == 'grayscale':
            grayscale_all(source)
        if action == 'cxcyhw_to_x1xn1x2yn2':
            cxcyhw_to_x1xn1x2yn2(source)
        if action == 'train_test_split':
            train_test_split(path=source, neg_path=None, split=0.2, train_path_img=train+'\\images', train_path_label=train+'\\labels', val_path_img=val+'\\images', val_path_label=val+'\\labels', test_path_img=test if test else None)       
        if action == 'create_yaml':
            create_yaml(train, val, test = test if test else None)  
            
    print("TRAINING START\n")
    from ultralytics import YOLO

    model = YOLO(model)
    model.train(data='dataset.yaml', epochs=epochs, imgsz=imgsz, batch=batch, project='res', name='tbox', device=device, workers=workers)
    
                    

@logger.catch
def create_yaml(train, val, test):
    if test is None:
        yaml_data = {
            'train': train,
            'val': val,
            # 'test': test,
            'nc': 1,  # количество классов
            'names': ['tbox']  # названия классов
        }
    else:
        yaml_data = {
            'train': train,
            'val': val,
            'test': test,
            'nc': 1,  # количество классов
            'names': ['tbox']  # названия классов
        }
    with open('dataset.yaml', 'w') as f:
        f.write('train: {}\n'.format(train))
        f.write('val: {}\n'.format(val))
        if test is not None:
            f.write('test: {}\n'.format(test))
        f.write("\n\n")
        f.write('nc: {}\n'.format(yaml_data['nc']))
        f.write('names: {}\n'.format(yaml_data['names']))
        f.close()


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    prepare_data(source=args.s, train=args.t, val=args.v, test=args.ts, model=args.m, device=args.d, workers=args.w, imgsz=args.imgsz, batch=args.b, epochs=args.ep)
    
