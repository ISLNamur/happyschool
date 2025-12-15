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
    <BRow>
        <BCol>
            <slot name="title">
                <h2>{{ title }}</h2>
            </slot>
        </BCol>
    </BRow>
    <BRow class="mb-1 text-right">
        <BCol>
            <BButton
                @click="getPDF"
                variant="outline-primary"
            >
                <IBiFileText />
                Télécharger PDF
            </BButton>
        </BCol>
    </BRow>

    <BRow v-if="student">
        <BCol>
            Éleve concerné : <strong>{{ displayStudent(student) }}</strong>
        </BCol>
    </BRow>

    <BRow>
        <BCol>
            <BFormGroup
                label="Destinataires"
                description="Si deux destinataires sont les mêmes, un seul courriel sera envoyé."
            >
                <BFormCheckboxGroup
                    v-model="recipient"
                    :options="recipientOptions"
                />
            </BFormGroup>
            <BFormGroup label="Autres personnes de l'école">
                <multiselect
                    id="responsible-0"
                    :internal-search="false"
                    :options="responsibleOptions"
                    @search-change="getResponsible"
                    placeholder="Ajouter une autre personne de l'école"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label="Cliquer dessus pour enlever"
                    v-model="otherRecipients"
                    label="display"
                    track-by="matricule"
                    :show-no-options="false"
                    multiple
                    ref="searchpeople"
                >
                    <template #noResult>
                        Aucun responsable trouvé.
                    </template>
                    <template #noOptions />
                </multiselect>
            </BFormGroup>
            <BFormGroup label="Expéditeurs">
                <BFormCheckboxGroup
                    v-model="replyTo"
                    :options="replyToOptions"
                />
            </BFormGroup>
            <BFormGroup label="Modèle">
                <BInputGroup v-if="templateOptions.length > 0">
                    <BFormSelect
                        v-model="template"
                        :options="templateOptions"
                        text-field="name"
                        value-field="id"
                        @update:model-value="getTemplate"
                    />
                    <BButton
                        :disabled="!template"
                        @click="getTemplate(template)"
                    >
                        <IBiArrowRepeat />
                    </BButton>
                </BInputGroup>
            </BFormGroup>
        </BCol>
        <BCol v-if="$slots.side">
            <slot name="side" />
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BCol>
            <text-editor v-model="text" />
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BCol>
            <BButton
                variant="primary"
                @click="send"
            >
                Envoyer
            </BButton>
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { useToastController } from "bootstrap-vue-next";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { getPeopleByName } from "@s:core/js/common/search.js";
import { displayStudent } from "@s:core/js/common/utilities";

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    emits: ["sending"],
    props: {
        studentId: {
            type: String,
            default: "-1",
        },
        teachings: {
            type: Array,
            default: () => [],
        },
        title: {
            type: String,
            default: "Send email",
        },
        getPdfUrl: {
            type: String,
            default: "/api/pdf/",
        },
        getPdfFilename: {
            type: String,
            default: "email.pdf",
        },
        templateUrl: {
            type: String,
            default: undefined,
        },
        templateContext: {
            type: Object,
            default: () => { },
        },
        baseTemplate: {
            type: String,
            default: "",
        },
    },
    data: function () {
        return {
            recipient: [],
            recipientOptions: [
                { text: "Père", value: "father" },
                { text: "Mère", value: "mother" },
                { text: "Élève (si disponible)", value: "student" },
                { text: "Responsable légal", value: "resp" },
                { text: "Responsable à l'école", value: "resp_school" },
            ],
            replyTo: [],
            replyToOptions: [],
            responsibleOptions: [],
            otherRecipients: [],
            template: null,
            templateOptions: [],
            text: "",
            searchId: -1,
            student: null,
        };
    },
    methods: {
        displayStudent,
        getResponsible: function (searchQuery, autoAdd) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "responsible")
                .then((resp) => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;

                    if (autoAdd && this.responsibleOptions.length === 1) {
                        this.otherRecipients.push(this.responsibleOptions[0]);
                    } else if (autoAdd) {
                        this.$refs.searchpeople.activate();
                    }
                })
                .catch((err) => {
                    alert(err);
                    // this.searching = false;
                });
        },
        send: function () {
            // Check if at least one reply to is selected.
            if (this.replyTo.length == 0) {
                this.show({
                    body: "Vous devez sélectionner au moins un expéditeur.",
                    variant: "danger",
                    noCloseButton: true,
                });
                return;
            }
            const data = {
                msg: this.text,
                student_id: this.studentId,
                recipients: this.recipient,
                other_recipients: this.otherRecipients.map(r => r.pk),
                reply_to: this.replyTo,
            };
            this.$emit("sending", data);
        },
        getTemplate: function (templateId) {
            const data = Object.assign({ student: this.studentId }, this.templateContext);
            axios.get(`${this.templateUrl}${templateId}/`, { params: data })
                .then((resp) => {
                    this.text = resp.data;
                });
        },
        getPDF: function () {
            const data = Object.assign(
                {
                    student_id: this.studentId,
                    text: this.text,
                },
                this.templateContext,
            );

            axios.post(this.getPdfUrl, data, {
                responseType: "blob",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
            })
                .then((resp) => {
                    const blob = new Blob([resp.data], { type: "application/pdf" });
                    var link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = this.getPdfFilename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
        },
    },
    mounted: function () {
        if (this.templateUrl) {
            axios.get(this.templateUrl)
                .then((resp) => {
                    this.templateOptions = resp.data.results;
                });
        }

        if (this.studentId) {
            axios.get(`/annuaire/api/school_responsible/${this.studentId}/`)
                .then((resp) => {
                    this.replyToOptions = Object.entries(resp.data).map((person) => {
                        return { text: person[1], value: person[0] };
                    });
                    this.replyTo = this.replyToOptions.map(rT => rT.value);
                });
        }

        this.text = this.baseTemplate;
    },
    components: {
        Multiselect,
        TextEditor,
    },
};
</script>

<style>
.scrollable {
    height: 400px;
    overflow-y: scroll;
}
</style>
