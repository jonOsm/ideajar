<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useSwipeState } from '../composables/useCardSwipe'

const { globalSwipeX } = useSwipeState()
const canvasRef = ref<HTMLCanvasElement | null>(null)

interface Particle {
    x: number
    y: number
    vx: number
    vy: number
    color: string
    size: number
    life: number
    maxLife: number
}

let particles: Particle[] = []
let animationFrameId: number | null = null

const updateCanvasSize = () => {
    if (canvasRef.value) {
        canvasRef.value.width = window.innerWidth
        canvasRef.value.height = window.innerHeight
    }
}

const spawnParticles = (side: 'left' | 'right') => {
    const count = 150 // Higher density
    // Start slightly off-screen
    const xBase = side === 'left' ? -50 : window.innerWidth + 50
    const color = side === 'left' ? '#f43f5e' : '#10b981' 
    
    const isDesktop = window.innerWidth > 768

    for (let i = 0; i < count; i++) {
        // "Volcano" origin: tightly clustered at vertical center
        const y = window.innerHeight / 2 + (Math.random() - 0.5) * 40
        
        // Eruption velocity: Fast and fanned out
        const speed = Math.random() * 20 + 15 
        
        const angleBase = side === 'left' ? 0 : Math.PI
        // Tighter fan spread on mobile, wider on desktop
        const spreadFactor = isDesktop ? 1.5 : 0.8
        const angleSpread = (Math.random() - 0.5) * spreadFactor
        const angle = angleBase + angleSpread

        particles.push({
            x: xBase,
            y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            color: color,
            size: Math.random() * 3 + 1, // Smaller particles (1-4px)
            life: 1,
            maxLife: 1
        })
    }
    
    if (!animationFrameId) {
        loop()
    }
}

const loop = () => {
    const canvas = canvasRef.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Update and Draw
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i]
        if (!p) continue
        
        // Add turbulence / noise
        p.vx += (Math.random() - 0.5) * 0.5
        p.vy += (Math.random() - 0.5) * 0.5
        
        p.x += p.vx
        p.y += p.vy
        p.vx *= 0.95 // Drag
        p.vy *= 0.95 
        p.life -= 0.015 // Decay

        if (p.life <= 0) {
            particles.splice(i, 1)
        } else {
            ctx.globalAlpha = p.life
            ctx.fillStyle = p.color
            ctx.beginPath()
             // Use circles
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
            ctx.fill()
        }
    }

    if (particles.length > 0) {
        animationFrameId = requestAnimationFrame(loop)
    } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        animationFrameId = null
    }
}

// Watch for the "Commit" signal
watch(globalSwipeX, (newVal) => {
    // Threshold from useCardSwipe is +/- 1000 for EXIT
    if (newVal <= -1000) {
        spawnParticles('left') // Swiped Left (Red)
    } else if (newVal >= 1000) {
        spawnParticles('right') // Swiped Right (Green)
    }
})

onMounted(() => {
    window.addEventListener('resize', updateCanvasSize)
    updateCanvasSize()
})

onUnmounted(() => {
    window.removeEventListener('resize', updateCanvasSize)
    if (animationFrameId) cancelAnimationFrame(animationFrameId)
})
</script>

<template>
    <canvas 
        ref="canvasRef" 
        class="fixed inset-0 pointer-events-none z-[100]" 
        style="width: 100%; height: 100%;"
    ></canvas>
</template>
