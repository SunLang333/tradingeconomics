<template>
  <div class="chart-container">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <canvas v-else ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import {
  Chart,
  CategoryScale,
  TimeScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  LineController
} from 'chart.js'
import 'chartjs-adapter-date-fns'
import { enUS } from 'date-fns/locale'

// Register required components
Chart.register(
  CategoryScale,
  TimeScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'SmoothChart',
  setup() {
    const loading = ref(true)
    const error = ref(null)
    const gdpData = ref(null)
    const chartCanvas = ref(null)
    let chart = null

    const createChart = async () => {
      if (!gdpData.value) return

      await nextTick()

      if (!chartCanvas.value) {
        error.value = 'Canvas element not found'
        return
      }

      try {
        const ctx = chartCanvas.value.getContext('2d')
        if (!ctx) {
          error.value = 'Failed to get canvas context'
          return
        }

        if (chart) chart.destroy()

        chart = new Chart(ctx, {
          type: 'line',
          data: {
            datasets: [
              {
                label: 'Actual GDP',
                data: gdpData.value.dates.map((date, i) => ({
                  x: date,
                  y: gdpData.value.values[i]
                })),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                pointRadius: 3
              },
              {
                label: 'Smoothed GDP Trend',
                data: gdpData.value.smoothedDates.map((date, i) => ({
                  x: date,
                  y: gdpData.value.smoothedValues[i]
                })),
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                borderWidth: 2,
                pointRadius: 0
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: {
                display: true,
                text: 'Mexico GDP - Actual vs Smoothed Trend'
              },
              tooltip: {
                mode: 'index',
                intersect: false
              }
            },
            scales: {
              x: {
                type: 'time',
                time: {
                  unit: 'quarter',
                  displayFormats: {
                    quarter: 'QQQ yyyy'
                  }
                },
                adapters: {
                  date: {
                    locale: enUS
                  }
                },
                title: {
                  display: true,
                  text: 'Date'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'GDP Value'
                }
              }
            }
          }
        })
      } catch (err) {
        error.value = `Chart creation failed: ${err.message}`
        console.error('Chart creation error:', err)
      }
    }

    const fetchGDPData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/gdp/mexico?init_date=2015-01-01')
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
        await createChart()
      } catch (err) {
        error.value = 'Error fetching GDP data: ' + err.message
        loading.value = false
        console.error('Data fetching error:', err)
      }
    }

    onMounted(() => {
      fetchGDPData()
    })

    onUnmounted(() => {
      if (chart) chart.destroy()
    })

    return {
      loading,
      error,
      gdpData,
      chartCanvas
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
</style>
