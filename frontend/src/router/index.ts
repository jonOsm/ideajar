import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import SwipePage from '../views/SwipePage.vue'
import { OpenAPI } from '../client/core/OpenAPI'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: LoginPage
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterPage
        },
        {
            path: '/',
            name: 'home',
            component: SwipePage,
            meta: { requiresAuth: true }
        }
    ]
})

router.beforeEach((to, _from, next) => {
    const token = localStorage.getItem('access_token')

    if (token) {
        OpenAPI.TOKEN = token
    }

    if (to.meta.requiresAuth && !token) {
        next({ name: 'login' })
    } else {
        next()
    }
})

export default router
