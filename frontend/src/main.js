import { createApp } from 'vue';
import DoctorList from './components/DoctorList.vue';

const app = createApp({});
app.component('doctor-list', DoctorList);
app.mount('#app');
