<template>
  <div id="app">
    <header class="sticky-top" v-if="!role && !$route.meta.hideNavigation">      
      <NoSessionNavbar  />      
    </header>
    <header v-else-if="role && !$route.meta.hideNavigation">
      <ActiveSessionNavbar />
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import NoSessionNavbar from './components/NoSessionNavbar.vue';
import ActiveSessionNavbar from './components/ActiveSessionNavbar.vue';

export default {
  name: 'App',
  components: {
    NoSessionNavbar, ActiveSessionNavbar
  },
  data() {
    return {      
      role: "admin"
      /* role: null */
    };
  },
}
</script>
