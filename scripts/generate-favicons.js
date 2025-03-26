/**
 * 生成网站图标指南 - 移动设备优化版
 * 
 * 本文件描述了如何从SVG源文件生成各种尺寸和格式的网站图标，适配各种设备包括移动设备
 * 
 * 需要安装的工具:
 * - Sharp (Node.js图像处理库): npm install sharp
 * - svgexport (SVG导出工具): npm install -g svgexport
 * 
 * 生成步骤:
 * 
 * 1. 从SVG生成基础PNG (使用svgexport)
 *    svgexport frontend/src/assets/logo.svg frontend/public/logo.png 512:512
 * 
 * 2. 生成各种尺寸的图标 (使用Sharp)
 *    使用以下Node.js代码:
 */

// 使用sharp生成各种尺寸图标的示例代码
// 保存为一个单独的脚本并运行: node generate-favicons.js

/*
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// 确保目标目录存在
const publicDir = path.resolve(__dirname, '../frontend/public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

const assetsDir = path.resolve(publicDir, 'assets');
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir, { recursive: true });
}

async function generateFavicons() {
  try {
    const svgSource = path.resolve(__dirname, '../frontend/src/assets/logo.svg');
    
    // 从SVG生成一个高质量的PNG基础图片
    await sharp(svgSource)
      .resize(512) // 最大尺寸
      .toFile(path.resolve(publicDir, 'logo-512.png'));
    
    // 创建各种iOS设备尺寸的图标
    const iosSizes = [180, 167, 152, 120, 114, 76, 72, 60, 57];
    for (const size of iosSizes) {
      await sharp(path.resolve(publicDir, 'logo-512.png'))
        .resize(size)
        .toFile(path.resolve(publicDir, `apple-touch-icon${size === 180 ? '' : `-${size}x${size}`}.png`));
    }
    
    // 创建Android设备的图标
    const androidSizes = [512, 384, 192, 144, 96, 72, 48, 36];
    for (const size of androidSizes) {
      await sharp(path.resolve(publicDir, 'logo-512.png'))
        .resize(size)
        .toFile(path.resolve(publicDir, `android-chrome-${size}x${size}.png`));
    }
    
    // 创建Windows平板和手机的图标
    const windowsSizes = [144, 70];
    for (const size of windowsSizes) {
      await sharp(path.resolve(publicDir, 'logo-512.png'))
        .resize(size)
        .toFile(path.resolve(publicDir, `mstile-${size}x${size}.png`));
    }
    
    // 创建包含多种尺寸的favicon.ico
    // favicon.ico通常包含16x16, 32x32, 48x48尺寸
    const icoSizes = [16, 32, 48];
    const icoBuffers = [];
    
    for (const size of icoSizes) {
      const buffer = await sharp(path.resolve(publicDir, 'logo-512.png'))
        .resize(size)
        .toBuffer();
      icoBuffers.push(buffer);
    }
    
    // 使用第一个尺寸创建favicon.ico
    // 注意：完整的多尺寸ICO需要特殊库支持
    await sharp(icoBuffers[1])
      .toFile(path.resolve(publicDir, 'favicon.ico'));
      
    console.log('所有图标已成功生成!');
  } catch (error) {
    console.error('生成图标时出错:', error);
  }
}

generateFavicons();
*/

/**
 * 3. 将生成的图标复制到正确的位置
 *    - 所有图标文件应放在public目录中，构建时会自动复制到网站根目录
 * 
 * 4. 在HTML中引用图标，或使用我们的动态favicon.js脚本:
 *    
 *    <!-- 基本SVG图标 -->
 *    <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
 *    
 *    <!-- 传统favicon - 用于不支持SVG的浏览器 -->
 *    <link rel="alternate icon" href="/favicon.ico" />
 *    
 *    <!-- iOS图标尺寸 -->
 *    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
 *    <link rel="apple-touch-icon" sizes="152x152" href="/assets/apple-touch-icon-152x152.png" />
 *    <link rel="apple-touch-icon" sizes="167x167" href="/assets/apple-touch-icon-167x167.png" />
 *    <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon-180x180.png" />
 *    
 *    <!-- Android图标 -->
 *    <link rel="icon" type="image/png" sizes="192x192" href="/assets/android-chrome-192x192.png" />
 *    <link rel="icon" type="image/png" sizes="512x512" href="/assets/android-chrome-512x512.png" />
 *    
 *    <!-- Windows平板和手机 -->
 *    <meta name="msapplication-TileImage" content="/assets/mstile-144x144.png" />
 *    <meta name="msapplication-TileColor" content="#2D6CDF" />
 *    
 *    <!-- Safari Pinned Tab -->
 *    <link rel="mask-icon" href="/assets/safari-pinned-tab.svg" color="#2D6CDF" />
 */ 