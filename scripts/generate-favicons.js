/**
 * 生成网站图标指南
 * 
 * 本文件描述了如何从SVG源文件生成各种尺寸和格式的网站图标
 * 
 * 需要安装的工具:
 * - Sharp (Node.js图像处理库): npm install sharp
 * - svgexport (SVG导出工具): npm install -g svgexport
 * 
 * 生成步骤:
 * 
 * 1. 从SVG生成PNG (使用svgexport)
 *    svgexport frontend/src/assets/logo.svg frontend/public/logo.png 512:512
 * 
 * 2. 生成favicon.ico (使用Sharp)
 *    使用以下Node.js代码:
 */

// 使用sharp生成favicon.ico的示例代码
// 保存为一个单独的脚本并运行: node generate-favicon.js

/*
const sharp = require('sharp');

async function generateFavicon() {
  try {
    // 从SVG生成一个高质量的PNG
    await sharp('frontend/src/assets/logo.svg')
      .resize(256) // 最大尺寸
      .toFile('frontend/public/favicon-256.png');
    
    // 创建包含多种尺寸的favicon.ico
    // favicon.ico通常包含16x16, 32x32, 48x48尺寸
    await sharp('frontend/public/favicon-256.png')
      .resize(16)
      .toBuffer()
      .then(data16 => {
        return sharp('frontend/public/favicon-256.png')
          .resize(32)
          .toBuffer()
          .then(data32 => {
            return sharp('frontend/public/favicon-256.png')
              .resize(48)
              .toBuffer()
              .then(data48 => {
                return sharp(data16)
                  .toFile('frontend/public/favicon.ico');
              });
          });
      });
      
    // 生成Apple Touch Icon (180x180)
    await sharp('frontend/src/assets/logo.svg')
      .resize(180)
      .toFile('frontend/public/apple-touch-icon.png');
      
    console.log('所有图标已成功生成!');
  } catch (error) {
    console.error('生成图标时出错:', error);
  }
}

generateFavicon();
*/

/**
 * 3. 将生成的图标复制到正确的位置
 *    - favicon.ico 应放在网站根目录
 *    - 其他尺寸的图标可以放在assets目录中
 * 
 * 4. 在HTML中引用图标
 *    <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
 *    <link rel="alternate icon" href="/favicon.ico" />
 *    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
 */ 