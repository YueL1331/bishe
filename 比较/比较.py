import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def calculate_feature_match_ratio(stitched_image_path, original_image_path):
    stitched_image = cv2.imread(stitched_image_path)
    original_image = cv2.imread(original_image_path)

    if stitched_image is None or original_image is None:
        raise FileNotFoundError("One or both image paths are incorrect or the images do not exist.")

    gray_stitched = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
    gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    keypoints_stitched, descriptors_stitched = orb.detectAndCompute(gray_stitched, None)
    keypoints_original, descriptors_original = orb.detectAndCompute(gray_original, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_stitched, descriptors_original)

    num_matches = len(matches)
    num_keypoints_stitched = len(keypoints_stitched)
    match_ratio = num_matches / num_keypoints_stitched if num_keypoints_stitched > 0 else 0

    return match_ratio, num_matches, num_keypoints_stitched


def process_images_in_directory(directory_path, original_image_path):
    results = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                stitched_image_path = os.path.join(root, file)
                try:
                    match_ratio, num_matches, num_keypoints_stitched = calculate_feature_match_ratio(
                        stitched_image_path, original_image_path)
                    results.append({
                        'image_name': stitched_image_path,
                        'match_ratio': match_ratio,
                        'num_matches': num_matches,
                        'num_keypoints_stitched': num_keypoints_stitched
                    })
                except FileNotFoundError as e:
                    print(e)

    return results


def plot_results(results, save_path):
    layer_data = {}
    batch_step_data = {}

    for result in results:
        file_name = os.path.basename(result['image_name'])
        parts = file_name.replace('.png', '').split('_')
        layer = parts[0]  # 'layer1'
        batch = int(parts[1])  # 10
        step = int(parts[2])  # 10

        if layer not in layer_data:
            layer_data[layer] = []
        layer_data[layer].append(result)

        batch_step_key = (batch, step)
        if batch_step_key not in batch_step_data:
            batch_step_data[batch_step_key] = []
        batch_step_data[batch_step_key].append(result)

    # 绘制 layer 之间的匹配比率图
    plt.figure()
    for layer, results in layer_data.items():
        ratios = [res['match_ratio'] for res in results]
        indices = range(len(ratios))
        plt.plot(indices, ratios, label=layer)
        mean_ratio = np.mean(ratios)
        plt.axhline(y=mean_ratio, color=plt.gca().lines[-1].get_color(), linestyle='--')
        for i, res in zip(indices, results):
            plt.text(i, res['match_ratio'], os.path.basename(res['image_name']), fontsize=8)
    plt.xlabel('Image Index')
    plt.ylabel('Match Ratio')
    plt.title('Match Ratio by Layer')
    plt.legend()
    plt.savefig(os.path.join(save_path, 'layer_match_ratio.png'))
    plt.show()

    # 绘制 batch size 和 step size 之间的匹配比率图
    plt.figure()
    for (batch, step), results in batch_step_data.items():
        ratios = [res['match_ratio'] for res in results]
        indices = range(len(ratios))
        plt.plot(indices, ratios, label=f'Batch {batch}, Step {step}')
        mean_ratio = np.mean(ratios)
        plt.axhline(y=mean_ratio, color=plt.gca().lines[-1].get_color(), linestyle='--')
        for i, res in zip(indices, results):
            plt.text(i, res['match_ratio'], os.path.basename(res['image_name']), fontsize=8)
    plt.xlabel('Image Index')
    plt.ylabel('Match Ratio')
    plt.title('Match Ratio by Batch Size and Step Size')
    plt.legend()
    plt.savefig(os.path.join(save_path, 'batch_step_match_ratio.png'))
    plt.show()

    # 打印相似度最高的图像名称
    max_match_ratio = max([result['match_ratio'] for result in results])
    highest_similarity_images = [result['image_name'] for result in results if result['match_ratio'] == max_match_ratio]

    print("Images with the highest similarity:")
    for image in highest_similarity_images:
        print(image)


# 示例
directory_path = r'D:\Git\bishe\api\stitched_images'
original_image_path = r'D:\bishe\data\data1\local\main.png'
save_path = r'.'  # 将图像保存在当前代码运行的文件夹中

results = process_images_in_directory(directory_path, original_image_path)

# 打印相似度最高的图像名称
max_match_ratio = max([result['match_ratio'] for result in results])
highest_similarity_images = [result['image_name'] for result in results if result['match_ratio'] == max_match_ratio]

print("Images with the highest similarity:")
for image in highest_similarity_images:
    print(image)

# 绘制图表并保存
plot_results(results, save_path)
