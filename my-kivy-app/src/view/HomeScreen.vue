<template>
  <div>
    <button v-for="button in buttons" :key="button.screenName" @click="switchScreen(button.screenName)">
      {{ button.text }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      buttons: [
        // { text: "选择文件", screenName: "file-selection" },
        // { text: "特征向量提取", screenName: "feature-extraction" },
        // { text: "图像拼接", screenName: "image-stitching" },
        // { text: "区域选择", screenName: "region-selection" }
      ]
    };
  },
  methods: {
    switchScreen(screenName) {
      this.$router.push({ name: screenName });
    }
  }
};
</script>