// 在HTML中直接使用SVG图标
// 这个脚本创建一个内联的favicon元素，确保在各种浏览器中都能正确显示

document.addEventListener('DOMContentLoaded', () => {
  // 创建一个favicons数组，包含不同尺寸的图标链接，适配各种移动设备
  const faviconsHTML = `
    <!-- 基本SVG图标 -->
    <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
    
    <!-- 传统favicon - 用于不支持SVG的浏览器 -->
    <link rel="alternate icon" href="/favicon.ico" />
    
    <!-- iOS图标尺寸 -->
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
    <link rel="apple-touch-icon" sizes="152x152" href="/assets/apple-touch-icon-152x152.png" />
    <link rel="apple-touch-icon" sizes="167x167" href="/assets/apple-touch-icon-167x167.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon-180x180.png" />
    
    <!-- Android图标 -->
    <link rel="icon" type="image/png" sizes="192x192" href="/assets/android-chrome-192x192.png" />
    <link rel="icon" type="image/png" sizes="512x512" href="/assets/android-chrome-512x512.png" />
    
    <!-- Windows平板和手机 -->
    <meta name="msapplication-TileImage" content="/assets/mstile-144x144.png" />
    <meta name="msapplication-TileColor" content="#2D6CDF" />
    
    <!-- Safari Pinned Tab -->
    <link rel="mask-icon" href="/assets/safari-pinned-tab.svg" color="#2D6CDF" />
  `;
  
  // 将图标链接插入到head中
  document.head.insertAdjacentHTML('beforeend', faviconsHTML);
}); 