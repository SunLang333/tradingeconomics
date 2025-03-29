<template>
  <v-card
    class="mx-auto"
    max-width="300"
  >
    <v-list>
      <v-list-subheader>Select Country</v-list-subheader>
      <v-list-item
        v-for="item in items"
        :key="item"
        :value="item"
        :title="item.charAt(0).toUpperCase() + item.slice(1)"
        :active="selected === item"
        @click="$emit('update:selected', item)"
      >
        <template #prepend>
          <v-icon
            :color="selected === item ? 'primary' : undefined"
            icon="mdi-chart-line"
          />
        </template>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true
  },
  selected: {
    type: String,
    required: true
  }
})

defineEmits(['update:selected'])
</script>
