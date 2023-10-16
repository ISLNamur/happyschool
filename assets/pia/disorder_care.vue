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
    <b-card>
        <b-row class="mb-1">
            <b-col>
                <strong>
                    <b-form inline>
                        Du<b-form-input
                            type="date"
                            :value="date_start"
                            @input="$emit('update:date_start', $event)"
                            class="mr-sm-2 ml-2"
                        />
                        au<b-form-input
                            type="date"
                            :value="date_end"
                            @input="$emit('update:date_end', $event)"
                            class="ml-2"
                        />
                    </b-form>
                </strong>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group
                    label="Trouble d'apprentissage"
                    label-cols="3"
                >
                    <multiselect
                        :options="store.disorders"
                        placeholder="Sélectionner le ou les différents troubles"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        :value="disorder"
                        :show-no-options="false"
                        track-by="id"
                        label="disorder"
                        @input="updateDisorderResponse"
                        multiple
                    >
                        <template #noResult>
                            Aucun trouble trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <h4>Aménagements incontournables</h4>
            </b-col>
        </b-row>
        <b-overlay
            v-if="disorder.length > 0"
            :show="loading"
        >
            <b-row>
                <b-col
                    v-for="category in this.disorderResponseCategories"
                    :key="category.id"
                >
                    <b-card no-body>
                        <template #header>
                            <div class="d-flex justify-content-between">
                                <span>
                                    <strong class="text-primary">{{ category.name }}</strong>
                                    <b-badge variant="primary">
                                        {{ disorderResponsesByCat(category.id, false, true).length }}
                                    </b-badge>
                                    <b-icon
                                        v-if="category.explanation"
                                        v-b-popover.hover.top="category.explanation"
                                        icon="question-circle"
                                        variant="primary"
                                    />
                                </span>
                                <b-form-checkbox
                                    v-model="editDisorderResponse"
                                    switch
                                >
                                    <span class="text-secondary">Modifier</span>
                                </b-form-checkbox>
                            </div>
                        </template>
                        <b-list-group
                            class="scrollable"
                            flush
                        >
                            <b-list-group-item
                                v-for="disorderResponse in disorderResponsesByCat(category.id, editDisorderResponse, true)"
                                :key="disorderResponse.id"
                                class="d-flex justify-content-between"
                                :variant="disorderResponse.selected_disorder_response ? '' : 'info'"
                            >
                                <span>
                                    <b-icon icon="chevron-compact-right" />
                                    {{ disorderResponse.response }}
                                    (<em>{{ disorder.find(d => d.id === disorderResponse.disorder).disorder }}</em>)
                                </span>
                                <span
                                    v-if="editDisorderResponse"
                                    class="ml-2"
                                >
                                    
                                    <b-btn
                                        size="sm"
                                        variant="danger"
                                        v-if="disorderResponse.selected_disorder_response"
                                        @click="removeDisorderResponse(disorderResponse.id, category.id)"
                                    >
                                        <b-icon icon="x" />
                                    </b-btn>
                                    <b-btn
                                        v-else
                                        size="sm"
                                        variant="success"
                                        @click="addDisorderResponse(disorderResponse, category.id)"
                                    >
                                        <b-icon icon="check" />
                                    </b-btn>
                                </span>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </b-col>
            </b-row>
            <b-row v-if="disorder.length > 0">
                <b-col>
                    <h4 class="mt-4">
                        Aménagements conseillés
                    </h4>
                </b-col>
            </b-row>
            <b-row
                v-if="disorder.length > 0"
                class="mb-2"
            >
                <b-col
                    v-for="category in this.disorderResponseCategories"
                    :key="category.id"
                >
                    <b-card no-body>
                        <template #header>
                            <div class="d-flex justify-content-between">
                                <span>
                                    <strong class="text-secondary">{{ category.name }}</strong>
                                    <b-badge>
                                        {{ disorderResponsesByCat(category.id, false, false).length }}
                                    </b-badge>
                                </span>
                                <b-btn
                                    size="sm"
                                    variant="outline-info"
                                    v-b-toggle="`adviced-response-cat-${category.id}`"
                                >
                                    <b-icon icon="chevron-bar-expand" />
                                </b-btn>
                            </div>
                        </template>
                        <b-collapse :id="`adviced-response-cat-${category.id}`">
                            <b-list-group
                                flush
                                class="scrollable"
                            >
                                <b-list-group-item
                                    v-for="disorderResponse in disorderResponsesByCat(category.id, false, false)"
                                    :key="disorderResponse.id"
                                    class="d-flex justify-content-between"
                                >
                                    <span>
                                        <b-icon icon="chevron-compact-right" />
                                        {{ disorderResponse.response }}
                                        (<em>{{ disorder.find(d => d.id === disorderResponse.disorder).disorder }}</em>)
                                    </span>
                                </b-list-group-item>
                            </b-list-group>
                        </b-collapse>
                    </b-card>
                </b-col>
            </b-row>
        </b-overlay>
    </b-card>
