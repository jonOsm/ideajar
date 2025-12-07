import { computed, type Ref } from 'vue'
import { usePointerSwipe } from '@vueuse/core'

interface SwipeOptions {
    threshold?: number
    onSwipeRight?: () => void
    onSwipeLeft?: () => void
}

export function useCardSwipe(target: Ref<HTMLElement | null>, options: SwipeOptions = {}) {
    const { threshold = 150, onSwipeRight, onSwipeLeft } = options

    const { distanceX, distanceY, isSwiping } = usePointerSwipe(target, {
        onSwipeEnd: () => {
            // VueUse: Positive distanceX is LEFT. We want Positive = RIGHT.
            // So we invert it.
            const x = -distanceX.value

            if (Math.abs(x) > threshold) {
                if (x > 0) {
                    onSwipeRight?.()
                } else {
                    onSwipeLeft?.()
                }
            }
        },
    })

    const visualOffset = computed(() => {
        if (!isSwiping.value) {
            return { x: 0, y: 0 }
        }

        // Invert distanceX so positive = right (following the cursor/finger)
        return {
            x: -distanceX.value,
            y: -distanceY.value
        }
    })

    const cardTransform = computed(() => {
        if (!isSwiping.value) {
            return {
                transform: 'translate(0px, 0px) rotate(0deg)',
                transition: 'transform 0.3s ease-out',
                opacity: 1,
                cursor: 'grab'
            }
        }

        const { x, y } = visualOffset.value
        const rotate = x * 0.05 // Slight rotation based on X movement

        return {
            transform: `translate(${x}px, ${y}px) rotate(${rotate}deg)`,
            transition: 'none',
            opacity: Math.max(0.5, 1 - Math.abs(x) / 1000),
            cursor: 'grabbing'
        }
    })

    // Expose simplified state
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
