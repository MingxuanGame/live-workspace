<script setup lang="ts">
import { computed } from 'vue'
import type { AggregatedGift } from '@/types/danmaku'
import UserAvatar from './UserAvatar.vue'

const props = defineProps<{
  gift: AggregatedGift
}>()

// 价格等级决定卡片颜色
const priceLevel = computed(() => {
  const price = props.gift.total_price
  if (price >= 1000) return 5
  if (price >= 100) return 4
  if (price >= 50) return 3
  if (price >= 10) return 2
  return 1
})

// 卡片背景色
const cardStyle = computed(() => {
  const level = priceLevel.value
  const colors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', // level 1
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', // level 2
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', // level 3
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', // level 4
    'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)', // level 5
  ]
  return {
    background: colors[level - 1]
  }
})
</script>

<template>
  <div class="gift-card" :class="`gift-card--level-${priceLevel}`" :style="cardStyle">
    <UserAvatar :src="gift.avatar" :size="36" class="gift-avatar" />
    <div class="gift-info">
      <div class="gift-header">
        <span class="gift-username">{{ gift.username }}</span>
      </div>
      <div class="gift-content">
        <span class="gift-name">{{ gift.gift_name }}</span>
        <span class="gift-separator">×</span>
        <span class="gift-num">{{ gift.total_num }}</span>
      </div>
    </div>
    <div class="gift-price" v-if="gift.total_price > 0">
      ¥{{ gift.total_price.toFixed(1) }}
    </div>
  </div>
</template>

<style scoped>
.gift-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  color: #fff;
  width: 100%;
  flex-shrink: 0;
  animation: gift-card-in 0.4s ease-out;
}

@keyframes gift-card-in {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.gift-avatar {
  flex-shrink: 0;
}

.gift-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.gift-header {
  display: flex;
  align-items: center;
  gap: 6px;
}

.gift-username {
  font-size: 13px;
  font-weight: 600;
  opacity: 0.9;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gift-content {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.gift-name {
  font-size: 16px;
  font-weight: 700;
}

.gift-separator {
  font-size: 14px;
  opacity: 0.8;
}

.gift-num {
  font-size: 20px;
  font-weight: 800;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.gift-price {
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.25);
  padding: 4px 8px;
  border-radius: 20px;
  flex-shrink: 0;
}

/* 高价值礼物加点特效 */
.gift-card--level-4,
.gift-card--level-5 {
  animation: gift-card-in 0.4s ease-out, gift-glow 2s ease-in-out infinite;
}

@keyframes gift-glow {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  50% {
    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.4), 0 0 30px rgba(255, 200, 100, 0.3);
  }
}
</style>
