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
    <b-container>
        <b-row>
            <b-col>
                <h2>Avertir les parents du retard</h2>
            </b-col>
        </b-row>
        <b-row class="mb-1 text-right">
            <b-col>
                <b-btn
                    @click="getPDF"
                    variant="outline-primary"
                >
                    <b-icon icon="file-text" />
                    Télécharger PDF
                </b-btn>
            </b-col>
        </b-row>

        <b-row v-if="student">
            <b-col>
                Éleve concerné : <strong>{{ displayStudent(student) }}</strong>
            </b-col>
        </b-row>

        <b-row>
            <b-col>
                <b-form-group
                    label="Destinataires"
                    description="Si deux destinataires sont les mêmes, un seul courriel sera envoyé."
                >
                    <b-form-checkbox-group
                        v-model="recipient"
                        :options="recipientOptions"
                    />
                </b-form-group>
                <b-form-group label="Autres personnes de l'école">
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
                    >
                        <template #noResult>
                            Aucun responsable trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-form-group>
            </b-col>
            <b-col
                cols="12"
                md="4"
            >
                <b-card
                    no-body
                    class="scrollable"
                    header="Derniers retards"
                >
                    <b-list-group>
                        <b-list-group-item
                            v-for="lateness in lastLatenesses"
                            :key="lateness.id"
                            class="d-flex justify-content-between align-items-center"
                        >
                            <span>
                                {{ niceDate(lateness.datetime_creation) }}
                            </span>
                            <span v-if="lateness.justified">
                                <strong>Justifié</strong>
                            </span>
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col>
                <text-editor v-model="text" />
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col>
                <b-overlay :show="sending">
                    <b-btn
                        variant="primary"
                        @click="send"
                    >
                        Envoyer
                    </b-btn>
                </b-overlay>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import axios from "axios";
import Moment from "moment";
import "moment/dist/locale/fr";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { getPeopleByName } from "@s:core/js/common/search.js";
import { displayStudent } from "@s:core/js/common/utilities";

import { latenessStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        studentId: {
            type: String,
            default: "-1"
        }
    },
    data: function () {
        return {
            recipient: ["resp_school"],
            recipientOptions: [
                { "text": "Père", "value": "father" },
                { "text": "Mère", "value": "mother" },
                { "text": "Responsable légal", "value": "resp" },
                { "text": "Responsable à l'école", "value": "resp_school" },
            ],
            responsibleOptions: [],
            otherRecipients: [],
            lastAbsences: [],
            absenceWarned: [],
            text: "",
            searchId: -1,
            sending: false,
            student: null,
            store: latenessStore()
        };
    },
    methods: {
        displayStudent,
        niceDate: function (dateStr) {
            return Moment(dateStr).format("HH:mm DD/MM");
        },
        getResponsible: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "responsible")
                .then((resp) => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                    // this.searching = false;
                })
                .catch((err) => {
                    alert(err);
                    // this.searching = false;
                });
        },
        send: function () {
            const data = {
                msg: this.text,
                student_id: this.studentId,
                recipients: this.recipient,
                other_recipients: this.otherRecipients.map(r => r.pk),
            };
            this.sending = true;
            axios.post("/lateness/api/mail_warning/", data, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/", () => {
                        this.$root.$bvToast.toast("Le message a bien été envoyé.", {
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch(err => {
                    console.log(err);
                    this.sending = false;
                });
        },
        getPDF: function () {
            const data = {
                student_id: this.studentId,
                text: this.text,
            };
            axios.post("/lateness/get_pdf_warning/", data, {
                responseType: "blob",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken"
            })
                .then(resp => {
                    const blob = new Blob([resp.data], { type: "application/pdf" });
                    var link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "retards.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });

        },
    },
    mounted: function () {
        axios.get(`/lateness/api/lateness/?student__matricule=${this.studentId}&activate_after_count=true&ordering=-datetime_creation`)
            .then((resp) => {
                this.lastLatenesses = resp.data.results;

                if (this.lastLatenesses.length === 0) {
                    return;
                }

                this.student = this.lastLatenesses[0].student;
                axios.get(`/lateness/api/mail_warning_template/${this.studentId}/`)
                    .then((templateResp) => {
                        this.text = templateResp.data;
                    });
            });
    },
    components: {
        Multiselect,
        TextEditor
    }
};
</script>

<style>
.scrollable {
    height:400px;
    overflow-y: scroll;
}
</style>
