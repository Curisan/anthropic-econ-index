# Anthropic Economic Index (Anthropic 经济指数)

基于 Anthropic Claude API 的职业任务分析系统，帮助了解 AI 对不同职业的影响程度。

## 功能特点

- 职业搜索：支持中英文职业搜索
- 任务分布：展示各职业的 AI 相关任务分布
- 对话占比：展示职业的 AI 对话使用频率排名
- 任务分析：展示职业的非零任务占比分析
- 热门任务：展示对话占比最高的任务列表

## 技术栈

### 前端
- Vue 3
- Element Plus
- ECharts
- TailwindCSS
- Vue I18n

### 后端
- FastAPI
- PostgreSQL
- Anthropic Claude API

## 部署指南

### 本地开发

1. 克隆仓库
```bash
git clone https://github.com/yourusername/anthropic-econ-index.git
cd anthropic-econ-index
```

2. 安装前端依赖
```bash
cd frontend
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

### Netlify 部署

1. Fork 本仓库

2. 在 Netlify 中创建新站点，选择从 Git 导入

3. 配置构建设置：
   见 `netlify.toml` 文件

4. 设置环境变量：
   - 添加 `API_URL` 环境变量，设置为你的后端 API 地址

5. 部署完成后，你可以通过 Netlify 分配的域名访问站点

### 环境变量

- `API_URL`: 后端 API 地址，例如 `http://your-api-domain.com`

## 开发指南

### 目录结构
```
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API 请求
│   │   ├── components/    # Vue 组件
│   │   ├── i18n/         # 国际化配置
│   │   ├── views/        # 页面视图
│   │   └── App.vue       # 根组件
│   └── package.json
├── backend/               # 后端代码
└── netlify.toml          # Netlify 配置文件
```

### 国际化

项目支持中英文双语：
- 中文配置：`frontend/src/i18n/locales/zh-CN.json`
- 英文配置：`frontend/src/i18n/locales/en-US.json`

## License

MIT License
