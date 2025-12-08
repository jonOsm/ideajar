<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCardSwipe } from '../composables/useCardSwipe'
import { PitchesService } from '../client'
import { getReadableError } from '../constants/errors'
import BaseCard from './BaseCard.vue'

const emit = defineEmits<{
  (e: 'created'): void
  (e: 'cancel'): void
}>()

const title = ref('')
const description = ref('')
const type = ref<'Idea' | 'Opinion'>('Idea') // Default type
const loading = ref(false)
const error = ref('')

// Card Swipe Logic (Swipe Right to Post, Swipe Left to Cancel)
const cardComponent = ref<InstanceType<typeof BaseCard> | null>(null)
const cardEl = computed(() => cardComponent.value?.$el as HTMLElement | null)

const { cardTransform, isSwipingRight, isSwipingLeft } = useCardSwipe(cardEl, {
    threshold: 100,
    onSwipeRight: () => submitPitch(),
    onSwipeLeft: () => emit('cancel')
})

const submitPitch = async () => {
    if (loading.value) return
    
    // Basic validation
    if (!title.value.trim() || !description.value.trim()) {
        error.value = "Please fill in all fields"
        return
    }

    loading.value = true
    error.value = ''

    try {
        await PitchesService.createPitch({
            title: title.value,
            description: description.value,
            type: type.value
        })
        emit('created')
    } catch (e: any) {
        error.value = getReadableError(e, "Failed to create pitch")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div ref="containerConfig" class="relative w-full h-full">
        <BaseCard
            ref="cardComponent"
            :type="type"
            class="card w-full h-full border-2"
            :class="{ 
                'border-info': type === 'Idea', 
                'border-secondary': type === 'Opinion' 
            }"
            :style="cardTransform"
        >
            <!-- Overlay Indicators -->
            <div v-if="isSwipingRight" class="absolute top-10 right-8 z-50 pointer-events-none transform rotate-12 border-4 border-success text-success rounded-lg px-4 py-2 text-4xl font-bold uppercase tracking-widest bg-base-100/20 backdrop-blur-sm">
                POST
            </div>
            <div v-if="isSwipingLeft" class="absolute top-10 left-8 z-50 pointer-events-none transform -rotate-12 border-4 border-error text-error rounded-lg px-4 py-2 text-4xl font-bold uppercase tracking-widest bg-base-100/20 backdrop-blur-sm">
                DISCARD
            </div>

            <div class="card-body p-6 flex flex-col h-full relative z-10">
                <!-- Header / Type Toggle -->
                <div class="flex justify-between items-center mb-2">
                    <h2 class="card-title text-2xl font-black">New {{ type }}</h2>
                    <div class="join">
                         <input 
                            class="join-item btn btn-sm" 
                            :class="{ 'btn-info': type === 'Idea' }"
                            type="radio" 
                            name="options" 
                            aria-label="Idea" 
                            :checked="type === 'Idea'"
                            @change="type = 'Idea'"
                         />
                         <input 
                            class="join-item btn btn-sm" 
                            :class="{ 'btn-secondary': type === 'Opinion' }"
                            type="radio" 
                            name="options" 
                            aria-label="Opinion" 
                            :checked="type === 'Opinion'"
                            @change="type = 'Opinion'"
                         />
                    </div>
                </div>

                <!-- Form Fields -->
                <div class="form-control w-full">
                    <label class="label py-1">
                        <span class="label-text font-bold">Title</span>
                    </label>
                    <input 
                        type="text" 
                        v-model="title" 
                        placeholder="What's the big idea?" 
                        class="input input-bordered w-full bg-base-100/50 backdrop-blur-sm"
                        :class="{ 'border-info': type === 'Idea', 'border-secondary': type === 'Opinion' }"
                        maxlength="50" 
                    />
                </div>

                <div class="form-control w-full mt-2 flex-grow flex flex-col">
                    <label class="label py-1">
                        <span class="label-text font-bold">Description</span>
                    </label>
                    <textarea 
                        v-model="description" 
                        class="textarea textarea-bordered w-full flex-grow resize-none leading-relaxed text-base bg-base-100/50 backdrop-blur-sm" 
                        :class="{ 'border-info': type === 'Idea', 'border-secondary': type === 'Opinion' }"
                        placeholder="Tell us more details..."
                    ></textarea>
                </div>

                <!-- Helper / Error -->
                <div class="min-h-[1.5rem] mt-2 text-center">
                    <span v-if="error" class="text-error text-sm font-bold">{{ error }}</span>
                    <span v-else class="text-slate-600 dark:text-white/90 text-xs uppercase tracking-wide font-bold shadow-black/5 drop-shadow-sm">
                        Swipe Right to Post &bull; Left to Cancel
                    </span>
                </div>
            </div>
        </BaseCard>
    </div>
</template>
