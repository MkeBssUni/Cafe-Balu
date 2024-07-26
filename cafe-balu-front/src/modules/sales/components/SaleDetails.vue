<template>
    <b-modal id="modal-sale-details" ref="modal-sale-details" centered scrollable hide-footer
        :no-close-on-backdrop="true" size="lg">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Detalles de una venta</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row class="p-2">
            <b-col cols="8">
                <h6>Fecha de la venta: <b>{{ sale.date }}</b></h6>
                <h6 class="mt-2">Total de la venta: <b class="text-darker-brown">${{ sale.total }}</b></h6>
            </b-col>
            <b-col cols="4" class="text-end">
                <b-badge :variant="sale.status ? 'success' : 'danger'">
                    <h6>{{ sale.status ? 'Completada' : 'Cancelada' }}</h6>
                </b-badge>
            </b-col>
        </b-row>
        <hr class="custom-divider" />
        <b-row class="p-2">
            <b-col cols="12">
                <b-card no-body>
                    <b-card-header>
                        <h6>Desglose de los productos</h6>
                    </b-card-header>
                    <b-card-body>
                        <b-table small hover responsive :items="sale.products" :fields="fields" label-sort-asc=""
                            label-sort-desc="" no-sort-reset class="mb-2">
                            <template #cell(price)="row">
                                <span>${{ row.value }}</span>
                            </template>
                            <template #cell(subtotal)="row">
                                <span>${{ row.value }}</span>
                            </template>
                        </b-table>
                        <div class="d-flex align-items-center justify-content-between">
                            <h6>Total</h6>
                            <h6>${{ sale.total }}</h6>
                        </div>
                    </b-card-body>
                </b-card>
            </b-col>
        </b-row>
    </b-modal>
</template>

<script>
export default {
    data() {
        return {
            sale: {
                date: '11/05/2021',
                total: 100,
                status: true,
                products: [
                    { name: 'Producto 1', price: 10, quantity: 2, subtotal: 20 },
                    { name: 'Producto 2', price: 20, quantity: 3, subtotal: 60 },
                    { name: 'Producto 3', price: 30, quantity: 1, subtotal: 30 }
                ],
            },
            fields: [
                { key: 'name', label: 'Nombre' },
                { key: 'price', label: 'Precio', sortable: true },
                { key: 'quantity', label: 'Cantidad', sortable: true },
                { key: 'subtotal', label: 'Subtotal', sortable: true }
            ]
        }
    }
}
</script>