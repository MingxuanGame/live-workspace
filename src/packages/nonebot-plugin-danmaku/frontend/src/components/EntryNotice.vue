<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { DisplayMessage, EnterLeaveMessage, LikeMessage } from '@/types/danmaku'
import UserAvatar from './UserAvatar.vue'
import UserMedal from './UserMedal.vue'

const props = withDefaults(defineProps<{
  messages: DisplayMessage[]
  maxNotices?: number
}>(), {
  maxNotices: 10
})

// 过滤只显示进场和点赞消息
const noticeMessages = computed(() => {
  return props.messages
    .filter(msg => msg.type === 'enter' || msg.type === 'like')
    .slice(-props.maxNotices)
})

// 获取消息数据
const getMessageData = (msg: DisplayMessage) => {
  return msg.data as EnterLeaveMessage | LikeMessage
}

// 获取动作文字
const getActionText = (type: string) => {
  return type === 'enter' ? '进入直播间' : '点赞了'
}
</script>

<template>
  <div class="entry-notice-container">
    <TransitionGroup name="notice">
      <div
        v-for="msg in noticeMessages"
        :key="msg.id"
        class="notice-item"
        :class="`notice-item--${msg.type}`"
      >
        <UserAvatar
          v-if="getMessageData(msg).avatar"
          :src="getMessageData(msg).avatar!"
          :size="24"
          class="notice-avatar"
        />
        <UserMedal
          v-if="getMessageData(msg).medal"
          :medal="getMessageData(msg).medal!"
          class="notice-medal"
        />
        <span class="notice-username">{{ getMessageData(msg).username }}</span>
        <span class="notice-action">{{ getActionText(msg.type) }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.entry-notice-container {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 4px;
  padding: 8px;
  scrollbar-width: none;
}

.entry-notice-container::-webkit-scrollbar {
  display: none;
}

.notice-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 24px;
  font-size: 15px;
  line-height: 1.5;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
  max-width: fit-content;
  min-height: 36px;
}

.notice-item--enter {
  border-left: 3px solid #4fc3f7;
}

.notice-item--like {
  border-left: 3px solid #ff6b9d;
}

.notice-avatar {
  flex-shrink: 0;
}

.notice-medal {
  flex-shrink: 0;
  transform: scale(0.9);
}

.notice-username {
  color: #81d4fa;
  font-weight: 600;
  font-size: 15px;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notice-item--like .notice-username {
  color: #ff8a80;
}

.notice-action {
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  font-weight: 500;
}

/* 过渡动画 */
.notice-enter-active {
  transition: all 0.3s ease-out;
}

.notice-leave-active {
  transition: all 0.2s ease-in;
}

.notice-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.notice-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.notice-move {
  transition: transform 0.3s ease;
}
</style>
