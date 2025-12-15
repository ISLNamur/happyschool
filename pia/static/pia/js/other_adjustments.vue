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
    <BOverlay :show="loading">
        <BRow>
            <BCol>
                <h4 class="mt-4">
                    Aménagements spécifiques
                </h4>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup>
                    <BFormSelect
                        :options="otherAdjustments"
                        value-field="id"
                        v-model="currentOtherAdjId"
                        @update:model-value="updatecurrentOtherAdj"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BButton
                    variant="outline-secondary"
                    @click="copy"
                    :disabled="otherAdjustments.length === 0"
                >
                    <IBiFiles />
                    Copier
                </BButton>
                <BButton
                    variant="success"
                    @click="add"
                >
                    <IBiPlus />
                    Ajouter
                </BButton>
                <BButton
                    variant="danger"
                    @click="remove"
                    :disabled="otherAdjustments.length === 0"
                >
                    <IBiTrash />
                    Supprimer
                </BButton>
            </BCol>
        </BRow>
        <BRow v-if="currentOtherAdj">
            <BCol>
                <BCard>
                    <BRow class="mb-1">
                        <BCol>
                            <strong>
                                <BForm inline>
                                    Du<BFormInput
                                        type="date"
                                        v-model="currentOtherAdj.date_start"
                                        class="mr-sm-2 ml-2"
                                    />
                                    au<BFormInput
                                        type="date"
                                        v-model="currentOtherAdj.date_end"
                                        class="ml-2"
                                    />
                                </BForm>
                            </strong>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <text-editor v-model="currentOtherAdj.other_adjustments" />
                        </BCol>
                    </BRow>
                </BCard>
            </BCol>
        </BRow>
    </BOverlay>
</template>

<script>
import axios from "axios";

import { useModalController } from "bootstrap-vue-next";

import { piaStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

import TextEditor from "@s:core/js/common/text_editor.vue";

export default {
    setup: function () {
        const { create } = useModalController();
        return { create };
    },
    props: {
        pia: {
            type: Number,
            default: -1,
        },
    },
    data: function () {
        return {
            loading: false,
            otherAdjustments: [],
            currentOtherAdjId: null,
            currentOtherAdj: { other_adjustments: "", id: -1 },
            store: piaStore(),
        };
    },
    methods: {
        add: function () {
            const newId = Math.min(Math.min(...this.otherAdjustments.map(sA => sA.id)), 0) - 1;
            this.otherAdjustments.push(
                { other_adjustments: "", id: newId, date_start: null, date_end: null, text: "Nouvel aménagement" },
            );
            this.currentOtherAdj = this.otherAdjustments[this.otherAdjustments.length - 1];
            this.currentOtherAdjId = newId;
        },
        copy: function () {
            let copy = Object.assign({}, this.currentOtherAdj);
            copy.id = Math.min(Math.min(...this.otherAdjustments.map(oA => oA.id)), 0) - 1;
            copy.text = `Copie de ${copy.text}`;
            this.otherAdjustments.push(copy);
            this.currentOtherAdj = this.otherAdjustments[this.otherAdjustments.length - 1];
            this.currentOtherAdjId = copy.id;
        },
        remove: function () {
            this.create({
                body: "Êtes-vous sûr de vouloir supprimer l'élément ?",
                title: "Attention !",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Non",
            }).then((confirm) => {
                if (confirm.ok) {
                    const sAIndex = this.otherAdjustments.findIndex(
                        sA => sA.id === this.currentOtherAdj.id && sA.date_start === this.currentOtherAdj.date_start,
                    );
                    const removedObj = this.otherAdjustments.splice(sAIndex, 1)[0];
                    this.currentOtherAdj = this.otherAdjustments[this.otherAdjustments.length - 1];
                    axios.delete(`/pia/api/other_adjustments/${removedObj.id}/`, token);
                }
            });
        },
        save: function (piaId) {
            return new Promise((resolve, reject) => {
                this.loading = true;
                Promise.all(
                    this.otherAdjustments.map((sA) => {
                        const isNew = sA.id < 0;
                        const send = isNew ? axios.post : axios.put;
                        const url = `/pia/api/other_adjustments/${isNew ? "" : sA.id + "/"}`;

                        // Copy other adjustment for sending.
                        let data = Object.assign({}, sA);
                        data.pia_model = piaId;
                        return send(url, data, token);
                    }),
                ).then((resps) => {
                    this.expandOtherAdjustment(resps.map(r => r.data));
                    this.loading = false;
                    resolve();
                }).catch((err) => {
                    console.log(err);
                    this.loading = false;
                    reject(err);
                });
            });
        },
        updatecurrentOtherAdj: function (selected) {
            this.currentOtherAdj = this.otherAdjustments.find(sA => sA.id === selected);
        },
        expandOtherAdjustment: function (otherAdjustments) {
            this.otherAdjustments = otherAdjustments.sort((a, b) => a.date_start < b.date_start).map((oA) => {
                oA.text = `Du ${oA.date_start} au ${oA.date_end}`;
                return oA;
            });

            if (this.otherAdjustments.length > 0) {
                this.currentOtherAdj = this.otherAdjustments[0];
                this.currentOtherAdjId = this.otherAdjustments[0].id;
            }
        },
    },
    components: {
        TextEditor,
    },
    mounted: function () {
        this.store.loadOptions()
            .then(() => {
                if (this.pia) {
                    axios.get(`/pia/api/other_adjustments/?pia_model=${this.pia}`)
                        .then((resp) => {
                            this.expandOtherAdjustment(resp.data.results);
                        });
                }
            });
    },
};
</script>
