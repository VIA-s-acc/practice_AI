import flet as ft
import os 
import json
import threading
import subprocess
import asyncio
import re
import pyperclip
from .utils.Tbox import TboxGenerator


def main_page(page: ft.Page):

    page.adaptive = True
    this_path = os.path.dirname(os.path.abspath(__file__))
    path_to_img = ''
    path_to_model = ''
    path_to_model_line = ''
    info_text1 = ft.Text('')
    info_text2 = ft.Text('')
    conf_text = ft.Text('')
    not_found_text = ft.Text('Model LineDetector not found ;(')
    error_text = ft.Text('Something went wrong. Please check your settings and try again. Change paths to models and image if you have cyrillic symbols in them.')
    if os.path.exists(os.path.dirname(this_path) + "\\Settings\\settings.json"):
        with open(os.path.dirname(this_path) + "\\Settings\\settings.json") as f:
            settings = json.load(f)
            path_to_model = settings["path_to_model"]
            path_to_img = settings["path_to_img"]
            path_to_model_line = settings["path_to_model_line"]
            conf = settings["conf"]
    else:
        path_to_model = ''
        path_to_img = ''
        path_to_model_line = ''


    def hide_text1():
        try:
            info_text1.value = ""
            info_text1.update()
        except:
            pass
    
    def hide_text2():
        try:
            info_text2.value = ""
            info_text2.update()
        except:
            pass

    async def process(e):
        for i in page.controls:
            if i.key == "selection":
                page.remove(i)
        page.add(info_text1)
        page.add(info_text2)
        page.add(conf_text)
        exit = False
        try:
            page.remove(process_button)
            page.update()
        except:
            pass

        try:
            page.remove(selection)
            page.update()
        except:
            pass
        
        if path_to_img == '':
            info_text1.value = 'No image selected | Select Image in Settings'
            info_text1.update()
            exit = True
            threading.Timer(3, hide_text1).start()
            
        if path_to_model == '':
            info_text2.value = 'No model selected | Select Model in Settings'
            info_text2.update()
            exit = True
            threading.Timer(3, hide_text2).start()
            
        if exit:
            return 
        
        info_text1.value = "Selected Image: " + path_to_img
        info_text1.update()
        info_text2.value = "Selected Model: " + path_to_model
        info_text2.update()
        conf_text.value = "Confidence: " + str(conf)
        conf_text.update()
        pr_text = ft.Text("Processing... ( Please dont close this page )")
        pr = ft.Column([ft.ProgressRing(scale = 0.5, height=page.window.height* 0.5, width = page.window.width * 0.5, stroke_align=1, stroke_cap=5, stroke_width=20), pr_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing = 10)
        page.add(pr)
        page.update()
        await asyncio.sleep(0.1)
        
        res = subprocess.run(["yolo", "task=obb", "mode=predict", f"model={path_to_model}", f"conf={conf}", f"source={path_to_img}", "line_width=5", "save_txt=true"], shell=True, capture_output=True, text=True)
        results_saved_pattern = r'Results saved to (.+)'
        labels_saved_pattern = r'label saved to (.+)'
        match_results_saved = re.search(results_saved_pattern, res.stdout)
        match_labels_saved = re.search(labels_saved_pattern, res.stdout)
        results_saved_path = ''
        labels_saved_path = '' 
        if match_results_saved:
            results_saved = match_results_saved.group(1)
            labels_saved = match_labels_saved.group(1)
            filename = os.path.basename(path_to_img).split('.')[0]
            info_text1.value = "Results saved to: " + results_saved[4:len(results_saved)-4] + '\\' + os.path.basename(path_to_img)
            info_text1.update()
            info_text2.value = "Labels saved to: " + labels_saved + '\\' + os.path.basename(path_to_img)
            info_text2.update()
            results_saved_path = results_saved[4:len(results_saved)-4] + '\\' + os.path.basename(path_to_img)
            labels_saved_path = labels_saved + '\\' + filename + '.txt'
        help_text = ft.Text("Click 'Image' Button to see image\nClick 'Labels' Button to see labels\nClick 'New' Button to new process\nClick 'Lines' Button to see lines\nClick 'Help' Button to see help\nAll results and labels will be saved BaseDir\\runs\\detect\\predict* folder", italic=True)
        image_container = ft.Container(ft.Image(src=results_saved_path, fit=ft.ImageFit.CONTAIN), width=page.width, height=page.height*0.6, visible=True, expand= True)
        cl = ft.Column(spacing = 0.1, height= 0.5 * page.window.height, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=page.window.width * 1, scroll = ft.ScrollMode.ALWAYS)
        cl_img = ft.Column(spacing = 0.5, height= 0.5 * page.window.height, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=page.window.width * 1, scroll = ft.ScrollMode.ALWAYS)
        
        labels = ''
        if os.path.exists(labels_saved_path):
            with open(labels_saved_path, 'r') as f:
                for line in f:
                    cl.controls.append(ft.Text(line, key = line))
                    labels += line
        else:
            cl.controls.append(ft.Text("No labels found"))
            with open(labels_saved_path, 'w') as f:
                f.write("No labels found")

        labels_container = ft.Container(cl, width=page.width, height=page.height*0.6, visible=True, expand= True)
        roi_container = ft.Container(cl_img, width=page.width, height=page.height*0.6, visible=True, expand= True)
            

        def copy_to_clipboard(e):
            def copy_text_del():
                page.remove(copy_text)
                page.update
            try:
                pyperclip.copy(labels)
                copy_text = ft.Text("Copied to clipboard :)", color="green", italic = True, size=15)
                page.add(copy_text)
                page.update()
                threading.Timer(1, copy_text_del).start()
            except:
                pass
        copy_button = ft.IconButton(ft.icons.COPY, on_click=copy_to_clipboard)
        global first_flag
        first_flag = True
        
        async def show(e):
            def try_remove(something):
                try:
                    page.remove(something)
                except:
                    pass
                
            
            def clear(e):
                try_remove(info_text1)
                try_remove(info_text2)
                try_remove(conf_text)
                try_remove(conf)
                try_remove(help_text)
                try_remove(image_container)
                try_remove(labels_container)
                try_remove(process_button)
                try_remove(copy_button)
                try_remove(roi_container)
                try_remove(not_found_text)
                try_remove(error_text)
                page.update()
        
            try:
                k = e.data[2]
            except:
                return
            
            if e.data[2] == '5':
                clear(e)
                page.add(help_text)
                page.update()
                return
            
            if e.data[2] == '4':
                clear(e)
                if path_to_model_line != '':
                    count = 0
                    indx = 1
                    page.add(pr)
                    pr_text.value = "Extracting boxes... "
                    pr.update() 
                    await asyncio.sleep(0.1)
                    try:
                        saved = TboxGenerator(path_to_img=path_to_img, path_to_labels=labels_saved_path, path_to_save=match_labels_saved.group(1)+'\\tbox\\', mode = 'OBB').generate()
                        paths = []
                        
                        #Useless code 
                        """   
                        if saved == False:
                            def remove_label_text():
                                try_remove(label_not_found_text)
                                page.update()
                            page.remove(pr)
                            label_not_found_text = ft.Text("No labels found", color="red", italic = True, size=15)
                            page.add(label_not_found_text)
                            threading.Timer(2, remove_label_text).start()
                            return
                        """
                        if os.path.exists(saved):
                            for file in os.listdir(saved):
                                count += 1       
                            pr_text.value = f'Extracting lines... Boxes extraction : {indx}\\{count}'
                            pr.update()
                            for file in os.listdir(saved):
                                if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg'): 
                                    file_path = saved + "\\" + file
                                    await asyncio.sleep(0.1)                           
                                    res = subprocess.run(["yolo", "task=obb", "mode=predict", f"model={path_to_model_line}", f"conf={conf}", f"source={file_path}", "line_width=1", "save_txt=true"], shell=True, capture_output=True, text=True)
                                    result_saved_at = None
                                    if re.search(results_saved_pattern, res.stdout) is not None:
                                        result_saved_at = re.search(results_saved_pattern, res.stdout).group(1)
                                    if result_saved_at == None:
                                        continue
                                    indx+=1
                                    pr_text.value = f'Extracting lines... Boxes extraction : {indx}\\{count}'
                                    pr.update()
                                    paths.append(result_saved_at[4:len(result_saved_at)-4] + '\\' + file)
                        cl_img.controls.clear()
                        for path in paths:
                            cl_img.controls.append(ft.Image(src=path, fit=ft.ImageFit.CONTAIN))
                            
                        page.remove(pr)
                        pr_text.value = f'Processing... ( Please dont close this page )'
                        page.add(roi_container)
                        page.update()
                    except:
                        try_remove(pr)
                        page.add(error_text)
                else:
                    page.add(not_found_text)
                    page.update()
                return
            
            if e.data[2] == '1':
                clear(e)
                page.add(image_container)
                page.update()
                return
            
            if e.data[2] == '2':
                clear(e)
                page.add(copy_button)
                page.add(labels_container)
                page.update()
                return
            if e.data[2] == '3':
                clear(e)
                page.add(process_button)
                page.update()
                return
        
            
        class fcall:
            def __init__(self):
                self.data = "001"
        
        selection = ft.SegmentedButton(
            on_change=show,
            selected_icon=ft.Icon(ft.icons.SELECT_ALL),
            allow_multiple_selection=False,
            allow_empty_selection=True,
            selected = ["1"],
            segments=[
                ft.Segment(
                    value="1",
                    label=ft.Text("Image"),
                    icon=ft.Icon(ft.icons.IMAGE),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("Labels"),
                    icon=ft.Icon(ft.icons.LABEL),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("New"),
                    icon=ft.Icon(ft.icons.NEW_LABEL),
                ),
                ft.Segment(
                    value="4",
                    label=ft.Text("Lines"),
                    icon=ft.Icon(ft.icons.LINE_AXIS),
                ),
                ft.Segment(
                    value="5",
                    label=ft.Text("Help"),
                    icon=ft.Icon(ft.icons.HELP),
                ),
            ],
            key = 'selection',
        )
        page.add(selection)
        if first_flag:
            await show(fcall())
            first_flag = False
        page.update()
        page.remove(pr)
        page.update()


    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    process_button = ft.ElevatedButton("Process", on_click=process)
    page.add(process_button)
    



    