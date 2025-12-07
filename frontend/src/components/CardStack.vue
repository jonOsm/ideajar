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
    <div class="stack w-full max-w-sm h-96 relative">
        <!-- Next Card (Bottom) -->
        <SwipableCard
            v-if="nextPitch"
            :key="nextPitch.id"
            :pitch="nextPitch"
            class="transform scale-90 translate-y-4 opacity-70 z-0 pointer-events-none absolute inset-0"
        />

        <!-- Active Card (Top) -->
        <SwipableCard
            v-if="activePitch"
            :key="activePitch.id"
            :pitch="activePitch"
            :is-active="true"
            @vote="handleCardVote"
            class="z-10 absolute inset-0"
        />

        <!-- No More Cards -->
        <NoMoreCard
            v-if="!activePitch"
            @refresh="emit('refresh')"
            class="z-0 absolute inset-0"
        />
    </div>
</template>
