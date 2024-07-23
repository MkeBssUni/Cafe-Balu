<template>
    <b-modal id="modal-sale-form" ref="modal-sale-form" centered scrollable hide-footer :no-close-on-backdrop="true"
        @closed="cleanForm()" @hidden="cleanForm()" modal-class="custom-modal">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Registrar venta</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row class="p-2">
            <b-col cols="12" lg="6">
                <b-card no-body class="custom-card">
                    <template #header>
                        <h6 v-if="!editMode">Formulario para agregar un producto</h6>
                        <h6 v-else>Formulario para editar un misceláneo</h6>
                    </template>
                    <b-card-body class="p-4">
                        <b-row>
                            <b-col cols="12">
                                <b-form-group>
                                    <label>Categoría: <b class="text-danger">*</b></label>
                                    <multi-select :options="categories" v-model="form.category"
                                        placeholder="Selecciona una categoría" label="name" track-by="name"
                                        :taggable="false" selectLabel="Presiona enter para seleccionar"
                                        selectedLabel="Seleccionado" deselectLabel="Presiona enter para eliminar">
                                    </multi-select>
                                </b-form-group>
                            </b-col>
                            <b-col cols="12" class="mt-3">
                                <b-form-group>
                                    <label>Producto: <b class="text-danger">*</b></label>
                                    <multi-select :options="products" v-model="form.product"
                                        placeholder="Selecciona un producto" label="name" track-by="name"
                                        :taggable="false" selectLabel="Presiona enter para seleccionar"
                                        selectedLabel="Seleccionado" deselectLabel="Presiona enter para eliminar">
                                    </multi-select>
                                </b-form-group>
                            </b-col>
                            <b-col cols="12" class="mt-3">
                                <b-form-group>
                                    <label>Cantidad: <b class="text-danger">*</b></label>
                                    <b-form-input type="number" v-model="form.quantity" min="0"></b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col cols="12" class="mt-4 d-flex justify-content-end" v-if="!editMode"
                                @click="cleanForm()">
                                <b-button variant="outline-danger" class="me-2">
                                    Limpiar
                                </b-button>
                                <b-button variant="outline-success" @click="addProduct()">
                                    Agregar
                                </b-button>
                            </b-col>
                            <b-col cols="12" class="mt-4 d-flex justify-content-end" v-else>
                                <b-button variant="outline-danger" class="me-2" @click="resetForm()">
                                    Cancelar
                                </b-button>
                                <b-button variant="outline-success" @click="editProduct()">
                                    Guardar
                                </b-button>
                            </b-col>
                        </b-row>
                    </b-card-body>
                </b-card>
            </b-col>
            <b-col cols="12" lg="6" class="mt-3 mt-lg-0">
                <b-card no-body class="custom-card">
                    <template #header>
                        <h6>Resumen de la venta</h6>
                    </template>
                    <b-card-body>
                        <b-list-group v-if="form.products.length > 0" class="scrollable" ref="summary">
                            <b-list-group-item v-for="(product, index) in form.products" :key="index">
                                <b-row>
                                    <b-col cols="9" md="6" lg="9">
                                        <b-row>
                                            <b-col cols="12" sm="9" xl="10">
                                                <p class="mb-1 text-muted">{{ product.category.name }}</p>
                                                <div class="d-flex">
                                                    <h6>
                                                        <b-badge variant="light-brown">
                                                            {{ product.quantity }}
                                                        </b-badge>
                                                    </h6>
                                                    <p class="ms-2 mb-1">{{ product.name }}</p>
                                                </div>
                                            </b-col>
                                            <b-col cols="12" sm="3" xl="2" class="d-flex align-items-center">
                                                <b>${{ product.price * product.quantity }}</b>
                                            </b-col>
                                        </b-row>
                                    </b-col>
                                    <b-col cols="3" md="6" lg="3" class="d-flex justify-content-end">
                                        <div class="d-flex flex-row flex-nowrap align-items-center">
                                            <b-button variant="outline-warning" size="sm" title="Editar"
                                                v-b-tooltip.hover.top class="me-1" @click="loadProduct(index)">
                                                <b-icon icon="pencil"></b-icon>
                                            </b-button>
                                            <b-button variant="outline-danger" size="sm" title="Eliminar"
                                                v-b-tooltip.hover.top @click="deleteProduct(index)">
                                                <b-icon icon="trash"></b-icon>
                                            </b-button>
                                        </div>
                                    </b-col>
                                </b-row>
                            </b-list-group-item>
                        </b-list-group>
                        <div class="d-flex justify-content-center align-items-center scrollable" v-else>
                            <h6 class="text-muted text-center">Sin productos por el momento</h6>
                        </div>
                        <hr class="custom-divider">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Total</span>
                            <h6>${{ total }}</h6>
                        </div>
                    </b-card-body>
                </b-card>
            </b-col>
            <b-col cols="12" class="mt-4">
                <b-row class="d-flex justify-content-end">
                    <b-col cols="12" class="d-flex justify-content-end">
                        <b-button variant="outline-danger" class="me-2">
                            Cancelar
                        </b-button>
                        <b-button variant="outline-success">
                            Registrar
                        </b-button>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-modal>
</template>

<script>
export default {
    name: 'SalesForm',
    data() {
        return {
            editMode: false,
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
            total: 0,
            form: {
                category: null,
                product: null,
                quantity: 0,
                products: []
            },
            productSelectedIndex: 0
        }
    },
    methods: {
        cleanForm() {
            this.form.category = null;
            this.form.product = null;
            this.form.quantity = 0;
        },
        resetForm() {
            this.editMode = false;
            this.cleanForm();
        },
        scrollToTop() {
            this.$refs.summary.scrollTop = 0;
        },
        addProduct() {
            this.form.products.unshift({
                id: this.form.product.id,
                name: this.form.product.name,
                price: this.form.product.price,
                quantity: this.form.quantity,
                category: {
                    id: this.form.category.id,
                    name: this.form.category.name
                }
            });
            this.total += this.form.product.price * this.form.quantity;
            this.cleanForm();
            this.scrollToTop();
        },
        loadProduct(index) {
            this.editMode = true;
            this.form.category = this.categories.find(category => category.id === this.form.products[index].category.id);
            this.form.product = this.products.find(product => product.id === this.form.products[index].id);
            this.form.quantity = this.form.products[index].quantity;
            this.productSelectedIndex = index;            
        },
        editProduct() {
            const index = this.productSelectedIndex;
            this.total -= this.form.products[index].price * this.form.products[index].quantity;
            this.form.products.splice(index, 1);
            this.form.products.unshift({
                id: this.form.product.id,
                name: this.form.product.name,
                price: this.form.product.price,
                quantity: this.form.quantity,
                category: {
                    id: this.form.category.id,
                    name: this.form.category.name
                }
            });
            this.total += this.form.product.price * this.form.quantity;
            this.resetForm();
            this.scrollToTop();            
        },
        deleteProduct(index) {
            this.total -= this.form.products[index].price * this.form.products[index].quantity;
            this.form.products.splice(index, 1);
        }
    }
}
</script>

<style scoped>
.custom-card {
    height: 70vh;
    display: flex;
    flex-direction: column;
}

.scrollable {
    overflow-y: auto;
    height: 49vh;
}

.divider {
    border-top: 1px solid black;
}
</style>