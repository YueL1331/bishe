<template>
  <div id="select-screen">
    <!-- 自定义的文件选择按钮 -->
    <div class="button-container">
      <button class="custom-file-button" @click="openFileInput">选择文件</button>
      <button class="feature-extraction-button" @click="goToFeatureExtraction">
        处理特征
      </button>
    </div>

    <!-- 大窗口展示 -->
    <div class="main-container">
      <div class="selected-image" v-if="selectedImage">
        <img :src="selectedImage" alt="Selected Image" />
      </div>
    </div>

    <!-- 缩略图和删除按钮 -->
    <div class="thumbnail-container">
      <div v-for="(image, index) in selectedImages" :key="index" class="thumbnail">
        <img :src="image" alt="Thumbnail" @click="selectImage(index)" />
        <button class="delete-button" @click="removeImage(index)">删除</button>
      </div>
    </div>

    <!-- 隐藏的文件选择输入 -->
    <input
      type="file"
      accept="image/*"
      multiple
      @change="handleFileSelection"
      ref="fileInput"
      style="display: none;"
    />
  </div>
</template>
export default {
  data() {
    return {
      selectedImages: [],
      selectedImage: null,
    };
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelection(event) {
      const files = Array.from(event.target.files); // 将文件转换为数组
      const newImages = [];

      for (let file of files) {
        const reader = new FileReader();
        reader.onload = (e) => {
          newImages.push(e.target.result);
        };
        reader.readAsDataURL(file);
      }

      this.selectedImages = [...this.selectedImages, ...newImages]; // 合并原有和新图片

      if (this.selectedImages.length === 1) {
        this.selectedImage = newImages[0]; // 设置第一张选中的图像
      }

      // 上传文件到后端
      const formData = new FormData();
      for (let file of files) {
        formData.append('file', file);
      }

      axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(() => {
          console.log('Files uploaded successfully');
        })
        .catch((error) => {
          console.error('Error uploading files:', error);
        });
    },
    removeImage(index) {
      this.selectedImages.splice(index, 1); // 从列表中删除缩略图
      if (this.selectedImages.length === 0) {
        this.selectedImage = null; // 如果列表为空，清除选中的图像
      } else if (index === 0) {
        this.selectedImage = this.selectedImages[0]; // 设置新第一张图像
      }
    },
    selectImage(index) {
      this.selectedImage = this.selectedImages[index]; // 点击缩略图时更新选中的图像
    },
    goToFeatureExtraction() {
      this.$router.push('/feature-extraction'); // 跳转到特征提取页面
    },
  },
};
<style scoped>
#select-screen {
  display: flex;
  flex-direction: column;  /* 使按钮位于顶部 */
  padding: 20px;
}

.button-container {
  display: flex;
  justify-content: space-around;  /* 确保两个按钮平均分布 */
  margin-bottom: 20px;  /* 让按钮与其他内容之间留出空间 */
}

.custom-file-button,
.feature-extraction-button {
  width: 200px;
  height: 50px;
  cursor: pointer;  /* 让按钮具有交互感 */
}

.main-container {
  flex: 1;
  border: 2px solid #ccc;  /* 边框以分割不同部分 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.selected-image img {
  max-width: 100%;
  max-height: 100%;
}

.thumbnail-container {
  display: flex;
  flex-direction: row;  /* 缩略图横向排列 */
  overflow-x: auto;  /* 防止溢出 */
}

.thumbnail {
  display: flex;
  flex-direction: column;  /* 让缩略图和删除按钮垂直排列 */
}

.thumbnail img {
  width: 100px;  /* 缩略图大小 */
  cursor: pointer;  /* 鼠标悬停时显示指针 */
}

.delete-button {
  background-color: red;
  color: #f2f2f2;
  padding: 5px;
  border: none;
  cursor: pointer;
}
</style>
