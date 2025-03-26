<template>
  <div class="home-container">
    <!-- 搜索区域 -->
    <div class="search-section" role="search" aria-label="职业搜索">
      <el-input
        v-model="searchQuery"
        :placeholder="t('occupation.searchPlaceholder')"
        class="search-input"
        @input="handleSearchInput"
        aria-label="搜索职业"
      >
        <!-- <template #append>
          <el-button type="primary" @click="handleSearch">
            {{ t('common.search') }}
          </el-button>
        </template> -->
      </el-input>

      <!-- 搜索结果下拉列表 -->
      <div v-if="showSearchResults && searchResults.length > 0" class="search-results" role="listbox">
        <ul>
          <li 
            v-for="title in searchResults" 
            :key="title"
            @click="selectOccupation(title)"
            role="option"
          >
            <div class="search-item">
              <i class="el-icon-search" aria-hidden="true"></i>
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
    <div class="card-container" role="region" aria-label="职业任务分布">
      <div class="chart-container" ref="tasksBarChartRef" aria-label="任务分布图表"></div>
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
import { ElMessage } from 'element-plus'

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
      tasksBarChart = echarts.init(tasksBarChartRef.value, null, {
        renderer: 'canvas',
        useDirtyRect: true // 提高移动设备性能
      })
      
      // 检测设备类型
      const isMobile = window.innerWidth <= 768
      const isExtraSmall = window.innerWidth <= 380
      
      tasksBarChart.setOption({
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
          name: '占比',
          nameLocation: 'end',
          nameTextStyle: {
            color: '#666',
            fontSize: isExtraSmall ? 9 : (isMobile ? 10 : 14),
            align: 'right'
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

    // 防抖处理搜索输入
    const handleSearchInput = debounce(async () => {
      // 判断搜索关键词是否包含中文字符
      const hasChinese = /[\u4e00-\u9fa5]/.test(searchQuery.value)
      
      // 对中文字符，允许单个字符搜索；对非中文，保持至少两个字符的限制
      if ((hasChinese && searchQuery.value.length < 1) || (!hasChinese && searchQuery.value.length < 2)) {
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
      
      // 判断搜索关键词是否包含中文字符
      const hasChinese = /[\u4e00-\u9fa5]/.test(searchQuery.value)
      
      // 对中文字符，允许单个字符搜索；对非中文，要求至少两个字符
      if ((!hasChinese && searchQuery.value.length < 2)) {
        ElMessage.warning(t('occupation.minSearchLength'))
        return
      }
      
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
          tasksBarChart.setOption({
            yAxis: {
              data: processedTasks.map(t => t.task)
            },
            series: [{
              data: processedTasks.map(t => t.percentage)
            }]
          })
          
          // 延迟调整大小，确保渲染完成
          setTimeout(() => {
            tasksBarChart.resize();
          }, 200);
        }
        
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
      } finally {
        loading.value = false
      }
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

    // 点击外部关闭搜索结果
    const handleClickOutside = (event) => {
      const searchSection = document.querySelector('.search-section')
      if (searchSection && !searchSection.contains(event.target)) {
        showSearchResults.value = false
      }
    }

    // 监听窗口大小变化
    const handleResize = () => {
      if (tasksBarChart) {
        // 检测是否是移动设备
        const isMobile = window.innerWidth <= 768
        const isExtraSmall = window.innerWidth <= 380
        
        // 更新图表配置以适应新尺寸
        tasksBarChart.setOption({
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
        
        // 如果当前有数据，并且是移动设备，可能需要限制项目数量并简化文本
        if (isMobile && popularTasks.value.length > 0) {
          const sortedTasks = [...popularTasks.value].sort((a, b) => b.percentage - a.percentage);
          const displayCount = isExtraSmall ? 5 : (isMobile ? 8 : sortedTasks.length)
          const displayTasks = sortedTasks.slice(0, displayCount);
          
          // 为移动设备处理任务文本
          const processedTasks = displayTasks.map(task => ({
            ...task,
            task: simplifyTaskText(task.task, isExtraSmall)
          }));
          
          tasksBarChart.setOption({
            yAxis: {
              data: processedTasks.map(t => t.task)
            },
            series: [{
              data: processedTasks.map(t => t.percentage)
            }]
          });
        }
        
        tasksBarChart.resize();
      }
    }

    onMounted(() => {
      initCharts()
      window.addEventListener('resize', handleResize)
      document.addEventListener('click', handleClickOutside)
      
      // 添加屏幕方向变化监听
      if (window.screen && window.screen.orientation) {
        window.screen.orientation.addEventListener('change', handleOrientationChange);
      } else if (window.matchMedia) {
        window.matchMedia('(orientation: portrait)').addEventListener('change', handleOrientationChange);
      }
    })

    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      document.removeEventListener('click', handleClickOutside)
      
      // 移除屏幕方向变化监听
      if (window.screen && window.screen.orientation) {
        window.screen.orientation.removeEventListener('change', handleOrientationChange);
      } else if (window.matchMedia) {
        window.matchMedia('(orientation: portrait)').removeEventListener('change', handleOrientationChange);
      }
      
      if (tasksBarChart) {
        tasksBarChart.dispose();
        tasksBarChart = null;
      }
    })

    // 处理屏幕方向变化
    const handleOrientationChange = () => {
      // 给浏览器一点时间来完成旋转
      setTimeout(() => {
        if (tasksBarChart) {
          // 检测是否是竖屏
          const isPortrait = window.innerHeight > window.innerWidth;
          const isMobile = window.innerWidth <= 768;
          const isExtraSmall = window.innerWidth <= 380;
          
          if (isMobile) {
            // 在竖屏模式下，需要更紧凑的布局
            if (isPortrait) {
              // 更新图表布局为竖屏模式
              tasksBarChart.setOption({
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
              tasksBarChart.setOption({
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
            
            // 重新计算要显示的任务项
            if (popularTasks.value.length > 0) {
              const sortedTasks = [...popularTasks.value].sort((a, b) => b.percentage - a.percentage);
              // 横屏可以显示更多项目
              const displayCount = isPortrait 
                ? (isExtraSmall ? 5 : 8) 
                : (isExtraSmall ? 8 : 12);
              const displayTasks = sortedTasks.slice(0, displayCount);
              
              // 为移动设备处理任务文本
              const processedTasks = displayTasks.map(task => ({
                ...task,
                task: simplifyTaskText(task.task, isExtraSmall && isPortrait)
              }));
              
              tasksBarChart.setOption({
                yAxis: {
                  data: processedTasks.map(t => t.task)
                },
                series: [{
                  data: processedTasks.map(t => t.percentage)
                }]
              });
            }
          }
          
          // 确保调整大小
          tasksBarChart.resize();
        }
      }, 300);
    }

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
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;

  .search-section {
    margin: 20px 0;
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
    padding: 16px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .chart-container {
      height: 380px;
      
      // 移动设备适配
      @media (max-width: 768px) {
        height: 320px;
      }
      
      @media (max-width: 480px) {
        height: 280px;
      }
      
      // 横屏状态
      @media (max-width: 768px) and (orientation: landscape) {
        height: 240px; // 横屏时高度更小，避免溢出
      }
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

// 横屏和竖屏适配
@media (orientation: landscape) and (max-width: 768px) {
  .home-container {
    .search-section {
      max-width: 70%;
    }
    
    .card-container {
      margin-top: 10px;
    }
  }
}

// 响应式样式
@media (max-width: 768px) {
  .home-container {
    padding: 12px;
    
    .search-section {
      margin: 16px 0;
      
      .search-input {
        :deep(.el-input__inner) {
          height: 36px;
          line-height: 36px;
          font-size: 14px;
        }
      }
    }
    
    .card-container {
      padding: 12px;
      margin-bottom: 16px;
    }
    
    .search-results {
      ul {
        li {
          .search-item {
            padding: 10px 12px;
            
            i {
              font-size: 14px;
            }
            
            .search-text {
              font-size: 13px;
            }
          }
        }
      }
    }
    
    .no-results {
      padding: 12px;
      font-size: 13px;
    }
  }
}

// 小屏幕手机
@media (max-width: 480px) {
  .home-container {
    padding: 8px;
    
    .search-section {
      margin: 12px 0;
    }
    
    .card-container {
      padding: 10px;
      border-radius: 6px;
    }
  }
}
</style> 