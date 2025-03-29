<template>
  <div class="growth-extremes">
    <p>
      <strong>Highest YoY Growth:</strong>
      {{ formatNumber(extremes.highest_growth.value) }}%
      ({{ extremes.highest_growth.year }})
    </p>
    <p>
      <strong>Lowest YoY Growth:</strong>
      {{ formatNumber(extremes.lowest_growth.value) }}%
      ({{ extremes.lowest_growth.year }})
    </p>
  </div>
</template>

<script>
export default {
  name: 'GDPExtremes',
  props: {
    extremes: {
      type: Object,
      required: true
    }
  },
  setup() {
    const formatNumber = (value) => {
      if (value === undefined || value === null) return 'N/A'
      return Number(value).toFixed(2)
    }

    return { formatNumber }
  }
}
</script>


