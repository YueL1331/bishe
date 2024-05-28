import os
import cv2


def calculate_feature_match_ratio(stitched_image_path, original_image_path):
    # 读取拼接图像和原图
    stitched_image = cv2.imread(stitched_image_path)
    original_image = cv2.imread(original_image_path)

    if stitched_image is None or original_image is None:
        raise FileNotFoundError("One or both image paths are incorrect or the images do not exist.")

    # 转换为灰度图像
    gray_stitched = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
    gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # 使用ORB检测关键点和描述符
    orb = cv2.ORB_create()
    keypoints_stitched, descriptors_stitched = orb.detectAndCompute(gray_stitched, None)
    keypoints_original, descriptors_original = orb.detectAndCompute(gray_original, None)

    # 使用Brute-Force匹配器进行匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_stitched, descriptors_original)

    # 计算匹配点数量
    num_matches = len(matches)

    # 计算拼接图像特征点的数量
    num_keypoints_stitched = len(keypoints_stitched)

    # 计算匹配点在原图中的占比
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


# 示例
directory_path = r'D:\Git\bishe\api\stitched_images'
original_image_path = r'D:\bishe\data\data1\local\main.png'

results = process_images_in_directory(directory_path, original_image_path)

# 打印结果
for result in results:
    print(f"Image Name: {result['image_name']}")
    print(f"Match Ratio: {result['match_ratio']:.2f}")
    print(f"Number of Matches: {result['num_matches']}")
    print(f"Number of Keypoints in Stitched Image: {result['num_keypoints_stitched']}")
    print()
