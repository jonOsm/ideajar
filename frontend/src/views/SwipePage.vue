<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SwipableCard from '../components/SwipableCard.vue'
import { PitchesService, type Pitch } from '../client'
import { OpenAPI } from '../client/core/OpenAPI'

const router = useRouter()
const pitches = ref<Pitch[]>([])
const loading = ref(true)
const drawerOpen = ref(false)

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
  <div class="drawer drawer-end fixed inset-0 font-['Nunito']">
    <input id="app-drawer" type="checkbox" class="drawer-toggle" v-model="drawerOpen" />
    
    <div class="drawer-content flex flex-col items-center justify-between p-4 sm:p-8 bg-base-200 overflow-hidden h-full">
        <!-- Page Content -->
        <header class="text-center flex flex-col items-center relative w-full max-w-sm shrink-0">
        <h1 class="text-4xl sm:text-5xl font-extrabold text-primary mb-1 sm:mb-2 font-['Outfit']">
            IdeaJar
        </h1>
        <p class="text-base-content/70 text-sm sm:text-base">Find your next big inspiration</p>
        <label for="app-drawer" class="btn btn-ghost btn-circle absolute right-0 top-0 drawer-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
        </label>
        </header>

        <main class="relative w-full max-w-md h-[70vh] max-h-[600px] my-4 flex items-center justify-center">
        <div v-if="loading" class="flex flex-col items-center w-full h-full">
            <div class="skeleton w-full h-full rounded-[2rem]"></div>
        </div>

        <div v-else-if="currentPitch" class="relative w-full h-full flex items-center justify-center">
            <SwipableCard 
            :key="currentPitch.id"
            :pitch="currentPitch" 
            @vote="handleVote"
            />
            
            <div v-if="pitches.length > 1" class="absolute inset-0 w-full h-full bg-base-100 rounded-[2rem] shadow-lg opacity-50 scale-95 -z-10 border border-base-300"></div>
        </div>

        <div v-else class="text-center">
            <div class="text-6xl mb-4">🎉</div>
            <h2 class="text-2xl font-bold font-['Outfit']">All caught up!</h2>
            <p class="text-base-content/70 mb-6">No more ideas to review right now.</p>
            <button 
            @click="fetchPitches" 
            class="btn btn-primary btn-lg rounded-full shadow-lg font-bold"
            >
            Check Again
            </button>
        </div>
        </main>
        
        <div class="shrink-0 h-4"></div> <!-- Bottom spacer -->
    </div> 
    
    <div class="drawer-side z-50">
        <label for="app-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
        <div class="menu p-4 w-80 min-h-full bg-base-100 text-base-content flex flex-col">
            <div class="flex justify-between items-center mb-6 px-4">
                <h2 class="text-2xl font-black font-['Outfit']">Menu</h2>
                 <button @click="drawerOpen = false" class="btn btn-ghost btn-circle btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <ul class="space-y-2">
                <li><a class="text-lg font-semibold py-3 active:bg-primary/20 active:text-primary">My Profile</a></li>
                <li><a class="text-lg font-semibold py-3 active:bg-primary/20 active:text-primary">Settings</a></li>
                <div class="divider my-2"></div>
                <li><a @click="handleLogout" class="text-lg font-semibold py-3 text-error active:bg-error/10">Sign Out</a></li>
            </ul>
        </div>
    </div>
  </div>
</template>
