import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    app: {
      title: 'Anthropic Economic Index'
    },
    language: {
      english: 'English',
      chinese: 'Chinese'
    },
    common: {
      search: 'Search',
      cancel: 'Cancel',
      submit: 'Submit',
      loading: 'Loading...'
    },
    feedback: {
      button: 'Feedback',
      title: 'Submit Feedback',
      type: 'Type',
      content: 'Content'
    },
    occupation: {
      searchPlaceholder: 'Enter occupation name',
      aiUsageRate: 'AI Usage Rate',
      taskDistribution: 'Task Distribution',
      popularTasks: 'Popular AI Tasks',
      task: 'Task',
      percentage: 'Percentage'
    }
  },
  zh: {
    app: {
      title: 'Anthropic 经济指数'
    },
    language: {
      english: '英文',
      chinese: '中文'
    },
    common: {
      search: '搜索',
      cancel: '取消',
      submit: '提交',
      loading: '加载中...'
    },
    feedback: {
      button: '反馈',
      title: '提交反馈',
      type: '类型',
      content: '内容'
    },
    occupation: {
      searchPlaceholder: '请输入职业名称',
      aiUsageRate: 'AI 使用率',
      taskDistribution: '任务分布',
      popularTasks: '热门 AI 任务',
      task: '任务',
      percentage: '占比'
    }
  }
}

const i18n = createI18n({
  legacy: false,
  locale: 'zh',
  fallbackLocale: 'en',
  messages
})

export default i18n 