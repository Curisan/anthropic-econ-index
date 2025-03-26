<template>
  <div class="app-container">
    <header class="app-header">
      <nav class="nav-container">
        <div class="logo">
          <h1>{{ t('app.title') }}</h1>
        </div>
        <div class="language-switch">
          <el-switch
            v-model="isEnglish"
            @change="toggleLanguage"
            :active-text="t('language.english')"
            :inactive-text="t('language.chinese')"
          />
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <footer class="app-footer">
      <div class="feedback-button">
        <el-button type="primary" @click="showFeedbackForm">
          {{ t('feedback.button') }}
        </el-button>
      </div>
    </footer>

    <!-- 反馈表单对话框 -->
    <el-dialog
      :title="t('feedback.title')"
      v-model="feedbackDialogVisible"
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
        <div class="dialog-footer" :class="{'mobile-footer': isMobile}">
          <el-button @click="feedbackDialogVisible = false">
            {{ t('common.cancel') }}
          </el-button>
          <el-button type="primary" @click="submitFeedback">
            {{ t('common.submit') }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
// import { useI18n } from 'vue-i18n'
import i18n from './i18n'
import { occupationApi } from './api'
import { ElMessage } from 'element-plus'

export default {
  name: 'App',
  setup() {
    // const { t, locale } = useI18n()
    const { t, locale } = i18n.global
    const isEnglish = ref(locale.value === 'en')
    const feedbackDialogVisible = ref(false)
    const feedbackForm = reactive({
      type: 'suggestion',
      content: ''
    })
    const isMobile = ref(window.innerWidth <= 768)

    const toggleLanguage = (val) => {
      locale.value = val ? 'en' : 'zh'
    }

    const showFeedbackForm = () => {
      feedbackDialogVisible.value = true
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
          feedbackDialogVisible.value = false;
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
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkDeviceType)
    })

    return {
      t,
      isEnglish,
      feedbackDialogVisible,
      feedbackForm,
      isMobile,
      toggleLanguage,
      showFeedbackForm,
      submitFeedback
    }
  }
}
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: var(--secondary-bg);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 1rem;

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo h1 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--text-color);
  }
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: var(--secondary-bg);
  padding: 1rem;
  text-align: center;

  .feedback-button {
    position: fixed;
    right: 2rem;
    bottom: 2rem;
  }
}

// Override Element Plus styles for dark theme
:deep(.el-button--primary) {
  background-color: #2d6cdf;
  border-color: #2d6cdf;
  
  &:hover, &:focus {
    background-color: #4d85e8;
    border-color: #4d85e8;
  }
}

:deep(.el-switch__core) {
  background-color: #375299;
}

:deep(.el-dialog) {
  background-color: var(--secondary-bg);
  color: var(--text-color);
  border-radius: 12px;
}

:deep(.el-dialog__title) {
  color: var(--text-color);
}

:deep(.el-form-item__label) {
  color: var(--text-color);
}

:deep(.el-input__inner) {
  background-color: #304490;
  border-color: #455ab3;
  color: white;
}

// 反馈表单移动端适配样式
.feedback-dialog {
  :deep(.el-dialog__header) {
    padding: 15px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  :deep(.el-dialog__body) {
    padding: 20px;
    
    @media (max-width: 768px) {
      padding: 15px;
    }
  }
  
  :deep(.el-dialog__footer) {
    padding: 10px 20px 20px;
    
    @media (max-width: 768px) {
      padding: 10px 15px 15px;
    }
  }
  
  .mobile-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    
    .el-button {
      flex: 1;
      margin-left: 0;
    }
  }
  
  @media (max-width: 480px) {
    :deep(.el-form-item) {
      margin-bottom: 15px;
    }
    
    :deep(.el-form-item__label) {
      font-size: 14px;
      padding-right: 5px;
    }
    
    :deep(.el-select) {
      width: 100%;
    }
    
    :deep(.el-button) {
      padding: 8px 15px;
      font-size: 14px;
    }
  }
}

// 移动设备适配
@media (max-width: 768px) {
  .app-header {
    padding: 0.5rem 1rem;
    
    .logo h1 {
      font-size: 1.2rem;
    }
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .app-footer {
    .feedback-button {
      right: 1rem;
      bottom: 1rem;
      
      .el-button {
        padding: 8px 15px;
        font-size: 0.9rem;
      }
    }
  }
}
</style> 