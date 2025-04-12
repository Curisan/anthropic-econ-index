<template>
  <el-dialog
    :title="t('feedback.title')"
    v-model="dialogVisible"
    :width="isMobile ? '90%' : '500px'"
    :top="isMobile ? '20vh' : '15vh'"
    class="feedback-dialog"
  >
    <el-form :model="feedbackForm" :label-width="isMobile ? '60px' : '100px'">
      <el-form-item :label="t('feedback.type')">
        <el-select v-model="feedbackForm.type" style="width: 100%">
          <el-option :label="t('feedback.suggestionType')" value="suggestion" />
          <el-option :label="t('feedback.problemType')" value="problem" />
          <el-option :label="t('feedback.otherType')" value="other" />
        </el-select>
      </el-form-item>
      <el-form-item :label="t('feedback.content')">
        <el-input
          type="textarea"
          v-model="feedbackForm.content"
          :rows="isMobile ? 3 : 4"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer" :class="{'flex justify-end gap-2 flex-col sm:flex-row': isMobile}">
        <el-button @click="closeDialog">
          {{ t('common.cancel') }}
        </el-button>
        <el-button type="primary" @click="submitFeedback">
          {{ t('common.submit') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import i18n from '../i18n'
import { occupationApi } from '../api'
import { ElMessage } from 'element-plus'

export default {
  name: 'FeedbackFormComponent',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:visible'],
  setup(props, { emit }) {
    const { t } = i18n.global
    const dialogVisible = ref(props.visible)
    const feedbackForm = reactive({
      type: 'suggestion',
      content: ''
    })
    const isMobile = ref(window.innerWidth <= 768)

    // 监听 props.visible 变化
    const updateVisible = () => {
      dialogVisible.value = props.visible
    }

    // 监听 dialogVisible 变化
    const updateVisibleProp = () => {
      emit('update:visible', dialogVisible.value)
    }

    // 关闭对话框
    const closeDialog = () => {
      dialogVisible.value = false
    }

    const submitFeedback = async () => {
      if (!feedbackForm.type || !feedbackForm.content) {
        ElMessage.warning(t('feedback.validation'));
        return;
      }
      
      try {
        // 将表单类型字段映射为后端接受的格式
        const typeMapping = {
          suggestion: '建议',
          problem: '问题',
          other: '其他'
        };
        
        const feedbackData = {
          feedback_type: typeMapping[feedbackForm.type],
          feedback_content: feedbackForm.content
        };
        
        const response = await occupationApi.submitFeedback(feedbackData);
        
        if (response.data.success) {
          ElMessage.success(t('feedback.success'));
          // 重置表单并关闭对话框
          feedbackForm.content = '';
          dialogVisible.value = false;
        } else {
          ElMessage.error(t('feedback.error') + ': ' + (response.data.error || t('feedback.unknownError')));
        }
      } catch (error) {
        console.error('提交反馈失败:', error);
        ElMessage.error(t('feedback.error'));
      }
    }

    // 检测设备类型
    const checkDeviceType = () => {
      isMobile.value = window.innerWidth <= 768
    }

    onMounted(() => {
      window.addEventListener('resize', checkDeviceType)
      // 监听 props 变化
      updateVisible()
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkDeviceType)
    })

    // 监听 props 变化
    const watchEffect = () => {
      updateVisible()
    }
    
    // 监听组件内部 dialogVisible 变化
    const watchDialogVisible = () => {
      updateVisibleProp()
    }

    // 设置 watch
    watch(() => props.visible, watchEffect)
    watch(() => dialogVisible.value, watchDialogVisible)

    return {
      t,
      dialogVisible,
      feedbackForm,
      isMobile,
      closeDialog,
      submitFeedback
    }
  }
}
</script>

<style lang="scss" scoped>
/* 反馈表单样式 */
:deep(.el-dialog__header) {
  @apply p-4 border-b border-white border-opacity-10;
  
  @media (max-width: 768px) {
    @apply py-3 px-4;
  }
}

:deep(.el-dialog__body) {
  @apply p-5;
  
  @media (max-width: 768px) {
    @apply p-4;
  }
}

:deep(.el-dialog__footer) {
  @apply py-2 px-5 pb-5;
  
  @media (max-width: 768px) {
    @apply py-2 px-4 pb-4;
  }
}

@media (max-width: 480px) {
  :deep(.el-form-item) {
    @apply mb-4;
  }
  
  :deep(.el-form-item__label) {
    @apply text-sm pr-1;
  }
  
  :deep(.el-select) {
    @apply w-full;
  }
  
  :deep(.el-button) {
    @apply py-2 px-4 text-sm;
  }
}
</style> 