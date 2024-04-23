import tkinter as tk
from tkinter import filedialog
import os
from kivy.app import App
from SelectUI import FileSelectionScreen
from data_manager import DataManager  # 确保已经存在此类

class SelectController:
    def __init__(self, screen):
        self.screen = screen
        self.data_manager = DataManager()

        # 绑定按钮的事件
        self.screen.select_button.bind(on_press=self.handle_folder_selection)

    def handle_folder_selection(self, instance):
        # 使用 Tkinter 文件夹选择对话框
        root = tk.Tk()
        root.withdraw()  # 隐藏Tkinter主窗口
        folder_path = filedialog.askdirectory()  # 显示选择文件夹对话框
        if folder_path:
            self.load_images_from_folder(folder_path)  # 加载文件夹中的图像
        root.destroy()  # 关闭Tkinter窗口

    def load_images_from_folder(self, folder_path):
        # 加载文件夹中的所有图像文件
        new_images = []
        for file in os.listdir(folder_path):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(folder_path, file)
                new_images.append(full_path)
        self.data_manager.add_images(new_images)  # 添加到数据管理器
        self.screen.update_thumbnails(self.data_manager.get_images())  # 更新缩略图
        if self.data_manager.get_images():
            self.screen.update_main_image(self.data_manager.get_images()[0])  # 设置主图像

    def handle_delete_thumbnail(self, instance):
        path = instance.background_normal  # 使用背景作为图像路径
        self.data_manager.remove_image(path)  # 从数据管理器中移除
        self.screen.update_thumbnails(self.data_manager.get_images())  # 更新缩略图

# 通过运行Kivy App并在启动时初始化SelectController
if __name__ == '__main__':
    app = App.get_running_app()  # 获取当前运行的应用
    controller = SelectController(app.root.get_screen('file_selection'))  # 初始化控制器
    app.run()  # 运行应用
