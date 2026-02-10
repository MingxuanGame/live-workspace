<script setup lang="ts">
import { ref, watch, nextTick, onMounted, onUnmounted, computed } from 'vue'
import type { DisplayMessage } from '@/types/danmaku'
import MessageItem from './MessageItem.vue'

const props = withDefaults(defineProps<{
  messages: DisplayMessage[]
  autoScroll?: boolean
  maxVisibleMessages?: number
}>(), {
  autoScroll: true,
  maxVisibleMessages: 50
})

const containerRef = ref<HTMLDivElement | null>(null)

// 限制可见消息数量以优化性能
// 只显示弹幕消息（danmaku），其他类型由专门的组件处理：
// - gift: GiftBar 组件处理
// - enter/like: EntryNotice 组件处理
// - superchat/guard: TickerBar 组件处理
const visibleMessages = computed(() => {
  const filtered = props.messages.filter(msg =>
    msg.type === 'danmaku' || msg.type === 'superchat' || msg.type === 'guard'
  )
  return filtered.slice(-props.maxVisibleMessages)
})

// 自动滚动到底部
const scrollToBottom = () => {
  if (!containerRef.value) return
  nextTick(() => {
    if (containerRef.value) {
      containerRef.value.scrollTop = containerRef.value.scrollHeight
    }
  })
}



// 监听可见消息变化，自动滚动
watch(
  () => visibleMessages.value,
  () => {
    if (props.autoScroll) {
      scrollToBottom()
    }
  },
  { deep: true, immediate: true }
)

// 手动滚动到底部
const forceScrollToBottom = () => {
  scrollToBottom()
}

onMounted(() => {
  scrollToBottom()
})

onUnmounted(() => {
  // Cleanup if needed
})

defineExpose({
  scrollToBottom: forceScrollToBottom
})
</script>

<template>
  <div class="danmaku-list-wrapper">
    <div
      ref="containerRef"
      class="danmaku-list"
    >
      <TransitionGroup name="message">
        <MessageItem
          v-for="message in visibleMessages"
          :key="message.id"
          :message="message"
          class="message-item"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<style scoped>
.danmaku-list-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
  background: transparent !important;
  display: flex;
  flex-direction: column;
}

.danmaku-list {
  flex: 1 1 0;
  min-height: 0;
  background: transparent !important;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.danmaku-list::-webkit-scrollbar {
  width: 6px;
}

.danmaku-list::-webkit-scrollbar-track {
  background: transparent;
}

.danmaku-list::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.danmaku-list::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

/* 消息过渡动画 */
.message-enter-active {
  transition: all 0.3s ease-out;
}

.message-leave-active {
  transition: all 0.2s ease-in;
}

.message-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.message-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.message-move {
  transition: transform 0.3s ease;
}
</style>
