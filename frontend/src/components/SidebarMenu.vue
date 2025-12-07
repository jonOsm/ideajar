<script setup lang="ts">
defineProps<{
  drawerId: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'logout'): void
}>()
</script>

<template>
    <div class="drawer-side z-50">
        <label :for="drawerId" aria-label="close sidebar" class="drawer-overlay"></label>
        <div class="menu p-4 w-80 min-h-full bg-base-100 text-base-content flex flex-col">
            <div class="flex justify-between items-center mb-6 px-4">
                <h2 class="text-2xl font-black font-['Outfit']">Menu</h2>
                 <button @click="emit('close')" class="btn btn-ghost btn-circle btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <ul class="space-y-2">
                <li><a class="text-lg font-semibold py-3 active:bg-primary/20 active:text-primary">My Profile</a></li>
                <li><a class="text-lg font-semibold py-3 active:bg-primary/20 active:text-primary">Settings</a></li>
                <div class="divider my-2"></div>
                <li><a @click="emit('logout')" class="text-lg font-semibold py-3 text-error active:bg-error/10">Sign Out</a></li>
            </ul>
        </div>
    </div>
</template>
