<script setup lang="ts">
import { computed } from 'vue'
import type {
  DisplayMessage,
  DanmakuMessage,
  EnterLeaveMessage,
  GiftMessage,
  SuperChatMessage,
  GuardMessage,
  LikeMessage,
  Emote
} from '@/types/danmaku'
import UserMedal from './UserMedal.vue'
import UserAvatar from './UserAvatar.vue'

const props = defineProps<{
  message: DisplayMessage
}>()

// 获取舰长等级文字
const getGuardLevelText = (level: number): string => {
  switch (level) {
    case 1: return '总督'
    case 2: return '提督'
    case 3: return '舰长'
    default: return ''
  }
}

// 获取SC价格等级 (blivechat 兼容)
const getSCPriceLevel = (price: number): number => {
  if (price >= 2000) return 7
  if (price >= 1000) return 6
  if (price >= 500) return 5
  if (price >= 100) return 4
  if (price >= 50) return 3
  if (price >= 30) return 2
  return 1
}

// 获取SC价格对应的颜色
const getSCPriceColor = (price: number): { bg: string; header: string; text: string } => {
  if (price >= 2000) return { bg: '#e62117', header: '#c41818', text: '#fff' }
  if (price >= 1000) return { bg: '#e62117', header: '#c41818', text: '#fff' }
  if (price >= 500) return { bg: '#e91e63', header: '#c2185b', text: '#fff' }
  if (price >= 100) return { bg: '#f57c00', header: '#e65100', text: '#fff' }
  if (price >= 50) return { bg: '#ffb300', header: '#ff8f00', text: '#fff' }
  if (price >= 30) return { bg: '#00bfa5', header: '#00897b', text: '#fff' }
  return { bg: '#1e88e5', header: '#1565c0', text: '#fff' }
}

// 解析消息内容中的表情，返回文本和表情片段
type ContentPart = { type: 'text'; content: string } | { type: 'emote'; emote: Emote }

const parseContentWithEmotes = (content: string, emots?: Emote[]): ContentPart[] => {
  if (!emots || emots.length === 0) {
    return [{ type: 'text', content }]
  }

  // 构建表情名到表情对象的映射
  const emoteMap = new Map<string, Emote>()
  for (const emote of emots) {
    emoteMap.set(emote.emoji, emote)
  }

  // 使用正则匹配方括号内容
  const parts: ContentPart[] = []
  const regex = /\[([^\]]+)\]/g
  let lastIndex = 0
  let match

  while ((match = regex.exec(content)) !== null) {
    // 添加匹配前的文本
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: content.slice(lastIndex, match.index) })
    }

    // 使用完整匹配（包括方括号），因为 emoji 字段本身就带方括号，如 "[花]"
    const emoteWithBrackets = match[0] as string
    const emote = emoteMap.get(emoteWithBrackets)

    if (emote) {
      // 找到对应表情，添加表情
      parts.push({ type: 'emote', emote })
    } else {
      // 未找到表情，保留原文
      parts.push({ type: 'text', content: match[0] })
    }

    lastIndex = regex.lastIndex
  }

  // 添加剩余文本
  if (lastIndex < content.length) {
    parts.push({ type: 'text', content: content.slice(lastIndex) })
  }

  return parts
}

// 类型断言辅助
const danmakuData = computed(() => props.message.data as DanmakuMessage)
const enterLeaveData = computed(() => props.message.data as EnterLeaveMessage)
const giftData = computed(() => props.message.data as GiftMessage)
const superChatData = computed(() => props.message.data as SuperChatMessage)
const guardData = computed(() => props.message.data as GuardMessage)
const likeData = computed(() => props.message.data as LikeMessage)

const scColors = computed(() => {
  if (props.message.type === 'superchat') {
    return getSCPriceColor(superChatData.value.price)
  }
  return { bg: '#1e88e5', header: '#1565c0', text: '#fff' }
})

