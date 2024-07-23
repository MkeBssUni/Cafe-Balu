<template>
    <b-container fluid>
        <b-row class="d-flex justify-content-center">
            <b-col cols="7" md="6" xl="7" class="p-0 d-none d-md-flex align-items-center justify-content-end">
                <b-img :src="require('@/assets/img/coffee-maker.jpg')" fluid alt="Coffee Maker" class="img"></b-img>
            </b-col>
            <b-col cols="12" md="6" xl="5" class="px-5 align-self-center">
                <b-row class="px-lg-2">
                    <b-col cols="12" class="pt-5 pt-md-0 pb-4">
                        <b-card no-body>
                            <b-card-body>
                                <h3 class="text-dark-brown mb-3">Bienvenido a Café Balu</h3>
                                <h6 class="mb-3 text-brown" v-if="role === 'sales'">
                                    Gracias por ser parte de nuestro equipo de ventas
                                </h6>
                                <p class="text-justify">
                                    Café Balu es un pequeño emprendimiento que ofrece una amplia
                                    variedad de productos relacionados con el café. Nuestro objetivo es brindar a
                                    nuestros clientes la mejor experiencia.
                                </p>
                            </b-card-body>
                        </b-card>
                    </b-col>
                    <b-col cols="12" sm="4" md="12" class="mt-3">
                        <b-button variant="lighter-brown" @click="goTo('/categories')"
                            class="w-100 py-2 border-darker-brown d-flex d-sm-none d-md-flex align-items-center justify-content-between">
                            <span class="text-darker-brown" v-if="role === 'admin'">Gestionar categorías</span>
                            <span class="text-darker-brown" v-else>Visualizar categorías</span>
                            <b-icon icon="list" variant="darker-brown" class="mr-2"></b-icon>
                        </b-button>
                        <b-card bg-variant="lighter-brown custom-card" @click="goTo('/categories')"
                            class="w-100 py-2 border-darker-brown d-none d-sm-flex d-md-none align-items-center justify-content-center">
                            <div class="text-center">
                                <b-icon icon="list" variant="darker-brown" class="mr-2" font-scale="2"></b-icon>
                                <h6 class="text-darker-brown mt-2">Categorías</h6>
                            </div>
                        </b-card>
                    </b-col>
                    <b-col cols="12" sm="4" md="12" class="mt-3">
                        <b-button variant="lighter-brown" @click="goTo('/products')"
                            class="w-100 py-2 border-darker-brown d-flex d-sm-none d-md-flex align-items-center justify-content-between">
                            <span class="text-darker-brown" v-if="role === 'admin'">Gestionar productos</span>
                            <span class="text-darker-brown" v-else>Visualizar productos</span>
                            <b-icon icon="box-seam" variant="darker-brown" class="mr-2"></b-icon>
                        </b-button>
                        <b-card bg-variant="lighter-brown custom-card" @click="goTo('/products')"
                            class="w-100 py-2 border-darker-brown d-none d-sm-flex d-md-none align-items-center justify-content-center">
                            <div class="text-center">
                                <b-icon icon="box-seam" variant="darker-brown" class="mr-2" font-scale="2"></b-icon>
                                <h6 class="text-darker-brown mt-2">Productos</h6>
                            </div>
                        </b-card>
                    </b-col>
                    <b-col cols="12" sm="4" md="12" class="mt-3">
                        <b-button variant="lighter-brown" @click="goTo('/sales')"
                            class="w-100 py-2 border-darker-brown d-flex d-sm-none d-md-flex align-items-center justify-content-between">
                            <span class="text-darker-brown">Gestionar ventas</span>
                            <b-icon icon="cart3" variant="darker-brown" class="mr-2"></b-icon>
                        </b-button>
                        <b-card bg-variant="lighter-brown custom-card" @click="goTo('/sales')"
                            class="w-100 py-2 border-darker-brown d-none d-sm-flex d-md-none align-items-center justify-content-center">
                            <div class="text-center">
                                <b-icon icon="cart3" variant="darker-brown" class="mr-2" font-scale="2"></b-icon>
                                <h6 class="text-darker-brown mt-2">Ventas</h6>
                            </div>
                        </b-card>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'Home',
    data() {
        return {
            role: "sales",
        };
    },
    methods: {
        goTo(route) {
            this.$router.push(route);
        },
    },
}
</script>

<style scoped>
.img {
    width: 100%;
    height: 89vh;
    object-fit: cover;
}

h3 {
    font-style: italic;
}

.text-justify {
    font-size: 0.9rem;
}

.custom-card {
    cursor: pointer;
}

.custom-card:hover {
    transform: scale(1.1);
}
</style>