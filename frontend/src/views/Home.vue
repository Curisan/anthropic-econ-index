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
        <template #append>
          <el-button type="primary" @click="handleSearch">
            {{ t('common.search') }}
          </el-button>
        </template>
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

    <!-- GDP增长率卡片 -->
    <div class="card-container">
      <div class="chart-title">GDP增长率</div>
      <div class="chart-subtitle">按季度统计的国内生产总值增长率</div>
      <div class="chart-container" ref="gdpChartRef"></div>
    </div>

    <!-- 数据展示区域 -->
    <div class="data-section" v-loading="loading">
      <!-- AI 使用率排行榜 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>{{ t('occupation.aiUsageRate') }}</span>
          </div>
        </template>
        <div class="chart-container" ref="aiUsageChartRef"></div>
      </el-card>

      <!-- 任务分布图表 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>{{ t('occupation.taskDistribution') }}</span>
          </div>
        </template>
        <div class="chart-container" ref="taskDistributionChartRef"></div>
      </el-card>

      <!-- 热门 AI 任务列表 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>{{ t('occupation.popularTasks') }}</span>
          </div>
        </template>
        <div class="table-container">
          <el-table :data="popularTasks" style="width: 100%">
            <el-table-column prop="task" :label="t('occupation.task')" />
            <el-table-column prop="percentage" :label="t('occupation.percentage')" />
          </el-table>
        </div>
      </el-card>
    </div>
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
    let gdpChart = null
    let aiUsageChart = null
    let taskDistributionChart = null
    
    const gdpChartRef = ref(null)
    const aiUsageChartRef = ref(null)
    const taskDistributionChartRef = ref(null)

    // 初始化图表
    const initCharts = () => {
      // GDP增长率图表
      gdpChart = echarts.init(gdpChartRef.value)
      gdpChart.setOption({
        backgroundColor: 'transparent',
        title: {
          text: '任务分布',
          left: 'center',
          top: 10,
          textStyle: {
            color: '#ffffff',
            fontSize: 18,
            fontWeight: 'bold'
          },
          subtext: '按任务重要程度排序',
          subtextStyle: {
            color: '#d1d1d1',
            fontSize: 14
          }
        },
        legend: {
          show: false
        },
        grid: {
          left: '30%',
          right: '10%',
          bottom: '5%',
          top: '20%',
          containLabel: true // 确保标签包含在内
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'value',
          position: 'top',
          name: '占比',
          nameLocation: 'end',
          nameTextStyle: {
            color: '#ffffff',
            fontSize: 14,
            padding: [5, 0, 0, 0]
          },
          max: function(value) {
            return Math.ceil(value.max * 1.2);
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ffffff',
              width: 2
            }
          },
          axisTick: {
            show: true,
            length: 5,
            lineStyle: {
              color: '#ffffff'
            }
          },
          splitLine: {
            show: false
          },
          axisLabel: {
            show: true,
            color: '#ffffff',
            fontSize: 12,
            formatter: '{value}%'
          }
        },
        yAxis: {
          type: 'category',
          inverse: true, // 反转Y轴，使最大值在顶部
          data: [],
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ffffff',
              width: 2
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            show: true,
            inside: false,
            color: '#ffffff',
            fontSize: 14,
            fontWeight: 'bold',
            padding: [0, 20, 0, 0],
            align: 'left',
            verticalAlign: 'middle',
            lineHeight: 20,
            rich: {
              value: {
                color: '#ffffff',
                fontSize: 14,
                fontWeight: 'bold',
                lineHeight: 20
              }
            }
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
                { offset: 0, color: '#39a0ff' },
                { offset: 1, color: '#4ed8da' }
              ]),
              borderRadius: [0, 5, 5, 0]
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c}%',
              color: '#ffffff',
              fontSize: 14,
              fontWeight: 'bold',
              distance: 10
            }
          }
        ]
      });

      // AI 使用率图表
      aiUsageChart = echarts.init(aiUsageChartRef.value)
      aiUsageChart.setOption({
        backgroundColor: 'transparent',
        title: {
          text: t('occupation.aiUsageRate'),
          textStyle: {
            color: '#fff'
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['职业A', '职业B', '职业C', '职业D', '职业E'],
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}%',
            color: 'rgba(255, 255, 255, 0.7)'
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        },
        series: [{
          data: [80, 70, 60, 50, 40],
          type: 'bar',
          itemStyle: {
            color: '#39a0ff'
          }
        }]
      })

      // 任务分布图表
      taskDistributionChart = echarts.init(taskDistributionChartRef.value)
      taskDistributionChart.setOption({
        backgroundColor: 'transparent',
        title: {
          text: t('occupation.taskDistribution'),
          textStyle: {
            color: '#fff'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%'
        },
        series: [{
          type: 'pie',
          radius: '50%',
          itemStyle: {
            color: function(params) {
              const colorList = ['#39a0ff', '#4ed8da', '#25c2e0', '#38a1de', '#505fdf'];
              return colorList[params.dataIndex % colorList.length];
            }
          },
          label: {
            color: '#fff',
            formatter: '{b}\n{c}%'
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          data: []
        }]
      })
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

    // 修改卡片标题
    const updateChartTitle = (title) => {
      if (gdpChart) {
        gdpChart.setOption({
          title: {
            text: title + '的任务分布',
            subtext: '按任务重要程度排序',
            left: 'center',
            textStyle: {
              color: 'rgba(255, 255, 255, 0.7)',
              fontSize: 16
            },
            subtextStyle: {
              color: 'rgba(255, 255, 255, 0.5)',
              fontSize: 12
            }
          }
        });
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

        // 更新任务分布图表
        if (taskDistributionChart) {
          taskDistributionChart.setOption({
            series: [{
              data: popularTasks.value.map(task => ({
                value: task.percentage,
                name: task.task
              }))
            }]
          })
        }

        // 更新任务分布图表（原GDP图表）
        if (gdpChart) {
          const tasks = response.data.tasks
          // 按百分比降序排序
          const sortedTasks = [...tasks].sort((a, b) => b.percentage - a.percentage)
          
          // 更新图表标题和数据
          gdpChart.setOption({
            title: {
              text: title + '的任务分布',
              subtext: '按任务重要程度排序'
            },
            yAxis: {
              data: sortedTasks.map(t => t.task)
            },
            series: [{
              data: sortedTasks.map(t => t.percentage)
            }]
          })
          
          // 延迟调整大小，确保渲染完成
          setTimeout(() => {
            gdpChart.resize();
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
      gdpChart?.resize()
      aiUsageChart?.resize()
      taskDistributionChart?.resize()
    }

    onMounted(() => {
      initCharts()
      window.addEventListener('resize', handleResize)
      document.addEventListener('click', handleClickOutside)
      
      // 修改GDP卡片的标题和说明
      const chartTitleEl = document.querySelector('.card-container .chart-title')
      const chartSubtitleEl = document.querySelector('.card-container .chart-subtitle')
      if (chartTitleEl) chartTitleEl.textContent = '职业任务分布'
      if (chartSubtitleEl) chartSubtitleEl.textContent = '选择职业后显示对应的任务分布'
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      document.removeEventListener('click', handleClickOutside)
      gdpChart?.dispose()
      aiUsageChart?.dispose()
      taskDistributionChart?.dispose()
    })

    return {
      t,
      searchQuery,
      loading,
      popularTasks,
      searchResults,
      showSearchResults,
      gdpChartRef,
      aiUsageChartRef,
      taskDistributionChartRef,
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
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .chart-title {
      font-size: 20px;
      font-weight: 600;
      color: var(--el-text-color-primary);
      margin-bottom: 8px;
      text-align: center;
    }

    .chart-subtitle {
      font-size: 14px;
      color: var(--el-text-color-secondary);
      margin-bottom: 24px;
      text-align: center;
    }

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