<template>
    <b-container fluid>
        <b-row class="p-4 d-flex justify-content-between">
            <b-col cols="12" sm="8" md="9" xl="8">
                <b-input-group>
                    <b-form-input placeholder="Buscar por nombre..."></b-form-input>
                    <b-button variant="secondary" class="d-flex align-items-center justify-content-between">
                        <b-icon icon="search"></b-icon>
                    </b-button>
                </b-input-group>
            </b-col>
            <b-col cols="12" sm="4" md="3" xl="2" class="mt-3 mt-sm-0">
                <b-button variant="outline-dark-brown" class="d-flex align-items-center justify-content-between w-100"
                    @click="saveCategory()">
                    <span>Registrar</span>
                    <b-icon icon="plus-circle"></b-icon>
                </b-button>
            </b-col>
        </b-row>
        <b-row class="shadow mx-4 mb-4">
            <b-col cols="12" class="pt-3 px-4">
                <b-table small hover borderless responsive :fields="fields" :items="categories"
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
                    <template v-slot:cell(status)="row">
                        <b-badge :variant="row.item.status ? 'success' : 'danger'">
                            {{ row.item.status ? 'Activa' : 'Inactiva' }}
                        </b-badge>
                    </template>
                    <template v-slot:cell(actions)="row">
                        <div class="d-flex flex-row flex-nowrap">
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
                    <b-col cols="10" sm="8" md="4" order-md="3"
                        class="d-flex align-items-center justify-content-between my-2 my-md-0">
                        <b>Registros por página</b>
                        <b-form-select v-model="pagination.size" :options="pageOptions"
                            class="form-select custom-pagination-select"></b-form-select>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <CategoryForm />
    </b-container>
</template>

<script>
export default {
    name: 'Categories',
    components: {
        CategoryForm: () => import('@/modules/categories/components/CategoryForm.vue')
    },
    data() {
        return {
            loading: false,
            search: "",
            pagination: {
                page: 1,
                size: 5,
                total: 12
            },
            pageOptions: [5, 10, 15, 20, 25],
            categories: [
                { id: 1, name: 'Pasteles', status: true },
                { id: 2, name: 'Galletas', status: false },
                { id: 3, name: 'Pan', status: true },
                { id: 4, name: 'Cupcakes', status: false },
                { id: 5, name: 'Tortas', status: true },
                { id: 6, name: 'Dulces', status: false },
                { id: 7, name: 'Helados', status: true },
                { id: 8, name: 'Chocolates', status: true },
                { id: 9, name: 'Caramelos', status: true },
                { id: 10, name: 'Gelatinas', status: true },
                { id: 11, name: 'Postres', status: false },
                { id: 12, name: 'Muffins', status: false },
            ],
            fields: [
                { key: 'count', label: '#' },
                { key: 'name', label: 'Nombre' },
                { key: 'status', label: 'Estado' },
                { key: 'actions', label: 'Acciones' }
            ],
        }
    },
    methods: {
        saveCategory() {
            this.$bvModal.show('modal-category-form');
        }
    },
}
</script>

<style scoped></style>