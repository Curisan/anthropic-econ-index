import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { copyFileSync, mkdirSync, existsSync } from 'fs'

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'copy-seo-files',
      closeBundle() {
        try {
          // 复制SEO相关文件到dist目录
          copyFileSync(path.resolve(__dirname, 'robots.txt'), path.resolve(__dirname, 'dist/robots.txt'));
          copyFileSync(path.resolve(__dirname, 'sitemap.xml'), path.resolve(__dirname, 'dist/sitemap.xml'));
          
          // 确保dist/assets目录存在
          const assetsDir = path.resolve(__dirname, 'dist/assets');
          if (!existsSync(assetsDir)) {
            mkdirSync(assetsDir, { recursive: true });
          }
          
          // 复制SVG图标到dist/assets目录
          copyFileSync(
            path.resolve(__dirname, 'src/assets/logo.svg'), 
            path.resolve(__dirname, 'dist/assets/logo.svg')
          );
          
          // 如果public目录中存在favicon.ico，复制到dist根目录
          const faviconSrc = path.resolve(__dirname, 'public/favicon.ico');
          const appleTouchIconSrc = path.resolve(__dirname, 'public/apple-touch-icon.png');
          
          if (existsSync(faviconSrc)) {
            copyFileSync(faviconSrc, path.resolve(__dirname, 'dist/favicon.ico'));
          }
          
          if (existsSync(appleTouchIconSrc)) {
            copyFileSync(appleTouchIconSrc, path.resolve(__dirname, 'dist/apple-touch-icon.png'));
          }
          
          console.log('SEO files and icons copied to dist directory');
        } catch (err) {
          console.error('Error copying files:', err);
        }
      }
    }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5010',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')  // 使用新的rewrite方法
      }
    }
  },
  build: {
    assetsInlineLimit: 0, // 确保SVG不会被内联为base64
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name.endsWith('.svg')) {
            return 'assets/[name][extname]';
          }
          return 'assets/[name]-[hash][extname]';
        }
      }
    }
  },
  // 定义public目录，里面的文件会被复制到构建目录的根目录下
  publicDir: 'public'
}) 