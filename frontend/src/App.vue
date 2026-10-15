<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { ref } from 'vue'
import { useFetch } from '@vueuse/core'

const selectedlocation = ref(null)
const selectedReport = ref(null)
const selectedProblemType = ref(null)
let temporaryMarker = null
let map = null
const description = ref('')
const { data: serverReports, execute: fetchReports } = useFetch(
  'https://pack-pendant-conclusions-summary.trycloudflare.com/api/reports/',
  {
    immediate: false,
  },
)
  .get()
  .json()

function addreportmarker(report) {
  L.marker([report.latitude, report.longitude], {
    title: 'Report:${report.type}',
  })
    .addTo(map)
    .on('click', () => {
      selectedReport.value = report
    })
}

//增添定位函数
function useCurrentLocation() {
  navigator.geolocation.getCurrentPosition((position) => {
    const location = L.latLng(position.coords.latitude, position.coords.longitude)
    map.setView(location, 17)

    if (temporaryMarker === null) {
      temporaryMarker = L.marker(location).addTo(map)
    } else {
      temporaryMarker.setLatLng(location)
    }
    selectedlocation.value = location
  })
}
async function submitreport() {
  //更改为向Django后端发送报告数据
  if (!selectedlocation.value) {
    return
  }
  try {
    const response = await fetch(
      'https://pack-pendant-conclusions-summary.trycloudflare.com/api/reports/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          latitude: selectedlocation.value.lat,
          longitude: selectedlocation.value.lng,
          type: selectedProblemType.value,
          description: description.value,
        }),
      },
    )

    if (!response.ok) {
      throw new Error(`Failed to submit report: ${response.status}`)
    }

    const savedReport = await response.json()
    addreportmarker(savedReport)

    map.removeLayer(temporaryMarker)
    temporaryMarker = null
    selectedlocation.value = null
    description.value = ''
  } catch (error) {
    console.error('Failed to submit report:', error)
  }
}

function cancelreport() {
  if (temporaryMarker) {
    map.removeLayer(temporaryMarker)
    temporaryMarker = null
  }
  selectedlocation.value = null
  description.value = ''
}
onMounted(async () => {
  map = L.map('map').setView([39.9042, 116.4074], 13)
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
  //从读取localstorge的报告改为从后端获取报告
  await fetchReports()
  serverReports.value.forEach((report) => {
    addreportmarker(report)
  })

  map.on('click', (event) => {
    selectedReport.value = null
    if (temporaryMarker === null) {
      temporaryMarker = L.marker(event.latlng).addTo(map)
    } else {
      temporaryMarker.setLatLng(event.latlng)
    }
    selectedlocation.value = event.latlng
  })
})
</script>

<template>
  <div id="map"></div>
  <section v-if="selectedReport" class="report-detail" aria-label="report detail title">
    <h3 id="report-detail-title">Report Details</h3>
    <p>peoblem type: {{ selectedReport.type }}</p>
    <p>description: {{ selectedReport.description }}</p>
    <p>reported at: {{ new Date(selectedReport.createdAt).toLocaleString() }}</p>
    <p>location: {{ selectedReport.latitude }}, {{ selectedReport.longitude }}</p>
    <button type="button" @click="selectedReport = null">Close</button>
  </section>

  <button type="button" @click="useCurrentLocation">Use My Location</button>

  <div v-if="selectedlocation && !selectedReport" class="report-panel">
    <h3>Report Tactile Paving Issue</h3>
    <p>latitude: {{ selectedlocation.lat }}</p>
    <p>longitude: {{ selectedlocation.lng }}</p>
    <label for="problemtype">problem type:</label>
    <select id="problemtype" v-model="selectedProblemType">
      <option>Tactile paving issue</option>
      <option>Blocked tactile paving</option>
      <option>Missing</option>
    </select>
    <button type="button" @click="cancelreport">Cancel</button>
    <label for="description">description:</label>
    <textarea
      id="description"
      v-model="description"
      placeholder="Please provide a brief description of the issue"
    ></textarea>
    <button @click="submitreport" submit>Submit Report</button>
  </div>
</template>

<style>
#map {
  height: 100vh;
  width: 100%;
}

.report-panel,
.report-detail {
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

.location-button {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 1000;
  padding: 8px 12px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.report-panel h3,
.report-panel p {
  margin: 0;
}

.report-panel p {
  margin-top: 6px;
}
</style>
