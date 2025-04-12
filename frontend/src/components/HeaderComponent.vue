<template>
  <header class="bg-secondary-bg shadow-md py-4">
    <nav class="max-w-7xl mx-auto px-4 flex justify-between items-center">
      <div class="logo">
        <h1 class="m-0 text-xl md:text-2xl text-text-color">{{ t('app.title') }}</h1>
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
</template>

<script>
import { ref } from 'vue'
import i18n from '../i18n'

export default {
  name: 'HeaderComponent',
  setup() {
    const { t, locale } = i18n.global
    const isEnglish = ref(locale.value === 'en')

    const toggleLanguage = (val) => {
      locale.value = val ? 'en' : 'zh'
    }

    return {
      t,
      isEnglish,
      toggleLanguage
    }
  }
}
</script> 