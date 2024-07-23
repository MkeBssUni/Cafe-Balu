<template>
    <b-container fluid>
        <b-row class="p-4">
            <b-col cols="12" md="5" lg="6">
                <b-input-group>
                    <b-form-input placeholder="Buscar por nombre..." @keyup.enter="searchProduct()"
                        v-model="search"></b-form-input>
                    <b-button variant="secondary" class="d-flex align-items-center justify-content-between"
                        @click="searchProduct()">
                        <b-icon icon="search"></b-icon>
                    </b-button>
                </b-input-group>
            </b-col>
            <b-col cols="12" sm="6" md="4" class="mt-3 mt-md-0">
                <multi-select :options="categories" v-model="category" placeholder="Selecciona una categoría"
                    label="name" track-by="name" :taggable="false" :allow-empty="false"
                    selectLabel="Presiona enter para seleccionar" selectedLabel="Seleccionado" deselectLabel="">
                </multi-select>
            </b-col>
            <b-col cols="12" sm="6" md="3" lg="2" class="mt-3 mt-md-0">
                <b-button variant="outline-dark-brown" class="d-flex align-items-center justify-content-between w-100"
                    @click="saveProduct()">
                    <span>Registrar</span>
                    <b-icon icon="plus-circle"></b-icon>
                </b-button>
            </b-col>
        </b-row>
        <b-row class="shadow mx-4 mb-4">
            <b-col cols="12" class="pt-3 px-4">
                <b-table small hover borderless responsive :fields="fields" :items="products"
                    :per-page="pagination.size" :current-page="pagination.page" :busy="loading">
                    <template #table-busy>
                        <div class="text-center text-primary my-2">
                            <b-spinner small></b-spinner>
                            <strong class="ml-2">Cargando...</strong>
                        </div>
                    </template>
                    <template v-slot:cell(count)="row">
                        {{ row.index + 1 }}
                    </template>
                    <template v-slot:cell(price)="row">
                        <span>${{ row.item.price }}</span>
                    </template>
                    <template v-slot:cell(status)="row">
                        <b-badge :variant="row.item.status ? 'success' : 'danger'">
                            {{ row.item.status ? 'Activo' : 'Inactivo' }}
                        </b-badge>
                    </template>
                    <template v-slot:cell(actions)="row">
                        <div class="d-flex flex-row flex-nowrap">
                            <b-button variant="outline-info" size="sm" title="Ver detalles" v-b-tooltip.hover.top
                                class="me-1" @click="getProductDetails()">
                                <b-icon icon="eye"></b-icon>
                            </b-button>
                            <b-button variant="outline-warning" size="sm" title="Editar" v-b-tooltip.hover.top
                                class="me-1">
                                <b-icon icon="pencil"></b-icon>
                            </b-button>
                            <b-button variant="outline-danger" size="sm" title="Desactivar" v-b-tooltip.hover.top
                                v-if="row.item.status">
                                <b-icon icon="arrow-down-square"></b-icon>
                            </b-button>
                            <b-button variant="outline-dark-success" size="sm" title="Activar" v-b-tooltip.hover.top
                                v-else>
                                <b-icon icon="arrow-up-square"></b-icon>
                            </b-button>
                        </div>
                    </template>
                </b-table>
            </b-col>
            <b-col cols="12" class="bg-light m-0">
                <b-row class="d-flex align-items-center justify-content-center">
                    <b-col cols="12" md="4" order-md="2" class="d-flex justify-content-center align-items-center mt-3">
                        <b-pagination size="sm" v-model="pagination.page" :total-rows="pagination.total"
                            :per-page="pagination.size" aria-controls="product-table">
                        </b-pagination>
                    </b-col>
                    <b-col cols="12" md="4" order-md="1" class="text-center text-md-start">
                        <b>Mostrando {{ pagination.size * (pagination.page - 1) + 1 }} al
                            {{ pagination.size * pagination.page }} de {{ pagination.total }}
                            registros</b>
                    </b-col>
                    <b-col cols="10" sm="8" md="4" order-md="3" class="d-flex align-items-center justify-content-between my-2 my-md-0">
                        <b>Registros por página</b>
                        <b-form-select v-model="pagination.size" :options="pageOptions"
                            class="form-select custom-pagination-select"></b-form-select>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <ProductForm />
        <ProductDetails />
    </b-container>
</template>

<script>
export default {
    name: 'Products',
    components: {
        ProductForm: () => import('@/modules/products/components/ProductForm.vue'),
        ProductDetails: () => import('@/modules/products/components/ProductDetails.vue')
    },
    data() {
        return {
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
            loading: false,
            search: "",
            pagination: {
                page: 1,
                size: 5,
                total: 12
            },
            pageOptions: [5, 10, 15, 20, 25],
            products: [
                { id: 1, name: 'Pastel de chocolate', category: 'Pasteles', price: 150.00, stock: 10, status: true },
                { id: 2, name: 'Panqué de naranja', category: 'Panqués', price: 100.00, stock: 5, status: true },
                { id: 3, name: 'Donas de chocolate', category: 'Donas', price: 10.00, stock: 20, status: true },
                { id: 4, name: 'Galletas de mantequilla', category: 'Galletas', price: 5.00, stock: 50, status: true },
                { id: 5, name: 'Café americano', category: 'Bebidas calientes', price: 20.00, stock: 100, status: false },
                { id: 6, name: 'Frappé moka', category: 'Bebidas frías', price: 15.00, stock: 200, status: true },
                { id: 7, name: 'Pastel de zanahoria', category: 'Pasteles', price: 200.00, stock: 8, status: false },
                { id: 8, name: 'Panqué de limón', category: 'Panqués', price: 90.00, stock: 3, status: true },
                { id: 9, name: 'Donas de azúcar', category: 'Donas', price: 8.00, stock: 15, status: true },
                { id: 10, name: 'Galletas de chocolate', category: 'Galletas', price: 7.00, stock: 40, status: false },
                { id: 11, name: 'Capuchino', category: 'Bebidas calientes', price: 25.00, stock: 80, status: false },
                { id: 12, name: 'Frappé vainilla', category: 'Bebidas frías', price: 18.00, stock: 150, status: true }
            ],
            fields: [
                { key: 'count', label: '#', sortable: false },
                { key: 'name', label: 'Nombre', sortable: false },
                { key: 'category', label: 'Categoría', sortable: false },
                { key: 'price', label: 'Precio', sortable: false },
                { key: 'stock', label: 'Existencia', sortable: false },
                { key: 'status', label: 'Estado', sortable: false },
                { key: 'actions', label: 'Acciones' }
            ],
        }
    },
    methods: {
        searchProduct() {
            if (this.search.trim().length > 0) this.products = this.products.filter(product => product.name.toLowerCase().includes(this.search.toLowerCase()));
        },
        saveProduct() {
            this.$bvModal.show('modal-product-form');
        },
        getProductDetails() {
            this.$bvModal.show('modal-product-details');
        }
    }
}
</script>

<style scoped></style>
