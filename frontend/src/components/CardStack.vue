<script setup lang="ts">
import { computed } from 'vue'
import SwipableCard from './SwipableCard.vue'
import NoMoreCard from './NoMoreCard.vue'
import type { Pitch } from '../client/models/Pitch'

const props = defineProps<{
  pitches: Pitch[]
}>()

const emit = defineEmits<{
  (e: 'vote', id: string, type: 'like' | 'dislike'): void
  (e: 'refresh'): void
}>()

const activePitch = computed(() => {
    return props.pitches[0] || null
})

const nextPitch = computed(() => {
    return props.pitches[1] || null
})

const handleCardVote = (type: 'like' | 'dislike') => {
    if (!activePitch.value || !activePitch.value.id) return
    emit('vote', activePitch.value.id, type)
}
</script>

<template>
    <div class="stack w-full h-full relative">
        <!-- Next Card (Bottom) -->
        <SwipableCard
            v-if="nextPitch"
            :key="nextPitch.id"
            :pitch="nextPitch"
            class="transform scale-90 translate-y-4 opacity-70 z-0 pointer-events-none absolute inset-0"
        />

        <!-- Active Card (Top) -->
        <Transition name="promote-card">
            <SwipableCard
                v-if="activePitch"
                :key="activePitch.id"
                :pitch="activePitch"
                :is-active="true"
                @vote="handleCardVote"
                class="z-10 absolute inset-0"
            />
        </Transition>

        <!-- No More Cards -->
        <NoMoreCard
            v-if="!activePitch"
            @refresh="emit('refresh')"
            class="z-0 absolute inset-0"
        />
    </div>
</template>

<style scoped>
.promote-card-enter-active {
    transition: all 0.2s ease-out;
}
.promote-card-enter-from {
    transform: scale(0.9) translateY(1rem) !important;
    opacity: 0.7;
}
</style>
