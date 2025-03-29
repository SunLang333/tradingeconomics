<template>
  <v-app id="inspire">
    <v-app-bar class="px-3" density="compact" flat>
      <v-avatar class="hidden-md-and-up" color="grey-darken-1" size="32" />
      <v-spacer />
      <v-tabs align-tabs="center" color="grey-darken-2">
        <v-tab v-for="link in links" :key="link" :text="link" />
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
          <v-col cols="12" md="2">
            <ListComponent
              :items="countries"
              v-model:selected="selectedCountry"
            />
          </v-col>

          <v-col cols="12" md="8">
            <v-sheet min-height="70vh" rounded="lg" class="pa-4">
              <SmoothChart
                :country="selectedCountry"
                init-date="2015-01-01"
              />
            </v-sheet>
          </v-col>

          <v-col cols="12" md="2">
            <v-sheet min-height="268" rounded="lg">
              <v-date-picker />
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
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
</script>
