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
    <BContainer>
        <BRow>
            <BCol>
                <h2>Avertir les parents de la sanction</h2>
            </BCol>
        </BRow>
        <BRow class="mb-1">
            <BCol>
                <BButton to="/">
                    Retour
                </BButton>
                <BButton
                    @click="getPDF"
                    variant="outline-primary"
                >
                    <IBiFileText />
                    Télécharger PDF
                </BButton>
            </BCol>
        </BRow>
        <BRow v-if="sanction && sanction.notified">
            <BCol>
                <BAlert
                    show
                    variant="warning"
                >
                    La sanction a déjà été notifié.
                </BAlert>
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
            </BCol>
        </BRow>
        <BRow>
            <BCol>
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
                    >
                        <template #noResult>
                            Aucun responsable trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BButton
                    variant="outline-secondary"
                    @click="addAskPerson"
                    size="sm"
                >
                    <IBiPlus />
                    Ajouter le demandeur
                </BButton>
            </BCol>
        </BRow>
        <BRow
            v-if="sanction"
            class="mt-2"
        >
            <BCol>
                <p style="font-family: sans-serif; font-size: 16px; font-weight: bold; margin: 0; Margin-bottom: 15px;">
                    {{ sanction.sanction_decision.sanction_decision }}
                </p>
                <p
                    style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 0px;"
                >
                    Concerne : <strong>{{ sanction.student.last_name }} {{ sanction.student.first_name }}</strong>
                </p>
                <p
                    v-if="sanction.student.classe"
                    style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 0px;"
                >
                    Classe : <strong>{{ sanction.student.classe.year }}{{ sanction.student.classe.letter.toUpperCase()
                    }}</strong>
                </p>
                <p
                    style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;"
                >
                    Objet : <strong>Mesure disciplinaire</strong>
                </p>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <text-editor v-model="text" />
            </BCol>
        </BRow>
        <BRow class="mt-2">
            <BCol>
                <BOverlay :show="sending">
                    <BButton
                        variant="primary"
                        @click="send"
                    >
                        Envoyer
                    </BButton>
                </BOverlay>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>
import TextEditor from "@s:core/js/common/text_editor.vue";

import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { useToastController } from "bootstrap-vue-next";

import { getPeopleByName } from "@s:core/js/common/search.js";

import { askSanctionsStore } from "./stores/ask_sanctions.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        id: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
            sanction: null,
            recipient: [],
            recipientOptions: [
                { "text": "Père", "value": "father" },
                { "text": "Mère", "value": "mother" },
                { "text": "Responsable légal", "value": "resp" },
                { "text": "Responsable à l'école", "value": "resp_school" },
            ],
            otherRecipients: [],
            responsibleOptions: [],
            searchId: 0,
            text: "",
            sending: false,
            store: askSanctionsStore(),
        };
    },
    methods: {
        send: function () {
            const data = {
                msg: this.text,
                cas_id: this.id,
                recipients: this.recipient,
                other_recipients: this.otherRecipients.map(r => r.pk),
            };
            this.sending = true;
            axios.post("/dossier_eleve/api/warn_sanction/", data, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/").then(() => {
                        this.show({props: {
                            body: "Le message a bien été envoyé.",
                            variant: "success",
                            noCloseButton: true,
                        }});
                    });
                })
                .catch(err => {
                    console.log(err);
                    this.sending = false;
                });
        },
        getPDF: function () {
            const data = {
                sanction: this.id,
                text: this.text,
            };
            axios.post("/dossier_eleve/get_pdf_sanction/", data, {
                responseType: "blob",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken"
            })
                .then(resp => {
                    const blob = new Blob([resp.data], { type: "application/pdf" });
                    var link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "sanction.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });

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
        addAskPerson: function () {
            const askPersonName = this.sanction.demandeur.split("—")[0].trim();
            axios.get(`/annuaire/api/people/?query=${askPersonName}&people_type=responsible`)
                .then((respSearch) => {
                    if (respSearch.data.length === 1) {
                        this.otherRecipients.push(respSearch.data[0]);
                    }
                });
        }
    },
    mounted: function () {
        axios.get(`/dossier_eleve/api/ask_sanctions/${this.id}/`)
            .then(resp => {
                this.sanction = resp.data;

            });
        axios.get(`/dossier_eleve/api/template_sanction/${this.id}/`)
            .then(resp => {
                this.text = resp.data;
            });
    },
    components: {
        TextEditor,
        Multiselect,
    }
};
</script>
