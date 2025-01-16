<template>
    <div>
      <h2>Doctor List</h2>
      <ul>
        <li v-for="doctor in doctors" :key="doctor.id">
          {{ doctor.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        doctors: [],
      };
    },
    async mounted() {
      const response = await axios.get("/doctors/api/doctors");
      this.doctors = response.data;
    },
  };
  </script>
  