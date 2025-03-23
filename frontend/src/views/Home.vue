<template>
  <div class="home-container">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        :placeholder="t('occupation.searchPlaceholder')"
        class="search-input"
        @input="handleSearchInput"
      >
        <!-- <template #append>
          <el-button type="primary" @click="handleSearch">
            {{ t('common.search') }}
          </el-button>
        </template> -->
      </el-input>

      <!-- 搜索结果下拉列表 -->
      <div v-if="showSearchResults && searchResults.length > 0" class="search-results">
        <ul>
          <li 
            v-for="title in searchResults" 
            :key="title"
            @click="selectOccupation(title)"
          >
            <div class="search-item">
              <i class="el-icon-search"></i>
              <span class="search-text">{{ title }}</span>
            </div>
          </li>
        </ul>
      </div>
      
      <!-- 无搜索结果提示 -->
      <div v-if="showSearchResults && searchResults.length === 0 && searchQuery" class="no-results">
        {{ t('occupation.noResults') }}
      </div>
    </div>

    <!-- 职业任务分布卡片 -->
    <div class="card-container">
      <div class="chart-container" ref="tasksBarChartRef"></div>
    </div>

    <!-- 数据展示区域已移除 -->
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
// import { useI18n } from 'vue-i18n'
import i18n from '../i18n'
import { occupationApi } from '../api'
import debounce from 'lodash/debounce'

