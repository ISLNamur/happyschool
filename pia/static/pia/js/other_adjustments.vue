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
    <b-overlay :show="loading">
        <b-row>
            <b-col>
                <h4 class="mt-4">
                    Aménagements spécifiques
                </h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group>
                    <b-select
                        :options="otherAdjustments"
                        value-field="id"
                        v-model="currentOtherAdjId"
                        @change="updatecurrentOtherAdj"
                    />
                </b-form-group>
            </b-col>
            <b-col>
                <b-btn
                    variant="outline-secondary"
                    @click="copy"
                    :disabled="otherAdjustments.length === 0"
                >
                    <b-icon icon="files" />
                    Copier
                </b-btn>
                <b-btn
                    variant="success"
                    @click="add"
                >
                    <b-icon icon="plus" />
                    Ajouter
                </b-btn>
                <b-btn
                    variant="danger"
                    @click="remove"
                    :disabled="otherAdjustments.length === 0"
                >
                    <b-icon icon="trash" />
                    Supprimer
                </b-btn>
            </b-col>
        </b-row>
        <b-row v-if="currentOtherAdj">
            <b-col>
                <b-card>
                    <b-row class="mb-1">
                        <b-col>
                            <strong>
                                <b-form inline>
                                    Du<b-form-input
                                        type="date"
                                        v-model="currentOtherAdj.date_start"
                                        class="mr-sm-2 ml-2"
                                    />
                                    au<b-form-input
                                        type="date"
                                        v-model="currentOtherAdj.date_end"
                                        class="ml-2"
                                    />
                                </b-form>
                            </strong>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <text-editor v-model="currentOtherAdj.other_adjustments" />
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>
        </b-row>
    </b-overlay>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

import TextEditor from "@s:core/js/common/text_editor.vue";


export default {
    props: {
        pia: {
            type: Number,
            default: -1
        }
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
                { other_adjustments: "", id: newId, date_start: null, date_end: null, text: "Nouvel aménagement" }
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
            this.$bvModal.msgBoxConfirm(
                "Êtes-vous sûr de vouloir supprimer l'élément ?",
                {
                    title: "Attention !",
                    okVariant: "danger",
                    okTitle: "Oui",
                    cancelTitle: "Non",
                },
            ).then((confirm) => {
                if (confirm) {
                    const sAIndex = this.otherAdjustments.findIndex(
                        sA => sA.id === this.currentOtherAdj.id && sA.date_start === this.currentOtherAdj.date_start
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
                    this.otherAdjustments.map(sA => {
                        const isNew = sA.id < 0;
                        const send = isNew ? axios.post : axios.put;
                        const url = `/pia/api/other_adjustments/${isNew ? "" : sA.id + "/"}`;

                        // Copy other adjustment for sending.
                        let data = Object.assign({}, sA);
                        data.pia_model = piaId;
                        return send(url, data, token);
                    })
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
            this.otherAdjustments = otherAdjustments.sort((a, b) => a.date_start < b.date_start).map(oA => {
                oA.text = `Du ${oA.date_start} au ${oA.date_end}`;
                return oA;
            });

            if (this.otherAdjustments.length > 0) {
                this.currentOtherAdj = this.otherAdjustments[0];
                this.currentOtherAdjId = this.otherAdjustments[0].id;
            }
        }
    },
    components: {
        TextEditor
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
    }
};
</script>
