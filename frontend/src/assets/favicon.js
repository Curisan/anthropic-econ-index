// 在HTML中直接使用SVG图标
// 这个脚本创建一个内联的favicon元素，确保在各种浏览器中都能正确显示

document.addEventListener('DOMContentLoaded', () => {
  // 创建一个favicons数组，包含不同尺寸的图标链接
  const faviconsHTML = `
    <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
    <link rel="alternate icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
  `;
  
  // 将图标链接插入到head中
  document.head.insertAdjacentHTML('beforeend', faviconsHTML);
}); 