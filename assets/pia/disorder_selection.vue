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
                <h4>
                    Aménagements raisonnables
                </h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group>
                    <b-select
                        :options="disorderCares"
                        value-field="id"
                        v-model="currentDisorderCare"
                        @change="saveBeforeChange"
                    />
                </b-form-group>
            </b-col>
            <b-col>
                <b-btn
                    variant="outline-secondary"
                    @click="copy"
                    :disabled="disorderCares.length === 0"
                >
                    <b-icon
                        icon="files"
                    />
                    Copier
                </b-btn>
                <b-btn
                    variant="success"
                    @click="add"
                >
                    <b-icon
                        icon="plus"
                    />
                    Ajouter
                </b-btn>
                <b-btn
                    variant="danger"
                    @click="remove"
                    :disabled="disorderCares.length === 0"
                >
                    <b-icon
                        icon="trash"
                    />
                    Supprimer
                </b-btn>
            </b-col>
        </b-row>
        <disorder-care
            v-if="currentDisorderCare"
            v-bind.sync="currentDisorderCareObj"
            :disorder-care-id="currentDisorderCare"
            ref="disorderCare"
        />
    </b-overlay>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";
import DisorderCare from "./disorder_care.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

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
                    const dCIndex = this.disorderCares.findIndex(
                        sA => sA.id === this.currentDisorderCare && sA.date_start === this.currentDisorderCareObj.date_start
                    );
                    const removedObj = this.disorderCares.splice(dCIndex, 1)[0];
                    if (this.disorderCares.length > 0) {
                        this.currentDisorderCare = this.disorderCares[0];
                    } else {
                        this.currentDisorderCare = null;
                    }
                    axios.delete(`/pia/api/disorder_care/${removedObj.id}/`, token);
                }
            });
        },
        saveBeforeChange: function (event) {
            if (this.pia < 0) {
                this.$bvModal.msgBoxOk("Sauvegarder avant de pouvoir créer un nouvel aménagement)");
            } else {
                this.save(this.pia)
                    .then(() => {
                        this.currentDisorderCare = event;
                    });
            }
        },
        save: function (piaId) {
            return new Promise((resolve) => {
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
            .then( () => {
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
