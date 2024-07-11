import Vue from 'vue'
import App from './App.vue'

// BootstrapVue
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './styles/styles.scss'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import './styles/styles.css'

// VueRouter
import router from './router/index'

// Vuelidate
import Vuelidate from 'vuelidate';
Vue.use(Vuelidate);

// VueSweetAlert
import VueSweetalert2 from 'vue-sweetalert2';
Vue.use(VueSweetalert2);

// VueMultiselect
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';
Vue.component('multi-select', Multiselect);

new Vue({
  router,
  render: (h) => h(App)
}).$mount('#app')