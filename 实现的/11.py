import cv2
import os


def load_images_from_folder_in_batches(folder, batch_size=15):
    filenames = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    for i in range(0, len(filenames), batch_size):
        batch = filenames[i:i + batch_size]
        images = [cv2.imread(img) for img in batch if cv2.imread(img) is not None]
        yield images


def stitch_images(images):
    # 创建 Stitcher 对象
    stitcher = cv2.Stitcher_create() if hasattr(cv2, 'Stitcher_create') else cv2.createStitcher()

    # 执行图像拼接
    status, stitched = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        return stitched
    else:
        print(f"Stitching failed with status: {status}")
        return None


if __name__ == "__main__":
    folder_path = "D:\\bishe\\data\\data1\\data"
    batch_size = 15
    stitched_results = []

    for images in load_images_from_folder_in_batches(folder_path, batch_size):
        if len(images) > 1:  # 需要至少两张图像才能进行拼接
            result = stitch_images(images)
            if result is not None:
                stitched_results.append(result)
            else:
                print("Batch stitching failed.")

    # 如果有多个批次结果，继续拼接这些批次结果
    if len(stitched_results) > 1:
        final_result = stitch_images(stitched_results)
    else:
        final_result = stitched_results[0] if stitched_results else None

    if final_result is not None:
        output_path = "D:\\bishe\\data\\stitched_result.jpg"
        cv2.imwrite(output_path, final_result)
        cv2.imshow("Stitched Image", final_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Final stitching failed.")
