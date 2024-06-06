from PIL import Image
import numpy as np
import os


def cut_image(image):
    h, w, _ = image.shape

    # 在水平方向上随机选择切割的高度比例
    cut_height_ratio_horizontal = np.random.uniform(0.2, 0.5)
    cut_height_horizontal = int(h * cut_height_ratio_horizontal)
    cut_top_horizontal = np.random.randint(0, h - cut_height_horizontal)

    # 在垂直方向上随机选择切割的宽度比例
    cut_width_ratio_vertical = np.random.uniform(0.2, 0.5)
    cut_width_vertical = int(w * cut_width_ratio_vertical)
    cut_left_vertical = np.random.randint(0, w - cut_width_vertical)

    # 确保切片中包含非白色部分
    split = image[cut_top_horizontal:cut_top_horizontal + cut_height_horizontal,
            cut_left_vertical:cut_left_vertical + cut_width_vertical, :]
    while np.all(split == 255):
        cut_top_horizontal = np.random.randint(0, h - cut_height_horizontal)
        split = image[cut_top_horizontal:cut_top_horizontal + cut_height_horizontal,
                cut_left_vertical:cut_left_vertical + cut_width_vertical, :]

    return split


# 读取整图
original_image = Image.open(r"F:\毕设\data\data1\原图片\main.png")
original_array = np.array(original_image)

# 创建保存切分图的文件夹
output_folder = r"F:\毕设\data\data1\随机切分图片文件夹"
os.makedirs(output_folder, exist_ok=True)

# 切分整图
min_blocks = 250
splits = []

while len(splits) < min_blocks:
    split = cut_image(original_array)

    # 检查是否包含白色，如果不包含白色且至少包含一个非白色像素，则加入切分列表
    if not np.all(split == 255) and np.any(split != 255):
        splits.append(split)

# 保存切分后的图像
for i, split in enumerate(splits):
    split_image = Image.fromarray(np.uint8(split))
    split_image.save(os.path.join(output_folder, f"split_{i}.png"))
