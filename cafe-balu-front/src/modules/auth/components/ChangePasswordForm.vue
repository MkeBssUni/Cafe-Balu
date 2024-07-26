<template>
    <b-modal id="modal-change-password-form" ref="modal-change-password-form" centered hide-footer
        :no-close-on-backdrop="true" @closed="cleanForm()" @hidden="cleanForm()">
        <template #modal-header="{ close }">
            <h5 class="mb-0">Cambiar contraseña</h5>
            <b-icon @click="close()" class="ms-auto" icon="x" font-scale="1.6" cursor="pointer"></b-icon>
        </template>
        <b-row class="p-2">
            <b-col cols="12">
                <b-form-group>
                    <label for="password" class="mb-2">
                        Contraseña actual: <b class="text-danger">*</b>
                    </label>
                    <b-input-group>
                        <b-form-input id="password" :type="showCurrentPassword ? 'text' : 'password'"
                            placeholder="Ingrese su contraseña actual..."></b-form-input>
                        <b-button variant="outline-brown" @click="togglePassword(1)">
                            <b-icon :icon="showCurrentPassword ? 'eye' : 'eye-slash'"></b-icon>
                        </b-button>
                    </b-input-group>
                </b-form-group>
                <b-form-group class="mt-3">
                    <label for="new-password" class="mb-2">
                        Nueva contraseña: <b class="text-danger">*</b>
                    </label>
                    <b-input-group>
                        <b-form-input id="new-password" :type="showNewPassword ? 'text' : 'password'"
                            placeholder="Ingrese su nueva contraseña..."></b-form-input>
                        <b-button variant="outline-brown" @click="togglePassword(2)">
                            <b-icon :icon="showNewPassword ? 'eye' : 'eye-slash'"></b-icon>
                        </b-button>
                    </b-input-group>
                </b-form-group>
                <b-form-group class="mt-3">
                    <label for="confirm-password" class="mb-2">
                        Confirmación de contraseña: <b class="text-danger">*</b>
                    </label>
                    <b-input-group>
                        <b-form-input id="confirm-password" :type="showConfirmPassword ? 'text' : 'password'"
                            placeholder="Confirme su nueva contraseña..."></b-form-input>
                        <b-button variant="outline-brown" @click="togglePassword(3)">
                            <b-icon :icon="showConfirmPassword ? 'eye' : 'eye-slash'"></b-icon>
                        </b-button>
                    </b-input-group>
                </b-form-group>
            </b-col>
            <b-col cols="12" class="mt-5">
                <b-row class="d-flex justify-content-end">
                    <b-col cols="12" class="d-flex justify-content-end">
                        <b-button variant="outline-danger" class="me-2">
                            Cancelar
                        </b-button>
                        <b-button variant="outline-success">
                            Guardar
                        </b-button>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-modal>
</template>

<script>
export default {
    name: 'ChangePassword',
    data() {
        return {
            showCurrentPassword: false,
            showNewPassword: false,
            showConfirmPassword: false,
            form: {
                currentPassword: "",
                newPassword: "",
                confirmPassword: "",
            }
        }
    },
    methods: {
        togglePassword(field) {
            switch (field) {
                case 1:
                    this.showCurrentPassword = !this.showCurrentPassword;
                    break;
                case 2:
                    this.showNewPassword = !this.showNewPassword;
                    break;
                case 3:
                    this.showConfirmPassword = !this.showConfirmPassword;
                    break;
            }
        },
        cleanForm() {
            this.form = {
                currentPassword: "",
                newPassword: "",
                confirmPassword: "",
            };
        }
    }
}
</script>