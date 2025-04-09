/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { VDateInput } from 'vuetify/labs/VDateInput'

// Composables
import { createVuetify } from 'vuetify';
import { en } from 'vuetify/locale';

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  locale: 'en',
  fallbackLocale: 'en',
  theme: {
    defaultTheme: 'light',
  },
  components: {
    VDateInput,
  },
});
