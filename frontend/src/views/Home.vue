<template>
  <div class="max-w-7xl mx-auto px-4 py-4">
    <!-- 搜索区域 -->
    <search-component @select-occupation="selectOccupation" />

    <!-- 职业任务分布卡片 -->
    <tasks-chart-component :tasks="popularTasks" />

    <!-- 职业统计卡片 -->
    <occupation-rank-chart :stats="occupationStats" @limit-change="handleLimitChange" />
  </div>
</template>

<script>
import { ref } from 'vue'
import i18n from '../i18n'
import { occupationApi } from '../api'
import SearchComponent from '../components/SearchComponent.vue'
import TasksChartComponent from '../components/TasksChartComponent.vue'
import OccupationRankChart from '../components/OccupationRankChart.vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Home',
  components: {
    SearchComponent,
    TasksChartComponent,
    OccupationRankChart
  },
  setup() {
    const { t } = i18n.global
    
    const loading = ref(false)
    const popularTasks = ref([])
    const occupationStats = ref([])
    
    // 获取职业统计数据
    const fetchOccupationStats = async (limit = 20) => {
      try {
        const response = await occupationApi.getStats(limit)
        occupationStats.value = response.data.stats
      } catch (error) {
        console.error('获取职业统计数据失败:', error)
        ElMessage.error(t('occupation.statsError'))
      }
    }
    
    // 处理 limit 变化
    const handleLimitChange = (newLimit) => {
      fetchOccupationStats(newLimit)
    }
    
    // 选择职业
    const selectOccupation = async (title) => {
      loading.value = true
      
      try {
        // 获取职业任务分布
        const hasEnglish = /[a-zA-Z]/.test(title)
        const language = hasEnglish ? 'en' : 'cn'
        const response = await occupationApi.getTasks(title, language)
        popularTasks.value = response.data.tasks
        
        // 更新页面标题，提高SEO（中英文双语）
        document.title = `${title} - Anthropic 经济指数 | Economic Index`
        
        // 更新meta描述（中英文双语）
        const metaDescription = document.querySelector('meta[name="description"]')
        if (metaDescription) {
          metaDescription.setAttribute('content', 
            `查看${title}的AI任务分布和自动化程度分析，了解AI如何影响该职业。` +
            `View AI task distribution and automation level analysis for ${title}, understand how AI impacts this profession.`
          )
        }
      } catch (error) {
        console.error('获取任务分布失败:', error)
        ElMessage.error(t('occupation.dataError'))
      } finally {
        loading.value = false
      }
    }

    // 页面加载时获取统计数据
    fetchOccupationStats()

    return {
      t,
      loading,
      popularTasks,
      occupationStats,
      selectOccupation,
      handleLimitChange
    }
  }
}
</script> 