import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
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

        # 文件显示标签，用于显示选中的文件路径或操作结果
        self.file_label = Label(text="请选择一个文件", size_hint=(1, 0.8), font_name="Roboto")
        layout.add_widget(self.file_label)

        return layout

    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        self.file_path = filedialog.askopenfilename()  # 显示文件选择对话框
        if self.file_path:
            self.file_label.text = f'选择的文件: {self.file_path}'
        root.destroy()

    def extract_features(self, instance):
        if not hasattr(self, 'file_path') or not self.file_path:
            self.file_label.text = "请先选择一个文件"
            return

        try:
            # 假设 process_image 返回一个特征数组
            features = process_image(self.file_path)
            features_str = np.array2string(features.cpu().numpy().flatten())
            self.file_label.text = f'特征: {features_str}'
        except Exception as e:
            self.file_label.text = f'错误: {str(e)}'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    HostUIApp().run()
