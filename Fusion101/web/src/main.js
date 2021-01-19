import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

import {library} from "@fortawesome/fontawesome-svg-core";
import {faLightbulb as regularFaLightbulb} from "@fortawesome/free-regular-svg-icons";
import {faLightbulb} from "@fortawesome/free-solid-svg-icons";
import {faCheck} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

library.add(regularFaLightbulb)
library.add(faLightbulb)
library.add(faCheck)

require('./css/globals/_main.scss')

createApp(App)
    .use(router)
    .component('font-awesome-icon', FontAwesomeIcon)
    .mount('#app')
