<template>
  <div id="feature-extraction-screen">
    <!-- 大窗口：上半部分展示选中的图像 -->
    <div class="main-container">
      <div class="selected-image" v-if="selectedImage">
        <img :src="selectedImage" alt="Selected Image" />
      </div>

      <!-- 导航栏和特征信息：下半部分 -->
      <div class="feature-section">
        <!-- 导航栏：选择特征层 -->
        <div class="layer-selection">
          <button
            v-for="layer in layers"
            :key="layer"
            :class="{ selected: layer === selectedLayer }"
            @click="selectLayer(layer)"
          >
            {{ layer }}
          </button>
        </div>

        <!-- 特征信息展示 -->
        <div class="feature-display">
          <div v-if="featureText">
            <h3>特征信息</h3>
            <pre>{{ featureText }}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- 缩略图展示 -->
    <div class="thumbnail-container">
      <div
        v-for="(image, index) in selectedImages"
        :key="index"
        class="thumbnail"
      >
        <img
          :src="image"
          alt="Thumbnail"
          @click="selectImage(index)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedImages: [],
      selectedImage: null,
      layers: ['layer1', 'layer2', 'layer3', 'layer4'],
      selectedLayer: 'layer1',
      featureText: null,
    };
  },
methods: {
  selectImage(index) {
    this.selectedImage = this.selectedImages[index];
    this.fetchFeatureText();
  },
  selectLayer(layer) {
    this.selectedLayer = layer;
    this.fetchFeatureText();
  },
  fetchFeatureText() {
    if (!this.selectedImage) return;
    const formData = new FormData();
    formData.append('file', this.selectedImage);
    formData.append('layer', this.selectedLayer);

    axios.post('http://localhost:8081/api/feature', formData)
      .then(response => {
        this.featureText = response.data.feature;
      })
      .catch(error => {
        console.error('Error fetching feature:', error);
        this.featureText = '无法获取特征信息';
      });
  }
},

  mounted() {
    const savedSelectedImages = localStorage.getItem('selectedImages');
    if (savedSelectedImages) {
      this.selectedImages = JSON.parse(savedSelectedImages);
      this.selectedImage = this.selectedImages[0]; // 初始显示第一张
      this.fetchFeatureText(); // 初始化时获取特征
    }
  },
};
</script>

<style scoped>
#feature-extraction-screen {
  display: flex;
  flex-direction: column;  /* 主要布局方向为垂直 */
  padding: 20px;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;  /* 大窗口上下布局 */
}

.selected-image {
  flex: 1;  /* 上半部分，用于显示图像 */
}

.selected-image img {
  max-width: 100%;
  max-height: 100%;  /* 防止溢出 */
}

.feature-section {
  display: flex;
  flex-direction: column;  /* 导航栏和特征信息在同一部分 */
  flex: 1;  /* 与图像部分同样占用空间 */
}

.layer-selection {
  display: flex;
  justify-content: space-around;  /* 导航栏居中 */
  padding: 10px;  /* 导航栏按钮的间距 */
}

.layer-selection button.selected {
  background-color: lightgray;  /* 选中的按钮的样式 */
}

.feature-display {
  flex: 1;  /* 特征展示区 */
}

.thumbnail-container {
  display: flex;
  flex-direction: row;  /* 缩略图横向排列 */
}

.thumbnail img {
  width: 50px;  /* 缩略图大小 */
  cursor: pointer;  /* 鼠标悬停时变为指针 */
}
</style>
