<template>
    <b-navbar class="bg-more-lighter-brown d-flex align-items-center justify-content-between px-3">
        <b-navbar-brand class="custom-navbar-brand d-flex align-items-center" @click="goTo('/home')">
            <b-img :src="require('@/assets/img/logos/logo.png')" class="custom-navbar-img"></b-img>
            <div class="ms-3">
                <h5>Café Balu</h5>
                <span>{{ session.role === 'admin' ? 'Administración' : 'Ventas' }}</span>
            </div>
        </b-navbar-brand>
        <b-navbar-nav>
            <b-nav-item class="position-relative" ref="options">
                <b-button variant="lighter-brown" class="border-dark-brown d-flex align-items-center"
                    @click="toggleDropdown(1)">
                    <span class="text-dark-brown d-sm-none">Opciones</span>
                    <span class="text-dark-brown d-none d-sm-block">Menú de opciones</span>
                    <b-icon :icon="dropdowns.options ? 'chevron-up' : 'chevron-down'" class="ms-2" variant="dark-brown"
                        font-scale="0.9"></b-icon>
                </b-button>
                <div v-if="dropdowns.options" class="custom-dropdown">
                    <div class="custom-dropdown-item d-flex align-items-center justify-content-between"
                        @click="goTo('/categories')">
                        <span v-if="session.role === 'admin'">Gestionar categorías</span>
                        <span v-else>Visualizar categorías</span>
                        <b-icon icon="list" font-scale="0.95"></b-icon>
                    </div>
                    <div class="custom-dropdown-item d-flex align-items-center justify-content-between"
                        @click="goTo('/products')">
                        <span v-if="session.role === 'admin'">Gestionar productos</span>
                        <span v-else>Visualizar productos</span>
                        <b-icon icon="box" font-scale="0.95"></b-icon>
                    </div>
                    <div class="custom-dropdown-item d-flex align-items-center justify-content-between"
                        @click="goTo('/sales')">
                        <span>Gestionar ventas</span>
                        <b-icon icon="cart3" font-scale="0.95"></b-icon>
                    </div>
                </div>
            </b-nav-item>
            <b-nav-item class="position-relative" ref="profile">
                <b-button variant="lighter-brown" class="border-dark-brown d-flex align-items-center"
                    @click="toggleDropdown(2)">
                    <span class="text-dark-brown d-sm-none">Perfil</span>
                    <span class="text-dark-brown d-none d-sm-block">Mi perfil</span>
                    <b-icon :icon="dropdowns.profile ? 'chevron-up' : 'chevron-down'" class="ms-2" variant="dark-brown"
                        font-scale="0.9"></b-icon>
                </b-button>
                <div v-if="dropdowns.profile" class="custom-dropdown">
                    <div class="custom-dropdown-header text-end">
                        <div class="d-flex align-items-center justify-content-end">
                            <span class="me-1">Role:</span>
                            <span class="text-brown role">
                                {{ session.role === 'admin' ? 'Administración' : 'Ventas' }}
                            </span>
                        </div>
                        <span class="text-brown email">{{ session.email }}</span>
                        <div v-if="session.role === 'admin'"
                            class="mt-2 py-2 px-3 d-flex align-items-center justify-content-between nip-container">
                            <div>
                                <span class="me-2">NIP de seguridad:</span>
                                <b>{{ showNip ? nip : '****' }}</b>
                            </div>
                            <b-button variant="outline-dark-brown" size="sm" class="d-flex align-items-center"
                                @click="showNip = !showNip">
                                <b-icon :icon="showNip ? 'eye' : 'eye-slash'"></b-icon>
                            </b-button>
                        </div>
                    </div>
                    <div class="custom-dropdown-item d-flex align-items-center justify-content-between"
                        @click="changePassword">
                        <span>Cambiar contraseña</span>
                        <b-icon icon="key" font-scale="0.98"></b-icon>
                    </div>
                    <div class="custom-dropdown-item d-flex align-items-center justify-content-between" @click="logout">
                        <span>Cerrar sesión</span>
                        <b-icon icon="box-arrow-right" font-scale="0.98"></b-icon>
                    </div>
                </div>
            </b-nav-item>
        </b-navbar-nav>
        <ChangePasswordForm />
    </b-navbar>
</template>

<script>
export default {
    data() {
        return {
            session: {
                email: "admin@gmail.com",
                role: "sales"
            },
            dropdowns: {
                options: false,
                profile: false
            },
            nip: "7133",
            showNip: false
        }
    },
    components: {
        ChangePasswordForm: () => import('@/modules/auth/components/ChangePasswordForm.vue')
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
    },
    beforeDestroy() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        toggleDropdown(index) {
            if (index == 1) {
                this.dropdowns.options = !this.dropdowns.options;
                this.dropdowns.profile = false;
            } else {
                this.dropdowns.profile = !this.dropdowns.profile;
                this.dropdowns.options = false;
            }
        },
        handleClickOutside(event) {
            const options = this.$refs.options;
            const profile = this.$refs.profile;

            if (options && !options.contains(event.target)) {
                this.dropdowns.options = false;
            }
            if (profile && !profile.contains(event.target)) {
                this.dropdowns.profile = false;
            }
        },
        goTo(route) {
            this.$router.push(route);
        },
        changePassword() {
            this.$bvModal.show('modal-change-password-form');
        },
        logout() {
            this.goTo('/login');
        }
    }
}
</script>

<style scoped>
.email {
    font-size: 0.9rem;
}

.role {
    font-style: italic;
    font-weight: 600;
}

.nip-container {
    font-size: 0.9rem;
    background-color: #f0d9b5;
    border-radius: 5px;
}
</style>
