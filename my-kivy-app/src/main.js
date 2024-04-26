import { createApp } from 'vue'; // Vue 3 的创建方法
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router'; // Vue 路由创建方法

// 引入页面组件
import HomeScreen from "@/view/HomeScreen.vue";
import FileSelectionScreen from "@/view/SelectScreen.vue";
import FeatureExtractionScreen from "@/view/FeatureExtractionScreen.vue"; // 特征提取屏幕

// 定义路由配置
const routes = [
    { path: '/', component: HomeScreen, name: 'home' },
    { path: '/file-selection', component: FileSelectionScreen },
    { path: '/feature-extraction', component: FeatureExtractionScreen },
    // 其他路由配置
];

// 创建路由器实例
const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 历史模式
    routes // 路由列表
});

// 创建 Vue 应用实例，并使用路由
createApp(App).use(router).mount('#app');
