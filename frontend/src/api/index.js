import axios from 'axios'

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '/api',
  timeout: 5000
})

export const occupationApi = {
  // 搜索职业数据
  search(query) {
    return api.get('/occupation/search', { params: { query } })
  },
  
  // 获取热门职业
  getPopular() {
    return api.get('/occupation/popular')
  },
  
  // 提交反馈
  submitFeedback(data) {
    return api.post('/feedback', data)
  },
  
  // 记录访问
  recordVisit() {
    return api.post('/stats/visit')
  },
  
  // 记录搜索
  recordSearch(query) {
    return api.post('/stats/search', { query })
  }
}

export default api 