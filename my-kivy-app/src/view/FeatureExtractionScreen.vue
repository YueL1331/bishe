<template>
  <div id="feature-extraction-screen">
    <!-- 图像展示区 -->
    <div class="main-container">
      <div class="selected-file" v-if="selectedImageUrl">
        <img :src="selectedImageUrl" alt="Selected Image" />
      </div>
      <!-- 文件名展示区 -->
      <div class="thumbnail-container">
        <div v-for="(filename, index) in selectedFiles" :key="index" class="thumbnail">
          <div @click="fetchImage(filename)">{{ filename }}</div>
          <button class="delete-button" @click="removeFile(index)">删除</button>
          <button class="show-feature-button" @click="showFeature(filename)">显示特征</button>
        </div>
      </div>
    </div>
    <!-- 特征信息与层级选择 -->
    <div class="feature-section">
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
      <div class="feature-display" v-if="featureText">
        <h3>特征信息</h3>
        <pre>{{ featureText }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: [],
      selectedImageUrl: null,
      selectedImage: null,
      layers: ['layer1', 'layer2', 'layer3', 'layer4'],
      selectedLayer: 'layer1',
      featureText: null,
    };
  },
  mounted() {
    this.loadSessionData();
    if (this.selectedFiles.length > 0) {
      this.fetchImage(this.selectedFiles[0]);
    }
  },
  methods: {
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
    },
    fetchImage(filename) {
      axios.get(`http://localhost:8081/api/files/${encodeURIComponent(filename)}`, {
        responseType: 'blob'
      })
      .then(response => {
        const url = URL.createObjectURL(response.data);
        this.selectedImageUrl = url;
        this.selectedImage = response.data;
      })
      .catch(error => {
        console.error('Error fetching image:', error);
      });
    },
    removeFile(index) {
      const filename = this.selectedFiles[index];
      axios.delete(`http://localhost:8081/api/delete/${filename}`)
        .then(() => {
          this.selectedFiles.splice(index, 1);
          if (filename === this.selectedImage) {
            this.selectedImageUrl = null;
            this.selectedImage = null;
          }
          this.updateSessionData();
        })
        .catch(error => {
          console.error('Error deleting the file:', error);
        });
    },
    showFeature(filename) {
      axios.get(`http://localhost:8081/api/files/${encodeURIComponent(filename)}`)
        .then(response => {
          console.log('Feature file content:', response.data);
          // 在此处添加将特征文件内容显示到界面的逻辑
        })
        .catch(error => {
          console.error('Error fetching feature file:', error);
        });
    },
    updateSessionData() {
      sessionStorage.setItem('selectedFiles', JSON.stringify(this.selectedFiles));
      sessionStorage.setItem('selectedImageUrl', this.selectedImageUrl);
      sessionStorage.setItem('selectedImage', this.selectedImage);
    },
    loadSessionData() {
      const files = sessionStorage.getItem('selectedFiles');
      const imageUrl = sessionStorage.getItem('selectedImageUrl');
      const image = sessionStorage.getItem('selectedImage');
      if (files) {
        this.selectedFiles = JSON.parse(files);
      }
      if (imageUrl) {
        this.selectedImageUrl = imageUrl;
      }
      if (image) {
        this.selectedImage = image;
      }
    }
  }
}
</script>


<style scoped>
#select-screen {
  display: flex;
  flex-direction: column;
  padding: 20px;
}
.button-container {
  position: fixed;
  top: 20px;
  left: 230px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}
.custom-file-button, .feature-extraction-button {
  width: 150px;
  height: 50px;
  cursor: pointer;
  margin-bottom: 10px;
}
.main-container {
  flex: 1;
  display: flex;  /* 改为横向布局 */
  border: 2px solid #ccc;
}
.selected-file {
  flex: none;  /* 不自动填充剩余空间 */
  width: 120vh;  /* 固定宽度 */
  height: 50vh;  /* 固定视图高度 */
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  margin: 20px;
}
.selected-file img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.thumbnail-container {
  width: 200px;  /* 设置固定宽度 */
  overflow-y: auto;  /* 只有垂直滚动 */
  border-left: 2px solid #ccc;  /* 添加左边框 */
}
.thumbnail {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.thumbnail div {
  cursor: pointer;
  flex-grow: 1;  /* 允许名称扩展占据空间 */
}
.delete-button {
  background-color: red;
  color: #f2f2f2;
  padding: 5px;
  border: none;
  cursor: pointer;
}
</style>
