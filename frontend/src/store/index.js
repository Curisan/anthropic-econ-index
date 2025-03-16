import { createStore } from 'vuex'

export default createStore({
  state: {
    occupationData: null,
    searchHistory: [],
    visitCount: 0
  },
  
  mutations: {
    SET_OCCUPATION_DATA(state, data) {
      state.occupationData = data
    },
    ADD_SEARCH_HISTORY(state, query) {
      state.searchHistory.unshift(query)
      if (state.searchHistory.length > 10) {
        state.searchHistory.pop()
      }
    },
    INCREMENT_VISIT_COUNT(state) {
      state.visitCount++
    }
  },
  
  actions: {
    async searchOccupation({ commit }, query) {
      try {
        // TODO: 实现搜索 API 调用
        const response = await fetch(`/api/occupation?query=${query}`)
        const data = await response.json()
        commit('SET_OCCUPATION_DATA', data)
        commit('ADD_SEARCH_HISTORY', query)
      } catch (error) {
        console.error('搜索失败:', error)
        throw error
      }
    },
    
    recordVisit({ commit }) {
      commit('INCREMENT_VISIT_COUNT')
      // TODO: 实现访问统计 API 调用
    }
  },
  
  getters: {
    getOccupationData: state => state.occupationData,
    getSearchHistory: state => state.searchHistory,
    getVisitCount: state => state.visitCount
  }
}) 