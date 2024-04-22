from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.text import LabelBase

# 注册中文支持的字体
LabelBase.register(name="Roboto",
                   fn_regular="NotoSerifSC-Black.otf")

class HostUIApp(App):
    def build(self):
        # 主布局
        layout = BoxLayout(orientation='vertical')

        # 打开文件选择器的按钮
        open_file_chooser_button = Button(text='打开文件选择器', size_hint=(1, 0.1), font_name="Roboto")
        open_file_chooser_button.bind(on_press=self.open_file_chooser)
        layout.add_widget(open_file_chooser_button)

        # 提取特征值的按钮
        extract_button = Button(text='提取特征值', size_hint=(1, 0.1), font_name="Roboto")
        layout.add_widget(extract_button)

        # 拼接图像的按钮
        stitch_button = Button(text='拼接图像', size_hint=(1, 0.1), font_name="Roboto")
        layout.add_widget(stitch_button)

        return layout

    def open_file_chooser(self, instance):
        # 文件选择器
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])

        # 弹出窗口布局
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(filechooser)

        # 添加返回按钮
        back_button = Button(text='返回', size_hint=(1, 0.1))
        back_button.bind(on_press=lambda x: self.popup.dismiss())  # 绑定返回事件，只是隐藏Popup
        popup_layout.add_widget(back_button)

        # 创建弹出窗口
        self.popup = Popup(title='选择文件', content=popup_layout,
                           size_hint=(0.9, 0.9), title_font="Roboto", auto_dismiss=False)
        self.popup.open()

if __name__ == '__main__':
    HostUIApp().run()
