<template>
  <div>
    <div class="controls">
      <button @click="openDownloadModal">下载图像</button>
      <select v-model="selectedOption" @change="selectOption">
        <option v-for="option in options" :key="`${option.batch}_${option.step}`" :value="option">
          Batch: {{ option.batch }}, Step: {{ option.step }}
        </option>
      </select>
    </div>

    <div class="image-grid">
      <div v-for="(image, index) in images" :key="index" class="image-container">
        <img :src="image.url" @error="handleImageError(index)" />
      </div>
    </div>

    <div v-if="showDownloadModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeDownloadModal">&times;</span>
        <div class="download-grid">
          <div v-for="(image, index) in allImages" :key="index" class="download-image-container">
            <img :src="image.url" @click="toggleSelection(index)" :class="{ selected: selectedImages.includes(index) }" />
            <div class="selector" :class="{ selected: selectedImages.includes(index) }"></div>
          </div>
        </div>
        <button @click="continueDownload">继续</button>
        <button @click="closeDownloadModal">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedOption: { batch: 10, step: 10 },
      options: [
        { batch: 10, step: 10 },
        { batch: 10, step: 15 },
        { batch: 15, step: 15 },
        { batch: 15, step: 10 }
      ],
      layers: ['layer1', 'layer2', 'layer3', 'layer4'],
      images: [],
      allImages: [],
      showDownloadModal: false,
      selectedImages: []
    };
  },
  methods: {
    selectOption() {
      this.loadStitchedImages();
    },
    async loadStitchedImages() {
      this.images = [];
      for (const layer of this.layers) {
        const index = this.layers.indexOf(layer);
        try {
          const response = await axios.get(`http://localhost:8081/api/stitched_images/${this.selectedOption.batch}_${this.selectedOption.step}/${layer}_${this.selectedOption.batch}_${this.selectedOption.step}.png`);
          this.images[index] = { url: response.config.url, error: false };
        } catch (error) {
          console.error(`Error loading stitched image for layer ${layer}:`, error);
          this.images[index] = { url: 'http://localhost:8081/static/error.jpg', error: true };
        }
      }
    },
    handleImageError(index) {
      this.images[index].url = 'http://localhost:8081/static/error.jpg';
      this.images[index].error = true;
    },
    openDownloadModal() {
      this.loadAllStitchedImages();
      this.showDownloadModal = true;
    },
    closeDownloadModal() {
      this.showDownloadModal = false;
    },
    toggleSelection(index) {
      if (this.selectedImages.includes(index)) {
        this.selectedImages = this.selectedImages.filter(i => i !== index);
      } else {
        this.selectedImages.push(index);
      }
    },
    async loadAllStitchedImages() {
      try {
        const response = await axios.get('http://localhost:8081/api/stitched_images');
        this.allImages = response.data.filter(image => !image.error).map(url => ({ url }));
      } catch (error) {
        console.error('Error loading all stitched images:', error);
      }
    },
    continueDownload() {
      if (this.selectedImages.length > 0) {
        const urls = this.selectedImages.map(index => this.allImages[index].url);
        this.downloadImages(urls);
      }
      this.closeDownloadModal();
    },
    async downloadImages(urls) {
      for (const url of urls) {
        const response = await axios.get(url, {
          responseType: 'blob'
        });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(response.data);
        link.download = url.split('/').pop();
        link.click();
      }
    }
  },
  mounted() {
    this.loadStitchedImages();
  }
};
</script>

<style>
/* 控制面板样式 */
.controls {
  display: flex;
  justify-content: flex-start; /* 左对齐 */
  align-items: center;
  margin-bottom: 20px;
}

/* 网格布局 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 80vh); /* 2列，每列80vh */
  grid-template-rows: repeat(2, 45vh); /* 2行，每行45vh */
  gap: 10px; /* 网格项之间的间距 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

/* 图像容器样式 */
.image-container {
  width: 80vh;
  height: 45vh;
  position: relative;
  overflow: hidden;
  border: 1px solid #ddd; /* 可选：为每个图像容器添加边框 */
}

/* 图像样式 */
.image-container img {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 100%;
  max-height: 100%;
}

/* 悬浮窗样式 */
.modal {
  display: block; /* 默认不显示 */
  position: fixed; /* 固定在屏幕 */
  z-index: 1000; /* 保证在最前 */
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto; /* 允许滚动 */
  background-color: rgb(0,0,0); /* 黑色背景 */
  background-color: rgba(0,0,0,0.4); /* 背景透明度 */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 垂直居中 */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* 宽度 */
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.download-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4列 */
  gap: 10px; /* 网格项之间的间距 */
}

.download-image-container {
  position: relative;
}

.download-image-container img {
  width: 100%;
  height: auto;
  cursor: pointer;
}

.selector {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: red;
  border: 2px solid white;
}

.selector.selected {
  background-color: green;
}

button {
  margin-top: 10px;
}

</style>
