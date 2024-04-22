from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.text import LabelBase
import os
import numpy as np
from FeatureExtractor import process_image

# 注册中文支持的字体
LabelBase.register(name="Roboto",
                   fn_regular="./NotoSerifSC-Black.otf")

class HostUIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # 打开文件选择器的按钮
        open_file_chooser_button = Button(text='打开文件选择器', size_hint=(1, 0.1), font_name="Roboto")
        open_file_chooser_button.bind(on_press=self.open_file_chooser)
        layout.add_widget(open_file_chooser_button)

        # 提取特征值的按钮
        extract_button = Button(text='提取特征值', size_hint=(1, 0.1), font_name="Roboto")
        extract_button.bind(on_press=self.on_extract_features)
        layout.add_widget(extract_button)

        return layout

    def open_file_chooser(self, instance):
        # 创建文件选择器
        self.file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])

        # 创建弹出窗口用于文件选择
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(self.file_chooser)

        # 添加返回按钮
        back_button = Button(text='返回', size_hint=(1, 0.1))
        back_button.bind(on_press=lambda x: self.popup.dismiss())
        popup_layout.add_widget(back_button)

        # 创建并显示弹出窗口
        self.popup = Popup(title='选择文件', content=popup_layout,
                           size_hint=(0.9, 0.9), title_font="Roboto", auto_dismiss=False)
        self.popup.open()

    def on_extract_features(self, instance):
        selected_files = self.file_chooser.selection
        if not selected_files:
            self.show_popup("错误", "未选择任何文件")
            return

        base_folder = os.path.dirname(selected_files[0])
        output_folder = os.path.join(base_folder, 'FeatureExtractor')
        os.makedirs(output_folder, exist_ok=True)

        for image_path in selected_files:
            features = process_image(image_path)
            for layer_name, feature in features.items():
                layer_output_folder = os.path.join(output_folder, layer_name)
                os.makedirs(layer_output_folder, exist_ok=True)
                output_path = os.path.join(layer_output_folder, os.path.basename(image_path).split('.')[0] + '.txt')
                np.savetxt(output_path, feature.cpu().numpy().flatten())

        self.show_popup("操作完成", "特征提取完成")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    HostUIApp().run()
