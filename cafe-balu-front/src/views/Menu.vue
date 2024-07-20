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
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'Menu',
    data() {
        return {
            slide: 0
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
