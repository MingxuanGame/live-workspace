<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useDanmakuWebSocket } from '@/composables/useDanmakuWebSocket'
import DanmakuList from '@/components/DanmakuList.vue'
import TickerBar from '@/components/TickerBar.vue'
import GiftBar from '@/components/GiftBar.vue'
import EntryNotice from '@/components/EntryNotice.vue'
import CommandBar from '@/components/CommandBar.vue'

const route = useRoute()

// 从 URL query 获取房间号
const roomId = computed(() => {
  return (route.query.room as string) || ''
})

const { messages, isConnected, error, connect, disconnect } = useDanmakuWebSocket({
  maxMessages: 200
})

const danmakuListRef = ref<InstanceType<typeof DanmakuList> | null>(null)

// 连接状态文字
const connectionStatus = computed(() => {
  if (error.value) return error.value
  if (isConnected.value) return '已连接'
  return '连接中...'
})

onMounted(() => {
  if (roomId.value) {
    connect(roomId.value)
  }
})

onUnmounted(() => {
  disconnect()
})
</script>

<template>
  <div class="danmaku-view room">
    <!-- 连接状态指示器（可选显示） -->
    <div v-if="!roomId" class="no-room">
      <p>请在 URL 中指定房间号</p>
      <p class="hint">例如：?room=123456</p>
    </div>

    <template v-else>
      <!-- 悬浮层：礼物和SC -->
      <div class="floating-layer">
        <!-- 付费消息固定栏 (Ticker) -->
        <TickerBar :messages="messages" class="ticker-container" />

        <!-- 礼物卡片栏 -->
        <GiftBar :messages="messages" class="gift-container" />
      </div>

      <!-- 主区域 (80%) -->
      <div class="main-area">
        <!-- 弹幕列表 -->
        <DanmakuList
          ref="danmakuListRef"
          :messages="messages"
          class="messages"
        />
      </div>

      <!-- 进场点赞区域 (10%) -->
      <div class="entry-area">
        <EntryNotice :messages="messages" :max-notices="4" />
      </div>

      <!-- 命令区域 (10%) -->
      <div class="command-area">
        <CommandBar />
      </div>

      <!-- 连接状态（调试用，可通过CSS隐藏） -->
      <div
        class="connection-status"
        :class="{ connected: isConnected, error: !!error }"
      >
        {{ connectionStatus }}
      </div>
    </template>
  </div>
</template>

<style scoped>
.danmaku-view {
  width: 100%;
  height: 100vh;
  background: transparent !important;
  background-color: rgba(0, 0, 0, 0) !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.no-room {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-room .hint {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

/* 主区域：80% 高度 */
.main-area {
  flex: 0 0 80%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 悬浮层：绝对定位在顶部 */
.floating-layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  pointer-events: none;
}

.floating-layer > * {
  pointer-events: auto;
}

.ticker-container {
  flex-shrink: 0;
}

.gift-container {
  flex-shrink: 0;
  max-height: 250px;
  overflow-y: auto;
}

.messages {
  flex: 1 1 0;
  min-height: 0;
  overflow: hidden;
}

/* 进场点赞区域：10% 高度 */
.entry-area {
  flex: 0 0 10%;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  overflow: hidden;
}

/* 命令区域：自适应高度 */
.command-area {
  flex-shrink: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
}

.connection-status {
  position: fixed;
  top: 8px;
  right: 8px;
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.5);
  color: #999;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.connection-status.connected {
  color: #4caf50;
}

.connection-status.error {
  color: #f44336;
  opacity: 1;
}

/* 鼠标悬停时显示连接状态 */
.danmaku-view:hover .connection-status {
  opacity: 1;
}
</style>
