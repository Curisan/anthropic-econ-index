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
      width="500px"
    >
      <el-form :model="feedbackForm" label-width="100px">
        <el-form-item :label="t('feedback.type')">
          <el-select v-model="feedbackForm.type">
            <el-option :label="t('feedback.suggestionType')" value="suggestion" />
            <el-option :label="t('feedback.problemType')" value="problem" />
            <el-option :label="t('feedback.otherType')" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('feedback.content')">
          <el-input
            type="textarea"
            v-model="feedbackForm.content"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="feedbackDialogVisible = false">
          {{ t('common.cancel') }}
        </el-button>
        <el-button type="primary" @click="submitFeedback">
          {{ t('common.submit') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
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

    return {
      t,
      isEnglish,
      feedbackDialogVisible,
      feedbackForm,
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
</style> 