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
        # 使用Tkinter的文件夹选择对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        folder_path = filedialog.askdirectory()  # 显示选择文件夹对话框
        if folder_path:
            self.load_images_from_folder(folder_path)
        root.destroy()  # 关闭Tkinter窗口

    def load_images_from_folder(self, folder_path):
        # 加载文件夹中的所有图像文件
        for file in os.listdir(folder_path):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder_path, file)
                self.data_manager.add_images([full_path])
        self.screen.update_thumbnails(self.data_manager.get_images())
        if self.data_manager.get_images():
            self.screen.update_main_image(self.data_manager.get_images()[0])

    def handle_delete_thumbnail(self, instance):
        path = instance.path  # 需要确保这个属性存在
        self.data_manager.remove_image(path)
        self.screen.update_thumbnails(self.data_manager.get_images())

if __name__ == '__main__':
    app = App.get_running_app()
    controller = SelectController(app.root.get_screen('file_selection'))
    app.run()
