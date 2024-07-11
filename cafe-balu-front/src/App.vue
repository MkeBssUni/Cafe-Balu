<template>
  <div id="app">
    <header>
      <Navbar v-if="!$route.meta.hideNavigation" />
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>
