<template>
  <div class="home-container">
    <!-- 搜索区域 -->
    <div class="search-section">
      <el-input
        v-model="searchQuery"
        :placeholder="t('occupation.searchPlaceholder')"
        class="search-input"
      >
        <template #append>
          <el-button type="primary" @click="handleSearch">
            {{ t('common.search') }}
          </el-button>
        </template>
      </el-input>
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

export default {
  name: 'Home',
  setup() {
    // const { t } = useI18n()
    const { t } = i18n.global
    
    const searchQuery = ref('')
    const loading = ref(false)
    const popularTasks = ref([])
    
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
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: ['2023Q1', '2023Q2', '2023Q3', '2023Q4', '2024Q1', '2024Q2'],
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
          name: 'GDP增长率 (%)',
          nameTextStyle: {
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
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.7)'
          }
        },
        series: [
          {
            name: 'GDP增长率',
            type: 'bar',
            barWidth: '40%',
            data: [4.4, 6.3, 4.9, 5.2, 5.3, 5.5],
            itemStyle: {
              color: '#39a0ff'
            }
          },
          {
            name: 'GDP同比增长',
            type: 'line',
            data: [0.7, 1.2, -0.3, 0.4, 0.8, -0.5],
            symbolSize: 6,
            lineStyle: {
              color: '#ffde33',
              width: 2
            },
            itemStyle: {
              color: '#ffde33'
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
          trigger: 'item'
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
            color: '#fff'
          },
          data: [
            { value: 35, name: '任务A' },
            { value: 25, name: '任务B' },
            { value: 20, name: '任务C' },
            { value: 15, name: '任务D' },
            { value: 5, name: '任务E' }
          ]
        }]
      })
    }

    // 处理搜索
    const handleSearch = async () => {
      if (!searchQuery.value) return
      
      loading.value = true
      try {
        // TODO: 实现搜索逻辑
        await new Promise(resolve => setTimeout(resolve, 1000))
        // 更新图表数据
      } catch (error) {
        console.error('搜索失败:', error)
      } finally {
        loading.value = false
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
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      gdpChart?.dispose()
      aiUsageChart?.dispose()
      taskDistributionChart?.dispose()
    })

    return {
      t,
      searchQuery,
      loading,
      popularTasks,
      gdpChartRef,
      aiUsageChartRef,
      taskDistributionChartRef,
      handleSearch
    }
  }
}
</script>

<style lang="scss" scoped>
.home-container {
  .search-section {
    margin-bottom: 2rem;
    
    .search-input {
      max-width: 600px;
      margin: 0 auto;
    }
  }

  .chart-container {
    height: 380px;
  }

  .data-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;

    .chart-card {
      background-color: var(--secondary-bg);
      border: none;
      border-radius: 12px;
      overflow: hidden;

      :deep(.el-card__header) {
        background-color: var(--card-bg);
        border-bottom: none;
        padding: 15px 20px;
      }

      .card-header {
        font-size: 18px;
        font-weight: bold;
        color: var(--text-color);
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
        background-color: transparent;
        color: var(--text-color);

        th, td {
          background-color: transparent;
          border-bottom-color: rgba(255, 255, 255, 0.1);
        }

        th {
          color: rgba(255, 255, 255, 0.7);
        }
      }
    }
  }
}
</style> 