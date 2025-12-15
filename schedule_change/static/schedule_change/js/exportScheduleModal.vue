<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <BModal
        size="lg"
        title="Exporter un récapitulatif"
        cancel-title="Annuler"
        :ok-disabled="!export_to || !export_from || processing"
        ref="exportModal"
        @hidden="resetModal"
    >
        <template #footer>
            <BButton
                variant="primary"
                :href="summaryUrl"
                target="_blank"
                rel="noopener noreferrer"
                @click="$refs.exportModal.hide()"
            >
                {{ buttonOkText }}
            </BButton>
        </template>
        <BRow class="mt-2">
            <BCol>
                <BFormRow>
                    <BFormGroup label="À partir du">
                        <input
                            type="date"
                            v-model="export_from"
                            :max="export_to"
                        >
                    </BFormGroup>
                </BFormRow>
            </BCol>
            <BCol>
                <BFormRow>
                    <BFormGroup label="Jusqu'au">
                        <input
                            type="date"
                            v-model="export_to"
                            :min="export_from"
                        >
                    </BFormGroup>
                </BFormRow>
            </BCol>
        </BRow>
        <BRow
            class="ml-2"
            v-if="store.canAdd"
        >
            <BFormGroup>
                <BFormCheckbox v-model="sendToTeachers">
                    Envoyer le récapitulatif aux enseignants concernés
                </BFormCheckbox>
            </BFormGroup>
        </BRow>
        <BRow>
            <BCol>
                <BFormTextarea
                    v-if="sendToTeachers"
                    v-model="message"
                    placeholder="Message à inclure dans l'email"
                    rows="3"
                    max-rows="6"
                    maxlength="240"
                />
            </BCol>
        </BRow>
    </BModal>
</template>

<script>
import { scheduleChangeStore } from "./stores/index.js";

export default {
    data: function () {
        return {
            export_to: null,
            export_from: null,
            buttonStr: "Créer le pdf",
            sendToTeachers: false,
            message: "",
            processing: false,
            store: scheduleChangeStore(),
        };
    },
    watch: {
        sendToTeachers: function (state) {
            if (state) {
                this.buttonStr = "Créer le PDF et envoyer";
            } else {
                this.buttonStr = "Créer le PDF";
            }
        },
        export_from: function (state) {
            if (state && !this.export_to) {
                this.export_to = this.export_from;
            }
        },
    },
    computed: {
        summaryUrl: function () {
            return "/schedule_change/api/summary_pdf/?page_size=500&date_change__gte="
              + `${this.export_from}&date_change__lte=${this.export_to}&send_to_teachers=${this.sendToTeachers}`
              + `&message=${encodeURIComponent(this.message)}`;
        },
        buttonOkText: function () {
            if (this.sendToTeachers) {
                return "Créer le PDF et envoyer";
            }
            return "Créer le PDF";
        },
    },
    methods: {
        show: function () {
            this.$refs.exportModal.show();
        },
        resetModal: function () {
            Object.assign(this.$data, this.$options.data.call(this));
        },
    },
};
</script>
