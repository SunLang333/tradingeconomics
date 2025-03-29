<template>
  <div class="stats-table">
    <h3>YoY Growth Rate Summary Statistics</h3>
    <table>
      <tbody>
        <tr v-for="(value, key) in statsData" :key="key">
          <td>{{ formatLabel(key) }}</td>
          <td>{{ formatNumber(value) }}{{ key !== 'count' ? '%' : '' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'GDPStats',
  props: {
    statsData: {
      type: Object,
      required: true
    }
  },
  setup() {
    const formatNumber = (value) => {
      if (value === undefined || value === null) return 'N/A'
      return Number(value).toFixed(2)
    }

    const formatLabel = (key) => {
      const labels = {
        count: 'Count',
        mean: 'Mean',
        std: 'Standard Deviation',
        min: 'Minimum',
        '25%': '25th Percentile',
        '50%': 'Median',
        '75%': '75th Percentile',
        max: 'Maximum'
      }
      return labels[key] || key
    }

    return { formatNumber, formatLabel }
  }
}
</script>


