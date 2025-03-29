<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Chart, CategoryScale, TimeScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, LineController } from 'chart.js'
import 'chartjs-adapter-date-fns'
import { enUS } from 'date-fns/locale'

Chart.register(CategoryScale, TimeScale, LinearScale, PointElement, LineElement, LineController, Title, Tooltip, Legend)

export default {
  name: 'GDPChart',
  props: {
    chartData: {
      type: Object,
      required: true
    },
    country: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chart = null

    const createChart = () => {
      if (!chartCanvas.value) return

      const ctx = chartCanvas.value.getContext('2d')
      if (chart) chart.destroy()

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'Actual GDP',
              data: props.chartData.dates.map((date, i) => ({
                x: date,
                y: props.chartData.values[i]
              })),
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              pointRadius: 3
            },
            {
              label: 'Smoothed GDP Trend',
              data: props.chartData.smoothedDates.map((date, i) => ({
                x: date,
                y: props.chartData.smoothedValues[i]
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
              text: `${props.country.charAt(0).toUpperCase() + props.country.slice(1)} GDP - Actual vs Smoothed Trend`
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
              }
            }
          }
        }
      })
    }

    watch(() => props.chartData, createChart, { deep: true })
    watch(() => props.country, createChart)

    onMounted(createChart)
    onUnmounted(() => {
      if (chart) chart.destroy()
    })

    return { chartCanvas }
  }
}
</script>

