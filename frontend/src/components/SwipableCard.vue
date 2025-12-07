<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePointerSwipe } from '@vueuse/core'
import type { Pitch } from '../client/models/Pitch'

interface CardTheme {
    backgroundClass: string;
    badgeClass: string;
    iconPath: string;
}

// Pulled out of THEMES to keep typechecker happy
const DEFAULT_THEME: CardTheme = {
    backgroundClass: 'bg-gradient-to-br from-gray-50 to-slate-100 dark:from-slate-900 dark:to-slate-800',
    badgeClass: 'badge-ghost',
    iconPath: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

const THEMES: Record<string, CardTheme> = {
    idea: {
        backgroundClass: 'bg-gradient-to-br from-blue-50 to-cyan-100 dark:from-slate-900 dark:to-cyan-900',
        badgeClass: 'badge-info',
        iconPath: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'
    },
    opinion: {
        backgroundClass: 'bg-gradient-to-br from-rose-50 to-orange-100 dark:from-slate-900 dark:to-rose-900',
        badgeClass: 'badge-secondary',
        iconPath: 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z'
    },
    default: DEFAULT_THEME
}

const props = defineProps<{
  pitch: Pitch
}>()

const emit = defineEmits<{
  (e: 'vote', direction: 'like' | 'dislike'): void
}>()

const cardRef = ref<HTMLElement | null>(null)

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
    transition: isSwiping.value ? 'none' : 'transform 0.3s ease-out'
  }
})

const currentTheme = computed(() => {
    return THEMES[props.pitch.type] || DEFAULT_THEME
})
</script>

<template>
  <div 
    ref="cardRef" 
    class="absolute w-full h-full card shadow-2xl border border-white/20 p-6 sm:p-10 touch-none select-none transition-transform duration-75 flex flex-col justify-center rounded-[2rem] cursor-grab active:cursor-grabbing overflow-hidden dark:text-white"
    :class="currentTheme.backgroundClass"
    :style="cardStyle"
  >
    <!-- Background Decor -->
    <div class="absolute -bottom-16 -right-16 opacity-[0.07] dark:opacity-[0.15] rotate-12 pointer-events-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-96 w-96" fill="currentColor" viewBox="0 0 24 24">
            <path :d="currentTheme.iconPath" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    </div>

    <div class="mb-6 relative z-10">
        <span class="badge badge-lg font-mono font-bold uppercase tracking-widest px-4 py-3" :class="currentTheme.badgeClass">
            {{ pitch.type }}
        </span>
    </div>
    
    <h2 class="text-4xl sm:text-5xl font-black mb-6 leading-tight font-['Outfit'] relative z-10 text-slate-800 dark:text-white">
      {{ pitch.title }}
    </h2>
    
    <p class="text-xl font-['Nunito'] font-semibold leading-relaxed relative z-10 text-slate-600 dark:text-white/90">
      {{ pitch.description }}
    </p>
    
    <div class="mt-auto pt-8 flex justify-between items-end border-t border-black/5 dark:border-white/10 relative z-10">
        <div class="flex flex-col">
            <span class="text-xs uppercase tracking-wider font-bold opacity-50 mb-1">Posted By</span>
            <span class="font-bold text-slate-700 dark:text-white">{{ pitch.submitter }}</span>
        </div>
        <div class="flex flex-col items-end opacity-50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
            <span class="text-xs font-bold uppercase tracking-wider">Swipe</span>
        </div>
    </div>
    
    <!-- Visual indicators for swipe -->
    <div v-if="visualOffset.x > 50" class="absolute top-8 right-8 text-emerald-500 font-black text-4xl border-4 border-emerald-500 rounded-lg px-4 py-2 rotate-12 bg-white/90 backdrop-blur-sm z-50 shadow-lg tracking-wider font-['Outfit']">
        YES
    </div>
    <div v-if="visualOffset.x < -50" class="absolute top-8 left-8 text-rose-500 font-black text-4xl border-4 border-rose-500 rounded-lg px-4 py-2 -rotate-12 bg-white/90 backdrop-blur-sm z-50 shadow-lg tracking-wider font-['Outfit']">
        NOPE
    </div>
  </div>
</template>
