<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

onMounted(() => {
  const map = L.map('map').setView([39.9042, 116.4074], 13)

  map.on('click', (event) => {
    L.marker(event.latlng).addTo(map)
  })

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  L.marker([39.9042, 116.4074]).addTo(map).bindPopup('Blocked tactile paving')
})
</script>

<template>
  <div id="map"></div>
</template>

<style>
#map {
  height: 100vh;
  width: 100%;
}
</style>
