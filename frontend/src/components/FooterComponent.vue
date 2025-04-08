<template>
  <footer class="bg-secondary-bg py-4 text-center">
    <div class="flex justify-end pr-4">
      <el-button type="primary" @click="showFeedbackForm" class="shadow-lg">
        {{ t('feedback.button') }}
      </el-button>
    </div>
  </footer>
</template>

<script>
import i18n from '../i18n'

export default {
  name: 'FooterComponent',
  setup(props, { emit }) {
    const { t } = i18n.global

    const showFeedbackForm = () => {
      emit('show-feedback')
    }

    return {
      t,
      showFeedbackForm
    }
  }
}
</script> 