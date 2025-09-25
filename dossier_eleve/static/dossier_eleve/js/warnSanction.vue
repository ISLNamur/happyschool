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
        <BOverlay :show="loading">
            <mail-template v-if="sanction && baseTemplate" :student-id="sanction.student.matricule"
                :teachings="store.settings.teachings" title="Avertir les parents de la sanction"
                get-pdf-url="/dossier_eleve/get_pdf_sanction/" get-pdf-filename="sanction.pdf"
                :base-template="baseTemplate" :extra-recipients="askPerson" @sending="send" ref="template">
                <template #side>
                    <BCol>
                        <div class="mt-4 ms-4">
                            <p
                                style="font-family: sans-serif; font-size: 16px; font-weight: bold; margin: 0; Margin-bottom: 15px;">
                                {{ sanction.sanction_decision.sanction_decision }}
                            </p>
                            <p
                                style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 0px;">
                                Concerne : <strong>{{ sanction.student.last_name }} {{ sanction.student.first_name
                                    }}</strong>
                            </p>
                            <p v-if="sanction.student.classe"
                                style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 0px;">
                                Classe : <strong>{{ sanction.student.classe.year }}{{
                                    sanction.student.classe.letter.toUpperCase()
                                    }}</strong>
                            </p>
                            <p
                                style="font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; Margin-bottom: 15px;">
                                Objet : <strong>Mesure disciplinaire</strong>
                            </p>
                            <BButton variant="outline-secondary" @click="addAskPerson" size="sm">
                                <IBiPlus />
                                Ajouter le demandeur
                            </BButton>
                        </div>
                    </BCol>
                </template>
            </mail-template>
        </BOverlay>
    </BContainer>
</template>

<script>
import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

import MailTemplate from "@s:core/js/common/MailTemplate.vue";
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
            baseTemplate: undefined,
            loading: false,
            store: askSanctionsStore(),
        };
    },
    methods: {
        addAskPerson: function () {
            const askPersonName = this.sanction.demandeur.split("—")[0].trim();
            this.$refs.template.getResponsible(askPersonName, true);
        },
        send: function (data) {
            this.loading = true;
            const completeData = Object.assign({ cas_id: this.sanction.id }, data);
            axios.post("/dossier_eleve/api/warn_sanction/", completeData, token)
                .then(() => {
                    this.loading = false;
                    this.$router.push("/").then(() => {
                        this.show({
                            body: "Le message a bien été envoyé.",
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch(err => {
                    console.log(err);
                    this.loading = false;
                });
        },
    },
    mounted: function () {
        this.loading = true;
        axios.get(`/dossier_eleve/api/ask_sanctions/${this.id}/`)
            .then(resp => {
                this.sanction = resp.data;
                this.loading = false;
            })
            .catch(err => {
                console.log(err);
                this.loading = false;
            });

        axios.get(`/dossier_eleve/api/template_sanction/${this.id}/`)
            .then(resp => {
                this.baseTemplate = resp.data;
            });
    },
    components: {
        MailTemplate,
    }
};
</script>
