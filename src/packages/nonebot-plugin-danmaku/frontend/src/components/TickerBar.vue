<script setup lang="ts">
import { computed } from 'vue'
import type { DisplayMessage, SuperChatMessage, GuardMessage } from '@/types/danmaku'
import UserAvatar from './UserAvatar.vue'

const props = defineProps<{
  messages: DisplayMessage[]
}>()

// 筛选出需要在 ticker 中显示的消息（SC 和上舰）
const tickerItems = computed(() => {
  const now = Date.now()
  return props.messages
    .filter(msg => {
      if (msg.type === 'superchat') {
        const data = msg.data as SuperChatMessage
        // SC 显示到结束时间
        return data.end_time > now
      }
      if (msg.type === 'guard') {
        // 上舰消息显示 5 分钟
        return now - msg.timestamp < 5 * 60 * 1000
      }
      return false
    })
    .slice(-10) // 最多显示 10 个
})

// 获取 ticker 项的背景色
const getTickerColor = (msg: DisplayMessage): string => {
  if (msg.type === 'superchat') {
    const price = (msg.data as SuperChatMessage).price
    if (price >= 2000) return '#e62117'
    if (price >= 1000) return '#e62117'
    if (price >= 500) return '#e91e63'
    if (price >= 100) return '#f57c00'
    if (price >= 50) return '#ffb300'
    if (price >= 30) return '#00bfa5'
    return '#1e88e5'
  }
  if (msg.type === 'guard') {
    const level = (msg.data as GuardMessage).guard_level
    if (level === 1) return '#e73b4d'
    if (level === 2) return '#a068f1'
    return '#0f9d58'
  }
  return '#1e88e5'
}

// 获取 ticker 项的文字
const getTickerText = (msg: DisplayMessage): string => {
  if (msg.type === 'superchat') {
    const price = (msg.data as SuperChatMessage).price
    return `CN¥${price >= 1 ? price.toFixed(0) : price.toFixed(2)}`
  }
  if (msg.type === 'guard') {
    const level = (msg.data as GuardMessage).guard_level
    if (level === 1) return '总督'
    if (level === 2) return '提督'
    return '舰长'
  }
  return ''
}

// 获取头像
const getAvatar = (msg: DisplayMessage): string => {
  if (msg.type === 'superchat') return (msg.data as SuperChatMessage).avatar || ''
  if (msg.type === 'guard') return (msg.data as GuardMessage).avatar
  return ''
}

const emit = defineEmits<{
  (e: 'click', msg: DisplayMessage): void
}>()
</script>

<template>
  <div v-if="tickerItems.length > 0" class="ticker">
    <div
      v-for="item in tickerItems"
      :key="item.id"
      class="ticker-item"
      :style="{ backgroundColor: getTickerColor(item) }"
      @click="emit('click', item)"
    >
      <UserAvatar
        :src="getAvatar(item)"
        :size="32"
        class="ticker-avatar"
      />
      <span class="ticker-text">{{ getTickerText(item) }}</span>
    </div>
  </div>
</template>

<style scoped>
.ticker {
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  padding: 8px 12px;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  flex-shrink: 0;
}

.ticker::-webkit-scrollbar {
  display: none;
}

.ticker-item {
  display: flex;
  align-items: center;
  padding: 4px 12px 4px 4px;
  border-radius: 999px;
  cursor: pointer;
  transition: transform 0.2s;
  flex-shrink: 0;
  text-shadow: none;
}

.ticker-item:hover {
  transform: scale(1.05);
}

.ticker-avatar {
  margin-right: 8px;
}

.ticker-text {
  font-size: 14px;
  font-weight: bold;
  color: #fff;
}
</style>
