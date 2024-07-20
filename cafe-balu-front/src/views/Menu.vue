<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" class="px-0">
                <b-carousel ref="carousel" v-model="slide" :interval="0" class="custom-carousel">
                    <b-carousel-slide>
                        <template #img>
                            <b-img :src="require('@/assets/img/cinnamon-rolls.jpg')" class="carousel-img"></b-img>
                        </template>
                    </b-carousel-slide>
                    <b-carousel-slide>
                        <template #img>
                            <b-img :src="require('@/assets/img/cinnamon-rolls.jpg')" class="carousel-img"></b-img>
                        </template>
                    </b-carousel-slide>
                    <b-carousel-slide>
                        <template #img>
                            <b-img :src="require('@/assets/img/cinnamon-rolls.jpg')" class="carousel-img"></b-img>
                        </template>
                    </b-carousel-slide>
                    <div class="d-flex align-items-center justify-content-between custom-controls">
                        <b-button @click="slide--"
                            class="custom-control-btn d-flex align-items-center justify-content-center">
                            <b-icon icon="chevron-left" font-scale="2"></b-icon>
                        </b-button>
                        <b-button @click="slide++"
                            class="custom-control-btn d-flex align-items-center justify-content-center">
                            <b-icon icon="chevron-right" font-scale="2"></b-icon>
                        </b-button>
                    </div>
                    <div class="custom-indicators mb-2">
                        <b-button v-for="(index) in 3" :key="index" @click="getSlide(index)"
                            :class="{ 'custom-indicator px-3': true, 'custom-indicator-active': index - 1 === slide }">
                        </b-button>
                    </div>
                </b-carousel>
            </b-col>
            <b-col cols="12" class="px-5 bg-more-lighter-brown">
                <b-row>
                    <b-col cols="12" class="d-flex align-items-center justify-content-center flex-wrap">
                        <b-col cols="12" sm="6" md="4" xl="3" v-for="product in products" :key="product.id"
                            class="px-3 mt-5">
                            <b-card no-body class="custom-card custom-card-body">
                                <b-card-body class="p-4 d-flex flex-column align-items-center">
                                    <b-img :src="product.img" class="custom-card-img mb-2"></b-img>
                                    <b-badge variant="brown">{{ product.category }}</b-badge>
                                    <h5 class="mt-2">{{ product.name }}</h5>
                                    <hr class="custom-card-divider my-3">
                                    <div class="d-flex align-items-center justify-content-between w-100">
                                        <span>Precio del producto:</span>
                                        <h5 class="text-card-title">${{ product.price }}</h5>
                                    </div>
                                    <p class="product-description mt-3">{{ product.description }}</p>
                                </b-card-body>
                            </b-card>
                        </b-col>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'Menu',
    data() {
        return {
            slide: 0,
            search: "",
            category: { id: 0, name: 'Todas las categorías' },
            categories: [
                { id: 0, name: 'Todas las categorías' },
                { id: 1, name: 'Pasteles' },
                { id: 2, name: 'Panqués' },
                { id: 3, name: 'Donas' },
                { id: 4, name: 'Galletas' },
                { id: 5, name: 'Bebidas calientes' },
                { id: 6, name: 'Bebidas frías' }
            ],
            products: [
                { id: 1, name: 'Pastel de chocolate', category: 'Pasteles', price: 150.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Delicioso pastel de chocolate con cobertura de chocolate.' },
                { id: 2, name: 'Panqué de naranja', category: 'Panqués', price: 150.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Esponjoso panqué de naranja, perfecto para acompañar con té.' },
                { id: 3, name: 'Donas de chocolate', category: 'Donas', price: 50.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Donas suaves y esponjosas cubiertas con glaseado de chocolate.' },
                { id: 4, name: 'Galletas de chocolate', category: 'Galletas', price: 20.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Crujientes galletas de chocolate, perfectas para un snack.' },
                { id: 5, name: 'Café americano', category: 'Bebidas calientes', price: 30.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Café americano caliente y recién hecho.' },
                { id: 6, name: 'Té helado', category: 'Bebidas frías', price: 25.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Refrescante té helado con un toque de limón.' },
                { id: 7, name: 'Pastel de zanahoria', category: 'Pasteles', price: 200.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Pastel de zanahoria con un glaseado de queso crema.' },
                { id: 8, name: 'Panqué de limón', category: 'Panqués', price: 120.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Panqué de limón con un toque cítrico refrescante.' },
                { id: 9, name: 'Donas de vainilla', category: 'Donas', price: 60.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Donas de vainilla con un glaseado dulce y cremoso.' },
                { id: 10, name: 'Galletas de mantequilla', category: 'Galletas', price: 25.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Galletas suaves de mantequilla que se deshacen en la boca.' },
                { id: 11, name: 'Café con leche', category: 'Bebidas calientes', price: 35.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Café con leche espumoso y caliente.' },
                { id: 12, name: 'Té verde', category: 'Bebidas frías', price: 30.00, img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png', description: 'Té verde frío y refrescante.' },
            ],
        }
    },
    methods: {
        getSlide(index) {
            this.slide = index - 1;
        }
    }
}
</script>

<style scoped>
.custom-card-img {
    width: 80%;
    height: auto;
    object-fit: cover;
}

.custom-card {
    border-radius: 14px;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    background-color: rgba(255, 255, 255, 0.6);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.custom-card-body {
    transition: height 0.3s ease;
}

.product-description {
    font-size: 0.875rem;
    color: #5f5f5f;
    text-align: center;
    margin-top: 10px;
    opacity: 0;
    max-height: 0;
    transition: opacity 0.3s ease, max-height 0.3s ease;
    overflow: hidden;
}

.custom-card:hover .product-description {
    opacity: 1;
    max-height: 100px;
}

.custom-card:hover {
    transform: scale(1.05);
    overflow: visible;
    /* Esto permite que el contenido expandido sea visible */
}

.custom-card-divider {
    width: 100%;
    border: 1px solid #271706 !important;
}



.carousel-img {
    width: 100%;
    height: 60vh;
    object-fit: cover;
}

.custom-controls {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 100%;
    padding: 0 1rem;
    z-index: 1;
}

.custom-control-btn {
    background-color: rgba(0, 0, 0, 0);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
}

.custom-control-btn:hover {
    background-color: rgba(0, 0, 0, 0);
}

.custom-control-btn:focus {
    background-color: rgba(0, 0, 0, 0);
}

.custom-indicators {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
}

.custom-indicator {
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 10%;
    margin: 0 0.5rem;
    padding-top: 0.025rem;
}

.custom-indicator-active {
    background-color: rgba(255, 255, 255, 1);
}
</style>