export default {
  name: 'Home',
  setup() {
    // const { t } = useI18n()
    const { t } = i18n.global
    
    const searchQuery = ref('')
    const loading = ref(false)
    const popularTasks = ref([])
    const searchResults = ref([])
    const showSearchResults = ref(false)
    
    // echarts 实例
    let tasksBarChart = null
    
    const tasksBarChartRef = ref(null)

    // 初始化图表
    const initCharts = () => {
      // 职业任务分布横向柱状图
      tasksBarChart = echarts.init(tasksBarChartRef.value)
      tasksBarChart.setOption({
        backgroundColor: 'transparent',
        legend: {
          show: false
        },
        grid: {
          left: '3%',
          right: '10%',
          bottom: '5%',
          top: '5%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}%'
        },
        xAxis: {
          type: 'value',
          name: '占比',
          nameLocation: 'end',
          nameTextStyle: {
            color: '#666',
            fontSize: 14
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ccc'
            }
          },
          axisTick: {
            show: true
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: '#eee'
            }
          },
          axisLabel: {
            show: true,
            color: '#666',
            formatter: '{value}%'
          }
        },
        yAxis: {
          type: 'category',
          data: [],
          inverse: true,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ccc'
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            show: true,
            color: '#666',
            fontSize: 14,
            width: 350,
            overflow: 'truncate'
          }
        },
        series: [
          {
            name: '任务占比',
            type: 'bar',
            barWidth: '60%',
            data: [],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#4facfe' },
                { offset: 1, color: '#00f2fe' }
              ]),
              borderRadius: [0, 4, 4, 0]
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c}%',
              color: '#666',
              fontSize: 14
            }
          }
        ]
      });
    }

    // 防抖处理搜索输入
    const handleSearchInput = debounce(async () => {
      if (searchQuery.value.length < 2) {
        searchResults.value = []
        showSearchResults.value = false
        return
      }
      
      try {
        // 判断搜索关键词是否包含英文字符
        const hasEnglish = /[a-zA-Z]/.test(searchQuery.value)
        const language = hasEnglish ? 'en' : 'cn'
        const response = await occupationApi.search(searchQuery.value, language)
        searchResults.value = response.data.occupations
        showSearchResults.value = true
      } catch (error) {
        console.error('搜索失败:', error)
        searchResults.value = []
      }
    }, 300)
    
    // 处理搜索按钮点击
    const handleSearch = async () => {
      if (!searchQuery.value) return
      
      loading.value = true
      try {
        // 判断搜索关键词是否包含英文字符
        const hasEnglish = /[a-zA-Z]/.test(searchQuery.value)
        const language = hasEnglish ? 'en' : 'cn'
        const response = await occupationApi.search(searchQuery.value, language)
        searchResults.value = response.data.occupations
        showSearchResults.value = true
      } catch (error) {
        console.error('搜索失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 选择职业
    const selectOccupation = async (title) => {
      searchQuery.value = title
      showSearchResults.value = false
      loading.value = true
      
      try {
        // 获取职业任务分布
        const hasEnglish = /[a-zA-Z]/.test(title)
        const language = hasEnglish ? 'en' : 'cn'
        const response = await occupationApi.getTasks(title, language)
        popularTasks.value = response.data.tasks

        // 更新任务分布柱状图
        if (tasksBarChart) {
          const tasks = response.data.tasks
          // 按百分比降序排序
          const sortedTasks = [...tasks].sort((a, b) => b.percentage - a.percentage)
          
          // 更新图表数据
          tasksBarChart.setOption({
            yAxis: {
              data: sortedTasks.map(t => t.task)
            },
            series: [{
              data: sortedTasks.map(t => t.percentage)
            }]
          })
          
          // 延迟调整大小，确保渲染完成
          setTimeout(() => {
            tasksBarChart.resize();
          }, 200);
        }
      } catch (error) {
        console.error('获取任务分布失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 点击外部关闭搜索结果
    const handleClickOutside = (event) => {
      const searchSection = document.querySelector('.search-section')
      if (searchSection && !searchSection.contains(event.target)) {
        showSearchResults.value = false
      }
    }

    // 监听窗口大小变化
    const handleResize = () => {
      tasksBarChart?.resize()
    }

    onMounted(() => {
      initCharts()
      window.addEventListener('resize', handleResize)
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      document.removeEventListener('click', handleClickOutside)
      tasksBarChart?.dispose()
    })

    return {
      t,
      searchQuery,
      loading,
      popularTasks,
      searchResults,
      showSearchResults,
      tasksBarChartRef,
      handleSearchInput,
      handleSearch,
      selectOccupation
    }
  }
}
</script>

<style lang="scss" scoped>
.home-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;

  .search-section {
    margin: 40px 0;
    position: relative;
    width: 100%;
    max-width: 600px;
    margin-left: 0;
    
    .search-input {
      width: 100%;

      :deep(.el-input__wrapper) {
        background-color: #fff;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        box-shadow: none;
        transition: all 0.3s;

        &:hover, &.is-focus {
          border-color: var(--el-color-primary);
        }
      }

      :deep(.el-input__inner) {
        height: 40px;
        line-height: 40px;
        font-size: 14px;
        padding: 0 15px;
        
        &::placeholder {
          color: #909399;
        }
      }

      :deep(.el-input-group__append) {
        padding: 0 20px;
        background-color: var(--el-color-primary);
        border-color: var(--el-color-primary);
        
        .el-button {
          padding: 0;
          border: none;
          color: #fff;
          font-size: 14px;
          
          &:hover {
            color: #fff;
            background-color: transparent;
          }
        }
      }
    }
  }

  .card-container {
    background-color: var(--el-bg-color-overlay);
    border-radius: 8px;
    padding: 0 24px 24px 0;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .chart-container {
      height: 380px;
    }
  }

  .data-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 24px;
    margin-top: 24px;

    .chart-card {
      background-color: var(--el-bg-color-overlay);
      border: none;
      border-radius: 8px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

      :deep(.el-card__header) {
        padding: 16px 20px;
        border-bottom: 1px solid var(--el-border-color-light);
      }

      .card-header {
        font-size: 16px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }

      :deep(.el-card__body) {
        padding: 20px;
      }

      .chart-container {
        height: 300px;
      }

      .table-container {
        max-height: 300px;
        overflow-y: auto;
      }

      :deep(.el-table) {
        --el-table-border-color: var(--el-border-color-lighter);
        --el-table-header-bg-color: var(--el-fill-color-light);
        
        th {
          background-color: var(--el-table-header-bg-color);
          color: var(--el-text-color-regular);
          font-weight: 600;
        }

        td {
          color: var(--el-text-color-regular);
        }
      }
    }
  }

  // 搜索结果样式
  .search-results {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    max-height: 300px;
    overflow-y: auto;
    z-index: 2000;
    
    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      
      li {
        padding: 0;
        cursor: pointer;
        
        &:hover {
          background-color: var(--el-color-primary-light-9);
        }
        
        .search-item {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          
          i {
            margin-right: 8px;
            color: #909399;
            font-size: 16px;
          }
          
          .search-text {
            color: var(--el-text-color-primary);
            font-size: 14px;
          }
        }
      }
    }
  }
  
  .no-results {
    position: absolute;
    top: calc(100% + 8px);
    left: 0;
    right: 0;
    background-color: #fff;
    padding: 16px;
    text-align: center;
    color: #909399;
    font-size: 14px;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    z-index: 2000;
  }
}
</style> 