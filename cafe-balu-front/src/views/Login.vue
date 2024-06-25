<template>
    <b-container fluid>
        <b-row class="bg-brown full-height">
            <b-col cols="6" class="p-0 d-flex align-items-center justify-content-end">
                <b-img src="https://i.pinimg.com/originals/0b/19/97/0b19978cb1b3ffe1e1d92422a02bb74d.jpg" fluid
                    alt="Coffee" class="img"></b-img>
            </b-col>
            <b-col cols="6" class="px-5 align-self-center">
                <b-card class="p-4 mx-5 rounded-card">
                    <b-row class="d-flex justify-content-center">
                        <b-col cols="12">
                            <h1 class="text-center text-dark-brown">Café Balú</h1>
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
                        <b-col cols="6" class="my-4">
                            <b-button class="w-100" variant="brown">
                                Iniciar sesión
                            </b-button>
                        </b-col>
                        <b-col cols="12" class="text-center">
                            <b-link class="text-dark-brown text-decoration-none">
                                <small>¿No recuerdas tu contraseña? Resetear contraseña</small>
                            </b-link>
                        </b-col>
                        <b-col cols="12" class="text-center">
                            <b-link class="text-dark-brown text-decoration-none">
                                <small>¿No tienes cuenta? Regístrate</small>
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
</style>