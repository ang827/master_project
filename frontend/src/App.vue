<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { ref } from 'vue'

const selectedlocation = ref(null)
const selectedProblemType = ref(null)
onMounted(() => {
  const map = L.map('map').setView([39.9042, 116.4074], 13)

  map.on('click', (event) => {
    L.marker(event.latlng).addTo(map).bindPopup(selectedProblemType.value)
    selectedlocation.value = event.latlng
  })

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
})
</script>

<template>
  <div id="map"></div>
  <div v-if="selectedlocation" class="report-panel">
    <h3>Report Tactile Paving Issue</h3>
    <p>latitude: {{ selectedlocation.lat }}</p>
    <p>longitude: {{ selectedlocation.lng }}</p>
    <label for="problemtype">problem type:</label>
    <select id="problemtype" v-model="selectedProblemType">
      <option>Tactile paving issue</option>
      <option>Blocked tactile paving</option>
      <option>Missing</option>
    </select>
  </div>
</template>

<style>
#map {
  height: 100vh;
  width: 100%;
}

.report-panel {
  position: fixed;
  top: 16px;
  left: 50%;
  z-index: 1000;
  transform: translateX(-50%);
  padding: 12px 16px;
  color: #222;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 20%);
}

.report-panel h3,
.report-panel p {
  margin: 0;
}

.report-panel p {
  margin-top: 6px;
}
</style>
