<template>
  <v-card
    class="mx-auto stats-card"
    max-width="400"
    hover
    elevation="2"
  >
    <v-card-item>
      <v-card-title>
        GDP Growth Statistics
      </v-card-title>
      <v-card-subtitle>
        Year over Year Growth Rate Analysis
      </v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <table class="stats-table">
        <tbody>
          <tr>
            <td>Highest YoY Growth</td>
            <td>{{ formatNumber(statsData.highest_growth?.value) }}% ({{ statsData.highest_growth?.year }})</td>
          </tr>
          <tr>
            <td>Lowest YoY Growth</td>
            <td>{{ formatNumber(statsData.lowest_growth?.value) }}% ({{ statsData.lowest_growth?.year }})</td>
          </tr>
          <tr
            v-for="(value, key) in filteredStats(statsData)"
            :key="key"
          >
            <td>{{ formatLabel(key) }}</td>
            <td>{{ formatNumber(value) }}{{ key !== 'count' ? '%' : '' }}</td>
          </tr>
        </tbody>
      </table>
    </v-card-text>
  </v-card>
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

    const filteredStats = (stats) => {
      const {highest_growth, lowest_growth, ...rest} = stats
      return rest
    }

    return {
      formatNumber,
      formatLabel,
      filteredStats
    }
  }
}
</script>

<style scoped>
.stats-card {
  background-color: #828282;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
}

.stats-table td {
  padding: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.stats-table td:first-child {
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
}

.stats-table td:last-child {
  text-align: right;
}
</style>
