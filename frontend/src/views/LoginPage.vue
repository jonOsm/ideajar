<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { AuthService } from '../client'
import { OpenAPI } from '../client/core/OpenAPI'

import { getReadableError, ErrorMessages } from '../constants/errors'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const successMessage = ref('')

// Check for registration success query param
if (router.currentRoute.value.query.registered) {
    successMessage.value = 'Registration successful! Please sign in.'
}

const handleLogin = async () => {
    loading.value = true
    error.value = ''
    successMessage.value = ''
    
    // Simple client-side validation to save API calls
    if (password.value.length < 1) {
         error.value = 'Please enter your password.'
         loading.value = false
         return
    }

    try {
        const login = AuthService.authJwtLoginApiAuthJwtLoginPost
        const response = await login({
            username: email.value,
            password: password.value
        })
        localStorage.setItem('access_token', response.access_token)
        OpenAPI.TOKEN = response.access_token
        router.push('/')
    } catch (e: any) {
        error.value = getReadableError(e, ErrorMessages.DEFAULT_LOGIN)
        console.error(e)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen flex items-start sm:items-center justify-center bg-base-200 p-0 sm:p-4">
        <div class="card w-full sm:max-w-sm shadow-none sm:shadow-2xl bg-base-100 h-screen sm:h-auto rounded-none sm:rounded-2xl">
            <div class="card-body justify-center">
                <h2 class="card-title justify-center text-3xl font-extrabold pb-8 pt-4">Sign in to IdeaJar</h2>
                
                <div v-if="successMessage" class="alert alert-success shadow-lg mb-4">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>{{ successMessage }}</span>
                    </div>
                </div>

                <form class="space-y-6" @submit.prevent="handleLogin">
                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text text-base font-bold">Email address</span>
                        </label>
                        <input type="email" required v-model="email" placeholder="email@example.com" class="input input-bordered input-lg w-full" />
                    </div>
                    
                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text text-base font-bold">Password</span>
                        </label>
                        <input type="password" required v-model="password" placeholder="********" class="input input-bordered input-lg w-full" />
                    </div>

                    <div v-if="error" class="alert alert-error shadow-lg">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            <span>{{ error }}</span>
                        </div>
                    </div>

                    <div class="form-control mt-8">
                        <button type="submit" class="btn btn-primary btn-lg w-full" :class="{ 'loading': loading }" :disabled="loading">
                            {{ loading ? 'Signing in...' : 'Sign in' }}
                        </button>
                    </div>
                    
                    <div class="text-center mt-6">
                        <router-link to="/register" class="link link-hover text-base p-2">
                            Don't have an account? Sign up
                        </router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
