<template>
  <div id="select-screen">
    <div class="button-container">
      <button class="custom-file-button" @click="openFileInput">选择文件</button>
      <button class="feature-extraction-button" @click="goToFeatureExtraction">处理特征</button>
    </div>
    <div class="main-container">
      <input type="file" accept="image/*" multiple @change="handleFileSelection" ref="fileInput" style="display:none;">
      <div class="selected-file" v-if="selectedImageUrl">
        <img :src="selectedImageUrl" alt="Selected Image" />
      </div>
      <div class="thumbnail-container">
        <div v-for="(filename, index) in selectedFiles" :key="index" class="thumbnail">
          <div @click="fetchImage(filename)">{{ filename }}</div>
          <button class="delete-button" @click="removeFile(index)">删除</button>
        </div>
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
      selectedFile: null,
    };
  },
  mounted() {
    this.loadSessionData();
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelection(event) {
      const files = Array.from(event.target.files);
      if (files.length > 0) {
        const formData = new FormData();
        files.forEach((file, index) => {
          formData.append(`file${index}`, file);
        });

        axios.post('http://localhost:8081/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(response => {
          this.selectedFiles = [...this.selectedFiles, ...response.data.files];
          this.updateSessionData();  // Update session storage
          if (response.data.files.length > 0) {
            this.fetchImage(response.data.files[0]);
            this.selectedFile = response.data.files[0];
          }
        }).catch(error => {
          console.error('Error uploading files:', error);
        });
      }
    },
    fetchImage(filename) {
      axios.get(`http://localhost:8081/api/files/${encodeURIComponent(filename)}`, {
        responseType: 'blob'
      })
      .then(response => {
        const url = URL.createObjectURL(response.data);
        this.selectedImageUrl = url;
        this.updateSessionData();  // Update session storage
        this.selectedFile = filename;
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
          if (filename === this.selectedFile) {
            this.selectedImageUrl = null;
            this.selectedFile = null;
          }
          this.updateSessionData();  // Clear session storage if necessary
        })
        .catch(error => {
          console.error('Error deleting the file:', error);
        });
    },
    goToFeatureExtraction() {
      this.$router.push('/feature-extraction');
    },
    updateSessionData() {
      sessionStorage.setItem('selectedFiles', JSON.stringify(this.selectedFiles));
      sessionStorage.setItem('selectedImageUrl', this.selectedImageUrl);
      sessionStorage.setItem('selectedFile', this.selectedFile);
    },
    loadSessionData() {
      const files = sessionStorage.getItem('selectedFiles');
      const imageUrl = sessionStorage.getItem('selectedImageUrl');
      const file = sessionStorage.getItem('selectedFile');
      if (files) {
        this.selectedFiles = JSON.parse(files);
      }
      if (imageUrl) {
        this.selectedImageUrl = imageUrl;
      }
      if (file) {
        this.selectedFile = file;
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
  height: 90vh;  /* 固定视图高度 */
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
  background-color:red;
  color: #f2f2f2;
  padding: 5px;
  border: none;
  cursor: pointer;
}
</style>
