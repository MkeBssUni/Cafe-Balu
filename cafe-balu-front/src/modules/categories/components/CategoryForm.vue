<template>
    <b-modal id="modal-category-form" ref="modal-category-form" centered scrollable hide-footer
        :no-close-on-backdrop="true" @closed="cleanForm()" @hidden="cleanForm()">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Registrar categoría</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row class="p-2">
            <b-col cols="12">
                <b-form-group>
                    <label>Nombre: <b class="text-danger">*</b></label>
                    <b-form-input v-model="form.name" placeholder="Nombre de la categoría" required></b-form-input>
                </b-form-group>
            </b-col>
            <b-col cols="12" class="mt-3">
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
    name: 'CategoryForm',
    data() {
        return {
            form: {
                name: "",
            }
        }
    },
    methods: {
        cleanForm() {
            this.form = {
                name: "",
            };
        }
    }
}
</script>