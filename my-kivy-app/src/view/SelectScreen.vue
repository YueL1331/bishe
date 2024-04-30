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
        <div v-for="(file, index) in selectedFiles" :key="index" class="thumbnail">
          {{ file }}
          <button class="view-button" @click="fetchImage(file)">查看</button>
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
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
  handleFileSelection(event) {
  const files = Array.from(event.target.files);
  if (files.length > 0) {
    const formData = new FormData();
    formData.append('file', files[0]);
    console.log([...formData]);
    axios.post('http://localhost:8081/api/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      this.selectedFiles = response.data.files; // 直接使用 response.data.files
      if (this.selectedFiles.length > 0) {
        this.fetchImage(this.selectedFiles[0]); // 自动加载第一张图像
        this.selectedFile = this.selectedFiles[0];
      }
    }).catch(error => {
      console.error('Error uploading files:', error);
    });
  }
},
fetchImage(filename) {
  // console.log('Fetching image with filename:', filename); // 调试语句
axios.get(`http://localhost:8081/api/files/${encodeURIComponent(filename)}`, {
  responseType: 'blob'  // 指定响应类型为 Blob
})
.then(response => {
  const url = URL.createObjectURL(response.data);
  this.selectedImageUrl = url;  // 使用生成的URL
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
            if (index > 0) {
              this.fetchImage(this.selectedFiles[index - 1]);
            } else if (this.selectedFiles.length > 0) {
              this.fetchImage(this.selectedFiles[0]);
            } else {
              this.selectedImageUrl = null;
              this.selectedFile = null;
            }
          }
        })
        .catch(error => {
          console.error('Error deleting the file:', error);
        });
    },
    goToFeatureExtraction() {
      this.$router.push('/feature-extraction');
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
  border: 2px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
}
.selected-file {
  display: flex;  /* 设置 flex 布局 */
  justify-content: center;  /* 水平居中 */
  align-items: center;  /* 垂直居中 */
  width: 100%;  /* 容器宽度 */
  height: 1000px;  /* 容器高度，根据需要调整 */
  background-color: white;  /* 背景颜色为白 */
  margin: 20px 0;  /* 添加一些外边距 */
}

.selected-file img {
  max-width: 100%;  /* 图片最大宽度不超过容器 */
  max-height: 100%;  /* 图片最大高度不超过容器 */
  object-fit: contain;  /* 保持图片比例 */
}

.thumbnail-container {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  height: 150px;
}
.thumbnail {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 10px;
}
.delete-button, .view-button {
  background-color: red;
  color: #f2f2f2;
  padding: 5px;
  border: none;
  cursor: pointer;
}
.view-button {
  background-color: green;
}
</style>
