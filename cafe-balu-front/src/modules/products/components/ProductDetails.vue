<template>
    <b-modal id="modal-product-details" ref="modal-product-details" centered scrollable hide-footer
        :no-close-on-backdrop="true" size="lg">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Detalles de un producto</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row>
            <b-col cols="12" lg="6">
                <b-img :src="product.image" fluid alt="Product image" class="img" />
            </b-col>
            <b-col cols="12" lg="6" class="mt-3 mt-lg-0">
                <b-card no-body class="d-flex align-items-center">
                    <b-card-body>
                        <b-card-title>{{ product.name }}</b-card-title>
                        <b-card-sub-title>{{ product.category.name }}</b-card-sub-title>
                        <b-row class="my-4">
                            <b-col cols="6" class="d-flex align-items-center">
                                <h6 class="me-2">Precio:</h6>
                                <h6 class="text-dark-brown">${{ product.price }}</h6>
                            </b-col>
                            <b-col cols="6" class="d-flex align-items-center">
                                <h6 class="me-2">Existencias:</h6>
                                <h6 :class="product.stock === 0 ? 'text-danger' : 'text-success'">{{ product.stock }}
                                </h6>
                            </b-col>
                        </b-row>
                        <h6>Descripción:</h6>
                        <p class="custom-font-size mt-1 mb-0">{{ product.description }}</p>
                    </b-card-body>
                </b-card>
            </b-col>
        </b-row>
    </b-modal>
</template>

<script>
export default {
    name: 'ProductDetails',
    data() {
        return {
            product: {
                id: 1,
                image: "https://www.recetasnestle.com.mx/sites/default/files/srh_recipes/6a5b47579f27ffcd61ac368a761f5b96.jpg",
                category: { id: 1, name: 'Pasteles' },
                name: "Galletas de chocolate",
                price: 480,
                stock: 20,
                description: "Lorem ipsum dolor sit amet consectetur adipiscing elit sapien, ante mattis phasellus taciti nostra condimentum nunc eu, torquent vestibulum quisque quis facilisis inceptos litora. Aenean lacinia dictum egestas rutrum nunc ultrices ut, a in mollis hac taciti sodales risus quisque, quam torquent felis non volutpat eleifend. Suscipit sociosqu nulla imperdiet congue, ligula dignissim pellentesque. Facilisis vulputate nunc faucibus montes platea, cursus cubilia facilisi eu arcu donec, massa volutpat.",
            },
        }
    },
}
</script>

<style scoped>
.img {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    object-fit: cover;
}

.custom-font-size {
    font-size: 0.8rem;
}
</style>