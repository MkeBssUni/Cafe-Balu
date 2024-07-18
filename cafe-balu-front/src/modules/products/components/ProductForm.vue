<template>
    <b-modal id="modal-product-form" ref="modal-product-form" centered scrollable hide-footer
        :no-close-on-backdrop="true" @closed="cleanForm()" @hidden="cleanForm()">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Registrar producto</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row>
            <b-col cols="12">
                <b-form-group>
                    <label>Imagen: <b class="text-danger">*</b></label><br>
                    <div class="d-flex justify-content-center">
                        <b-button @click="handleImageClick"
                            :variant="form.image ? 'outline-danger' : 'outline-dark-brown'"
                            class="d-flex align-items-center">
                            <span>{{ form.image ? 'Eliminar imagen' : 'Agregar imagen' }}</span>
                            <b-icon :icon="form.image ? 'trash' : 'plus-circle'" class="ms-2"></b-icon>
                        </b-button>
                    </div>
                    <input type="file" ref="imageInput" @change="previewImage" accept="image/*"
                        style="display: none;" />
                    <div v-if="imagePreview" class="mt-3 mx-5 d-flex justify-content-center">
                        <img :src="imagePreview" alt="Vista previa de la imagen" class="img-fluid" />
                    </div>
                </b-form-group>
            </b-col>
            <b-col cols="12" class="mt-3">
                <b-form-group>
                    <label>Categoría: <b class="text-danger">*</b></label>
                    <multi-select :options="categories" v-model="form.category" placeholder="Selecciona una categoría"
                        label="name" track-by="name" :taggable="false" :allow-empty="false"
                        selectLabel="Presiona enter para seleccionar" selectedLabel="Seleccionado" deselectLabel="">
                    </multi-select>
                </b-form-group>
            </b-col>
            <b-col cols="12" class="mt-3">
                <b-form-group>
                    <label>Nombre: <b class="text-danger">*</b></label>
                    <b-form-input v-model="form.name" placeholder="Nombre del producto" required></b-form-input>
                </b-form-group>
            </b-col>
            <b-col cols="6" class="mt-3">
                <b-form-group>
                    <label>Precio: <b class="text-danger">*</b></label>
                    <b-form-input v-model="form.price" type="number" placeholder="Precio del producto"
                        required></b-form-input>
                </b-form-group>
            </b-col>
            <b-col cols="6" class="mt-3">
                <b-form-group>
                    <label>Existencias: <b class="text-danger">*</b></label>
                    <b-form-input v-model="form.stock" type="number" placeholder="Existencias del producto"
                        required></b-form-input>
                </b-form-group>
            </b-col>
            <b-col cols="12" class="mt-3">
                <b-form-group>
                    <label>Descripción: <b class="text-danger">*</b></label>
                    <b-form-textarea v-model="form.description" placeholder="Descripción del producto" rows="3"
                        required></b-form-textarea>
                </b-form-group>
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
    name: 'SaveProductForm',
    data() {
        return {
            categories: [
                { id: 0, name: 'Todas las categorías' },
                { id: 1, name: 'Pasteles' },
                { id: 2, name: 'Panqués' },
                { id: 3, name: 'Donas' },
                { id: 4, name: 'Galletas' },
                { id: 5, name: 'Bebidas calientes' },
                { id: 6, name: 'Bebidas frías' }
            ],
            form: {
                name: "",
                description: "",
                price: 0,
                stock: 0,
                category: null,
                image: null
            },
            imagePreview: null
        }
    },
    methods: {
        cleanForm() {
            this.form = {
                name: "",
                description: "",
                price: 0,
                stock: 0,
                category: null,
                image: null
            };
            this.imagePreview = null;
        },
        previewImage(event) {
            const file = event.target.files[0];
            if (file) {
                this.imagePreview = URL.createObjectURL(file);
                this.form.image = file;
            } else {
                this.imagePreview = null;
                this.form.image = null;
            }
        },
        handleImageClick() {
            if (this.form.image) {
                this.form.image = null;
                this.imagePreview = null;
                this.$refs.imageInput.value = null;
            } else {
                this.$refs.imageInput.click();
            }
        }
    }
}
</script>

<style scoped>
.img-fluid {
    max-width: 100%;
    height: auto;    
    border-radius: 0.25rem;
    object-fit: cover;
}
</style>
