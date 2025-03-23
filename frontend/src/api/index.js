import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

export const occupationApi = {
  // 搜索职业数据
  search(keyword, language = 'cn') {
    return api.get('/occupation/search', { 
      params: { 
        keyword,
        language 
      } 
    })
  },
  
  // 获取职业任务
  getOccupationTasks(onetSocCode) {
    return api.get(`/occupation/${onetSocCode}/tasks`)
  },
  
  // 获取热门职业
  getPopular() {
    return api.get('/occupation/popular')
  },
  
  // 提交反馈
  submitFeedback(formData) {
    if (formData instanceof FormData) {
      return api.post('/feedback', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    } else {
      // 支持直接传入对象格式
      const data = new FormData();
      for (const key in formData) {
        data.append(key, formData[key]);
      }
      return api.post('/feedback', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    }
  },
  
  // 记录访问
  recordVisit() {
    return api.post('/stats/visit')
  },
  
  // 记录搜索
  recordSearch(query) {
    return api.post('/stats/search', { query })
  },
  
  // 获取职业任务分布
  getTasks: (title, language = 'cn') => {
    return api.get('/occupation/tasks', {
      params: {
        title,
        language
      }
    })
  }
}

export default api 