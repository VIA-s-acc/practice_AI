from gui.Main.utils.Tbox import TboxGenerator ### TO USE EXPEREMENTAL TboxGenerator WITH ROTATION FIX REPLACE gui.Main.utuils.Tbox WITH gui.Main.utils.Tbox_modify
from loguru import logger
import sys
import argparse
import os
logger.remove(0)
logger.add('logs/predict.log', level="DEBUG", rotation='10 MB')
logger.add(sys.stderr, level="INFO")

@logger.catch
def parse_args(args):
    parser = argparse.ArgumentParser(
        prog='Predictor',
        description="Predict on image",
    )
    parser.add_argument('-t', '-task', type=str, required=True, default='obb', help='task (obb | detect | segment | classify | pose | OBB)')
    parser.add_argument('-s', '-src','-source', type=str, help='path to image', required=True)
    parser.add_argument('-mb', '-model-block', type=str, required=True,help='path to .pt model ( of text block detector )')
    parser.add_argument('-ml', '-model-line', type=str, required=True,help='path to .pt model ( of text line detector )')
    parser.add_argument('-c', '-conf', type=float, required=False, default=0.51, help='confidence level ( from 0 to 1 )')
    parser.add_argument('-l','-line','-line_width', type=int, required=False, default=5, help='line width')

    return parser.parse_args(args)

@logger.catch
def predict(**kwargs):
    from ultralytics import YOLO
    model_block = YOLO(kwargs['model-b'])
    model_line = YOLO(kwargs['model-l'])
    model_block.predict(kwargs['source'], save = True, save_txt = True, conf = kwargs['conf'], line_width = kwargs['line_width'])
    path = f'runs/{kwargs["task"]}/'
    pred_dirs = [d for d in os.listdir(path) if d.startswith('predict')]
    last_pred_dir = None
    for i in range(2, len(pred_dirs)+1):
        if f'predict{i}' in pred_dirs:
            last_pred_dir = path + f'predict{i}'
        else:
            last_pred_dir = path + f'predict'
            break
    if last_pred_dir is None:
        last_pred_dir = path + f'predict'
    run_dir = os.path.dirname(os.path.abspath(__file__))
    last_pred_dir = os.path.join(run_dir, last_pred_dir)
    labels_dir = os.path.join(last_pred_dir, 'labels')
    if not os.path.exists(labels_dir):
        return
    try:
        label_file = os.listdir(labels_dir)[0]
    except:
        label_file = 'labels.txt'
        with open(os.path.join(labels_dir,label_file), 'w') as f:
            f.write('No labels found')
            
    if os.path.getsize(os.path.join(labels_dir,label_file)) == 0:
        with open(os.path.join(labels_dir,label_file), 'w') as f:
            f.write('No labels found')
    Boxes_save_path = os.path.join(labels_dir, 'tbox')
    generator = TboxGenerator(kwargs['source'], os.path.join(labels_dir, label_file), Boxes_save_path, kwargs['task'])
    generator.generate()
    boxes_files = [os.path.join(Boxes_save_path, f) for f in os.listdir(Boxes_save_path)]
    model_line.predict(boxes_files, save = True, save_txt = True, conf = kwargs['conf'], line_width = kwargs['line_width'])
    
#yolo task=detect mode=predict model=C:\practice\result\tbox\weights\best.pt conf=0.59 source=C:\practice\Train\images\0043.jpg line_width=5 save_txt=true       

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    kwargs = {'task': args.t, 'source': args.s, 'model-b': args.mb, 'model-l': args.ml, 'conf': args.c, 'line_width': args.l}
    predict(**kwargs)