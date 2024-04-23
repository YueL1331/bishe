import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from SelectUI import FileSelectionScreen
from data_manager import DataManager
import os

class SelectController:
    def __init__(self, screen):
        self.screen = screen
        self.data_manager = DataManager()

        # 绑定按钮的事件
        self.screen.select_button.bind(on_press=self.handle_folder_selection)

    def handle_folder_selection(self, instance):
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        folder_path = filedialog.askdirectory()  # 显示选择文件夹对话框
        if folder_path:
            self.load_images_from_folder(folder_path)

    def load_images_from_folder(self, folder_path):
        data_manager = DataManager()
        data_manager.clear_images()
        images = []
        for file in os.listdir(folder_path):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder_path, file)
                images.append(full_path)
                data_manager.add_image(full_path)
        self.update_ui(images)

    @mainthread
    def update_ui(self, images):
        self.screen.ids.thumbnail_layout.clear_widgets()
        for img_path in images:
            img = tk.Image(source=img_path, size_hint_y=None, height=100)
            self.screen.ids.thumbnail_layout.add_widget(img)
        if images:
            self.screen.ids.main_image.source = images[0]

if __name__ == '__main__':
    app = SelectApp()
    controller = SelectController(app.root.get_screen('file_selection'))
    app.run()