const scPriceLevel = computed(() => {
  if (props.message.type === 'superchat') {
    return getSCPriceLevel(superChatData.value.price)
  }
  return 1
})

// 解析弹幕消息内容（包含表情）
const danmakuContentParts = computed(() => {
  if (props.message.type !== 'danmaku') return []
  return parseContentWithEmotes(danmakuData.value.content, danmakuData.value.emots)
})
</script>

<template>
  <div
    class="message"
    :class="[`message--${message.type}`]"
  >
    <!-- 弹幕消息 -->
    <template v-if="message.type === 'danmaku'">
      <UserAvatar
        v-if="danmakuData.avatar"
        :src="danmakuData.avatar"
        :size="32"
        class="avatar"
      />
      <div class="message-body">
        <div class="message-header">
          <span class="username">{{ danmakuData.username }}</span>
          <UserMedal v-if="danmakuData.medal" :medal="danmakuData.medal" />
        </div>
        <div class="message-bubble">
          <span
            v-if="danmakuData.reply_uname"
            class="reply-prefix"
          >回复 @{{ danmakuData.reply_uname }} </span>
          <template v-for="(part, i) in danmakuContentParts" :key="i">
            <span v-if="part.type === 'text'" class="text">{{ part.content }}</span>
            <img
              v-else
              class="emote"
              :class="{ 'emote--big': part.emote.is_big_face }"
              :src="part.emote.url"
              :alt="part.emote.emoji"
              :style="{
                height: part.emote.is_big_face ? '40px' : `${Math.min(part.emote.height, 24)}px`,
                width: 'auto'
              }"
              loading="lazy"
            />
          </template>
        </div>
      </div>
    </template>

    <!-- 进场消息 -->
    <template v-else-if="message.type === 'enter'">
      <UserAvatar v-if="enterLeaveData.avatar" :src="enterLeaveData.avatar" :size="20" class="avatar" />
      <UserMedal v-if="enterLeaveData.medal" :medal="enterLeaveData.medal" />
      <span class="username">{{ enterLeaveData.username }}</span>
      <span class="action-text">进入直播间</span>
    </template>

    <!-- 离场消息 -->
    <template v-else-if="message.type === 'leave'">
      <UserAvatar v-if="enterLeaveData.avatar" :src="enterLeaveData.avatar" :size="20" class="avatar" />
      <UserMedal v-if="enterLeaveData.medal" :medal="enterLeaveData.medal" />
      <span class="username">{{ enterLeaveData.username }}</span>
      <span class="action-text">离开直播间</span>
    </template>

    <!-- 礼物消息 -->
    <template v-else-if="message.type === 'gift'">
      <UserAvatar :src="giftData.avatar" :size="24" class="avatar" />
      <UserMedal v-if="giftData.medal" :medal="giftData.medal" />
      <span class="username">{{ giftData.username }}</span>
      <span class="action-text">
        赠送 <span class="gift-name">{{ giftData.gift_name }}</span>
        <span class="gift-num">x{{ giftData.gift_num }}</span>
      </span>
    </template>

    <!-- 醒目留言 (SuperChat) -->
    <template v-else-if="message.type === 'superchat'">
      <UserAvatar :src="superChatData.avatar || ''" :size="32" class="avatar" />
      <div class="message-body">
        <div class="message-header">
          <span class="username">{{ superChatData.username }}</span>
          <UserMedal v-if="superChatData.medal" :medal="superChatData.medal" />
        </div>
        <div
          class="sc-card"
          :class="`sc--level-${scPriceLevel}`"
          :blc-price-level="scPriceLevel"
        >
          <div class="sc-header">
            <span class="sc-price">CN¥{{ superChatData.price.toFixed(superChatData.price >= 1 ? 0 : 2) }}</span>
          </div>
          <div class="sc-content">{{ superChatData.content }}</div>
        </div>
      </div>
    </template>

    <!-- 上舰消息 (大航海) -->
    <template v-else-if="message.type === 'guard'">
      <UserAvatar :src="guardData.avatar" :size="32" class="avatar" />
      <div
        class="guard-card"
        :class="`guard--level-${guardData.guard_level}`"
        :blc-guard-level="guardData.guard_level"
      >
        <span class="guard-username">{{ guardData.username }}</span>
        <UserMedal v-if="guardData.medal" :medal="guardData.medal" />
        <span class="guard-badge">新{{ getGuardLevelText(guardData.guard_level) }}</span>
      </div>
    </template>

    <!-- 点赞消息 -->
    <template v-else-if="message.type === 'like'">
      <UserAvatar v-if="likeData.avatar" :src="likeData.avatar" :size="20" class="avatar" />
      <UserMedal v-if="likeData.medal" :medal="likeData.medal" />
      <span class="username">{{ likeData.username }}</span>
      <span class="action-text">点赞了直播间</span>
    </template>
  </div>
