<template>
  <div class="chart-container">
    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="gdpData">
      <!-- Add your chart rendering logic here -->
      {{ gdpData }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SmoothChart',
  data() {
    return {
      gdpData: null,
      loading: true,
      error: null
    }
  },
  async created() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/gdp/mexico?init_date=2015-01-01')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      this.gdpData = await response.json()
    } catch (err) {
      this.error = 'Error fetching GDP data: ' + err.message
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.chart-container {
  padding: 20px;
}
</style>
