import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Anthropic 经济指数 | Economic Index',
      description: '探索人工智能对不同职业的影响和自动化程度，了解各职业的任务分布和AI占比。Explore the impact of artificial intelligence on different occupations and their automation levels. Understand task distribution and AI percentage across various professions.'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 动态更新页面标题
router.beforeEach((to, from, next) => {
  // 更新文档标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 更新meta描述
  if (to.meta.description) {
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', to.meta.description)
    }
  }
  
  next()
})

export default router 