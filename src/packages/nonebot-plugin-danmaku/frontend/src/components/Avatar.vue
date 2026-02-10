<script setup lang="ts">
defineProps<{
  src: string
  alt?: string
  size?: number
}>()
</script>

<template>
  <img
    class="avatar"
    :src="src"
    :alt="alt || 'avatar'"
    :style="{ width: `${size || 24}px`, height: `${size || 24}px` }"
    loading="lazy"
    @error="(e) => (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22><circle cx=%2212%22 cy=%2212%22 r=%2212%22 fill=%22%23666%22/></svg>'"
  />
</template>

<style scoped>
.avatar {
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  vertical-align: middle;
}
</style>