</template>

<style scoped>
/* 消息基础样式 */
.message {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 6px 8px;
  line-height: 1.4;
  word-break: break-word;
  animation: message-in 0.3s ease-out;
  background: transparent !important;
}

@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 头像 */
.avatar {
  flex-shrink: 0;
}

/* 消息主体 */
.message-body {
  display: inline-flex;
  flex-direction: column;
  gap: 2px;
  max-width: 100%;
}

/* 消息头部（用户名+勋章） */
.message-header {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* 用户名 */
.username {
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
  font-size: 13px;
  text-shadow: none;
}

/* 消息气泡 */
.message-bubble {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  background: #0dbc5e;
  color: #fff;
  padding: 6px 12px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.5;
  text-shadow: none;
  word-break: break-word;
  width: fit-content;
  max-width: 100%;
}

/* 消息文本 */
.text {
  color: #fff;
}

/* 回复前缀 */
.reply-prefix {
  color: rgba(255, 255, 255, 0.7);
  margin-right: 4px;
}

/* 表情 */
.emote {
  vertical-align: middle;
  margin: 0 2px;
}

/* 大表情包 */
.emote--big {
  margin: 0 4px;
  line-height: 1;
}

/* 进场/离场消息 */
.message--enter,
.message--leave {
  font-size: 12px;
  opacity: 0.7;
}

/* 动作文本 */
.action-text {
  color: rgba(0, 0, 0, 0.5);
  margin-left: 4px;
  text-shadow: none;
  font-size: 13px;
}

/* 礼物消息 */
.gift-name {
  color: #ffd700;
  font-weight: bold;
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.gift-num {
  color: #ff6b6b;
  font-weight: bold;
  margin-left: 2px;
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

/* 醒目留言 (SuperChat) 卡片样式 */
.sc-card {
  border-radius: 18px;
  overflow: hidden;
  text-shadow: none;
  max-width: 100%;
}

.sc-header {
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.15);
}

.sc-price {
  font-size: 12px;
  font-weight: bold;
  color: #fff;
}

.sc-content {
  padding: 8px 12px;
  color: #fff;
  font-size: 14px;
  line-height: 1.4;
}

/* SC 等级颜色 */
.sc--level-1 { background: #1e88e5; }
.sc--level-2 { background: #00bfa5; }
.sc--level-3 { background: #ffb300; }
.sc--level-4 { background: #f57c00; }
.sc--level-5 { background: #e91e63; }
.sc--level-6 { background: #e62117; }
.sc--level-7 { background: #e62117; }

/* 上舰消息卡片样式 */
.guard-card {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 18px;
  padding: 8px 14px;
  text-shadow: none;
}

.guard-username {
  color: #fff;
  font-weight: 500;
  font-size: 14px;
}

.guard-badge {
  color: #fff;
  font-size: 13px;
  margin-left: 4px;
}

.guard--level-1 {
  background: #e73b4d;
}

.guard--level-2 {
  background: #a068f1;
}

.guard--level-3 {
  background: #0f9d58;
}

/* 点赞消息 */
.message--like {
  font-size: 12px;
  opacity: 0.6;
}
</style>
