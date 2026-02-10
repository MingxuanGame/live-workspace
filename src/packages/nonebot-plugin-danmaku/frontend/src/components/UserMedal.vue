<script setup lang="ts">
import type { Medal } from '@/types/danmaku'

defineProps<{
  medal: Medal
}>()

// 根据舰长等级获取边框颜色
const getGuardColor = (guardLevel: number): string => {
  switch (guardLevel) {
    case 1: return '#e73b4d' // 总督
    case 2: return '#a068f1' // 提督
    case 3: return '#6eb9ff' // 舰长
    default: return '#666'
  }
}

// 根据粉丝牌等级获取背景颜色
const getLevelColor = (level: number): string => {
  if (level <= 4) return '#61c05a'
  if (level <= 8) return '#5896de'
  if (level <= 12) return '#a068f1'
  if (level <= 16) return '#ff6b9e'
  if (level <= 20) return '#ff8c00'
  if (level <= 24) return '#e73b4d'
  return '#c0a550'
}
</script>

<template>
  <span
    class="medal"
    :class="{ 'medal--light': medal.is_light, 'medal--dark': !medal.is_light }"
    :style="{
      borderColor: medal.guard_level > 0 ? getGuardColor(medal.guard_level) : getLevelColor(medal.level)
    }"
  >
    <span class="medal-name">{{ medal.name }}</span>
    <span
      class="medal-level"
      :style="{ backgroundColor: getLevelColor(medal.level) }"
    >
      {{ medal.level }}
    </span>
  </span>
</template>

<style scoped>
.medal {
  display: inline-flex;
  align-items: center;
  height: 22px;
  font-size: 12px;
  border-radius: 3px;
  border: 1px solid;
  overflow: hidden;
  margin-right: 6px;
  vertical-align: middle;
}

.medal--dark {
  opacity: 0.5;
}

.medal-name {
  padding: 0 6px;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.3);
  line-height: 20px;
}

.medal-level {
  padding: 0 6px;
  color: #fff;
  line-height: 20px;
  font-weight: bold;
}
</style>
