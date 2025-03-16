import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import i18n from './i18n'
import './assets/styles/main.scss'

const app = createApp(App)

app.use(router)
   .use(store)
   .use(ElementPlus)
   .use(i18n)
   .mount('#app') 