<template>
  <div id="image-stitching">
    <div class="navigation">
      <ul>
        <li v-for="(option, index) in options" :key="index" @click="selectOption(option)">
          Batch: {{ option.batch }} Step: {{ option.step }}
        </li>
      </ul>
    </div>
    <div class="image-container">
      <div v-for="(img, index) in images" :key="index" class="image-box">
        <img :src="img.url" alt="Stitched Image" @error="handleImageError(index)">
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
      images: []  // 初始空数组，准备填充图像 URL
    };
  },
methods: {
  selectOption(option) {
    this.selectedOption = option;
    this.loadStitchedImages();
  },
  async loadStitchedImages() {
    this.images = [];  // 重置图片数组
    for (const layer of this.layers) {
      const index = this.layers.indexOf(layer);
      try {
        const response = await axios.get(`http://localhost:8081/api/stitched_images/${this.selectedOption.batch}_${this.selectedOption.step}/${layer}_${this.selectedOption.batch}_${this.selectedOption.step}.jpg`);
        this.images[index] = {url: response.data.url};  // 直接赋值
      } catch (error) {
        console.error(`Error loading stitched image for layer ${layer}:`, error);
        this.images[index] = {url: 'http://localhost:8081/static/error.jpg'};  // 错误时直接赋值
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

}
</script>




<style scoped>
.navigation {
  position: fixed;
  top: 0;
  left: 50px;
  width: 100%;
  z-index: 100;
  background-color: #f3f3f3;
  justify-content: center;
}

.navigation ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.navigation li {
  padding: 10px 20px;
  cursor: pointer;
  background-color: #fff;
}

.navigation li:hover {
  background-color: #ddd;
}

.image-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 10px;
  height: 90vh;
  width: 120vh;
  margin: auto;
  margin-top: 60px; /* Ensure content is not covered by the navbar */
}

.image-box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-box img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Ensure images are not distorted */
  border: 1px solid #ccc; /* Optional, adds a border for visual separation */
}
</style>
