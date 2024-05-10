<template>
  <div id="feature-extraction-screen">
     <button class="feature-extraction-button" @click="goToImageStitching">图像拼接</button> <!-- 新增按钮 -->
    <!-- 图像展示区 -->
    <div class="main-container">
      <div class="selected-file" v-if="selectedImageUrl">
        <img :src="selectedImageUrl" alt="Selected Image" />
      </div>
      <!-- 文件名展示区 -->
      <div class="thumbnail-container">
        <div v-for="(filename, index) in selectedFiles" :key="index" class="thumbnail">
          <div @click="showFeature(filename)">{{ filename }}</div>
          <button class="delete-button" @click="removeFile(index)">删除</button>
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
        <h3>特征信息只展示1000个数字，其余请到文件中查看</h3>
        <pre>{{ limitedFeatureText }}</pre>
        <h3>特征信息只展示1000个数字，其余请到文件中查看</h3>
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
      limitedFeatureText: '',
      maxFeaturesToShow: 1000  // Max number of feature groups to show
    };
  },
  watch: {
    featureText(newVal) {
      this.limitedFeatureText = newVal.split(',').slice(0, this.maxFeaturesToShow).join(', ');
    }
  },
  mounted() {
    this.loadSessionData();
    if (this.selectedFiles.length > 0) {
      this.showFeature(this.selectedFiles[0]);
    }
  },
  methods: {
    selectLayer(layer) {
      this.selectedLayer = layer;
      this.fetchFeatureText();
    },
    fetchFeatureText() {
      if (!this.selectedImage || !this.selectedLayer) {
        console.log('No selected file or layer.');
        return;
      }
      const featureFilePath = `http://localhost:8081/api/features/${this.selectedLayer}/${encodeURIComponent(this.selectedImage)}_${this.selectedLayer}.txt`;
      axios.get(featureFilePath, { responseType: 'text' })
        .then(response => {
          this.featureText = response.data;
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
        this.selectedImage = filename;
        this.fetchFeatureText();
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
            this.featureText = null;
          }
          this.updateSessionData();
        })
        .catch(error => {
          console.error('Error deleting the file:', error);
        });
    },
    showFeature(filename) {
      this.fetchImage(filename);
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
    },
    goToImageStitching() {
      this.$router.push('/image-stitching');
    }
  }
}
</script>

<style scoped>
#feature-extraction-screen {
  display: flex;
  flex-direction: column;
}
.main-container {
  display: flex; /* 水平布局 */
  flex: 1; /* 占满剩余空间 */
  border: 2px solid #ccc; /* 边框 */
  padding: 20px; /* 内边距 */
  overflow: hidden; /* 隐藏溢出内容 */
}
.selected-file {
  width: 120vh;  /* 固定宽度 */
  height: 50vh;  /* 与特征信息框的高度一致 */
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
  height: 50vh; /* 设置固定高度，这里使用视口高度的百分比 */
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
.feature-extraction-button {
  width: 150px;
  height: 50px;
  cursor: pointer;
  margin-bottom: 10px;
  background-color: #05ed05; /* Green background */
  color: white; /* White text */
  border: none;
  border-radius: 5px;
}
.feature-display {
  width: 120vh;  /* 和图像展示框相同的宽度 */
  height: 50vh;  /* 与图像展示框高度一致 */
  overflow-y: auto;  /* 允许垂直滚动 */
  border: 2px solid #ccc;  /* 边框样式 */
}
.feature-display pre {
  white-space: pre-wrap;  /* 允许自动换行 */
  word-wrap: break-word;  /* 长单词或URL也可换行 */
}
</style>

