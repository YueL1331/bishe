import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
import os
import numpy as np
from kivy.uix.popup import Popup

from FeatureExtractor import process_image

# 注册中文支持的字体
LabelBase.register(name="Roboto",
                   fn_regular="./NotoSerifSC-Black.otf")

class HostUIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # 打开文件选择器的按钮
        open_file_chooser_button = Button(text='打开文件选择器', size_hint=(1, 0.1), font_name="Roboto")
        open_file_chooser_button.bind(on_press=self.open_file_dialog)
        layout.add_widget(open_file_chooser_button)

        # 提取特征的按钮
        extract_features_button = Button(text='提取特征', size_hint=(1, 0.1), font_name="Roboto")
        extract_features_button.bind(on_press=self.extract_features)
        layout.add_widget(extract_features_button)

        # 创建一个ScrollView，用于展示所选图像
        self.scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=True, do_scroll_y=False)
        self.image_grid = GridLayout(cols=1, size_hint_y=None)
        self.image_grid.bind(minimum_height=self.image_grid.setter('height'))
        self.scroll_view.add_widget(self.image_grid)
        layout.add_widget(self.scroll_view)

        return layout

    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        self.file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if self.file_paths:
            self.display_images()
        root.destroy()

    def display_images(self):
        self.image_grid.clear_widgets()  # 清除之前的图像
        for path in self.file_paths:
            # 为每个图像创建一个Image控件并添加到GridLayout中
            img = Image(source=path, size_hint_y=None, height=200)
            self.image_grid.add_widget(img)

    def extract_features(self, instance):
        if not hasattr(self, 'file_paths') or not self.file_paths:
            self.show_popup("错误", "请先选择文件")
            return

        output_info = []
        for file_path in self.file_paths:
            try:
                features = process_image(file_path)
                features_str = np.array2string(features.cpu().numpy().flatten())
                output_info.append(f'{os.path.basename(file_path)}: {features_str}')
            except Exception as e:
                output_info.append(f'{os.path.basename(file_path)} 错误: {str(e)}')

        self.show_popup("操作完成", "\n".join(output_info))

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    HostUIApp().run()
