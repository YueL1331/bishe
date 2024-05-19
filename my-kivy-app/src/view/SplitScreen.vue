<template>
  <div>
    <select v-model="selectedOption" @change="selectOption">
      <option v-for="option in options" :key="`${option.batch}_${option.step}`" :value="option">
        Batch: {{ option.batch }}, Step: {{ option.step }}
      </option>
    </select>

    <div class="image-grid">
      <div v-for="(image, index) in images" :key="index" class="image-container">
        <img :src="image.url" @error="handleImageError(index)" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';  // 导入axios

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
      images: []
    };
  },
  methods: {
    selectOption() {
      this.loadStitchedImages();
    },
    async loadStitchedImages() {
      this.images = [];  // 重置图片数组
      for (const layer of this.layers) {
        const index = this.layers.indexOf(layer);
        try {
          const response = await axios.get(`http://localhost:8081/api/stitched_images/${this.selectedOption.batch}_${this.selectedOption.step}/${layer}_${this.selectedOption.batch}_${this.selectedOption.step}.png`);
          this.images[index] = { url: response.config.url };  // 使用请求的URL
        } catch (error) {
          console.error(`Error loading stitched image for layer ${layer}:`, error);
          this.images[index] = { url: 'http://localhost:8081/static/error.jpg' };  // 错误时直接赋值
        }
      }
    },
    handleImageError(index) {
      this.images[index].url = 'http://localhost:8081/static/error.jpg';
    }
  },
  mounted() {
    this.loadStitchedImages();
  }
};
</script>

<style>
/* 网格布局 */
.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 80vh); /* 2列，每列60vh */
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
</style>
