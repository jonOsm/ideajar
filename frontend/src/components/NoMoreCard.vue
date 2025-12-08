<script setup lang="ts">
defineEmits<{
  (e: 'refresh'): void
}>()
</script>

<template>
    <div class="text-center flex flex-col items-center justify-center h-full w-full">
        <div class="text-6xl mb-4">🎉</div>
        <h2 class="text-2xl font-bold font-['Outfit']">All caught up!</h2>
        <p class="text-base-content/70 mb-6">No more ideas to review right now.</p>
        <button 
        @click="$emit('refresh')" 
        class="btn btn-primary btn-lg rounded-full shadow-lg font-bold"
        >
        Check Again
        </button>
    </div>
</template>
