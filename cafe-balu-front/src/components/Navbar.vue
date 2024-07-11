<template>
    <b-navbar class="bg-lighter-brown d-flex align-items-center justify-content-between">
        <b-navbar-brand class="d-flex align-items-center">
            <b-img :src="require('@/assets/img/logo.png')" class="img mx-3"></b-img>
            <h4 class="text-dark-brown mb-0">Café Balú</h4>
        </b-navbar-brand>
        <b-navbar-nav class="me-3">
            <b-nav-item>
                <b-button variant="outline-dark-brown" class="d-flex align-items-center">
                    <span>Menú de opciones</span>
                    <b-icon icon="chevron-down" class="ms-2" font-scale="0.9"></b-icon>
                </b-button>
            </b-nav-item>
            <b-nav-item>
                <b-button variant="outline-dark-brown" class="d-flex align-items-center">                    
                    <span>Perfil</span>
                    <b-icon icon="person" class="ms-2"></b-icon>
                </b-button>
            </b-nav-item>
            <b-nav-item>
                <b-button variant="outline-dark-brown" class="d-flex align-items-center">                    
                    <span>Cerrar sesión</span>
                    <b-icon icon="box-arrow-right" class="ms-2" font-scale="0.95"></b-icon>
                </b-button>
            </b-nav-item>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {

}
</script>

<style scoped>
.img {
    width: 50px;
    height: 100%;
}
</style>