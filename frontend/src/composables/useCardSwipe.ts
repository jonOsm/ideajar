import { computed, ref, watch, type Ref } from 'vue'
import { usePointerSwipe } from '@vueuse/core'

interface SwipeOptions {
    threshold?: number
    onSwipeRight?: () => void
    onSwipeLeft?: () => void
}

export function useCardSwipe(target: Ref<HTMLElement | null>, options: SwipeOptions = {}) {
    const { threshold = 150, onSwipeRight, onSwipeLeft } = options

    // State
    const isExiting = ref(false)
    const exitDirection = ref(0) // 1 for right, -1 for left
    const currentDistanceX = ref(0) // Manually track distance to avoid reset issues

    const { distanceX, distanceY, isSwiping } = usePointerSwipe(target, {
        // We handle logic in watcher instead of onSwipeEnd to ensure we catch state changes
        // before values reset or in sync with them.
    })

    // Sync distance only while swiping to capture the last valid value
    watch(distanceX, (newVal) => {
        if (isSwiping.value && !isExiting.value) {
            // VueUse: Positive distanceX is LEFT. We invert to match screen coordinates (Right = +).
            currentDistanceX.value = -newVal
        }
    })

    // Handle Swipe End
    watch(isSwiping, (newSwiping, oldSwiping) => {
        if (oldSwiping && !newSwiping) {
            // User released
            const x = currentDistanceX.value

            if (Math.abs(x) > threshold) {
                // Commit to exit
                isExiting.value = true
                exitDirection.value = x > 0 ? 1 : -1

                // Trigger callbacks after animation
                setTimeout(() => {
                    if (exitDirection.value === 1) {
                        onSwipeRight?.()
                    } else {
                        onSwipeLeft?.()
                    }

                    // Cleanup / Reset
                    setTimeout(() => {
                        isExiting.value = false
                        exitDirection.value = 0
                        currentDistanceX.value = 0
                    }, 50)
                }, 200) // 200ms Animation duration
            } else {
                // Reset (snap back)
                currentDistanceX.value = 0
            }
        }
    })

    const visualOffset = computed(() => {
        if (isExiting.value) {
            return { x: exitDirection.value * 1000, y: 0 }
        }

        // While swiping, use the current tracked distance
        if (isSwiping.value) {
            return { x: currentDistanceX.value, y: -distanceY.value }
        }

        return { x: 0, y: 0 }
    })

    const cardTransform = computed(() => {
        // 1. Exit Animation (Highest Priority)
        if (isExiting.value) {
            const x = exitDirection.value * 1200 // Fly off screen
            const rotate = exitDirection.value * 30 // Dramatic rotation
            return {
                transform: `translate(${x}px, 0px) rotate(${rotate}deg)`,
                transition: 'transform 0.2s ease-out, opacity 0.2s ease-out', // Snappier exit
                opacity: 0,
                cursor: 'grabbing'
            }
        }

        // 2. Active Swipe
        if (isSwiping.value) {
            const x = currentDistanceX.value
            const y = -distanceY.value
            const rotate = x * 0.05

            return {
                transform: `translate(${x}px, ${y}px) rotate(${rotate}deg)`,
                transition: 'none', // No transition while dragging
                opacity: Math.max(0.5, 1 - Math.abs(x) / 1000),
                cursor: 'grabbing'
            }
        }

        // 3. Idle / Snap Back
        return {
            transform: 'translate(0px, 0px) rotate(0deg)',
            transition: 'transform 0.3s ease-out', // Smooth snap back
            opacity: 1,
            cursor: 'grab'
        }
    })

    // Expose simplified state
    const isSwipingRight = computed(() => currentDistanceX.value > 20)
    const isSwipingLeft = computed(() => currentDistanceX.value < -20)

    return {
        isSwiping,
        cardTransform,
        isSwipingRight,
        isSwipingLeft,
        visualOffset
    }
}
