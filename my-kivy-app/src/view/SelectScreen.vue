<template>
  <div id="select-screen">
    <!-- 自定义的文件选择按钮 -->
    <button class="custom-file-button" @click="openFileInput">选择文件</button>

    <!-- 大窗口展示 -->
    <div class="main-container">
      <div class="selected-image" v-if="selectedImage !== null">
        <img :src="selectedImage" alt="Selected Image">
      </div>
    </div>

    <!-- 右侧缩略图和删除按钮 -->
    <div class="thumbnail-container">
      <div v-for="(image, index) in selectedImages" :key="index" class="thumbnail">
        <img :src="image" alt="Thumbnail" @click="selectImage(index)">
        <button class="delete-button" @click="removeImage(index)" :disabled="fileUploading">删除</button>
      </div>
    </div>

    <!-- 隐藏的文件选择输入 -->
    <input type="file" accept="image/*" multiple @change="handleFileSelection" ref="fileInput" style="position: absolute; left: -9999px; opacity: 0;">
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedImages: [], // 存储选中的图像文件
      selectedImage: null, // 存储当前选中的图像文件
      fileUploading: false // 标记文件是否正在上传
    };
  },
  methods: {
    openFileInput() {
      // 触发隐藏的文件选择输入的点击事件
      this.$refs.fileInput.click();
    },
    handleFileSelection(event) {
      const files = event.target.files;
      // 清空已选中的图像数组
      this.selectedImages = [];
      // 读取选中的图像文件
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            // 将读取到的图像添加到选中的图像数组中
            const imageData = e.target.result;
            this.selectedImages.push(imageData);
            // 设置选中的第一张图像作为展示图像
            if (i === 0) {
              this.selectedImage = imageData;
            }
          };
          reader.readAsDataURL(file);
        }
      }
    },
    removeImage(index) {
      this.selectedImages.splice(index, 1);
      // 如果删除的是当前展示的图像，则更新展示的图像为第一张图像
      if (index === 0 && this.selectedImages.length > 0) {
        this.selectedImage = this.selectedImages[0];
      } else if (index === 0 && this.selectedImages.length === 0) {
        this.selectedImage = null;
      }
    },
    selectImage(index) {
      this.selectedImage = this.selectedImages[index];
    }
  },
  beforeRouteLeave(to, from, next) {
    // 保存数据到 localStorage
    localStorage.setItem('selectedImages', JSON.stringify(this.selectedImages));
    localStorage.setItem('selectedImage', this.selectedImage);
    next();
  },
  beforeRouteEnter(to, from, next) {
    // 加载数据
    const savedSelectedImages = localStorage.getItem('selectedImages');
    const savedSelectedImage = localStorage.getItem('selectedImage');
    next(vm => {
      if (savedSelectedImages && savedSelectedImage) {
        vm.selectedImages = JSON.parse(savedSelectedImages);
        vm.selectedImage = savedSelectedImage;
      }
    });
  }
};
</script>

<style scoped>
#select-screen {
  display: flex;
  flex-direction: row; /* 修改为水平排列 */
  padding: 20px;
  position: relative;
}

.custom-file-button {
  width: 200px; /* 固定自定义按钮的宽度 */
  height: 50px; /* 固定自定义按钮的高度 */
  margin-right: 20px; /* 调整按钮与其他内容的间距 */
}

.main-container {
  display: flex;
  align-items: center;
  border: 2px solid #ccc; /* 添加边框 */
  flex-grow: 1; /* 自动扩展以占据剩余空间 */
}

.selected-image img {
  max-width: 100%; /* 图像最大宽度为容器的100% */
  max-height: 100%; /* 图像最大高度为容器的100% */
}

.thumbnail-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end; /* 缩略图右对齐 */
}

.thumbnail {
  margin-bottom: 10px;
}

.thumbnail img {
  width: 100px;
  height: auto;
}

.delete-button {
  width: 100%;
  padding: 5px;
  background-color: red;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
