from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# 导入各个功能屏幕
from SelectUI import FileSelectionScreen
# from FeatureExtractorUI import FeatureExtractionScreen
# from SplitUI import ImageStitchingScreen
# from ChooseUI import RegionSelectionScreen

# 注册中文支持的字体
LabelBase.register(name="Roboto", fn_regular="./NotoSerifSC-Black.otf")

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        buttons = [
            ("选择文件", 'file_selection')
            # ("特征向量提取", 'feature_extraction'),
            # ("图像拼接", 'image_stitching'),
            # ("区域选择", 'region_selection')
        ]
        for text, screen_name in buttons:
            btn = Button(text=text)
            btn.bind(on_press=lambda instance, sn=screen_name: self.switch_screen(sn))
            layout.add_widget(btn)
        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(FileSelectionScreen(name='file_selection'))
        # sm.add_widget(FeatureExtractionScreen(name='feature_extraction'))
        # sm.add_widget(ImageStitchingScreen(name='image_stitching'))
        # sm.add_widget(RegionSelectionScreen(name='region_selection'))
        return sm

if __name__ == '__main__':
    MyApp().run()
