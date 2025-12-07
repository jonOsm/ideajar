<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PitchesService } from '../client'
import type { Pitch } from '../client/models/Pitch'
import AppHeader from '../components/AppHeader.vue'
import SidebarMenu from '../components/SidebarMenu.vue'
import CardStack from '../components/CardStack.vue'
import PitchCreationCard from '../components/PitchCreationCard.vue'

const router = useRouter()
const pitches = ref<Pitch[]>([])
const loading = ref(false)
const showMenu = ref(false)
const isCreating = ref(false)

const fetchPitches = async () => {
  if (isCreating.value) return // Don't fetch if creating
  loading.value = true
  try {
    pitches.value = await PitchesService.getPitches()
  } catch (error) {
    console.error("Failed to fetch pitches", error)
  } finally {
    loading.value = false
  }
}

const handleVote = async (id: string, type: 'like' | 'dislike') => {
    // Optimistic UI update
    const pitch = pitches.value.find(p => p.id === id)
    if (!pitch) return

    pitches.value = pitches.value.filter(p => p.id !== id)

    try {
        await PitchesService.submitVote({
            pitch_id: id,
            vote_type: type
        })
    } catch (error) {
        console.error('Failed to submit vote:', error)
        // Ideally revert optimistic update here, but for now we just log
    }
}

const handleCreated = () => {
    isCreating.value = false
    fetchPitches() // Refresh stack to maybe show new pitch (or just refresh)
}

const handleLogout = () => {
    localStorage.removeItem('access_token')
    router.push('/login')
}

onMounted(() => {
  fetchPitches()
})
</script>

<template>
  <div class="drawer drawer-end fixed inset-0 font-['Nunito']">
    <input id="app-drawer" type="checkbox" class="drawer-toggle" v-model="showMenu" />
    
    <div class="drawer-content flex flex-col items-center justify-between p-4 sm:p-8 bg-base-200 overflow-hidden h-full">
        <!-- Page Content -->
        <AppHeader @openMenu="showMenu = true" />

        <div class="relative w-full max-w-md h-[70vh] md:h-[75vh] max-h-[600px] md:max-h-[700px] flex items-center justify-center">
             <Transition name="fade" mode="out-in">
                <PitchCreationCard
                    v-if="isCreating"
                    @created="handleCreated"
                    @cancel="isCreating = false"
                />
                
                <CardStack
                    v-else
                    :pitches="pitches"
                    @vote="handleVote"
                    @refresh="fetchPitches"
                />
             </Transition>
        </div>
        
        <!-- Action Buttons -->
        <div class="shrink-0 h-16 flex items-center justify-center w-full max-w-md">
            <button 
                v-if="!isCreating"
                @click="isCreating = true" 
                class="btn btn-circle btn-primary btn-lg shadow-xl hover:scale-105 transition-transform"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
            </button>
             <button 
                v-else
                @click="isCreating = false" 
                class="btn btn-circle btn-ghost btn-lg text-base-content/50 hover:bg-base-300"
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    </div> 
    
    <SidebarMenu 
        drawerId="app-drawer" 
        @close="showMenu = false" 
        @logout="handleLogout" 
    />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
