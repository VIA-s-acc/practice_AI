import flet as ft
import json
import os
import threading

def settings_page(page: ft.Page):
    page.adaptive = True
    page.horizontal_alignment = ft.CrossAxisAlignment.START

    this_directory = os.path.dirname(os.path.abspath(__file__))
    global path_to_model, path_to_img, conf 
    path_to_model = ''
    path_to_img = ''
    conf = 0.5
    

    
    def show_files(e):


        if os.path.exists(this_directory + "/settings.json"):
            with open(this_directory + "/settings.json") as f:
                settings = json.load(f)
                theme = settings["theme"]
                pthtimg = settings["path_to_img"]
                pthtmdl = settings["path_to_model"]
                cnftxt = settings["conf"] * 100

        else:
            theme = page.theme_mode.name
            cnftxt = "Default (50)"
        if pthtimg == '':
            pthtimg = 'No file selected'
        if pthtmdl == '':
            pthtmdl = 'No file selected'
        def hide_text():
            try:
                show_text.value = ""
                show_text.update()
                try:
                    page.remove(image_container)
                except:
                    pass
            except:
                pass

        threading.Timer(3, hide_text).start()
        if pthtimg != 'No file selected':
            image = ft.Image(src=pthtimg, fit = ft.ImageFit.CONTAIN)
            image_container = ft.Container(
                content=image, width=page.window.width*1, height=page.window.height*0.6, alignment= ft.alignment.center, visible=True,  expand=True
            )
            page.add(image_container)
        show_text.value = f"Theme: {theme}\nPath to image: {pthtimg}\nPath to model: {pthtmdl}\nConfidence: {cnftxt}"
        show_text.update()
    
    
    
    
    def save_settings(e, path_to_model = path_to_model, path_to_img = path_to_img, conf = conf):
        with open( this_directory + "/settings.json", "w") as f:
            json.dump({"theme": page.theme_mode.name, 'path_to_model': path_to_model, 'path_to_img': path_to_img, "conf": conf}, f)

    def save(e):
        global path_to_model, path_to_img, conf
        save_settings(e, path_to_model, path_to_img, conf/100)

    async def change_theme(e):
        if theme_checkbox.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        save_settings(e, path_to_model, path_to_img, conf/100)
        page.update()

    theme_checkbox = ft.Checkbox(label="Dark theme", value=False, on_change=change_theme)
    model_file_select = ft.FilePicker(on_result=lambda e: path_to_model)
    img_file_select = ft.FilePicker(on_result=lambda e: path_to_img)
    save_button = ft.ElevatedButton("Save", on_click=save)
    show_button = ft.ElevatedButton("Show", on_click=show_files)

    if os.path.exists(this_directory + "/settings.json"):
        with open( this_directory + "/settings.json" ) as f:
            settings = json.load(f)
            theme = settings["theme"]
            if theme == "DARK":
                theme_checkbox.value = True
            else:
                theme_checkbox.value = False
            path_to_img = settings["path_to_img"]
            path_to_model = settings["path_to_model"]
            conf = settings["conf"] * 100
    else:
        theme_checkbox.value = False
        

    page.add(ft.Text("Settings"))
    page.add(theme_checkbox)
    def pick_models_result(e: ft.FilePickerResultEvent):
        selected_file_model.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        ) 
        if e.files is not None:
            if not (e.files[0].path.endswith('keras') or e.files[0].path.endswith('k5') or e.files[0].path.endswith('pt') or e.files[0].path.endswith('onnx')):
                    selected_file_model.value = "Only .keras, .k5, .pt, .onnx files are allowed"
                    selected_file_model.update()
                    return
        selected_file_model.update()
        if e.files is None:
            return
        global path_to_model
        path_to_model = e.files[0].path

    def change_conf(e):
        global conf
        conf_text.value = "Confidence: " + str(e.control.value)
        conf_text.update()
        conf = e.control.value

    
    def pick_img_result(e: ft.FilePickerResultEvent):
        selected_file_img.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        if e.files is not None:
            if not (e.files[0].path.endswith('jpg') or e.files[0].path.endswith('png') or e.files[0].path.endswith('jpeg') or e.files[0].path.endswith('mp4')):
                    selected_file_img.value = "Only .jpg, .png, .jpeg, .mp4 files are allowed"
                    selected_file_img.update()
                    return
        selected_file_img.update()
        if e.files is None:
            return
        global path_to_img
        path_to_img = e.files[0].path

    model_file_select = ft.FilePicker(on_result=pick_models_result)
    img_file_select = ft.FilePicker(on_result=pick_img_result)
    conf_input = ft.Slider(min=0, max=100, value = conf, divisions=100, on_change=change_conf, expand=True, label = "Confidence: {value}%", adaptive=True, height=page.window.height*0.025, width=page.window.width*0.25)
    selected_file_model = ft.Text(path_to_model)
    selected_file_img = ft.Text(path_to_img)
    

    page.overlay.append(model_file_select)
    page.overlay.append(img_file_select)

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick model",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: model_file_select.pick_files(
                        allow_multiple=False
                    ), adaptive=True
                ),
                selected_file_model,
            ],
        )
    )

    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Pick image",   
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: img_file_select.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_file_img,
            ],
        )
    )
    conf_text = ft.Text("Confidence: " + str(conf))
    page.add(ft.Column([conf_text, conf_input, ], spacing = 10))
    page.add(save_button)
    page.add(show_button)
    show_text = ft.Text('')
    page.add(show_text)



