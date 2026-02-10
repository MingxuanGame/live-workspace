import { ref, type Ref } from 'vue'
import type { WSMessage, DisplayMessage } from '@/types/danmaku'

export interface UseDanmakuWebSocketOptions {
  maxMessages?: number // 最大消息数量，用于性能优化
  reconnectInterval?: number // 重连间隔（毫秒）
  maxReconnectAttempts?: number // 最大重连次数
}

export interface UseDanmakuWebSocketReturn {
  messages: Ref<DisplayMessage[]>
  isConnected: Ref<boolean>
  error: Ref<string | null>
  connect: (roomId: string) => void
  disconnect: () => void
  clearMessages: () => void
}

export function useDanmakuWebSocket(options: UseDanmakuWebSocketOptions = {}): UseDanmakuWebSocketReturn {
  const {
    maxMessages = 100,
    reconnectInterval = 3000,
    maxReconnectAttempts = 10
  } = options

  const messages = ref<DisplayMessage[]>([])
  const isConnected = ref(false)
  const error = ref<string | null>(null)

  let ws: WebSocket | null = null
  let reconnectAttempts = 0
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let currentRoomId: string | null = null
  let messageIdCounter = 0

  // 生成唯一消息ID
  const generateMessageId = (): string => {
    return `msg_${Date.now()}_${++messageIdCounter}`
  }

  // 处理WebSocket消息
  const handleMessage = (event: MessageEvent) => {
    try {
      const wsMessage: WSMessage = JSON.parse(event.data)
      const displayMessage: DisplayMessage = {
        id: generateMessageId(),
        type: wsMessage.type,
        data: wsMessage.data,
        timestamp: wsMessage.data.time || Date.now()
      }

      // 添加消息并限制数量
      messages.value = [...messages.value, displayMessage].slice(-maxMessages)
    } catch (e) {
      console.error('Failed to parse WebSocket message:', e)
    }
  }

  // 连接WebSocket
  const connect = (roomId: string) => {
    if (ws) {
      disconnect()
    }

    currentRoomId = roomId
    reconnectAttempts = 0
    error.value = null

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/danmaku/ws/${roomId}`

    try {
      ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        isConnected.value = true
        error.value = null
        reconnectAttempts = 0
        console.log(`WebSocket connected to room ${roomId}`)
      }

      ws.onmessage = handleMessage

      ws.onclose = (event) => {
        isConnected.value = false
        console.log('WebSocket closed:', event.code, event.reason)

        // 非正常关闭时尝试重连
        if (!event.wasClean && currentRoomId && reconnectAttempts < maxReconnectAttempts) {
          reconnectAttempts++
          console.log(`Attempting to reconnect (${reconnectAttempts}/${maxReconnectAttempts})...`)
          reconnectTimer = setTimeout(() => {
            if (currentRoomId) {
              connect(currentRoomId)
            }
          }, reconnectInterval)
        } else if (reconnectAttempts >= maxReconnectAttempts) {
          error.value = '连接失败，已达到最大重连次数'
        }
      }

      ws.onerror = (event) => {
        console.error('WebSocket error:', event)
        error.value = '连接错误'
      }
    } catch (e) {
      error.value = `连接失败: ${e}`
      console.error('Failed to create WebSocket:', e)
    }
  }

  // 断开WebSocket
  const disconnect = () => {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }

    currentRoomId = null

    if (ws) {
      ws.close(1000, 'Manual disconnect')
      ws = null
    }

    isConnected.value = false
  }

  // 清空消息
  const clearMessages = () => {
    messages.value = []
  }

  return {
    messages,
    isConnected,
    error,
    connect,
    disconnect,
    clearMessages
  }
}
