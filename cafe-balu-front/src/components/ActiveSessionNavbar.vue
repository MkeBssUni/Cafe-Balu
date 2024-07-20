<template>
    <b-navbar class="bg-lighter-brown d-flex align-items-center justify-content-between">
        <b-navbar-brand class="d-flex align-items-center">
            <b-img :src="require('@/assets/img/logo.png')" class="img mx-3"></b-img>
            <h4 class="text-dark-brown">Café Balu</h4>
        </b-navbar-brand>
        <b-navbar-nav v-if="role">
            <b-nav-item class="position-relative">
                <b-button variant="outline-dark-brown"
                    class="d-flex align-items-center position-relative d-none d-sm-block" @click="toggleDropdown()">
                    <span>Menú de opciones</span>
                    <b-icon :icon="dropdown ? 'chevron-up' : 'chevron-down'" class="ms-2" font-scale="0.95"></b-icon>
                </b-button>
                <b-button variant="outline-dark-brown"
                    class="d-flex align-items-center py-2 position-relative d-sm-none" @click="toggleDropdown()"
                    v-b-tooltip.hover.left="'Menú de opciones'">
                    <b-icon :icon="dropdown ? 'chevron-up' : 'chevron-down'" font-scale="0.95"></b-icon>
                </b-button>
                <b-list-group v-if="dropdown && role === 'admin'" class="options">
                    <b-list-group-item class="d-flex align-items-center justify-content-between">
                        <span>Mi perfil</span>
                        <b-icon icon="person-circle" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                    <b-list-group-item class="d-flex align-items-center justify-content-between"
                        @click="goTo('/categories')">
                        <span>Gestionar categorías</span>
                        <b-icon icon="list" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                    <b-list-group-item class="d-flex align-items-center justify-content-between"
                        @click="goTo('/products')">
                        <span>Gestionar productos</span>
                        <b-icon icon="box" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                    <b-list-group-item class="d-flex align-items-center justify-content-between"
                        @click="goTo('/sales')">
                        <span>Gestionar ventas</span>
                        <b-icon icon="cart3" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                </b-list-group>
                <b-list-group v-else-if="dropdown && role === 'sales'" class="options">
                    <b-list-group-item class="d-flex align-items-center justify-content-between">
                        <span>Mi perfil</span>
                        <b-icon icon="person-circle" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                    <b-list-group-item class="d-flex align-items-center justify-content-between"
                        @click="goTo('/products')">
                        <span>Ver productos</span>
                        <b-icon icon="box" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                    <b-list-group-item class="d-flex align-items-center justify-content-between"
                        @click="goTo('/sales')">
                        <span>Gestionar ventas</span>
                        <b-icon icon="cart3" font-scale="0.95"></b-icon>
                    </b-list-group-item>
                </b-list-group>
            </b-nav-item>
            <b-nav-item>
                <b-button variant="outline-dark-brown" class="d-none d-sm-flex align-items-center" @click="logout">
                    <span>Cerrar sesión</span>
                    <b-icon icon="box-arrow-right" class="ms-2" font-scale="0.95"></b-icon>
                </b-button>
                <b-button variant="outline-dark-brown" class="d-flex align-items-center py-2 d-sm-none" @click="logout"
                    v-b-tooltip.hover.left="'Cerrar sesión'">
                    <b-icon icon="box-arrow-right" font-scale="0.95"></b-icon>
                </b-button>
            </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav v-else>
            <b-nav-item>
                <b-button variant="outline-dark-brown" class="d-flex align-items-center" @click="goTo('/login')">
                    <span>Iniciar sesión</span>
                    <b-icon icon="box-arrow-in-right" class="ms-2" font-scale="0.95"></b-icon>
                </b-button>
            </b-nav-item>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {
    data() {
        return {
            role: "admin",
            dropdown: false
        }
    },
    methods: {
        toggleDropdown() {
            this.dropdown = !this.dropdown;
        },
        goTo(route) {
            this.$router.push(route);
        },
        logout() {
            this.goTo('/login');
        }
    }
}
</script>

<style scoped>
.img {
    width: 50px;
    height: 100%;
}

.options {
    position: absolute;
    top: 88%;
    right: 0;
    margin-right: 0.5rem;
    width: 240px;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.options .list-group-item:hover {
    background-color: #f8f9fa;
}
</style>
