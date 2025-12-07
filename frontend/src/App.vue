<script setup lang="ts">
import { OpenAPI } from './client/core/OpenAPI'

// Global config
OpenAPI.BASE = '' 
</script>

<template>
  <router-view />
</template>

<style>
body {
    background-color: #f9fafb;
}
</style>
