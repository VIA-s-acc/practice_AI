[EN-README](https://github.com/VIA-s-acc/practice_AI/blob/main/README.md)

## Content
- [Models](#download-models)
- [Train](#train)
   - [Auto Train](#auto-train)
   - [Manual Train](#manual-train)
- [GUI](#with-gui)
- [Terminal](#with-terminal)

### Update : 08.07.2024 INFO

- Добавлен скрипт predict.py для автоматизации процесса предсказывания
- [In with Terminal](#with-terminal)

### Update : 05.07.2024 INFO

- Добавлен скрипт train.py для автоматизации процесса обучения
- [Auto Train](#auto-train)

#### Update : 01.07.2024 INFO 
- Изменён графический интерфейс.
- Теперь в стандартном режиме графический интерфейс будет работать только с моделью `OBB.pt`.
- Инструкция по переходу на старую версию

   - Для использования режима *Detect* измените 3 строку файла `gui.main` с:
   
   ```python
   from Main.main_page import main_page
   ```
   на 
   ```python
   from Main.main_page_detect import main_page
   ```

   - В *Standart* режиме будет использоваться OBB.
   - Режим *Detect* не будет работать с моделью `OBB.pt`, а режим *OBB* не будет работать с моделью `detect.pt`.l.
### Download Models
   - Скачайте модели для блоков и строк текста по ссылке: [Models](https://disk.yandex.ru/d/xP_VxJ5_Kd4cVA)
      - Для *TextBlocks OBB* скачайте `TextBlock-OBB.pt`
      - Для *TextBlocks Detect* скачайте `TextBlock-detect.pt`
      - Для *TextLines Detect* загрузите `TextLine-detect.pt`
      - Для *TextLines OBB* скачайте `TextLine-OBB.pt` 

   


## With GUI

1. **Клонирование репозитория****
   - Клонируйте репозиторий на свой локальный компьютер:
     ```bash
     git clone git@github.com:VIA-s-acc/practice_AI.git
     ```

2. **Переход в репозиторий**
   - Откройте терминал или командную строку.
   - Измените каталог на клонированный репозиторий:
     ```bash
     cd path/to/your/local/repository
     ```
   Поменяйте `cd path/to/your/local/repository` с путем к вашему локальному репозиторию.

3. **Run***
   - Выполните скрипт запуска:
     ```bash
     .\run.bat
     ```

4. **Просмотр выходных данных**
   - Проверьте терминал или командную строку на наличие выводимых данных или ошибок, сгенерированных сценарием.

5. **Просмотр журналов**
   - При наличии ошибок просмотрите журналы или выходные данные консоли, чтобы узнать, как их устранить.

## With Terminal

1. **Клонирование репозитория**
   - Клонируйте репозиторий на свой локальный компьютер:
     ```bash
     git clone git@github.com:VIA-s-acc/practice_AI.git
     ```

2. **Переход в репозиторий**
   - Откройте терминал или командную строку.
   - Измените каталог на клонированный репозиторий:
     ```bash
     cd path/to/your/local/repository
     ```
   Поменяйте `cd path/to/your/local/repository` с путем к вашему локальному репозиторию.

3. **Run**
   - Выполнить команду запуска:
   ```bash
   yolo task=obb mode=predict model=`path to model` conf=0.6 source=`path to image` line_width=5 save_txt=true       
   ```
   - `path to model` следует заменить на путь к загруженной модели.
   —  `path to image` следует заменить путем к изображению, которое вы хотите предсказать.
   - `conf` следует заменить на желаемый уровень доверия.
   - результаты будут сохранены в папке `runs\obb\predict{k}`.

   Или

   ```bash
   python .\predict.py -t obb -s C:\practice\0041.jpg -mb C:\practice\models\best\TextBlock-OBBv2.pt -ml C:\practice\models\best\TextLine-OBB.pt -c 0.59 -l 1
   ```

   predict.py CLI options:
   ```bash
   usage: Predictor [-h] -t T -s S -mb MB -ml ML [-c C] [-l L]

   Predict on image

   options:
   -h, --help            Показать это сообщение
   -t T, -task T         задача (obb | detect | segment | classify | pose | OBB)
   -s S, -src S, -source S
                           путь к изображению
   -mb MB, -model-block MB
                           путь к модели ( Детектор блоков )
   -ml ML, -model-line ML
                           путь к модели ( Детектор линий )
   -c C, -conf C         Минимальный порог доверия ( from 0 to 1 )
   -l L, -line L, -line_width L
                           Ширина линий
   ```

---
## Train 

###
   - Установите необходимые пакеты
   ```bash
   pip install -r requirements.txt
   ```
   - Скачайте и скопируйте yolov8x-obb.pt в `path\to\model` ([Link](https://disk.yandex.ru/d/A8FiDY1jf2XH6A))
   - Скопируйте все изображения и метки в `\path\to\folder`
---
#### Auto-train
   - Запустить скрипт `train.py`
   ```bash
   python train.py -src=`path\to\folder` -train=`path\to\train\folder` -val=`path\to\val\folder` -model=`path\to\model` -test=`path\to\test\folder` 
   ```
   
   - *`-src`* : Путь к папке с изображениями и метками
   - *`-train`* : Путь к папке с обучающими изображениями и метками (будет использоваться для сохранения изображений и меток после разбиения) | По умолчанию .\Train
   - *`-val`* : Путь к папке с изображениями и метками для валидации (будет использоваться для сохранения изображений и меток после разбиения) | По умолчанию .\Val
   - *`-test`* : путь к папке с тестовыми изображениями и метками (будет использоваться для сохранения изображений и меток после разбиения) | (Необязательно)
   - *`-model`* : путь к .pt модели | По умолчанию yolov8x.pt
   ---
   - ***`CLI`*** info: 
      ```bash
      
      Использование: Trainer [-h] -s S [-t T] [-v V] -m M [-ts TS] [-b B] [-ep EP]
      
      Подготовка данных и обучение модели

      Опции:
      -h, --help            показать это справочное сообщение и выйти
      -s S, -src S, -source S
                            путь к папке данных с изображениями и метками
      -t T, -train T        путь к папке поезда (будет использоваться для сохранения изображений и меток поездов) | По умолчанию .\Train
      -v V, -val V          путь к папке val (будет использоваться для сохранения изображений и меток val) | По умолчанию .\Val
      -m M, -model M        путь к .pt model
      -ts TS, -test TS      (Необязательно) путь к тестовой папке (будет использоваться для сохранения тестовых изображений и этикеток)
      -b B, -batch B        размер партии | По умолчанию 8
      -ep EP, -epochs EP    количество эпох | По умолчанию 10
      -d D, -device D       устройство (cuda или процессор | по умолчанию: cuda, если доступно) 
      -w W, -workers W      количество рабочих | По умолчанию 8
      -n N, -name N         название проекта
      -p P, -project P      сохранить папку
      -imgsz IMGSZ          размер изображения | По умолчанию 640
      ```
      - Если в процессе обучения что-то пойдет не так, попробуйте изменить устройство на **`'cpu'`** с помощью опции **`'-dcpu'`**.
      - Для использования графического процессора требуется `cuda 11.8`.
         - Если у вас другая версия CUDA, выполните следующие действия:
            1. Удалите torch и torchvision:
               ```bash
               pip uninstall torch torchvision
               ```
            2. Установите правильную версию из [link](https://pytorch.org/)
         - Если всё ещё не работает, попробуйте установить ***torchvision==0.18.1+cu****:
            ```bash
            pip install torchvision==0.18.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html
            ```
            - replace `==0.18.1+cu118` to your version.

       

   - метки должны быть в формате .xml с именем объекта = <Text_Box>
      - Пример
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
   - Скрипт будет изменять размеры всех изображений на `(imgsz, imgsz)`, преобразовывать их в оттенки серого, преобразовывать формат меток из `.xml (class_id,cx,cy,h,w)` в `.txt (class_id,x1,y1,x2,y2,x3,y3,x4,y4)`, а затем запустить обучение модели.
   ---
#### Manual train
   - Создавать папки данных
   - Создать структуру папок
      - Создайте `Train` и `Val` в `path\to\train\folder` и `path\to\val\folder`
      - В папке Train создайте папки images и labels.
      - В папке Val создайте папки images и labels.
      - (Необязательно) создайте папку `Test` в `path\to\test\folder`. В папке Test создайте папки images и labels.
   - скопируйте все изображения поездов в `Train\images` и все метки поездов в `Train\labels`
   - скопируйте все изображения val в `Val\images` и все метки val в `Val\labels`
   - (Необязательно) скопируйте все тестовые изображения в `Test\images` и все тестовые метки в `Test\labels`.
   
   - Создать `dataset.yaml` файл
   ```yaml
   # dataset.yaml example
   train: path\to\train\folder # path to train data ( folder with folders images and labels)
   val: path\to\val\folder # path to validate data
   # test: path\to\test\folder # path to test data ( non required )

   # classes
   nc: 1  #  class number
   names: ['tbox']  #  class names
   ```
   - Команда запуска train
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
   - В обучении моделей из [Models](#download-models) использовались параметры `task=obb`, `epoches=100`, and `batch=16`.


