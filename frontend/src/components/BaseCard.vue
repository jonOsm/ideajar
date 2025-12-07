
<template>
  <div 
    class="w-full h-full card shadow-xl touch-none select-none flex flex-col justify-center rounded-[2rem] overflow-hidden dark:text-white border border-white/20"
    :class="currentTheme.backgroundClass"
  >
    <!-- Background Decor -->
    <div class="absolute -bottom-16 -right-16 opacity-[0.07] dark:opacity-[0.15] rotate-12 pointer-events-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-96 w-96" fill="currentColor" viewBox="0 0 24 24">
            <path :d="currentTheme.iconPath" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    </div>

    <!-- Content Slot -->
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface CardTheme {
    backgroundClass: string;
    iconPath: string;
}

const DEFAULT_THEME: CardTheme = {
    backgroundClass: 'bg-gradient-to-br from-gray-50 to-slate-100 dark:from-slate-900 dark:to-slate-800',
    iconPath: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
}

const THEMES: Record<string, CardTheme> = {
    Idea: {
        backgroundClass: 'bg-gradient-to-br from-blue-50 to-cyan-100 dark:from-slate-900 dark:to-cyan-900',
        iconPath: 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z'
    },
    Opinion: {
        backgroundClass: 'bg-gradient-to-br from-rose-50 to-orange-100 dark:from-slate-900 dark:to-rose-900',
        iconPath: 'M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z'
    },
    default: DEFAULT_THEME
}

const props = withDefaults(defineProps<{
    type?: 'Idea' | 'Opinion' | string
}>(), {
    type: 'Idea'
})

const currentTheme = computed(() => {
    // Normalization to handle potential case issues or loose strings
    // but strict type matching is better if we control inputs.
    // The previous code had lower case 'idea'/'opinion' incorrectly in SwipableCard?
    // Let's check SwipableCard.vue again - pitch.type comes from backend.
    
    // In SwipableCard it was lower case keys 'idea', 'opinion' in THEME object,
    // but pitch.type usually is capitalized from backend 'Idea', 'Opinion'.
    // Let's verify standard.
    
    // PitchCreationCard uses 'Idea' / 'Opinion' strings.
    // Backend models usually PascalCase or capitalize.
    // Let's safe-guard by checking both or normalizing.
    
    const key = props.type
    // Direct match
    if (THEMES[key]) return THEMES[key]
    
    // We'll update THEMES keys to be forgiving or matching what's used.
    // Let's stick to the key passed.
    
    // Wait, in SwipableCard earlier:
    // THEMES keys were 'idea' (lowercase).
    // pitch.type used in template: {{ pitch.type }} -> likely 'Idea' or 'Opinion'.
    // Access: THEMES[props.pitch.type].
    // If pitch.type is 'Idea', THEMES['Idea'] would be undefined if keys are lower case.
    // It's likely pitch.type is lowercase 'idea'/'opinion' from backend OR the previous code was buggy OR I misread.
    // Let's check models.py content if I can, or just be robust.
    
    // I will use a robust lookup.
    return THEMES[key] || THEMES[props.type.charAt(0).toUpperCase() + props.type.slice(1).toLowerCase()] || DEFAULT_THEME
})

</script>
