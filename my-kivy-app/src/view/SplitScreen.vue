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
        <img :src="url" alt="Stitched Image">
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
        { batch: 15, step: 10 },
        { batch: 15, step: 15 }
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
        this.stitchedImages = await Promise.all(this.layers.map(async (layer) => {
          const response = await axios.get(`/api/stitch/${layer}?batch_size=${this.selectedOption.batch}&step_size=${this.selectedOption.step}`);
          return response.data.url;
        }));
      } catch (error) {
        console.error('Error loading stitched images:', error);
      }
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
  object-fit: cover;
}
</style>
