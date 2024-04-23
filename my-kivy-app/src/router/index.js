Vue.use(Router);

export default new Router({
    mode: 'history',
    routes: [
        { path: '/', component: Home },
        { path: '/file-selection', component: FileSelection },
    //     { path: '/feature-extraction', component: FeatureExtraction },
    //     { path: '/image-stitching', component: ImageStitching },
    //     { path: '/region-selection', component: RegionSelection }
    ]
});
