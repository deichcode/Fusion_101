import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
require('./css/globals/_main.scss')

createApp(App).use(router).mount('#app')