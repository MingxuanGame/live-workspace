<script setup lang="ts">
import { ref, watch, computed, onUnmounted } from 'vue'
import type { DisplayMessage, GiftMessage, AggregatedGift } from '@/types/danmaku'
import GiftCard from './GiftCard.vue'

const props = withDefaults(defineProps<{
  messages: DisplayMessage[]
  mergeWindow?: number // 礼物合并时间窗口（毫秒）
  expireTime?: number // 礼物卡片过期时间（毫秒）
}>(), {
  mergeWindow: 60000, // 1分钟内的同类礼物会合并
  expireTime: 300000  // 5分钟后过期消失
})

// 聚合礼物存储
const aggregatedGifts = ref<Map<string, AggregatedGift>>(new Map())

// 生成礼物唯一键
const getGiftKey = (uid: string, giftName: string): string => {
  return `${uid}_${giftName}`
}

// 处理新的礼物消息
const processGiftMessage = (msg: DisplayMessage) => {
  if (msg.type !== 'gift') return

  const giftData = msg.data as GiftMessage
  const key = getGiftKey(giftData.id, giftData.gift_name)
  const now = Date.now()

  const existing = aggregatedGifts.value.get(key)

  if (existing && (now - existing.lastTime) < props.mergeWindow) {
    // 在时间窗口内，合并礼物
    existing.total_num += giftData.gift_num
    existing.total_price += giftData.price * giftData.gift_num
    existing.lastTime = now
  } else {
    // 新的礼物或超出时间窗口
    aggregatedGifts.value.set(key, {
      key,
      uid: giftData.id,
      username: giftData.username,
      avatar: giftData.avatar,
      medal: giftData.medal,
      gift_name: giftData.gift_name,
      total_num: giftData.gift_num,
      total_price: giftData.price * giftData.gift_num,
      firstTime: now,
      lastTime: now
    })
  }

  // 强制触发响应式更新
  aggregatedGifts.value = new Map(aggregatedGifts.value)
}

// 清理过期礼物
const cleanupExpiredGifts = () => {
  const now = Date.now()
  let hasChanges = false

  for (const [key, gift] of aggregatedGifts.value.entries()) {
    if (now - gift.lastTime > props.expireTime) {
      aggregatedGifts.value.delete(key)
      hasChanges = true
    }
  }

  if (hasChanges) {
    aggregatedGifts.value = new Map(aggregatedGifts.value)
  }
}

// 定时清理过期礼物
const cleanupInterval = setInterval(cleanupExpiredGifts, 10000)

onUnmounted(() => {
  clearInterval(cleanupInterval)
})

// 监听消息变化
let lastProcessedLength = 0
watch(
  () => props.messages.length,
  (newLen) => {
    // 只处理新增的消息
    const newMessages = props.messages.slice(lastProcessedLength)
    for (const msg of newMessages) {
      if (msg.type === 'gift') {
        processGiftMessage(msg)
      }
    }
    lastProcessedLength = newLen
  },
  { immediate: true }
)

// 礼物列表（按最后更新时间倒序）
const giftList = computed(() => {
  return Array.from(aggregatedGifts.value.values())
    .sort((a, b) => b.lastTime - a.lastTime)
})
</script>

<template>
  <div class="gift-bar" v-if="giftList.length > 0">
    <TransitionGroup name="gift" tag="div" class="gift-list">
      <GiftCard
        v-for="gift in giftList"
        :key="gift.key"
        :gift="gift"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
.gift-bar {
  width: 100%;
  padding: 8px;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
}

.gift-bar::-webkit-scrollbar {
  display: none;
}

.gift-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

/* 过渡动画 */
.gift-enter-active {
  transition: all 0.4s ease-out;
}

.gift-leave-active {
  transition: all 0.3s ease-in;
}

.gift-enter-from {
  opacity: 0;
  transform: translateX(-20px) scale(0.9);
}

.gift-leave-to {
  opacity: 0;
  transform: translateX(20px) scale(0.9);
}

.gift-move {
  transition: transform 0.4s ease;
}
</style>
