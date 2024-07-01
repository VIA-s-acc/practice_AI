import flet as ft
from Settings.settings import settings_page
from Main.main_page import main_page
import os
import json

def main(page: ft.Page):
    page.adaptive = True
    this_directory = os.path.dirname(os.path.abspath(__file__))
    page.adaptive = True
    if os.path.exists(this_directory+"/Settings/settings.json"):
        with open(this_directory+"/Settings/settings.json" ) as f:
            settings = json.load(f)
            theme = settings["theme"]
            if theme == "DARK":
                page.theme_mode = ft.ThemeMode.DARK
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()
    page.appbar = ft.AppBar(
        title=ft.Text("TboxRec"),
    )

    def on_navigation_change(e):
        page.controls.clear()
        if e.control.selected_index == 0:
            main_page(page)
        elif e.control.selected_index == 1:
            settings_page(page)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.HOME, label="Main"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
        border=ft.Border(
            top=ft.BorderSide(color=ft.cupertino_colors.SYSTEM_GREY2, width=0)
        ),
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
        animation_duration=1000,
        selected_index=0,
        on_change=on_navigation_change,
    )

    main_page(page)
    page.update()

ft.app(target=main)
