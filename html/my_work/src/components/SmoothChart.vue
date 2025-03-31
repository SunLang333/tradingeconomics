<template>
  <div>
    <div v-if="loading">
      <SkeletonLoader />
    </div>
    <div v-else-if="error">
      {{ error }}
    </div>
    <template v-else>
      <GDPChart
        :chart-data="gdpData"
        :country="country"
      />
      <GDPStats
        :stats-data="gdpData.growthSummary"
      />
    </template>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import GDPChart from './GDPChart.vue'
import GDPStats from './GDPStats.vue'
//import GDPExtremes from './GDPExtremes.vue'

export default {
  name: 'SmoothChart',
  components: {
    GDPChart,
    GDPStats,
    //GDPExtremes
  },
  props: {
    country: {
      type: String,
      required: true,
      validator: (value) => {
        return ['mexico', 'new zealand', 'sweden', 'thailand'].includes(value.toLowerCase())
      }
    },
    initDate: {
      type: String,
      default: '2015-01-01'
    }
  },
  setup(props) {
    const loading = ref(true)
    const error = ref(null)
    const gdpData = ref(null)

    const fetchGDPData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/gdp/${props.country}?init_date=${props.initDate}`)
        if (!response.ok) throw new Error('Network response was not ok')

        const rawData = await response.json()
        const parsedData = JSON.parse(rawData)

        gdpData.value = {
          dates: parsedData.data.map(item => new Date(item.DateTime)),
          values: parsedData.data.map(item => item.Value),
          smoothedDates: parsedData.X_smooth_tolist.map(days => {
            const startDate = new Date(parsedData.data[0].DateTime)
            return new Date(startDate.getTime() + days[0] * 24 * 60 * 60 * 1000)
          }),
          smoothedValues: parsedData.y_smooth,
          growthSummary: parsedData.yoy_growth_summary
        }

        loading.value = false
      } catch (err) {
        error.value = 'Error fetching GDP data: ' + err.message
        loading.value = false
        console.error('Data fetching error:', err)
      }
    }

    watch(() => props.country, () => {
      loading.value = true
      fetchGDPData()
    })

    onMounted(() => {
      fetchGDPData()
    })

    return {
      loading,
      error,
      gdpData
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  margin: 20px 0;
}

.stats-table {
  margin: 20px auto;
  max-width: 600px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stats-table h3 {
  color: #333;
  margin-bottom: 15px;
  text-align: center;
}

.stats-table table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.stats-table td {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

.stats-table td:first-child {
  font-weight: 500;
  color: #666;
}

.stats-table td:last-child {
  text-align: right;
}

.growth-extremes {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
}

.growth-extremes p {
  margin: 10px 0;
  color: #333;
}
</style>
