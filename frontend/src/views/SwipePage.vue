<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SwipableCard from '../components/SwipableCard.vue'
import { PitchesService, type Pitch } from '../client'
import { OpenAPI } from '../client/core/OpenAPI'

const router = useRouter()
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
      pitch_id: currentPitch.id!,
      vote_type: direction
    })
    console.log(`Voted ${direction} on ${currentPitch.title}`)
  } catch (error) {
    console.error("Failed to submit vote", error)
  }
}

const handleLogout = () => {
    localStorage.removeItem('access_token')
    OpenAPI.TOKEN = ''
    router.push('/login')
}

onMounted(() => {
  fetchPitches()
})

const currentPitch = computed(() => pitches.value[0])
</script>

<template>
  <div class="fixed inset-0 bg-base-200 flex flex-col items-center justify-between p-4 sm:p-8 overflow-hidden">
    <header class="text-center flex flex-col items-center relative w-full max-w-sm shrink-0">
      <h1 class="text-4xl sm:text-5xl font-extrabold text-primary mb-1 sm:mb-2">
        IdeaJar
      </h1>
      <p class="text-base-content/70 text-sm sm:text-base">Find your next big inspiration</p>
      <button @click="handleLogout" class="btn btn-ghost btn-sm absolute right-0 top-0">
        Sign Out
      </button>
    </header>

    <main class="relative w-full max-w-md h-[70vh] max-h-[600px] my-4 flex items-center justify-center">
      <div v-if="loading" class="flex flex-col items-center w-full h-full">
         <div class="skeleton w-full h-full rounded-3xl"></div>
      </div>

      <div v-else-if="currentPitch" class="relative w-full h-full flex items-center justify-center">
        <SwipableCard 
          :key="currentPitch.id"
          :pitch="currentPitch" 
          @vote="handleVote"
        />
        
        <div v-if="pitches.length > 1" class="absolute inset-0 w-full h-full bg-base-100 rounded-3xl shadow-lg opacity-50 scale-95 -z-10 border border-base-300"></div>
      </div>

      <div v-else class="text-center">
        <div class="text-6xl mb-4">🎉</div>
        <h2 class="text-2xl font-bold">All caught up!</h2>
        <p class="text-base-content/70 mb-6">No more ideas to review right now.</p>
        <button 
          @click="fetchPitches" 
          class="btn btn-primary btn-lg rounded-full shadow-lg"
        >
          Check Again
        </button>
      </div>
    </main>
    
    <div class="shrink-0 h-4"></div> <!-- Bottom spacer -->
  </div>
</template>
