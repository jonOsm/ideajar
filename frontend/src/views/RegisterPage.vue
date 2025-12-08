<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { AuthService } from '../client'

import { getReadableError, ErrorMessages } from '../constants/errors'
import { ValidationRules } from '../constants/validation'

const router = useRouter()
const email = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
    loading.value = true
    error.value = ''
    
    // Client-side validation
    if (password.value.length < ValidationRules.MIN_PASSWORD_LENGTH) {
        error.value = ErrorMessages.REGISTER_INVALID_PASSWORD
        loading.value = false
        return
    }

    if (username.value.length < ValidationRules.USERNAME_MIN_LENGTH || username.value.length > ValidationRules.USERNAME_MAX_LENGTH) {
        error.value = ErrorMessages.REGISTER_INVALID_USERNAME_LENGTH
        loading.value = false
        return
    }

    if (!ValidationRules.USERNAME_PATTERN.test(username.value)) {
        error.value = ErrorMessages.REGISTER_INVALID_USERNAME_FORMAT
        loading.value = false
        return
    }
    
    try {
        const register = AuthService.registerRegisterApiAuthRegisterPost
        await register({
            email: email.value,
            password: password.value,
            username: username.value,
            is_active: true,
            is_superuser: false,
            is_verified: false
        })
        // Redirect to login (or auto login, but let's keep it simple)
        // Redirect to login with success indicator
        router.push({ path: '/login', query: { registered: 'true' } })
    } catch (e: any) {
        error.value = getReadableError(e, ErrorMessages.DEFAULT_REGISTER)
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
                <h2 class="card-title justify-center text-3xl font-extrabold pb-8 pt-4">Create Account</h2>
                
                <form class="space-y-6" @submit.prevent="handleRegister">
                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text text-base font-bold">Username <small class="text-sm font-normal text-base-content/60 ml-2">(Alphanumeric and underscores)</small></span>
                        </label>
                        <input type="text" required v-model="username" placeholder="cool_user" class="input input-bordered input-lg w-full" />
                    </div>

                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text text-base font-bold">Email address</span>
                        </label>
                        <input type="email" required v-model="email" placeholder="email@example.com" class="input input-bordered input-lg w-full" />
                    </div>
                    
                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text text-base font-bold">Password <small class="text-sm font-normal text-base-content/60 ml-2">(Minimum {{ ValidationRules.MIN_PASSWORD_LENGTH }} chars)</small></span>
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
                             {{ loading ? 'Registering...' : 'Sign Up' }}
                        </button>
                    </div>
                    
                    <div class="text-center mt-6">
                        <router-link to="/login" class="link link-hover text-base p-2">
                            Already have an account? Sign in
                        </router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
