import os

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import tkinter as tk
from tkinter import filedialog
from data_manager import DataManager

class FileSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(FileSelectionScreen, self).__init__(**kwargs)
        # 主布局分为左侧边栏和右侧内容区
        main_layout = BoxLayout(orientation='horizontal')

        # 左侧边栏
        sidebar = BoxLayout(orientation='vertical', size_hint_x=0.1)
        home_button = Button(text='首页')
        home_button.bind(on_press=self.go_home)
        sidebar.add_widget(home_button)
        main_layout.add_widget(sidebar)

        # 右侧内容区
        content_layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserIconView(filters=['*.jpg', '*.jpeg', '*.png'], multiselect=True, size_hint_y=None, height=0)
        content_layout.add_widget(self.filechooser)

        self.select_button = Button(text='选择图像')
        content_layout.add_widget(self.select_button)

        self.main_image = Image(size_hint_y=0.8)
        content_layout.add_widget(self.main_image)

        self.thumbnail_view = ScrollView(size_hint_y=0.2, do_scroll_x=True)
        self.thumbnail_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.thumbnail_view.add_widget(self.thumbnail_layout)
        content_layout.add_widget(self.thumbnail_view)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def go_home(self, instance):
        # 此方法假设存在一个名为 'home' 的屏幕
        self.manager.current = 'home'

class SelectApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.file_selection_screen = FileSelectionScreen(name='file_selection')
        self.screen_manager.add_widget(self.file_selection_screen)
        return self.screen_manager

    def on_start(self):
        self.controller = SelectController(self.file_selection_screen)

class SelectController:
    def __init__(self, screen):
        self.screen = screen
        self.data_manager = DataManager()
        self.screen.select_button.bind(on_press=self.handle_folder_selection)

    def handle_folder_selection(self, instance):
        # 使用Tkinter的文件夹选择对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        folder_path = filedialog.askdirectory()  # 显示选择文件夹对话框
        if folder_path:
            self.load_images_from_folder(folder_path)
        root.destroy()  # 关闭Tkinter窗口

    def load_images_from_folder(self, folder_path):
        # 加载文件夹中的所有图像文件
        self.data_manager.clear_images()
        for file in os.listdir(folder_path):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder_path, file)
                self.data_manager.add_image(full_path)
        self.screen.update_thumbnails(self.data_manager.get_images())
        if self.data_manager.get_images():
            self.screen.update_main_image(self.data_manager.get_images()[0])

if __name__ == '__main__':
    SelectApp().run()
