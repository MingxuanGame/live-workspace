<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface Command {
  name: string
  description: string
  usage: string
}

interface CommandsResponse {
  commands: Record<string, Command>
  prefix: string[]
}

const commands = ref<Record<string, Command>>({})
const prefixes = ref<string[]>([])
const loading = ref(true)
const error = ref('')

// 计算显示的命令列表
const displayCommands = computed(() => {
  const primaryPrefix = prefixes.value[0] || ''
  return Object.values(commands.value).map(cmd => ({
    ...cmd,
    displayName: `${primaryPrefix}${cmd.name}`
  }))
})

// 计算前缀提示文本
const prefixHint = computed(() => {
  if (prefixes.value.length <= 1) return ''
  return `可用前缀: ${prefixes.value.join(', ')}`
})

// 获取命令列表
async function fetchCommands() {
  try {
    const response = await fetch('/danmaku/commands')
    if (!response.ok) {
      throw new Error('Failed to fetch commands')
    }
    const data: CommandsResponse = await response.json()
    commands.value = data.commands
    prefixes.value = data.prefix || ['/']
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCommands()
})
</script>

<template>
  <div class="command-bar">
    <div v-if="loading" class="loading">加载命令中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="commands-container">
      <div class="commands-scroll">
        <div
          v-for="cmd in displayCommands"
          :key="cmd.name"
          class="command-item"
        >
          <span class="command-name">{{ cmd.displayName }}</span>
          <span class="command-usage">{{ cmd.usage }}</span>
          <span class="command-desc">{{ cmd.description }}</span>
        </div>
        <div v-if="prefixHint" class="prefix-hint">{{ prefixHint }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.command-bar {
  width: 100%;
  height: 100%;
  background: transparent;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.loading,
.error {
  padding: 8px 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  text-shadow: none;
}

.error {
  color: #f44336;
  text-shadow: none;
}

.commands-container {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.commands-container::-webkit-scrollbar {
  display: none;
}

.commands-scroll {
  display: flex;
  gap: 16px;
  padding: 8px 16px;
  white-space: nowrap;
  align-items: center;
}

.command-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.1);
  padding: 6px 12px;
  border-radius: 16px;
}

.command-name {
  color: #4fc3f7;
  font-weight: 600;
  font-size: 13px;
  text-shadow: none;
}

.command-usage {
  color: #81c784;
  font-size: 12px;
  text-shadow: none;
}

.command-desc {
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  text-shadow: none;
}

.prefix-hint {
  color: rgba(255, 255, 255, 0.6);
  font-size: 11px;
  font-style: italic;
  margin-left: 8px;
  flex-shrink: 0;
  text-shadow: none;
}
</style>
