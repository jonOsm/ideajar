<script setup lang="ts">
defineEmits<{
  (e: 'openMenu'): void
}>()
</script>

<template>
    <header class="text-center flex flex-col items-center relative w-full max-w-sm shrink-0">
    <h1 class="text-4xl sm:text-5xl font-extrabold text-primary mb-1 sm:mb-2 font-['Outfit']">
        IdeaJar
    </h1>
    <p class="text-base-content/70 text-sm sm:text-base">Find your next big inspiration</p>
    <button @click="$emit('openMenu')" class="btn btn-ghost btn-circle absolute right-0 top-0 drawer-button">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
    </button>
    </header>
</template>
