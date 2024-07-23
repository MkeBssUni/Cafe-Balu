<template>
    <b-container fluid>
        <b-row class="bg-lighter-brown full-height d-flex justify-content-center">
            <b-col cols="4" lg="6" class="p-0 d-none d-md-flex align-items-center justify-content-end">
                <b-img :src="require('@/assets/img/login.webp')" fluid
                    alt="Coffee" class="img"></b-img>
            </b-col>
            <b-col cols="12" sm="11" md="8" lg="6" class="px-5 align-self-center">
                <b-card class="p-4 mx-xl-4 rounded-card">
                    <b-row class="d-flex justify-content-center">
                        <b-col cols="12">
                            <h1 class="text-center text-dark-brown" style="font-weight: 600;">Café Balú</h1>
                            <h5 class="text-center text-brown">Inicio de sesión</h5>
                        </b-col>
                        <b-col cols="12" class="mt-3">
                            <b-form-group>
                                <label for="email" class="mb-2">
                                    Correo electrónico: <b class="text-danger">*</b>
                                </label>
                                <b-form-input id="email" type="email" placeholder="Ingrese su correo electrónico..."
                                    required></b-form-input>
                            </b-form-group>
                            <b-form-group class="mt-3">
                                <label for="password" class="mb-2">
                                    Contraseña: <b class="text-danger">*</b>
                                </label>
                                <b-input-group>
                                    <b-form-input id="password" :type="showPassword ? 'text' : 'password'"
                                        placeholder="Ingrese su contraseña..." required></b-form-input>
                                    <b-button variant="outline-brown" @click="togglePassword()">
                                        <b-icon :icon="showPassword ? 'eye' : 'eye-slash'"></b-icon>
                                    </b-button>
                                </b-input-group>
                            </b-form-group>
                        </b-col>
                        <b-col cols="8" class="my-4">
                            <b-button class="w-100" variant="light-brown">
                                Iniciar sesión
                            </b-button>
                        </b-col>
                        <b-col cols="12" class="text-center">
                            <b-link class="text-dark-brown text-decoration-none" to="/validate-password">
                                <small>Haz clic aquí para validar tu contraseña</small>
                            </b-link>
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            showPassword: false
        };
    },
    methods: {
        togglePassword() {
            this.showPassword = !this.showPassword;
        }
    }
}
</script>

<style scoped>
.img {
    width: 100%;
    height: 100vh;
    object-fit: cover;
}

.rounded-card {
    border-radius: 20px;        
    background-color: rgba(255, 255, 255, 0.9);    
    box-shadow: 5px 5px 15px 5px rgba(0, 0, 0, 0.1);
}
</style>