// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/view/HomeScreen.vue'
import FileSelection from "@/view/SelectScreen.vue";
import FeatureExtraction from "@/view/FeatureExtractionScreen.vue";
import SplitScreen from "@/view/SplitScreen.vue";



const routes = [
    { path: '/', component: Home },
    { path: '/file-selection', component: FileSelection },
    { path: '/feature-extraction', component: FeatureExtraction },
    { path: '/image-stitching', component: SplitScreen },
    // { path: '/region-selection', component: RegionSelection }
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
