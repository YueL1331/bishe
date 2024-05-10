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
      <div v-for="(url, index) in stitchedImages" :key="index" class="image-box">
        <img :src="url" alt="Stitched Image" @error="handleImageError">
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
      stitchedImages: []
    };
  },
  methods: {
    selectOption(option) {
      this.selectedOption = option;
      this.loadStitchedImages();
    },
    async loadStitchedImages() {
      try {
        const response = await axios.get(`/api/stitch/all_layers`, {
          params: {
            batch_size: this.selectedOption.batch,
            step_size: this.selectedOption.step
          }
        });
        // 假设返回的数据结构是 { layer1: url1, layer2: url2, layer3: url3, layer4: url4 }
        this.stitchedImages = this.layers.map(layer => response.data[layer] || '');
      } catch (error) {
        console.error('Error loading stitched images:', error);
        this.stitchedImages = []; // 出错时清空数组
      }
    },
    handleImageError(event) {
      event.target.src = 'my-kivy-app/src/pic/error.jpg'; // 设置默认图像或错误图像路径
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
}

.navigation ul {
  display: flex;
  list-style: none;
  padding: 0;
  background-color: #f3f3f3;
  margin: 0;
  justify-content: center;
}

.navigation li {
  padding: 10px 20px;
  cursor: pointer;
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
  margin-top: 60px; /* 确保内容不被导航栏遮挡 */
}

.image-box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-box img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 使用 contain 来保证图片不失真 */
  border: 1px solid #ccc; /* 可选，增加边框以便于视觉上区分各个图层 */
}
</style>
