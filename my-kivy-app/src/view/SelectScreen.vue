<template>
  <div id="select-screen">
    <!-- 自定义的文件选择按钮 -->
    <button class="custom-file-button" @click="openFileInput">选择文件</button>

    <!-- 大窗口展示 -->
    <div class="main-container">
      <div class="selected-image" v-if="selectedImage">
        <img :src="selectedImage" alt="Selected Image">
      </div>
    </div>

    <!-- 右侧缩略图和删除按钮 -->
    <div class="thumbnail-container">
      <div v-for="(image, index) in selectedImages" :key="index" class="thumbnail">
        <img :src="image" alt="Thumbnail" @click="selectImage(index)">
        <button class="delete-button" @click="removeImage(index)">删除</button>
      </div>
    </div>

    <!-- 隐藏的文件选择输入 -->
    <input type="file" accept="image/*" multiple @change="handleFileSelection" ref="fileInput" style="display: none;">
  </div>
</template>

<script>
import axios from 'axios';

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
      const files = event.target.files;
      const formData = new FormData();

      // 读取选中的图像并更新缩略图和展示图像
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        formData.append('file', file);

        const reader = new FileReader();
        reader.onload = (e) => {
          const imageData = e.target.result;
          this.selectedImages.push(imageData);

          if (i === 0) {
            this.selectedImage = imageData;
          }
        };

        reader.readAsDataURL(file);
      }

      // 上传文件到后端
      axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        console.log('File uploaded successfully:', response.data);
      }).catch(error => {
        console.error('Error uploading file:', error);
      });
    },
    removeImage(index) {
      this.selectedImages.splice(index, 1);

      if (index === 0) {
        this.selectedImage = this.selectedImages.length > 0 ? this.selectedImages[0] : null;
      }
    },
    selectImage(index) {
      this.selectedImage = this.selectedImages[index];
    }
  },
  beforeRouteLeave(to, from, next) {
    // 在导航离开前保存当前的图像状态
    localStorage.setItem('selectedImages', JSON.stringify(this.selectedImages));
    localStorage.setItem('selectedImage', this.selectedImage);
    next();
  },
  beforeRouteEnter(to, from, next) {
    // 在导航进入时恢复之前保存的状态
    const savedSelectedImages = localStorage.getItem('selectedImages');
    const savedSelectedImage = localStorage.getItem('selectedImage');

    next(vm => {
      if (savedSelectedImages) {
        vm.selectedImages = JSON.parse(savedSelectedImages);
      }
      if (savedSelectedImage) {
        vm.selectedImage = savedSelectedImage;
      }
    });
  },
};
</script>

<style scoped>
#select-screen {
  display: flex;
  flex-direction: row;
  padding: 20px;
}

.custom-file-button {
  width: 200px;
  height: 50px;
}

.main-container {
  flex-grow: 1;
  border: 2px solid #ccc;
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
  flex-direction: column;
}

.thumbnail img {
  width: 100px;
  cursor: pointer;
}

.delete-button {
  background-color: red;
  color: white;
  padding: 5px;
  border: none;
  cursor: pointer;
}
</style>
