import '@/assets/scss/main.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createDiscreteApi } from 'naive-ui'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import 'virtual:svg-icons-register'

declare global {
  interface Window {
    $message: ReturnType<typeof useMessage>
    $notification: ReturnType<typeof useNotification>
  }
}

const { message, notification } = createDiscreteApi(['message', 'notification'])

window.$message = message
window.$notification = notification

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.mount('#app')
