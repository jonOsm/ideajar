<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import SwipableCard from '../components/SwipableCard.vue'
import SidebarMenu from '../components/SidebarMenu.vue'
import AppHeader from '../components/AppHeader.vue'
import NoMoreCard from '../components/NoMoreCard.vue'
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
        <AppHeader @openMenu="drawerOpen = true" />

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

        <NoMoreCard v-else @refresh="fetchPitches" />
        </main>
        
        <div class="shrink-0 h-4"></div> <!-- Bottom spacer -->
    </div> 
    
    <SidebarMenu 
        drawerId="app-drawer" 
        @close="drawerOpen = false" 
        @logout="handleLogout" 
    />
  </div>
</template>
