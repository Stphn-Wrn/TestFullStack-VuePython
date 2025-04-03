<template>
    <div class="card border rounded-lg p-4 shadow hover:shadow-lg transition">
      <div class="flex justify-between items-start">
        <h3 class="text-xl font-bold">{{ campaign.name }}</h3>
        <span 
          class="i-mdi-power text-2xl cursor-pointer" 
          :class="campaign.active ? 'text-green-500' : 'text-red-500'"
          @click="toggleStatus(campaign.id)"
        />
      </div>
      <p class="text-gray-600 mt-2">{{ campaign.description }}</p>
      <div class="mt-4 flex justify-between text-sm">
        <span>Budget: {{ campaign.budget }}$</span>
        <span>Du {{ formatDate(campaign.start_date) }} au {{ formatDate(campaign.end_date) }}</span>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps(['campaign'])
  const emit = defineEmits(['toggle'])
  
  const toggleStatus = (id) => emit('toggle', id)
  </script>