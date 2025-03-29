<template>
  <div>
    <select v-model="selectedCountry">
      <option value="mexico">
        Mexico
      </option>
      <option value="new zealand">
        New Zealand
      </option>
      <option value="sweden">
        Sweden
      </option>
      <option value="thailand">
        Thailand
      </option>
    </select>

    <SmoothChart
      :country="selectedCountry"
      init-date="2015-01-01"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SmoothChart from '@/components/SmoothChart.vue';

const selectedCountry = ref('mexico')

</script>
