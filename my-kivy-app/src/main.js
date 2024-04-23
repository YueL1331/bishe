import { createApp } from 'vue'; // 使用 Vue 3 的 createApp 方法
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router'; // 使用 Vue 3 的路由创建方法

// 这里引入你的页面组件
import HomeScreen from "@/view/HomeScreen.vue";
import FileSelection from "@/view/SelectScreen.vue";

// 定义路由配置
const routes = [
    { path: '/', component: HomeScreen, name: 'home' },
    { path: '/file-selection', component: FileSelection },
    // 其他路由配置
];

// 创建路由器实例
const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 History 模式
    routes
});

// 创建 Vue 应用实例，并将路由器实例传递进去
createApp(App).use(router).mount('#app');
