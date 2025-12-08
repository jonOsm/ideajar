import { computed, ref, watch, onUnmounted, type Ref } from 'vue'
import { usePointerSwipe } from '@vueuse/core'

interface SwipeOptions {
    threshold?: number
    onSwipeRight?: () => void
    onSwipeLeft?: () => void
}

const globalSwipeX = ref(0) // Shared state for global effects

export function useSwipeState() {
    return { globalSwipeX }
}

export function useCardSwipe(target: Ref<HTMLElement | null>, options: SwipeOptions = {}) {
    const { threshold = 150, onSwipeRight, onSwipeLeft } = options

    // State
    const isExiting = ref(false)
    const exitDirection = ref(0)
    const currentDistanceX = ref(0)

    const { distanceX, distanceY, isSwiping } = usePointerSwipe(target)

    // Sync distance only while swiping to capture the last valid value
    watch(distanceX, (newVal) => {
        if (isSwiping.value && !isExiting.value) {
            currentDistanceX.value = -newVal
            // Update global state only if we are actively swiping
            globalSwipeX.value = -newVal
        }
    })

    // Handle Swipe Release
    watch(isSwiping, (newSwiping, oldSwiping) => {
        if (oldSwiping && !newSwiping) {
            const x = currentDistanceX.value

            if (Math.abs(x) > threshold) {
                // Determine direction and commit to exit
                const dir = x > 0 ? 1 : -1
                isExiting.value = true
                exitDirection.value = dir

                // Maximize global glow for exit
                globalSwipeX.value = dir * 1000

                // Trigger callbacks after animation
                setTimeout(() => {
                    if (dir === 1) onSwipeRight?.()
                    else onSwipeLeft?.()

                    // Reset state
                    isExiting.value = false
                    exitDirection.value = 0
                    currentDistanceX.value = 0
                    // We also reset global swipe X here, but checking if WE set it? 
                    // It's safe to reset if we were the ones exiting.
                    globalSwipeX.value = 0
                }, 200)
            } else {
                // Snap back
                currentDistanceX.value = 0
                globalSwipeX.value = 0
            }
        }
    })

    // Safety cleanup
    onUnmounted(() => {
        // If this component was controlling the glow, reset it.
        // Simple heuristic: if the glow matches our direction or if we were exiting.
        // Or just reset it. Since unmounting usually happens after interaction or page leave.
        if (isExiting.value || Math.abs(currentDistanceX.value) > 0) {
            globalSwipeX.value = 0
        }
    })

    const visualOffset = computed(() => {
        // During exit, keep the offset large so overlays (YES/NOPE) stay visible
        if (isExiting.value) return { x: exitDirection.value * 1000, y: 0 }

        // During swipe, use tracked distance; otherwise reset
        const x = isSwiping.value ? currentDistanceX.value : 0
        const y = isSwiping.value ? -distanceY.value : 0
        return { x, y }
    })

    const cardTransform = computed(() => {
        const { x, y } = visualOffset.value
        const isExit = isExiting.value

        // Rotation: Dramatic on exit, subtle during swipe
        const rotate = isExit ? exitDirection.value * 30 : x * 0.05

        let transition = 'transform 0.3s ease-out'
        let opacity = 1
        let cursor = 'grab'

        if (isExit) {
            transition = 'transform 0.2s ease-out, opacity 0.2s ease-out'
            opacity = 0
            cursor = 'grabbing'
        } else if (isSwiping.value) {
            transition = 'none'
            opacity = Math.max(0.5, 1 - Math.abs(x) / 1000)
            cursor = 'grabbing'
        }

        return {
            transform: `translate(${x}px, ${y}px) rotate(${rotate}deg)`,
            transition,
            opacity,
            cursor
        }
    })

    // Expose simplified state for UI
    const isSwipingRight = computed(() => visualOffset.value.x > 20)
    const isSwipingLeft = computed(() => visualOffset.value.x < -20)

    return {
        isSwiping,
        cardTransform,
        isSwipingRight,
        isSwipingLeft,
        visualOffset
    }
}
