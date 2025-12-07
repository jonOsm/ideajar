<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import SwipableCard from './components/SwipableCard.vue'
import { PitchesService, type Pitch } from './client'
import { OpenAPI } from './client/core/OpenAPI'

OpenAPI.BASE = '' 

const pitches = ref<Pitch[]>([])
const loading = ref(true)

const fetchPitches = async () => {
  loading.value = true
  try {
    pitches.value = await PitchesService.getPitches()
  } catch (error) {
    console.error("Failed to fetch pitches", error)
  } finally {
    loading.value = false
  }
}

const handleVote = async (direction: 'like' | 'dislike') => {
  const currentPitch = pitches.value[0]
  if (!currentPitch) return

  // Optimistic UI: Remove card immediately
  pitches.value.shift()

  try {
    await PitchesService.submitVote({
      pitch_id: currentPitch.id,
      vote_type: direction
    })
    console.log(`Voted ${direction} on ${currentPitch.title}`)
  } catch (error) {
    console.error("Failed to submit vote", error)
  }
}


onMounted(() => {
  fetchPitches()
})

const currentPitch = computed(() => pitches.value[0])
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
    <header class="mb-8 text-center">
      <h1 class="text-4xl font-extrabold text-violet-600">
        IdeaSwipe
      </h1>
      <p class="text-gray-500 mt-2">Find your next big inspiration</p>
    </header>

    <main class="relative w-full max-w-sm h-[600px] flex items-center justify-center">
      <div v-if="loading" class="animate-pulse flex flex-col items-center">
        <div class="h-64 w-64 bg-gray-200 rounded-full mb-4"></div>
        <div class="h-4 w-32 bg-gray-200 rounded"></div>
      </div>

      <div v-else-if="currentPitch" class="relative w-full h-full flex items-center justify-center">
        <SwipableCard 
          :key="currentPitch.id"
          :pitch="currentPitch" 
          @vote="handleVote"
        />
        
        <div v-if="pitches.length > 1" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-sm h-auto p-6 bg-white rounded-xl shadow opacity-50 scale-95 -z-10 border border-gray-100">
             <div class="h-48"></div>
        </div>
      </div>

      <div v-else class="text-center">
        <div class="text-6xl mb-4">🎉</div>
        <h2 class="text-2xl font-bold text-gray-800">All caught up!</h2>
        <p class="text-gray-500 mb-6">No more ideas to review right now.</p>
        <button 
          @click="fetchPitches" 
          class="px-6 py-3 bg-gradient-to-r from-pink-500 to-violet-500 text-white font-bold rounded-full shadow hover:shadow-lg transition transform hover:-translate-y-1"
        >
          Check Again
        </button>
      </div>
    </main>
  </div>
</template>

<style>

body {
    background-color: #f9fafb;
}
</style>
