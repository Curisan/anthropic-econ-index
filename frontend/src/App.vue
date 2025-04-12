<template>
  <div class="flex flex-col min-h-screen">
    <header-component />

    <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
      <router-view></router-view>
    </main>

    <footer-component @show-feedback="feedbackDialogVisible = true" />

    <!-- 反馈表单对话框 -->
    <feedback-form-component v-model:visible="feedbackDialogVisible" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import i18n from './i18n'
import HeaderComponent from './components/HeaderComponent.vue'
import FooterComponent from './components/FooterComponent.vue'
import FeedbackFormComponent from './components/FeedbackFormComponent.vue'

export default {
  name: 'App',
  components: {
    HeaderComponent,
    FooterComponent,
    FeedbackFormComponent
  },
  setup() {
    const { t } = i18n.global
    const feedbackDialogVisible = ref(false)
    const isMobile = ref(window.innerWidth <= 768)

    // 检测设备类型
    const checkDeviceType = () => {
      isMobile.value = window.innerWidth <= 768
    }

    onMounted(() => {
      window.addEventListener('resize', checkDeviceType)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkDeviceType)
    })

    return {
      t,
      feedbackDialogVisible,
      isMobile
    }
  }
}
</script>

<style lang="scss">
/* 覆盖Element Plus样式 */
:deep(.el-button--primary) {
  @apply bg-blue-600 border-blue-600;
  
  &:hover, &:focus {
    @apply bg-blue-500 border-blue-500;
  }
}

:deep(.el-switch__core) {
  @apply bg-blue-800;
}

:deep(.el-dialog) {
  @apply bg-secondary-bg text-text-color rounded-xl;
}

:deep(.el-dialog__title) {
  @apply text-text-color;
}

:deep(.el-form-item__label) {
  @apply text-text-color;
}

:deep(.el-input__inner) {
  @apply bg-blue-900 border-blue-700 text-white;
}
</style> 