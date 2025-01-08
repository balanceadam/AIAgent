import { fileURLToPath, URL } from 'node:url'

import { defineConfig, ConfigEnv, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import viteCompression from 'vite-plugin-compression'

// https://vitejs.dev/config/
export default defineConfig(({ mode }: ConfigEnv) => {
  const env = loadEnv(mode, process.cwd())
  console.log('env: ', env)
  return {
    css: {
      preprocessorOptions: {
        scss: {
          silenceDeprecations: ['legacy-js-api', 'color-functions']
        }
      }
    },
    plugins: [
      vue(),
      AutoImport({
        resolvers: [],
        // 自定引入 Vue VueRouter API,如果还需要其他的可以自行引入
        imports: [
          'vue',
          'vue-router',
          {
            'naive-ui': ['useDialog', 'useMessage', 'useNotification']
          }
        ],
        // 调整自动引入的文件位置
        dts: 'src/types/auto-import.d.ts',
        // 解决自动引入eslint报错问题 需要在eslintrc的extend选项中引入
        eslintrc: {
          enabled: true,
          // 配置文件的位置
          filepath: './.eslintrc-auto-import.json',
          globalsPropValue: true
        }
      }),
      Components({
        dirs: ['src/components'],
        resolvers: [NaiveUiResolver()],
        dts: 'src/types/components.d.ts'
      }),
      createSvgIconsPlugin({
        // 指定需要缓存的图标文件夹
        iconDirs: [fileURLToPath(new URL('./src/assets/icons', import.meta.url))],
        // 指定symbolId格式
        symbolId: 'icon-[dir]-[name]'
      }),
      viteCompression({
        algorithm: 'gzip',
        deleteOriginFile: false,
        threshold: 10240
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      proxy: {
        [env.VITE_APP_API_PREFIX]: {
          target: env.VITE_APP_API_ORIGIN,
          changeOrigin: true
          // rewrite: (path) => path.replace(new RegExp(`^${env.VITE_APP_API_PREFIX}`), '')
        }
      }
    }
  }
})
