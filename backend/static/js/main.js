// backend/static/js/main.js

// Importation de Vue
import { createApp } from 'vue';

// Importation de votre composant principal
import App from './App.vue';

// Création de l'application Vue
const app = createApp(App);

// Montre l'application sur l'élément #app
app.mount('#app');
