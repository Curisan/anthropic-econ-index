import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { copyFileSync, mkdirSync, existsSync, readdirSync } from 'fs'

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
          
          // 处理public目录中的所有图标文件
          const publicDir = path.resolve(__dirname, 'public');
          if (existsSync(publicDir)) {
            const files = readdirSync(publicDir);
            
            // 复制所有图标文件到dist根目录
            for (const file of files) {
              // 跳过目录
              const filePath = path.resolve(publicDir, file);
              if (existsSync(filePath) && !filePath.includes('assets') && file !== '.DS_Store') {
                copyFileSync(filePath, path.resolve(__dirname, 'dist', file));
              }
            }
            
            // 复制assets子目录的文件
            const publicAssetsDir = path.resolve(publicDir, 'assets');
            if (existsSync(publicAssetsDir)) {
              const assetFiles = readdirSync(publicAssetsDir);
              for (const file of assetFiles) {
                if (file !== '.DS_Store') {
                  copyFileSync(
                    path.resolve(publicAssetsDir, file),
                    path.resolve(assetsDir, file)
                  );
                }
              }
            }
          }
          
          console.log('SEO文件和图标已成功复制到dist目录');
        } catch (err) {
          console.error('复制文件时出错:', err);
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