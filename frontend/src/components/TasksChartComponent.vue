<template>
  <div class="bg-secondary-bg rounded-xl p-6 shadow-lg mb-6" role="region" aria-label="职业任务分布">
    <div class="h-96 md:h-[450px]" ref="chartRef" aria-label="任务分布图表"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import i18n from '../i18n'

export default {
  name: 'TasksChartComponent',
  props: {
    tasks: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const { t } = i18n.global
    const chartRef = ref(null)
    let chart = null
    
    // 初始化图表
    const initChart = () => {
      if (!chartRef.value) return
      
      chart = echarts.init(chartRef.value, null, {
        renderer: 'canvas',
        useDirtyRect: true // 提高移动设备性能
      })
      
      // 检测设备类型
      const isMobile = window.innerWidth <= 768
      const isExtraSmall = window.innerWidth <= 380
      
      chart.setOption({
        backgroundColor: 'transparent',
        legend: {
          show: false
        },
        grid: {
          left: isExtraSmall ? '15%' : (isMobile ? '15%' : '3%'),
          right: isExtraSmall ? '8%' : (isMobile ? '15%' : '10%'),
          bottom: isExtraSmall ? '15%' : '5%',
          top: isExtraSmall ? '10%' : '5%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}%',
          confine: true, // 确保提示框在屏幕内
          position: function(point, params, dom, rect, size) {
            // 自适应定位，确保在小屏幕上完全可见
            return ['50%', '50%'];
          }
        },
        xAxis: {
          type: 'value',
          name: t('occupation.percentage'),
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#666',
            fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
            align: 'right',
            verticalAlign: 'bottom',
            lineHeight: -5,
            padding: [10, 0, 0, 0] // 添加padding来调整位置, 0, 0, 0, 10 表示左padding为0，右padding为0，上padding为0，下padding为10
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
            formatter: '{value}%',
            fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 12),
            margin: isExtraSmall ? 6 : (isMobile ? 8 : 10)
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
            fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
            width: isExtraSmall ? 90 : (isMobile ? 120 : 350),
            overflow: 'truncate',
            formatter: function(value) {
              // 超小屏设备上更短的文本
              if (isExtraSmall && value.length > 10) {
                return value.substring(0, 10) + '...';
              }
              // 移动设备上截断长文本
              else if (isMobile && value.length > 15) {
                return value.substring(0, 15) + '...';
              }
              return value;
            }
          }
        },
        series: [
          {
            name: '任务占比',
            type: 'bar',
            barWidth: isExtraSmall ? '45%' : (isMobile ? '50%' : '60%'),
            data: [],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#4facfe' },
                { offset: 1, color: '#00f2fe' }
              ]),
              borderRadius: [0, 4, 4, 0]
            },
            label: {
              show: !isExtraSmall, // 超小屏不显示标签
              position: 'right',
              formatter: '{c}%',
              color: '#666',
              fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
              distance: isExtraSmall ? 4 : (isMobile ? 5 : 10)
            }
          }
        ]
      });
    }

    // 更新图表数据
    const updateChart = () => {
      if (!chart || !props.tasks.length) return

      // 按百分比降序排序
      const sortedTasks = [...props.tasks].sort((a, b) => b.percentage - a.percentage)
      
      // 检测是否是移动设备
      const isMobile = window.innerWidth <= 768
      const isExtraSmall = window.innerWidth <= 380
      
      // 在移动设备上限制显示的项目数
      const displayCount = isExtraSmall ? 5 : (isMobile ? 8 : sortedTasks.length)
      const displayTasks = sortedTasks.slice(0, displayCount)
      
      // 为移动设备处理任务文本
      const processedTasks = displayTasks.map(task => {
        if (isMobile) {
          // 移动设备上简化任务文本
          return {
            ...task,
            task: simplifyTaskText(task.task, isExtraSmall)
          };
        }
        return task;
      });
      
      // 更新图表数据
      chart.setOption({
        yAxis: {
          data: processedTasks.map(t => t.task)
        },
        series: [{
          data: processedTasks.map(t => t.percentage)
        }]
      })
      
      // 延迟调整大小，确保渲染完成
      setTimeout(() => {
        chart.resize();
      }, 200);
    }

    // 简化任务文本，移除重复内容和冗余词汇
    const simplifyTaskText = (text, isExtraSmall = false) => {
      // 如果文本超过一定长度，尝试简化
      const maxLength = isExtraSmall ? 15 : 25
      
      if (text.length > maxLength) {
        // 移除常见的冗余前缀
        text = text.replace(/^(负责|进行|执行|开展|实施|提供|编写|制定|设计|管理|协助|参与|组织)\s*/i, '');
        
        // 移除常见的连接词和语气词
        text = text.replace(/\s*(以及|并且|而且|但是|然后|因此|所以|可能|应该|必须|需要)\s*/g, ' ');
        
        // 如果还是很长，截断并添加省略号
        if (text.length > maxLength) {
          // 尝试在适当的断句处截断
          const punctuation = text.indexOf('，');
          if (punctuation > maxLength * 0.4 && punctuation < maxLength) {
            return text.substring(0, punctuation) + '...';
          }
          return text.substring(0, maxLength) + '...';
        }
      }
      return text;
    }

    // 监听窗口大小变化
    const handleResize = () => {
      if (chart) {
        // 检测是否是移动设备
        const isMobile = window.innerWidth <= 768
        const isExtraSmall = window.innerWidth <= 380
        
        // 更新图表配置以适应新尺寸
        chart.setOption({
          grid: {
            left: isExtraSmall ? '15%' : (isMobile ? '15%' : '3%'),
            right: isExtraSmall ? '8%' : (isMobile ? '15%' : '10%'),
            bottom: isExtraSmall ? '15%' : '5%',
            top: isExtraSmall ? '10%' : '5%'
          },
          xAxis: {
            nameTextStyle: {
              fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14)
            },
            axisLabel: {
              fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 12),
              margin: isExtraSmall ? 6 : (isMobile ? 8 : 10)
            }
          },
          yAxis: {
            axisLabel: {
              fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
              width: isExtraSmall ? 90 : (isMobile ? 120 : 350),
              formatter: function(value) {
                if (isExtraSmall && value.length > 10) {
                  return value.substring(0, 10) + '...';
                }
                else if (isMobile && value.length > 15) {
                  return value.substring(0, 15) + '...';
                }
                return value;
              }
            }
          },
          series: [{
            barWidth: isExtraSmall ? '45%' : (isMobile ? '50%' : '60%'),
            label: {
              show: !isExtraSmall,
              fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
              distance: isExtraSmall ? 4 : (isMobile ? 5 : 10)
            }
          }]
        });
        
        // 如果当前有数据，重新更新图表
        if (props.tasks.length > 0) {
          updateChart();
        }
        
        chart.resize();
      }
    }

    // 处理屏幕方向变化
    const handleOrientationChange = () => {
      // 给浏览器一点时间来完成旋转
      setTimeout(() => {
        if (chart) {
          // 检测是否是竖屏
          const isPortrait = window.innerHeight > window.innerWidth;
          const isMobile = window.innerWidth <= 768;
          const isExtraSmall = window.innerWidth <= 380;
          
          if (isMobile) {
            // 在竖屏模式下，需要更紧凑的布局
            if (isPortrait) {
              // 更新图表布局为竖屏模式
              chart.setOption({
                grid: {
                  left: isExtraSmall ? '15%' : '15%',
                  right: isExtraSmall ? '8%' : '10%',
                  bottom: isExtraSmall ? '15%' : '10%',
                  top: isExtraSmall ? '10%' : '5%'
                },
                yAxis: {
                  axisLabel: {
                    width: isExtraSmall ? 90 : 120
                  }
                }
              });
            } else {
              // 横屏模式可以显示更多信息
              chart.setOption({
                grid: {
                  left: '10%',
                  right: '10%',
                  bottom: '5%',
                  top: '5%'
                },
                yAxis: {
                  axisLabel: {
                    width: 200
                  }
                }
              });
            }
            
            // 如果有数据，重新更新图表
            if (props.tasks.length > 0) {
              updateChart();
            }
          }
          
          // 确保调整大小
          chart.resize();
        }
      }, 300);
    }

    // 监听 props.tasks 变化
    watch(() => props.tasks, (newTasks) => {
      if (newTasks.length > 0) {
        updateChart()
      }
    }, { deep: true })

    // 监听语言变化
    watch(() => i18n.global.locale.value, () => {
      if (chart) {
        chart.setOption({
          xAxis: {
            name: t('occupation.percentage')
          }
        });
      }
    })

    onMounted(() => {
      initChart()
      window.addEventListener('resize', handleResize)
      
      // 添加屏幕方向变化监听
      if (window.screen && window.screen.orientation) {
        window.screen.orientation.addEventListener('change', handleOrientationChange);
      } else if (window.matchMedia) {
        window.matchMedia('(orientation: portrait)').addEventListener('change', handleOrientationChange);
      }
      
      // 初始更新
      if (props.tasks.length > 0) {
        updateChart()
      }
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      
      // 移除屏幕方向变化监听
      if (window.screen && window.screen.orientation) {
        window.screen.orientation.removeEventListener('change', handleOrientationChange);
      } else if (window.matchMedia) {
        window.matchMedia('(orientation: portrait)').removeEventListener('change', handleOrientationChange);
      }
      
      if (chart) {
        chart.dispose();
        chart = null;
      }
    })

    return {
      chartRef
    }
  }
}
</script> 