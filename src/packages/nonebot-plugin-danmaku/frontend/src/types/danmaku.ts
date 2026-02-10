// 粉丝牌信息
export interface Medal {
  name: string
  level: number
  is_light: boolean
  guard_level: number // 0:无, 1:总督, 2:提督, 3:舰长
}

// 表情信息
export interface Emote {
  emoji: string // 表情名称，如 "dog"，对应消息中的 [dog]
  url: string
  width: number
  height: number
  is_big_face?: boolean // 是否是大表情包
}

// 聚合礼物信息（用于礼物折叠显示）
export interface AggregatedGift {
  key: string // uid + gift_name 组合的唯一键
  uid: string
  username: string
  avatar: string
  medal?: Medal
  gift_name: string
  total_num: number
  total_price: number
  firstTime: number
  lastTime: number
}

// 基础消息类型
export interface BaseMessage {
  time: number // 时间戳，单位毫秒
  username: string
  id: string // 用户ID
  medal?: Medal
}

// 弹幕消息
export interface DanmakuMessage extends BaseMessage {
  content: string
  color?: string // 默认白色
  font_size?: number // 默认25
  emots?: Emote[]
  reply_uname?: string // 回复的用户名
  avatar?: string
}

// 进场/离场消息
export interface EnterLeaveMessage extends BaseMessage {
  avatar?: string
}

// 礼物消息
export interface GiftMessage extends BaseMessage {
  avatar: string
  gift_name: string
  gift_num: number
  price: number // RMB
}

// 醒目留言
export interface SuperChatMessage extends BaseMessage {
  start_time: number
  end_time: number
  content: string
  color?: string
  font_size?: number
  price: number // RMB
  avatar?: string
}

// 上舰消息
export interface GuardMessage extends BaseMessage {
  avatar: string
  guard_level: number // 1:总督, 2:提督, 3:舰长
  price: number
}

// 点赞消息
export interface LikeMessage extends BaseMessage {
  avatar?: string
}

// 消息类型
export type MessageType = 'danmaku' | 'enter' | 'leave' | 'gift' | 'superchat' | 'guard' | 'like'

// WebSocket 消息结构
export interface WSMessage {
  type: MessageType
  data: DanmakuMessage | EnterLeaveMessage | GiftMessage | SuperChatMessage | GuardMessage | LikeMessage
}

// 统一消息结构（用于存储和显示）
export interface DisplayMessage {
  id: string // 唯一标识
  type: MessageType
  data: DanmakuMessage | EnterLeaveMessage | GiftMessage | SuperChatMessage | GuardMessage | LikeMessage
  timestamp: number
}
