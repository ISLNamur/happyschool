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
                <h4>
                    Aménagements raisonnables
                </h4>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup>
                    <BFormSelect
                        :options="disorderCares"
                        value-field="id"
                        v-model="currentDisorderCare"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BButtonGroup>
                    <BButton
                        variant="outline-secondary"
                        @click="copy"
                        :disabled="disorderCares.length === 0"
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
                        :disabled="disorderCares.length === 0"
                    >
                        <IBiTrash />
                        Supprimer
                    </BButton>
                </BButtonGroup>
            </BCol>
        </BRow>
        <disorder-care
            v-if="currentDisorderCare"
            v-model:date_start="currentDisorderCareObj.date_start"
            v-model:date_end="currentDisorderCareObj.date_end"
            v-model:disorder="currentDisorderCareObj.disorder"
            v-model:other_adjustments="currentDisorderCareObj.other_adjustments"
            :disorder-care-id="currentDisorderCare"
            ref="disorderCare"
        />
    </BOverlay>
</template>

<script>
import axios from "axios";

import { useModalController } from "bootstrap-vue-next";

import { piaStore } from "./stores/index.js";
import DisorderCare from "./disorder_care.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { create } = useModalController();
        return { create };
    },
    props: {
        pia: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
            loading: false,
            disorderCares: [],
            currentDisorderCare: null,
            store: piaStore(),
        };
    },
    computed: {
        lastDisorder: function () {
            return this.disorderCares.length > 0 ? this.disorderCares[0] : null;
        },
        currentDisorderCareObj: function () {
            return this.currentDisorderCare ? this.disorderCares.find(dC => dC.id === this.currentDisorderCare) : null;
        }
    },
    methods: {
        add: function () {
            const newId = Math.min(Math.min(...this.disorderCares.map(dC => dC.id)), 0) - 1;
            this.disorderCares.push({
                id: newId,
                date_start: null,
                date_end: null,
                disorder: [],
                text: "Nouvel aménagement"
            });
            this.currentDisorderCare = newId;
        },
        copy: function () {
            let copy = Object.assign({}, this.currentDisorderCareObj);
            const newId = Math.min(Math.min(...this.disorderCares.map(dC => dC.id)), 0) - 1;
            copy.id = newId;
            copy.text = `Copie de ${copy.text}`;
            this.disorderCares.push(copy);
            this.currentDisorderCare = newId;
            this.$refs.disorderCare.resetSelectionId();
        },
        remove: function () {
            this.create(
                {
                    body: "Êtes-vous sûr de vouloir supprimer l'élément ?",
                    title: "Attention !",
                    okVariant: "danger",
                    okTitle: "Oui",
                    cancelTitle: "Non",
                }
            ).then((confirm) => {
                if (confirm.ok) {
                    const dCIndex = this.disorderCares.findIndex(
                        sA => sA.id === this.currentDisorderCare && sA.date_start === this.currentDisorderCareObj.date_start
                    );
                    if (this.disorderCares.length > 1) {
                        this.currentDisorderCare = this.disorderCares[0].id;
                    } else {
                        this.currentDisorderCare = null;
                    }
                    const removedObj = this.disorderCares.splice(dCIndex, 1)[0];
                    axios.delete(`/pia/api/disorder_care/${removedObj.id}/`, token);
                }
            });
        },
        save: function (piaId) {
            return new Promise((resolve) => {
                if (!this.currentDisorderCare) {
                    resolve();
                }
                const currentDisorderIndex = this.disorderCares.findIndex(dC => dC.id === this.currentDisorderCare);
                Promise.all(this.disorderCares.map(dC => {
                    let disorderCare = Object.assign({}, dC);
                    disorderCare.disorder = dC.disorder.map(d => d.id);
                    disorderCare.pia_model = piaId;
                    if (dC.id > 0) {
                        return axios.put(`/pia/api/disorder_care/${dC.id}/`, disorderCare, token);
                    } else {
                        return axios.post("/pia/api/disorder_care/", disorderCare, token);
                    }
                })).then((resps) => {
                    resps.forEach((r, i) => {
                        // Set id to disorder cares.
                        if (this.disorderCares[i].id < 0) {
                            this.disorderCares[i].id = r.data.id;
                        }
                    });
                    this.currentDisorderCare = this.disorderCares[currentDisorderIndex].id;
                    this.$refs.disorderCare.save(this.currentDisorderCare).then(() => {
                        resolve();
                    });
                });
            });
        }
    },
    mounted: function () {
        this.loading = true;
        this.store.loadOptions()
            .then(() => {
                if (this.pia) {
                    axios.get(`/pia/api/disorder_care/?pia_model=${this.pia}`)
                        .then((resp) => {
                            this.disorderCares = resp.data.results.map(dC => {
                                dC.text = `Du ${dC.date_start} au ${dC.date_end}`;
                                dC.disorder = dC.disorder.map(dis => this.store.disorders.find(d => d.id === dis));
                                return dC;
                            });
                            this.currentDisorderCare = this.lastDisorder ? this.lastDisorder.id : null;
                            this.loading = false;
                        });
                } else {
                    this.currentDisorderCare = null;
                    this.loading = false;
                }
            });
    },
    components: {
        DisorderCare
    }
};
</script>
