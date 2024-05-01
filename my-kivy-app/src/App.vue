<template>
  <div id="app">
    <nav class="sidebar">
      <ul class="nav-list">
        <li><router-link to="/" class="nav-link">首页</router-link></li>
        <li><router-link to="/file-selection" class="nav-link">选择文件</router-link></li>
        <li><router-link to="/feature-extraction" class="nav-link">特征向量提取</router-link></li>
        <li><router-link to="/image-stitching" class="nav-link">图像拼接</router-link></li>
        <li><router-link to="/region-selection" class="nav-link">区域选择</router-link></li>
      </ul>
    </nav>
    <main>
      <router-view/>
    </main>
  </div>
</template>


<script>
// 引入必要的库和组件
import { createRouter, createWebHistory } from 'vue-router';
import Home from './view/HomeScreen.vue';
import FileSelection from './view/SelectScreen.vue';
import FeatureExtraction from './view/FeatureExtractionScreen.vue';
import ImageStitching from './view/SplitScreen.vue';
import RegionSelection from './view/ChooseScreen.vue';

// 创建路由实例
const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 历史模式
  routes: [
    { path: '/', component: Home },
    { path: '/file-selection', component: FileSelection },
    { path: '/feature-extraction', component: FeatureExtraction },
    { path: '/image-stitching', component: ImageStitching },
    { path: '/region-selection', component: RegionSelection }
  ]
});

// 导出路由实例
export default router;
</script>

<style>
/* 你的样式可以保持不变，确保它们正确应用到你的HTML结构 */
#app {
  display: flex;
  flex-direction: row; /* 明确指定为横向布局 */
  min-height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f9f9f9;
  padding: 20px;
  box-sizing: border-box;
  flex-shrink: 0; /* 阻止侧边栏缩小 */
  height: 100vh; /* 可选：如果你希望侧边栏高度填满整个视口高度 */
  overflow-y: auto; /* 可选：如果侧边栏内容过多，允许滚动 */
}

.main {
  flex-grow: 1;
  padding: 20px; /* 确保内容区域有足够的间距 */
  overflow-y: auto; /* 可选：允许内容区域滚动 */
}

.nav-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: block;
  padding: 10px;
  text-decoration: none;
  color: #2c3e50;
}

.nav-link:hover {
  background-color: #f2f2f2;
}

.router-link-active {
  color: #42b983;
}
</style>
