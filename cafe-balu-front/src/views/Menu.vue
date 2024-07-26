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
            <b-col cols="12" id="products">
                <b-row v-for="category in categories" :key="category.id"
                    :class="{ 'bg-more-lighter-brown': category.id % 2 === 0, 'px-5 d-flex align-items-center justify-content-center': true }">
                    <b-col cols="3" v-for="product in category.products" :key="product.id" class="px-3 py-5">
                        <b-card no-body
                            :class="{ 'custom-card-light custom-card-body': category.id % 2 === 0, 'custom-card-dark custom-card-body': category.id % 2 !== 0 }">
                            <b-card-body class="px-4 d-flex flex-column align-items-center">
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
            categories: [
                {
                    id: 1,
                    name: 'Pasteles',
                    products: [
                        { id: 1, name: 'Pastel de zanahoria', category: 'Pasteles', price: 250, description: 'Pastel de zanahoria con betún de queso crema y nuez picada', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 2, name: 'Pastel de chocolate', category: 'Pasteles', price: 200, description: 'Pastel de chocolate con betún de chocolate y chispas de chocolate', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 3, name: 'Pastel de tres leches', category: 'Pasteles', price: 180, description: 'Pastel de tres leches con betún de crema batida y fresas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 7, name: 'Pastel de red velvet', category: 'Pasteles', price: 300, description: 'Pastel de red velvet con betún de queso crema y fresas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' }
                    ]
                },
                {
                    id: 2,
                    name: 'Panqués',
                    products: [
                        { id: 4, name: 'Panqué de naranja', category: 'Panqués', price: 100, description: 'Panqué de naranja con nuez y azúcar glas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 5, name: 'Panqué de limón', category: 'Panqués', price: 90, description: 'Panqué de limón con almendra y azúcar glas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 6, name: 'Panqué de vainilla', category: 'Panqués', price: 80, description: 'Panqué de vainilla con nuez y azúcar glas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' },
                        { id: 8, name: 'Panqué de chocolate', category: 'Panqués', price: 110, description: 'Panqué de chocolate con nuez y azúcar glas', img: 'https://png.pngtree.com/png-clipart/20230429/original/pngtree-cake-chocolate-cut-png-image_9120780.png' }
                    ]
                }
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

/* estilos de las card */

.custom-card-light,
.custom-card-dark {
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease;
    border-radius: 14px;
    border: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.custom-card-light {
    background-color: rgba(255, 255, 255, 0.6);
}

.custom-card-dark {
    background-color: rgba(251, 242, 234, 1);
}

.custom-card-img {
    width: 80%;
    height: auto;
    object-fit: cover;
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

.custom-card-light:hover .product-description,
.custom-card-dark:hover .product-description {
    opacity: 1;
    max-height: 100px;
}

.custom-card-light:hover,
.custom-card-dark:hover {
    transform: scale(1.05);
    overflow: visible;
}

.custom-card-divider {
    width: 100%;
    border: 1px solid #271706 !important;
}

/* estilos del carrusel */

.carousel-img {
    width: 100%;
    height: 60vh;
    object-fit: cover;
}

.custom-controls {
    width: 100%;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
    padding: 0 1rem;
}

.custom-control-btn {
    width: 50px;
    height: 50px;
    background-color: rgba(0, 0, 0, 0);
    color: white;
    border: none;
    border-radius: 50%;
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
    margin: 0 0.5rem;
    padding-top: 0.025rem;
    background-color: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 10%;
}

.custom-indicator-active {
    background-color: rgba(255, 255, 255, 1);
}
</style>
