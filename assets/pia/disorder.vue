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
                <b-form-group>
                    <b-select
                        :options="disorderCares"
                        value-field="id"
                        v-model="currentDisorderCare"
                    />
                </b-form-group>
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
        save: function (piaId) {
            return new Promise((resolve) => {
                Promise.all(this.disorderCares.map(dC => {
                    let disorderCare = Object.assign({}, dC);
                    disorderCare.disorder = dC.disorder.map(d => d.id);
                    disorderCare.pia_model = piaId;
                    if ("id" in dC) {
                        return axios.put(`/pia/api/disorder_care/${dC.id}/`, disorderCare, token);
                    } else {
                        return axios.post("/pia/api/disorder_care/", disorderCare, token);
                    }
                })).then((resps) => {
                    resps.forEach((r, i) => {
                        // Set id to disorder cares.
                        if (!("id" in this.disorderCares[i])) {
                            this.disorderCares[i].id = r.data.id;
                        }
                    });
                    this.$refs.disorderCare.save().then(() => {
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
                axios.get(`/pia/api/disorder_care/?pia_model=${this.pia}`)
                    .then((resp) => {
                        this.disorderCares = resp.data.results.map(dC => {
                            dC.text = `Du ${dC.date_start} au ${dC.date_end}`;
                            dC.disorder = dC.disorder.map(dis => this.store.disorders.find(d => d.id === dis));
                            return dC;
                        });
                        this.currentDisorderCare = this.lastDisorder ? this.lastDisorder.id : {};
                        this.loading = false;
                    });
            });
    },
    components: {
        DisorderCare
    }
};
</script>
