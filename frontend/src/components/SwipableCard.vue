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
        case 'idea': return 'bg-blue-100 text-blue-800'
        case 'opinion': return 'bg-purple-100 text-purple-800'
        case 'pitch': return 'bg-green-100 text-green-800'
        default: return 'bg-gray-100 text-gray-800'
    }
})
</script>

<template>
  <div 
    ref="cardRef" 
    class="absolute w-full max-w-sm bg-white rounded-xl shadow-2xl p-6 border-2 border-gray-100 touch-none select-none transition-transform duration-75"
    :style="cardStyle"
  >
    <div class="mb-4">
        <span :class="['px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide', typeColor]">
            {{ pitch.type }}
        </span>
    </div>
    <h2 class="text-3xl font-bold mb-2 text-gray-800">{{ pitch.title }}</h2>
    <p class="text-gray-600 text-lg leading-relaxed">{{ pitch.description }}</p>
    
    <div class="mt-6 pt-4 border-t border-gray-100 flex justify-between text-sm text-gray-400">
        <span>Submitted by {{ pitch.submitter }}</span>
        <span>Swipe L/R to Vote</span>
    </div>
    
    <!-- Visual indicators for swipe -->
    <div v-if="visualOffset.x > 50" class="absolute top-4 right-4 text-green-500 font-bold text-xl border-2 border-green-500 rounded px-2 rotate-12 bg-white/80">
        LIKE
    </div>
    <div v-if="visualOffset.x < -50" class="absolute top-4 left-4 text-red-500 font-bold text-xl border-2 border-red-500 rounded px-2 -rotate-12 bg-white/80">
        NOPE
    </div>
  </div>
</template>
