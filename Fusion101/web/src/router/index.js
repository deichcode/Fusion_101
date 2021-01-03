import {createRouter, createWebHashHistory} from 'vue-router'

// Define routes for navigation inside the palette web app accordingly to https://router.vuejs.org/guide/
const routes = [
    // routing for multiple tutorials.json
    // {
    //   path: '/',
    //   name: 'Overview of all available Tutorials',
    //   component: TutorialsOverview
    // },
    // routing as long as only single tutorial exists
    {
        path: '/',
        redirect: '/tutorial-contents/building-a-house'
    },
    {
        path: '/tutorial-contents',
        redirect: '/'
    },
    {
        path: '/tutorial-contents/:tutorialId',
        name: 'tutorial-contents',
        component: () => import(/* webpackChunkName: "[request]" */ '../views/TutorialContents.vue') //https://vuedose.tips/naming-webpack-chunks-on-lazy-loaded-routes-in-vuejs/
    },
    {
        path: '/tutorial-chapter/:tutorialId/:chapterId',
        name: 'chapter',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "[request]" */ '../views/TutorialChapter.vue') //https://vuedose.tips/naming-webpack-chunks-on-lazy-loaded-routes-in-vuejs/
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
