// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../view/HomeScreen.vue'
import ImageStitching from '../view/SelectScreen.vue'
import RegionSelection from '../view/FeatureExtractionScreen.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/image-stitching', component: ImageStitching },
  { path: '/region-selection', component: RegionSelection }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;

