[RU-README](https://github.com/VIA-s-acc/practice_AI/blob/main/INFO/ru-readme.md)

## Content
- [Models](#download-models)
- [GUI](#with-gui)
- [Terminal](#with-terminal)
- [Train](#train)
   - [Auto Train](#auto-train)
   - [Manual Train](#manual-train)



### Update : 08.07.2024 INFO

- Add predict.py script to automate the process of prediction
- [In with Terminal](#with-terminal)

### Update : 05.07.2024 INFO

- Add train.py script to automate the process of training 
- [Auto Train](#auto-train)

#### Update : 01.07.2024 INFO 
- Changed the gui.
- Now in standart mode the gui will work only  with `OBB.pt` model.
- insructions for changing to old version

   - For use *Detect* mode change `gui.main` file 3 line from:
   
   ```python
   from Main.main_page import main_page
   ```
   to 
   ```python
   from Main.main_page_detect import main_page
   ```

   - *Standart* mode will use OBB.
   - *Detect* mode will not work with `OBB.pt` and *OBB* mode will not work with `detect.pt` model.
### Download Models
   - Download the best model for Text Blocks and Lines from: [Models](https://disk.yandex.ru/d/xP_VxJ5_Kd4cVA)
      - For *TextBlocks OBB* download `TextBlock-OBB.pt`
      - For *TextBlocks Detect* download `TextBlock-detect.pt`
      - For *TextLines Detect* download `TextLine-detect.pt`
      - For *TextLines OBB* download `TextLine-OBB.pt` 

   


## With GUI

1. **Clone the Repository**
   - Clone the repository to your local machine:
     ```bash
     git clone git@github.com:VIA-s-acc/practice_AI.git
     ```

2. **Navigate to the Repository**
   - Open a terminal or command prompt.
   - Change directory to the cloned repository:
     ```bash
     cd path/to/your/local/repository
     ```
   Replace `cd path/to/your/local/repository` with the actual path where your repository is located.

3. **Run the bat**
   - Execute the run script:
     ```bash
     .\run.bat
     ```

4. **View Output**
   - Check the terminal or command prompt for any output or errors generated by the script.

5. **Adjust as Necessary**
   - If there are errors, review the logs or console output for guidance on how to resolve them.

## With Terminal

1. **Clone the Repository**
   - Clone the repository to your local machine:
     ```bash
     git clone git@github.com:VIA-s-acc/practice_AI.git
     ```

2. **Navigate to the Repository**
   - Open a terminal or command prompt.
   - Change directory to the cloned repository:
     ```bash
     cd path/to/your/local/repository
     ```
   Replace `cd path/to/your/local/repository` with the actual path where your repository is located.

3. **Run**
   - run start command:
   ```bash
   yolo task=obb mode=predict model=`path to model` conf=0.6 source=`path to image` line_width=5 save_txt=true       
   ```
   - `path to model` should be replaced with the path to the downloaded model.
   - `path to image` should be replaced with the path to the image you want to predict.
   - `conf` should be replaced with the desired confidence level.
   - results will be saved in `runs\obb\predict{k}` folder.

   OR

   ```bash
   python .\predict.py -t obb -s C:\practice\0041.jpg -mb C:\practice\models\best\TextBlock-OBBv2.pt -ml C:\practice\models\best\TextLine-OBB.pt -c 0.59 -l 1
   ```

   predict.py CLI options:
   ```bash
   usage: Predictor [-h] -t T -s S -mb MB -ml ML [-c C] [-l L]

   Predict on image

   options:
   -h, --help            show this help message and exit
   -t T, -task T         task (obb | detect | segment | classify | pose | OBB)
   -s S, -src S, -source S
                           path to image
   -mb MB, -model-block MB
                           path to .pt model ( of text block detector )
   -ml ML, -model-line ML
                           path to .pt model ( of text line detector )
   -c C, -conf C         confidence level ( from 0 to 1 )
   -l L, -line L, -line_width L
                           line width
   ```
---
## Train 

###
   - Install required packages
   ```bash
   pip install -r requirements.txt
   ```
   - Download and copy yolov8x-obb.pt to `path\to\model` ([Link](https://disk.yandex.ru/d/A8FiDY1jf2XH6A))
   - Copy all images and labels to `\path\to\folder`
---
#### Auto-train
   - Run script `train.py`
   ```bash
   python train.py -src=`path\to\folder` -train=`path\to\train\folder` -val=`path\to\val\folder` -model=`path\to\model` -test=`path\to\test\folder` 
   ```
   
   - *`-src`* : path to folder with images and labels
   - *`-train`* : path to train folder (will used to save train images and labels after split) | Default .\Train
   - *`-val`* : path to val folder (will used to save val images and labels after split) | Default .\Val
   - *`-test`* : path to test folder (will used to save test images and labels after split) | (Optional)
   - *`-model`* : path to .pt model | Default yolov8x.pt
   ---
   - ***`CLI`*** info: 
      ```bash
      
      usage: Trainer [-h] -s S [-t T] [-v V] -m M [-ts TS] [-b B] [-ep EP]
      
      Prepare data and train model

      options:
      -h, --help            show this help message and exit
      -s S, -src S, -source S
                            path to data folder with images and labels
      -t T, -train T        path to train folder (will used to save train images and labels) | Default .\Train
      -v V, -val V          path to val folder (will used to save val images and labels) | Default .\Val
      -m M, -model M        path to .pt model
      -ts TS, -test TS      (Optional) path to test folder (will used to save test images and labels)
      -b B, -batch B        batch size | Default 8
      -ep EP, -epochs EP    number of epochs | Default 10
      -d D, -device D       device (cuda or cpu | default: cuda if available) 
      -w W, -workers W      number of workers | Default 8
      -n N, -name N         name of project
      -p P, -project P      save folder
      -imgsz IMGSZ          image size | Default 640
      ```
      - If something goes wrong during the training process, try changing the device to **`'cpu'`** using the **`'-d cpu'`** option.
      - Requires `cuda 11.8` to use GPU
         - If you have a different version of CUDA, follow the following steps:
            1. Remove torch and torchvision:
               ```bash
               pip uninstall torch torchvision
               ```
            2. Install correct version from [link](https://pytorch.org/)
         - If still not working, try to install ***torchvision==0.18.1+cu****:
            ```bash
            pip install torchvision==0.18.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html
            ```
            - replace `==0.18.1+cu118` to your version.

       

   - labels must be in .xml format with object name = <Text_Box>
      - Example
      ---------
      ```xml
      <annotation>
      <folder>...</folder>
      <filename>...</filename>
         <path>...</path>
      <source>
         <database>...</database>
      </source>
      <size>
         <width>w</width>
         <height>h</height>
         <depth>d</depth>
      </size>
         <segmented>0</segmented>
      <object>
         <name>Text_Box</name>
         <pose>Unspecified</pose>
         <truncated>1</truncated>
         <difficult>0</difficult>
         <bndbox>
            <xmin>1</xmin>
            <ymin>9</ymin>
            <xmax>1960</xmax>
            <ymax>93</ymax>
         </bndbox>
      </object>
      ```
   - Script will resize all images to `(imgsz, imgsz)`, covnert to grayscale, convert **`.xml (class_id,cx,cy,h,w)`** format to **`.txt (class_id,x1,y1,x2,y2,x3,y3,x4,y4)`** and run model train.
   ---
#### Manual train
   - create data folders
   - create folder structure
      - Create `Train` and `Val` in `path\to\train\folder` and `path\to\val\folder`
      - In `Train` folder create `images` and `labels` folders
      - In `Val` folder create `images` and `labels` folders
      - (Optional) create `Test` folder in `path\to\test\folder`. In `Test` folder create `images` and `labels` folders
   - copy all train images to `Train\images` and all train labels to `Train\labels`
   - copy all val images to `Val\images` and all val labels to `Val\labels`
   - (Optional) copy all test images to `Test\images` and all test labels to `Test\labels` 
   
   - create `dataset.yaml` file
   ```yaml
   # dataset.yaml example
   train: path\to\train\folder # path to train data ( folder with folders images and labels)
   val: path\to\val\folder # path to validate data
   # test: path\to\test\folder # path to test data ( non required )

   # classes
   nc: 1  #  class number
   names: ['tbox']  #  class names
   ```
   - run train command
   ```bash
   yolo task=obb mode=train model=yolov8m.pt data="path to dataset.yaml" epochs=10 imgsz=640 batch=8 project=(path to result) name="name"  
   ```
      - task= detect: detect mode
      - task= segment: segment mode
      - task= classify: classify mode
      - task= Pose: pose mode
      - task= OBB: object detection bounding box mode
      - batch: batch size
      - epochs: number of epochs
      - imgsz: image size
      - name: name of the model
      - project: path to result
      - data: path to dataset.yaml
      - model: path to model
   - In training, the parameters used were `task=obb`, `epoches=100`, and `batch=16`.


