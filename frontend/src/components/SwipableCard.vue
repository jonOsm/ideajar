<script setup lang="ts">
import { ref, computed } from 'vue'

import type { Pitch } from '../client/models/Pitch'

const props = defineProps<{
  pitch: Pitch
}>()

const emit = defineEmits<{
  (e: 'vote', direction: 'like' | 'dislike'): void
}>()

const cardRef = ref<HTMLElement | null>(null)

import { usePointerSwipe } from '@vueuse/core'

const { distanceX, distanceY, isSwiping } = usePointerSwipe(cardRef, {
  onSwipeEnd: () => {
    const swipeDist = -distanceX.value
    
    if (swipeDist > 150) {
      emit('vote', 'like')
    } else if (swipeDist < -150) {
      emit('vote', 'dislike')
    }
  },
})

// Visual offset wrapper: If acting upon drag, reflect distance.
// If released (not swiping), we want it to snap to 0 (unless removed by parent).
// We use a CSS class for transition to animate the snap back.
const visualOffset = computed(() => {
    if (isSwiping.value) {
        return { x: -distanceX.value, y: -distanceY.value }
    }
    return { x: 0, y: 0 }
})

const cardStyle = computed(() => {
  const { x, y } = visualOffset.value
  const rotateOutput = x * 0.05
  
  return {
    transform: `translate(${x}px, ${y}px) rotate(${rotateOutput}deg)`,
    cursor: isSwiping.value ? 'grabbing' : 'grab',
    opacity: 1 - Math.abs(x) / 1000,
    // Enable transition when NOT swiping (so it animates back to 0)
    // Disable when swiping (so it follows finger instantly)
    transition: isSwiping.value ? 'none' : 'transform 0.3s ease-out'
  }
})


const typeColor = computed(() => {
    switch(props.pitch.type) {
        case 'idea': return 'badge-info'
        case 'opinion': return 'badge-secondary'
        case 'pitch': return 'badge-accent'
        default: return 'badge-ghost'
    }
})
</script>

<template>
  <div 
    ref="cardRef" 
    class="absolute w-full max-w-sm card bg-base-100 shadow-xl border-2 border-base-200 p-6 touch-none select-none transition-transform duration-75"
    :style="cardStyle"
  >
    <div class="mb-4">
        <span class="badge badge-lg font-bold uppercase tracking-wide" :class="typeColor">
            {{ pitch.type }}
        </span>
    </div>
    <h2 class="text-3xl font-bold mb-2 text-base-content">{{ pitch.title }}</h2>
    <p class="text-base-content/80 text-lg leading-relaxed">{{ pitch.description }}</p>
    
    <div class="mt-6 pt-4 border-t border-base-200 flex justify-between text-sm text-base-content/60">
        <span>Submitted by {{ pitch.submitter }}</span>
        <span>Swipe L/R to Vote</span>
    </div>
    
    <!-- Visual indicators for swipe -->
    <div v-if="visualOffset.x > 50" class="absolute top-4 right-4 text-success font-bold text-xl border-4 border-success rounded-lg px-2 rotate-12 bg-base-100/80">
        LIKE
    </div>
    <div v-if="visualOffset.x < -50" class="absolute top-4 left-4 text-error font-bold text-xl border-4 border-error rounded-lg px-2 -rotate-12 bg-base-100/80">
        NOPE
    </div>
  </div>
</template>
