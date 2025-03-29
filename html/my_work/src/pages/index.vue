<template>
  <v-app id="inspire">
    <v-app-bar
      class="px-3"
      density="compact"
      flat
    >
      <v-avatar
        class="hidden-md-and-up"
        color="grey-darken-1"
        size="32"
      />
      <v-spacer />
      <v-tabs
        align-tabs="center"
        color="grey-darken-2"
      >
        <v-tab
          v-for="link in links"
          :key="link"
          :text="link"
        />
      </v-tabs>
      <v-spacer />
      <v-avatar
        class="hidden-sm-and-down"
        color="grey-darken-1"
        size="32"
        image="https://avatars.githubusercontent.com/u/75293447?v=4"
      />
    </v-app-bar>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-row>
          <v-col
            cols="12"
            md="2"
          >
            <ListComponent
              v-model:selected="selectedCountry"
              :items="countries"
            />
          </v-col>

          <v-col
            cols="12"
            md="8"
          >
            <v-sheet
              min-height="70vh"
              rounded="lg"
              class="pa-4"
            >
              <SmoothChart
                :key="`${selectedCountry}-${selectedDate}`"
                :country="selectedCountry"
                :init-date="selectedDate"
              />
            </v-sheet>
          </v-col>

          <v-col
            cols="12"
            md="2"
          >
            <v-sheet
              min-height="268"
              rounded="lg"
            >
              <v-date-picker
                v-model="selectedDate"
                :min="minDate"
                :max="maxDate"
                :date-adapter="dateAdapter"
                @update:model-value="handleDateChange"
              />
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ListComponent from '@/components/ListComponent.vue'
import SmoothChart from '@/components/SmoothChart.vue'

const links = ['Dashboard']

const countries = [
  'mexico',
  'new zealand',
  'sweden',
  'thailand'
]

const selectedCountry = ref('mexico')
const selectedDate = ref('2015-01-01') // Default date
const minDate = '2010-01-01' // Optional: Set minimum allowed date
const maxDate = new Date().toISOString().split('T')[0] // Today's date as max

// Format date to YYYY-MM-DD without timezone adjustment
const formatDate = (date) => {
  if (!date) return null
  if (typeof date === 'string' && date.match(/^\d{4}-\d{2}-\d{2}$/)) return date

  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// Handle date change
const handleDateChange = (date) => {
  const formattedDate = formatDate(date)
  if (formattedDate) {
    selectedDate.value = formattedDate
  }
}

// Add watch effect to trigger component update
watch([selectedDate, selectedCountry], () => {
  // The SmoothChart component will automatically re-fetch data
  // when its props (init-date or country) change
}, { immediate: true })

// Watch for changes with immediate effect
watch([selectedDate, selectedCountry], (newValues) => {
  console.log('Date or country changed:', newValues)
}, { immediate: true })

// Optional: Configure date adapter for better localization
const dateAdapter = {
  locale: 'en-US',
  formats: {
    dateA11y: 'YYYY-MM-DD'
  }
}
</script>
