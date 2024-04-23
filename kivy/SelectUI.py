from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class FileSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(FileSelectionScreen, self).__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='horizontal')

        # 创建按钮和其他UI元素，并将它们存储为类的属性
        self.sidebar = BoxLayout(orientation='vertical', size_hint_x=0.1)
        self.home_button = Button(text='首页')
        self.sidebar.add_widget(self.home_button)

        self.content_layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserIconView(filters=['*.jpg', '*.jpeg', '*.png'], multiselect=True, size_hint_y=None)
        self.content_layout.add_widget(self.filechooser)

        self.select_button = Button(text='选择图像')
        self.content_layout.add_widget(self.select_button)

        self.main_image = Image(size_hint_y=0.8)
        self.content_layout.add_widget(self.main_image)

        self.thumbnail_view = ScrollView(size_hint_y=0.2, do_scroll_x=True)
        self.thumbnail_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.thumbnail_view.add_widget(self.thumbnail_layout)
        self.content_layout.add_widget(self.thumbnail_view)

        self.main_layout.add_widget(self.sidebar)
        self.main_layout.add_widget(self.content_layout)
        self.add_widget(self.main_layout)

class SelectApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FileSelectionScreen(name='file_selection'))
        return sm

if __name__ == '__main__':
    SelectApp().run()
