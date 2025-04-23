<template>
    <div class="bg-white rounded-xl p-6 shadow-lg mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold text-gray-700">{{ t('occupation.topTasks') }}</h2>
        <select v-model="limit" @change="onLimitChange" class="px-3 py-1 border rounded text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="10">Top 10</option>
          <option value="20">Top 20</option>
          <option value="30">Top 30</option>
          <option value="50">Top 50</option>
          <option value="100">Top 100</option>
          <option value="1000">Top 1000</option>
        </select>
      </div>
      <div :style="chartStyle" ref="chartRef" aria-label="对话占比最高任务图表"></div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
  import * as echarts from 'echarts'
  import i18n from '../i18n'
  
  export default {
    name: 'TopTasksTable',
    props: {
      stats: {
        type: Array,
        default: () => []
      }
    },
    emits: ['limit-change'],
    setup(props, { emit }) {
      const { t } = i18n.global
      const chartRef = ref(null)
      const limit = ref(20)
      let chart = null
      
      // 计算图表样式，包括动态高度
      const chartStyle = computed(() => {
        const baseHeight = 400
        const itemHeight = 30
        const height = baseHeight + (Number(limit.value) - 10) * itemHeight
        return {
          height: `${height}px`,
          minHeight: '400px'
        }
      })
      
      // 处理 limit 变化
      const onLimitChange = () => {
        emit('limit-change', Number(limit.value))
        if (chart) {
          setTimeout(() => {
            chart.resize()
          }, 0)
        }
      }
      
      // 初始化图表
      const initChart = () => {
        if (!chartRef.value) return
        
        chart = echarts.init(chartRef.value, null, {
          renderer: 'canvas',
          useDirtyRect: true
        })
        
        const isMobile = window.innerWidth <= 768
        const isExtraSmall = window.innerWidth <= 380
        
        chart.setOption({
          backgroundColor: 'transparent',
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: '{b}: {c}%'
          },
          grid: {
            left: isExtraSmall ? '5%' : (isMobile ? '5%' : '5%'),
            right: '5%',
            bottom: '5%',
            top: '5%',
            containLabel: true
          },
          xAxis: {
            type: 'value',
            name: t('occupation.percentage'),
            nameLocation: 'middle',
            nameGap: 30,
            axisLabel: {
              formatter: '{value}%'
            }
          },
          yAxis: {
            type: 'category',
            data: [],
            inverse: true,
            axisLabel: {
              width: isExtraSmall ? 90 : (isMobile ? 120 : 200),
              overflow: 'truncate'
            }
          },
          series: [
            {
              name: t('occupation.percentage'),
              type: 'bar',
              data: [],
              barWidth: isExtraSmall ? '45%' : (isMobile ? '50%' : '60%'),
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#4facfe' },
                  { offset: 1, color: '#00f2fe' }
                ]),
                borderRadius: [0, 4, 4, 0]
              },
              label: {
                show: !isExtraSmall,
                position: 'right',
                formatter: '{c}%'
              }
            }
          ]
        })
      }
  
      // 更新图表数据
      const updateChart = () => {
        if (!chart || !props.stats.length) return
  
        // 按百分比排序并限制数量
        const sortedStats = [...props.stats]
          .sort((a, b) => b.percentage - a.percentage)
          .slice(0, limit.value)
  
        // 准备数据
        const tasks = sortedStats.map(s => i18n.global.locale.value === 'en' ? s.task : s.task_cn)
        const percentages = sortedStats.map(s => Number(s.percentage.toFixed(2)))
  
        // 更新图表
        chart.setOption({
          yAxis: {
            data: tasks
          },
          series: [{
            data: percentages
          }]
        })
      }
  
      // 监听窗口大小变化
      const handleResize = () => {
        if (chart) {
          const isMobile = window.innerWidth <= 768
          const isExtraSmall = window.innerWidth <= 380
          
          chart.setOption({
            grid: {
              left: isExtraSmall ? '20%' : (isMobile ? '25%' : '15%')
            },
            yAxis: {
              axisLabel: {
                width: isExtraSmall ? 90 : (isMobile ? 120 : 200)
              }
            },
            series: [{
              barWidth: isExtraSmall ? '45%' : (isMobile ? '50%' : '60%'),
              label: {
                show: !isExtraSmall
              }
            }]
          })
          
          chart.resize()
        }
      }
  
      // 监听数据变化
      watch(() => props.stats, updateChart, { deep: true })
      
      // 监听显示数量变化
      watch(limit, updateChart)
      
      // 监听语言变化
      watch(() => i18n.global.locale.value, () => {
        if (chart) {
          chart.setOption({
            xAxis: {
              name: t('occupation.percentage')
            },
            series: [{
              name: t('occupation.percentage')
            }]
          })
        }
        updateChart()
      })
  
      onMounted(() => {
        initChart()
        window.addEventListener('resize', handleResize)
        if (props.stats.length > 0) {
          updateChart()
        }
      })
  
      onUnmounted(() => {
        window.removeEventListener('resize', handleResize)
        if (chart) {
          chart.dispose()
          chart = null
        }
      })
  
      return {
        chartRef,
        limit,
        t,
        onLimitChange,
        chartStyle
      }
    }
  }
  </script>
  
  <style scoped>
  select {
    appearance: auto;
    outline: none;
  }
  
  select:focus {
    border-color: #3B82F6;
    ring: 2px;
    ring-color: #93C5FD;
  }
  
  option {
    color: #374151;
    background-color: white;
  }
  </style> 