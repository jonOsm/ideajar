<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { AuthService } from '../client'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
    loading.value = true
    error.value = ''
    try {
        const register = AuthService.registerRegisterApiAuthRegisterPost
        await register({
            email: email.value,
            password: password.value,
            is_active: true,
            is_superuser: false,
            is_verified: false
        })
        // Redirect to login (or auto login, but let's keep it simple)
        router.push('/login')
    } catch (e: any) {
        error.value = 'Registration failed. Try a different email.'
        console.error(e)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create Account</h2>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="email-address" class="sr-only">Email address</label>
                        <input id="email-address" name="email" type="email" required v-model="email"
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-violet-500 focus:border-violet-500 focus:z-10 sm:text-sm"
                            placeholder="Email address">
                    </div>
                    <div>
                        <label for="password" class="sr-only">Password</label>
                        <input id="password" name="password" type="password" required v-model="password"
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-violet-500 focus:border-violet-500 focus:z-10 sm:text-sm"
                            placeholder="Password">
                    </div>
                </div>

                <div v-if="error" class="text-red-500 text-sm text-center">{{ error }}</div>

                <div>
                    <button type="submit" :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-violet-600 hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500 disabled:opacity-50">
                        <span v-if="loading">Registering...</span>
                        <span v-else>Sign Up</span>
                    </button>
                </div>
                
                <div class="text-center text-sm">
                    <router-link to="/login" class="font-medium text-violet-600 hover:text-violet-500">
                        Already have an account? Sign in
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>
