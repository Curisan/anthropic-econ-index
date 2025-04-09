<template>
  <div class="w-full bg-white rounded-lg shadow p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-semibold text-gray-700">{{ t('occupationRanking') }}</h2>
      <select v-model="limit" @change="onLimitChange" class="px-3 py-1 border rounded text-gray-700 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="10">Top 10</option>
        <option value="20">Top 20</option>
        <option value="30">Top 30</option>
        <option value="50">Top 50</option>
      </select>
    </div>
    <div :style="chartStyle" ref="chartRef" aria-label="职业对话占比排名图表"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import i18n from '../i18n'

export default {
  name: 'OccupationRankChart',
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
    const limit = ref(20)  // 默认显示前20个
    let chart = null
    
    // 计算图表样式，包括动态高度
    const chartStyle = computed(() => {
      const baseHeight = 400 // 基础高度（像素）
      const itemHeight = 30  // 每个项目的高度（像素）
      const height = baseHeight + (Number(limit.value) - 10) * itemHeight
      return {
        height: `${height}px`,
        minHeight: '400px'
      }
    })
    
    // 处理 limit 变化
    const onLimitChange = () => {
      emit('limit-change', Number(limit.value))
      // 当数据量改变时，需要重新调整图表大小
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
      
      // 检测设备类型
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
          left: isExtraSmall ? '25%' : (isMobile ? '30%' : '20%'),
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
            name: t('occupation.dialoguePercentage'),
            type: 'bar',
            data: [],
            barWidth: isExtraSmall ? '45%' : (isMobile ? '50%' : '60%'),
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#1E40AF' },  // 深蓝色起始
                { offset: 1, color: '#3B82F6' }   // 亮蓝色结束
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
        .sort((a, b) => b.percentage_sum - a.percentage_sum)
        .slice(0, limit.value)

      // 准备数据
      const titles = sortedStats.map(s => i18n.global.locale.value === 'en' ? s.title : s.title_cn)
      const percentages = sortedStats.map(s => Number(s.percentage_sum.toFixed(2)))

      // 更新图表
      chart.setOption({
        yAxis: {
          data: titles
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
            left: isExtraSmall ? '25%' : (isMobile ? '30%' : '20%')
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
    watch(() => i18n.global.locale.value, updateChart)

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