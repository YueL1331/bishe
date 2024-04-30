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
          <div @click="fetchImage(file)">{{ file }}</div>
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
    files.forEach((file, index) => {
      formData.append(`file${index}`, file); // 确保每个文件都有唯一的 key
    });

    axios.post('http://localhost:8081/api/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      // 追加文件到现有数组，而不是替换它
      this.selectedFiles = [...this.selectedFiles, ...response.data.files];
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
  display: flex;  /* 改为横向布局 */
  border: 2px solid #ccc;
}
.selected-file {
  flex: 1;  /* 自动占满剩余空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;  /* 视图高度 */
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

