import { createApp } from 'vue'; // 使用 Vue 3 的 createApp 方法
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router'; // 使用 Vue 3 的路由创建方法

// 引入页面组件
import HomeScreen from "@/view/HomeScreen.vue";
import FileSelectionScreen from "@/view/SelectScreen.vue";
import FeatureExtractionScreen from "@/view/FeatureExtractionScreen.vue"; // 确保正确导入特征提取屏幕组件

// 定义路由配置
const routes = [
    { path: '/', component: HomeScreen, name: 'Home' },  // 主页
    { path: '/file-selection', component: FileSelectionScreen, name: 'FileSelection' },  // 文件选择屏幕
    { path: '/feature-extraction', component: FeatureExtractionScreen, name: 'FeatureExtraction' }  // 特征提取屏幕
];

// 创建路由器实例
const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 历史模式
    routes // 将路由配置传递到路由器
});

// 创建 Vue 应用实例，并使用路由
const app = createApp(App);
app.use(router);
app.mount('#app'); // 挂载应用到 DOM
