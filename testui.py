#:kivy 2.3.0


import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

# 设定模型和设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=True).to(device)
model.eval()

# 图像转换
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class FeatureExtractor(torch.nn.Module):
    def __init__(self, model):
        super(FeatureExtractor, self).__init__()
        self.model = model
        self.selected_layers = ['layer1', 'layer2', 'layer3', 'layer4']

    def forward(self, x, layers):
        outputs = {}
        for name, layer in self.model.named_children():
            x = layer(x)
            if name in layers:
                outputs[name] = x.detach()  # 使用detach()来避免计算图的保存
            if all(layer in outputs for layer in layers):
                break
        return outputs

# 创建特征提取器实例
extractor = FeatureExtractor(model)

class FeatureExtractorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # 文件选择器
        self.file_chooser = FileChooserIconView()
        self.file_chooser.bind(on_selection=self.update_output_folder)
        layout.add_widget(self.file_chooser)

        # 提取特征按钮
        extract_button = Button(text="提取特征", size_hint=(1, None), height=50)
        extract_button.bind(on_press=self.extract_features)
        layout.add_widget(extract_button)

        return layout

    def update_output_folder(self, instance, selection):
        if selection:
            selected_folder = selection[0]
            self.output_folder = os.path.join(selected_folder, "FeatureVector")

    def extract_features(self, instance):
        if not hasattr(self, 'output_folder'):
            self.show_popup("错误", "请先选择一个文件")
            return

        selected_files = self.file_chooser.selection
        if not selected_files:
            self.show_popup("错误", "请先选择一个文件")
            return

        # 创建输出文件夹
        os.makedirs(self.output_folder, exist_ok=True)

        # 处理每张图像
        for image_path in selected_files:
            if image_path.lower().endswith('.png'):  # 确保仅处理以.png结尾的文件
                img = Image.open(image_path).convert('RGB')
                img_t = transform(img).unsqueeze(0).to(device)

                # 提取特征
                features = extractor(img_t, ['layer1', 'layer2', 'layer3', 'layer4'])

                # 保存特征向量到文本文件，每个层的输出在单独的文件夹中
                for layer_name, feature in features.items():
                    layer_output_folder = os.path.join(self.output_folder, layer_name)
                    os.makedirs(layer_output_folder, exist_ok=True)  # 确保层的文件夹存在
                    output_path = os.path.join(layer_output_folder, f"{os.path.basename(image_path)[:-4]}.txt")  # 移除'.png'并添加'.txt'
                    with open(output_path, 'w') as f:
                        f.write(f"{feature.flatten().tolist()}\n")

        self.show_popup("提取完成", "特征提取完成")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    FeatureExtractorApp().run()
