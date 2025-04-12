<template>
  <div class="relative mb-6 max-w-xl search-section" role="search" aria-label="职业搜索">
    <el-input
      v-model="searchQuery"
      :placeholder="t('occupation.searchPlaceholder')"
      class="w-full"
      @input="handleSearchInput"
      aria-label="搜索职业"
    />

    <!-- 搜索结果下拉列表 -->
    <div v-if="showSearchResults && searchResults.length > 0" 
         class="absolute w-full mt-2 bg-white rounded-md shadow-lg z-50 max-h-80 overflow-y-auto" 
         role="listbox">
      <ul class="py-1">
        <li 
          v-for="title in searchResults" 
          :key="title"
          @click="selectOccupation(title)"
          class="px-4 py-3 hover:bg-blue-50 cursor-pointer"
          role="option"
        >
          <div class="flex items-center">
            <i class="el-icon-search mr-2 text-gray-400" aria-hidden="true"></i>
            <span class="text-gray-700">{{ title }}</span>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- 无搜索结果提示 -->
    <div v-if="showSearchResults && searchResults.length === 0 && searchQuery" 
         class="absolute w-full mt-2 bg-white rounded-md shadow-lg z-50 p-4 text-center text-gray-500">
      {{ t('occupation.noResults') }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import i18n from '../i18n'
import { occupationApi } from '../api'
import debounce from 'lodash/debounce'
import { ElMessage } from 'element-plus'

export default {
  name: 'SearchComponent',
  emits: ['select-occupation'],
  setup(props, { emit }) {
    const { t } = i18n.global
    
    const searchQuery = ref('')
    const searchResults = ref([])
    const showSearchResults = ref(false)

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
    
    // 选择职业
    const selectOccupation = (title) => {
      searchQuery.value = title
      showSearchResults.value = false
      emit('select-occupation', title)
    }

    // 点击外部关闭搜索结果
    const handleClickOutside = (event) => {
      const searchSection = document.querySelector('.search-section')
      if (searchSection && !searchSection.contains(event.target)) {
        showSearchResults.value = false
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      t,
      searchQuery,
      searchResults,
      showSearchResults,
      handleSearchInput,
      selectOccupation
    }
  }
}
</script> 