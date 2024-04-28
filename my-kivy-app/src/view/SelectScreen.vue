<template>
  <div id="select-screen">
    <!-- 自定义的文件选择按钮 -->
    <div class="button-container">
      <button class="custom-file-button" @click="openFileInput">选择文件</button>
      <button class="feature-extraction-button" @click="goToFeatureExtraction">
        处理特征
      </button>
    </div>

    <!-- 文件名称展示 -->
    <div class="main-container">
      <div class="selected-file" v-if="selectedFile">
        {{ selectedFile }}  <!-- 显示文件名称 -->
      </div>
    </div>

    <!-- 文件缩略图和删除按钮 -->
    <div class="thumbnail-container">
      <div v-for="(file, index) in selectedFiles" :key="index" class="thumbnail">
        {{ file }}  <!-- 显示文件名称作为缩略图 -->
        <button class="delete-button" @click="removeFile(index)">删除</button>
      </div>
    </div>

    <!-- 隐藏的文件选择输入 -->
    <input
      type="file"
      accept="image/*"
      multiple
      @change="handleFileSelection"
      ref="fileInput"
      style="display: none;"
    />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFiles: [],  // 用于存储文件名称
      selectedFile: null,  // 当前选中的文件
    };
  },
  mounted() {
    // 在组件加载时检查 sessionStorage 是否存在存储的数据
    const storedFiles = sessionStorage.getItem('selectedFiles');
    const storedFile = sessionStorage.getItem('selectedFile');
    if (storedFiles && storedFile) {
      this.selectedFiles = JSON.parse(storedFiles);
      this.selectedFile = storedFile;
    }
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileSelection(event) {
      const files = Array.from(event.target.files);
      this.uploadFiles(files);
    },
    uploadFiles(files) {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('file', file);  // 添加文件到 FormData
      });

      axios.post('api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(response => {
        const uploadedFiles = response.data.files.map(f => f.name);  // 提取文件名称
        this.selectedFiles = [...this.selectedFiles, ...uploadedFiles];
        this.selectedFile = this.selectedFiles[0];
        sessionStorage.setItem('selectedFiles', JSON.stringify(this.selectedFiles));
        sessionStorage.setItem('selectedFile', this.selectedFile);
        console.log('Files uploaded successfully');
      })
      .catch((error) => {
        console.error('Error uploading files:', error);
      });
    },
    removeFile(index) {
      this.selectedFiles.splice(index, 1);
      if (this.selectedFiles.length === 0) {
        this.selectedFile = null;
      } else if (index === 0) {
        this.selectedFile = this.selectedFiles[0];
      }
      sessionStorage.setItem('selectedFiles', JSON.stringify(this.selectedFiles));
      sessionStorage.setItem('selectedFile', this.selectedFile);
    },
    selectFile(index) {
      this.selectedFile = this.selectedFiles[index];  // 选择一个文件
    },
    goToFeatureExtraction() {
      this.$router.push('/feature-extraction');  // 导航到其他路由
    }
  },
  beforeRouteLeave(to, from, next) {
    // 离开页面时清除 sessionStorage
    sessionStorage.removeItem('selectedFiles');
    sessionStorage.removeItem('selectedFile');
    next();
  },
}
</script>

<style scoped>
#select-screen {
  display: flex;
  flex-direction: column;  /* 采用列布局 */
  padding: 20px;
}

.button-container {
  position: fixed; /* 固定按钮位置 */
  top: 20px;       /* 顶部对齐 */
  left: 230px;      /* 靠左 */
  z-index: 1000;   /* 保持在最前面 */
  display: flex;
  flex-direction: column;  /* 垂直排列 */
}

.custom-file-button,
.feature-extraction-button {
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
  font-size: 1.2em;  /* 较大字体显示文件名称 */
}

.thumbnail-container {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  height: 150px;  /* 限制高度，激活滚动条 */
}

.thumbnail {
  display: flex;
  flex-direction: row;  /* 使缩略图和删除按钮并排 */
  align-items: center;
  margin-bottom: 10px;
}

.delete-button {
  background-color: red;
  color: #f2f2f2;
  padding: 5px;
  border: none;
  cursor: pointer;
}

</style>
