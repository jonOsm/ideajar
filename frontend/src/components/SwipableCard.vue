<script setup lang="ts">
import { computed, ref } from 'vue'
import { useCardSwipe } from '../composables/useCardSwipe'
import type { Pitch } from '../client/models/Pitch'
import BaseCard from './BaseCard.vue'

const props = defineProps<{
  pitch: Pitch
}>()

const emit = defineEmits<{
  (e: 'vote', direction: 'like' | 'dislike'): void
}>()

const cardComponent = ref<InstanceType<typeof BaseCard> | null>(null)
// Access the underlying DOM element for useCardSwipe
const cardEl = computed(() => cardComponent.value?.$el as HTMLElement | null)

const { cardTransform, visualOffset } = useCardSwipe(cardEl, {
    onSwipeRight: () => emit('vote', 'like'),
    onSwipeLeft: () => emit('vote', 'dislike'),
    threshold: 150
})
</script>

<template>
  <BaseCard
    ref="cardComponent"
    :type="pitch.type"
    class="absolute p-6 sm:p-10"
    :style="cardTransform"
  >
    <div class="mb-6 relative z-10">
        <span 
            class="badge badge-lg font-mono font-bold uppercase tracking-widest px-4 py-3" 
            :class="pitch.type === 'Opinion' ? 'badge-secondary' : 'badge-info'"
        >
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
    <!-- We check if visualOffset.x is enough to show labels -->
    <div v-if="visualOffset.x > 50" class="absolute top-8 right-8 text-emerald-500 font-black text-4xl border-4 border-emerald-500 rounded-lg px-4 py-2 rotate-12 bg-white/90 backdrop-blur-sm z-50 shadow-lg tracking-wider font-['Outfit'] pointer-events-none">
        YES
    </div>
    <div v-if="visualOffset.x < -50" class="absolute top-8 left-8 text-rose-500 font-black text-4xl border-4 border-rose-500 rounded-lg px-4 py-2 -rotate-12 bg-white/90 backdrop-blur-sm z-50 shadow-lg tracking-wider font-['Outfit'] pointer-events-none">
        NOPE
    </div>
  </BaseCard>
</template>

