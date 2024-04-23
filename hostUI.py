import os
import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from FeatureExtractor import process_image, save_features  # 确保这些功能模块已正确实现

# 注册中文支持的字体
LabelBase.register(name="Roboto", fn_regular="./NotoSerifSC-Black.otf")

class HostUIApp(App):
    def __init__(self, **kwargs):
        super(HostUIApp, self).__init__(**kwargs)
        self.file_paths = []  # 初始化文件路径列表

    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        # 图像显示区域
        image_display_layout = BoxLayout(orientation='horizontal', size_hint_y=0.75)
        self.main_image = Image()
        image_display_layout.add_widget(self.main_image)

        # 右侧缩略图和控制按钮区域
        control_and_thumbnail_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
        # 打开文件选择器按钮
        open_file_chooser_button = Button(text='选择图像文件或文件夹')
        open_file_chooser_button.bind(on_press=self.open_file_dialog)
        control_and_thumbnail_layout.add_widget(open_file_chooser_button)

        # 缩略图的滚动视图
        self.scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.thumbnail_grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.thumbnail_grid.bind(minimum_height=self.thumbnail_grid.setter('height'))
        self.scroll_view.add_widget(self.thumbnail_grid)
        control_and_thumbnail_layout.add_widget(self.scroll_view)

        image_display_layout.add_widget(control_and_thumbnail_layout)
        main_layout.add_widget(image_display_layout)

        # 功能按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        # 特征向量处理按钮
        feature_button = Button(text='特征向量处理')
        feature_button.bind(on_press=self.handle_feature_extraction)
        button_layout.add_widget(feature_button)

        # 拼接图像按钮
        stitch_button = Button(text='拼接图像')
        button_layout.add_widget(stitch_button)

        # 区域选择按钮
        region_button = Button(text='区域选择')
        button_layout.add_widget(region_button)

        main_layout.add_widget(button_layout)

        return main_layout

    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()
        paths = filedialog.askopenfilenames(title="Select Images or Folder", filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")])
        if paths:
            self.file_paths = []  # 清空现有列表
            for path in paths:
                if os.path.isdir(path):
                    # 如果是文件夹，则列出文件夹中的所有图像文件
                    dir_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]
                    self.file_paths.extend(dir_files)
                elif path.endswith(('.jpg', '.jpeg', '.png')):
                    self.file_paths.append(path)
            self.display_thumbnails()
        root.destroy()

    def display_thumbnails(self):
        self.thumbnail_grid.clear_widgets()
        for path in self.file_paths:
            thumbnail_container = FloatLayout(size_hint_y=None, height=100)
            img_btn = Button(background_normal=path, size_hint=(1, 1))
            img_btn.bind(on_release=lambda instance, path=path: self.set_main_image(path))
            thumbnail_container.add_widget(img_btn)
            self.thumbnail_grid.add_widget(thumbnail_container)

    def set_main_image(self, path):
        self.main_image.source = path

    def handle_feature_extraction(self, instance):
        if not self.file_paths:
            self.show_popup("错误", "请先选择一个图像")
            return

        for file_path in self.file_paths:
            features = process_image(file_path)
            save_features(file_path, features)
        self.show_popup("成功", "特征已保存到 FeatureExtractor 文件夹")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(300, 200))
        popup.open()

if __name__ == '__main__':
    HostUIApp().run()
