<template>
    <div>
        <b-navbar class="bg-white d-flex align-items-center justify-content-center">
            <b-navbar-brand class="d-flex align-items-center">
                <h4 class="text-navbar-brown">Café</h4>
                <b-img :src="require('@/assets/img/logos/logo.png')" class="custom-navbar-img mx-3"></b-img>
                <h4 class="text-navbar-brown">Balu</h4>
            </b-navbar-brand>
        </b-navbar>
        <b-navbar class="bg-more-lighter-brown d-flex align-items-center justify-content-center">
            <b-link class="custom-nav-item" @click="scrollToTop">Inicio</b-link>
            <b-link class="custom-nav-item" href="#top">Lo mejor</b-link>
            <b-link class="custom-nav-item" href="#categories">Categorías</b-link>
            <b-link class="custom-nav-item" href="#products">Productos</b-link>
            <b-link class="custom-nav-item" href="#about">Sobre nosotros</b-link>
        </b-navbar>
    </div>
</template>

<script>
export default {
    data() {
        return {

        }
    },
    methods: {
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    }
}
</script>

<style scoped>
.custom-nav-item {
    color: #8B5D2E;
    font-size: 1.2rem;
    font-weight: 500;
    padding: 0.5rem 1rem;
    text-decoration: none;
}

.custom-nav-item:hover {    
    color: #4E2F11;
}

.custom-nav-item:active {
    color: #4E2F11;
}
</style>