</template>

<script>
import axios from "axios";
 
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import { piaStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: [
        "disorderCareId",
        "date_start",
        "date_end",
        "disorder"
    ],
    data: function () {
        return {
            store: piaStore(),
            // eslint-disable-next-line no-undef
            disorderResponseCategories: disorderResponseCategories,
            selected_disorder_response: [],
            deselected: [],
            editDisorderResponse: false,
            inputStates: {
                date_start: null,
                date_end: null,
            },
            loading: true,
        };
    },
    watch: {
        disorderCareId: function () {
            this.loadSelected();
        }
    },
    methods: {
        updateDisorderResponse: function ($event) {
            this.$emit("update:disorder", $event);
        },
        disorderResponsesByCat: function (categoryId, showAll, selectionned) {
            const responses = this.store.disorderResponses.filter(
                dR => dR.categories.includes(categoryId)
                && this.disorder.map(d => d.id).includes(dR.disorder)
            ).map(dR => {
                dR.selected_disorder_response = this.selected_disorder_response.find(
                    sDR => sDR.category === categoryId && sDR.disorder_response === dR.id
                );
                return dR;
            });

            if (showAll) {
                return responses;
            } else {
                if (selectionned) {
                    return responses.filter(r => r.selected_disorder_response);
                } else {
                    return responses.filter(r => !r.selected_disorder_response);
                }
            }
        },
        removeDisorderResponse: function (disorderResponseId, categoryId) {
            const sDRIndex = this.selected_disorder_response.findIndex(
                sDR => sDR.disorder_response === disorderResponseId && sDR.category === categoryId
            );
            const removedResponse = this.selected_disorder_response.splice(sDRIndex, 1);
            if ("id" in removedResponse[0]) {
                this.deselected.push(removedResponse[0]);
            }
        },
        addDisorderResponse: function (disorderResponse, categoryId) {
            // Find an already removed response.
            const removedResponseIndex = this.deselected.findIndex(dR => dR.category === categoryId && dR.disorder_response === disorderResponse.id);
            if (removedResponseIndex >= 0) {
                this.selected_disorder_response.push(this.deselected.splice(removedResponseIndex, 1)[0]);
            }
            this.selected_disorder_response.push({
                disorder_response: disorderResponse.id, category: categoryId
            });
        },
        resetSelectionId: function () {
            this.selected_disorder_response.forEach(sDR => {
                delete sDR["id"];
            });
        },
        save: function (disorderCareId) {
            return new Promise(resolve => {
                const baseUrl = "/pia/api/selected_disorder_response_new/";
                Promise.all(
                    this.selected_disorder_response.map(dR => {
                        const method = dR.id > 0 ? axios.put : axios.post;
                        const url = dR.id > 0 ? `${baseUrl}${dR.id}/` : baseUrl;
                        let data = Object.assign({}, dR);
                        data.disorder_care = disorderCareId;
                        return method(url, data, token);
                    }).concat(
                        this.deselected.map(desel => axios.delete(`${baseUrl}${desel.id}/`, token))
                    )
                ).then(resps => {
                    this.selected_disorder_response = resps
                        .filter(resp => resp.config.method === "post" || resp.config.method === "put")
                        .map(resp => resp.data);
                    resolve();
                });
            });
        },
        loadSelected: function () {
            if (this.disorderCareId > 0) {
                axios.get(`/pia/api/selected_disorder_response_new/?disorder_care=${this.disorderCareId}`)
                    .then((resp) => {
                        this.selected_disorder_response = resp.data.results;
                        this.loading = false;
                    });
            } else {
                this.loading = false;
            }
        }
    },
    mounted: function () {
        this.loadSelected();
    },
    components: {
        Multiselect
    }
};
</script>

<style>

</style>
