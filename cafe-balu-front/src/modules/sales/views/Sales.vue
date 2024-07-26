<template>
    <b-container fluid>
        <b-row class="p-4 d-flex align-items-lg-center justify-content-end">
            <b-col cols="12" md="9" lg="10">
                <b-row>
                    <b-col cols="12" lg="6" xl="5"
                        class="d-flex align-items-center justify-content-between justify-content-sm-end justify-content-lg-start">
                        <label class="mb-0 me-3">Fecha de inicio: <b class="text-danger">*</b></label>
                        <b-form-group>
                            <b-form-datepicker v-model="startDate" class="w-100">
                            </b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col cols="12" lg="6" xl="5"
                        class="mt-3 mt-lg-0 d-flex align-items-center justify-content-between justify-content-sm-end justify-content-lg-start">
                        <label class="mb-0 me-3">Fecha de fin: <b class="text-danger">*</b></label>
                        <b-form-group>
                            <b-form-datepicker v-model="endDate" class="w-100">
                            </b-form-datepicker>
                        </b-form-group>
                    </b-col>
                </b-row>
            </b-col>
            <b-col cols="8" sm="6" md="3" lg="2" class="mt-3 mt-md-0">
                <b-button variant="outline-dark-brown" class="d-flex align-items-center justify-content-between w-100"
                    @click="saleForm()">
                    <span>Registrar</span>
                    <b-icon icon="plus-circle"></b-icon>
                </b-button>
            </b-col>
        </b-row>
        <b-row class="shadow mx-4 mb-4">
            <b-col cols="12" class="pt-3 px-4">
                <b-table small hover borderless responsive :fields="fields" :items="sales" :per-page="pagination.size"
                    :current-page="pagination.page" :busy="loading" label-sort-asc="" label-sort-desc="" no-sort-reset>
                    <template #table-busy>
                        <div class="text-center text-primary my-2">
                            <b-spinner small></b-spinner>
                            <strong class="ml-2">Cargando...</strong>
                        </div>
                    </template>
                    <template v-slot:cell(count)="row">
                        {{ row.index + 1 }}
                    </template>
                    <template v-slot:cell(total)="row">
                        <span>${{ row.item.total }}</span>
                    </template>
                    <template v-slot:cell(status)="row">
                        <b-badge variant="success" v-if="row.item.status">
                            Completada
                        </b-badge>
                        <b-badge variant="danger" v-else>
                            Cancelada
                        </b-badge>
                    </template>
                    <template v-slot:cell(actions)="row">
                        <div class="d-flex flex-row flex-nowrap">
                            <b-button variant="outline-info" size="sm" title="Ver detalles" v-b-tooltip.hover.top
                                class="me-1" @click="getSaleDetails()">
                                <b-icon icon="eye"></b-icon>
                            </b-button>
                            <b-button variant="outline-danger" size="sm" title="Cancelar" v-b-tooltip.hover.top
                                :disabled="row.item.status">
                                <b-icon icon="x-circle"></b-icon>
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
        <SaleForm />
        <SaleDetails />
    </b-container>
</template>

<script>
const today = new Date();
export default {
    name: 'Sales',
    components: {
        SaleForm: () => import('@/modules/sales/components/SaleForm.vue'),
        SaleDetails: () => import('@/modules/sales/components/SaleDetails.vue')
    },
    data() {
        return {
            startDate: today,
            endDate: today,
            loading: false,
            pagination: {
                page: 1,
                size: 5,
                total: 12
            },
            pageOptions: [5, 10, 15, 20, 25],
            sales: [
                { count: 1, date: '11/07/2024', vendor: 'Balu Café', client: 'Marianne Santos', total: 1000, status: false },
                { count: 2, date: '04/07/2024', vendor: 'Balu Café', client: 'Miguel Aguario', total: 2000, status: true },
                { count: 3, date: '10/07/2024', vendor: 'Balu Café', client: 'Lisseth Figueroa', total: 4000, status: false },
                { count: 4, date: '10/07/2024', vendor: 'Balu Café', client: 'Andrea Zagal', total: 1000, status: true },
                { count: 5, date: '11/07/2024', vendor: 'Balu Café', client: 'Matthew Domínguez', total: 6000, status: false },
                { count: 6, date: '09/07/2024', vendor: 'Balu Café', client: 'Linda Pérez', total: 2000, status: true },
                { count: 7, date: '01/07/2024', vendor: 'Balu Café', client: 'Balu Aguario', total: 4000, status: false },
                { count: 8, date: '11/07/2024', vendor: 'Balu Café', client: 'Bolita Santos', total: 1000, status: true },
                { count: 9, date: '03/07/2024', vendor: 'Balu Café', client: 'Juan Pérez', total: 1000, status: false },
                { count: 10, date: '08/07/2024', vendor: 'Balu Café', client: 'Sofía López', total: 2000, status: true },
                { count: 11, date: '08/07/2024', vendor: 'Balu Café', client: 'Fernanda Fuentes', total: 4000, status: false },
                { count: 12, date: '04/07/2024', vendor: 'Balu Café', client: 'María Díaz', total: 1000, status: true },
            ],
            fields: [
                { key: 'count', label: '#', sortable: false },
                { key: 'date', label: 'Fecha', sortable: true },
                { key: 'vendor', label: 'Vendedor', sortable: false },
                { key: 'client', label: 'Cliente', sortable: false },
                { key: 'total', label: 'Total', sortable: true },
                { key: 'status', label: 'Estado', sortable: false },
                { key: 'actions', label: 'Acciones' }
            ],
        }
    },
    methods: {
        saleForm() {
            this.$bvModal.show('modal-sale-form');
        },
        getSaleDetails() {
            this.$bvModal.show('modal-sale-details');
        }
    }
}
</script>

<style></style>