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
                        :model-value="disorder"
                        :show-no-options="false"
                        track-by="id"
                        label="disorder"
                        @update:model-value="updateDisorderResponse"
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
                <h4>
                    Aménagements incontournables
                </h4>
            </b-col>
            <b-col class="text-right">
                <b-form-checkbox
                    v-model="editDisorderResponse"
                    switch
                >
                    <span class="text-secondary">Modifier</span>
                </b-form-checkbox>
            </b-col>
        </b-row>
        <b-overlay
            v-if="disorder.length > 0"
            :show="loading"
        >
            <b-row>
                <b-col
                    v-for="category, index in this.disorderResponseCategories"
                    :key="category.id"
                >
                    <b-card no-body>
                        <template #header>
                            <div class="d-flex justify-content-between">
                                <span>
                                    <strong class="text-primary">{{ category.name }}</strong>
                                    <b-badge variant="primary">
                                        {{ selectedRespList[index].length }}
                                    </b-badge>
                                    <b-icon
                                        v-if="category.explanation"
                                        v-b-popover.hover.top="category.explanation"
                                        icon="question-circle"
                                        variant="primary"
                                    />
                                </span>
                                <span v-if="editDisorderResponse">
                                    <b-btn
                                        size="sm"
                                        variant="outline-success"
                                        @click="showAddCustomResponse(category)"
                                    >
                                        <b-icon icon="plus" />
                                        Ajouter
                                    </b-btn>
                                </span>
                            </div>
                        </template>
                        <b-list-group
                            class="scrollable"
                            flush
                        >
                            <b-list-group-item
                                v-for="disorderResponse in editDisorderResponse ? allDisorderRespList[index] : selectedRespList[index]"
                                :key="`${disorderResponse.id}-${disorderResponse.response}`"
                                class="d-flex justify-content-between"
                                :variant="selectedRespList[index].find(selResp => disorderResponse.id === selResp.id) ? '' : 'info'"
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
                                        v-if="selectedRespList[index].find(selResp => disorderResponse.id === selResp.id)"
                                        @click="removeDisorderResponse(disorderResponse, category.id)"
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
            <b-row class="mt-2">
                <b-col>
                    <text-editor
                        :value="other_adjustments"
                        @input="$emit('update:other_adjustments', $event)"
                    />
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
                    v-for="category, index in this.disorderResponseCategories"
                    :key="category.id"
                >
                    <b-card no-body>
                        <template #header>
                            <div class="d-flex justify-content-between">
                                <span>
                                    <strong class="text-secondary">{{ category.name }}</strong>
                                    <b-badge>
                                        {{ notSelectedRespList[index].length }}
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
                                    v-for="disorderResponse in notSelectedRespList[index]"
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
        <b-modal
            id="add-custom-response"
            title="Ajouter une réponse personnalisée"
            ok-title="Ajouter"
            ok-variant="success"
            cancel-title="Annuler"
            @ok="addCustomResponse"
        >
            <b-form-group label="Réponse personnalisée">
                <b-input v-model="customResponse.text" />
            </b-form-group>
        </b-modal>
    </b-card>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { piaStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {

    props: [
        "disorderCareId",
        "date_start",
        "date_end",
        "disorder",
        "other_adjustments",
    ],
    data: function () {
        return {
            store: piaStore(),
            // eslint-disable-next-line no-undef
            disorderResponseCategories: disorderResponseCategories,
            selected_disorder_response: [],
            deselected: [],
            customResponse: { text: "" },
            customResponseCategory: null,
            editDisorderResponse: false,
            editorOptions: {
                modules: {
                    toolbar: [
                        ["bold", "italic", "underline", "strike"],
                        ["blockquote"],
                        [{ "list": "ordered" }, { "list": "bullet" }],
                        [{ "indent": "-1" }, { "indent": "+1" }],
                        [{ "align": [] }],
                        ["clean"]
                    ]
                },
                placeholder: ""
            },
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
    computed: {
        constDisorderRespList: function () {
            return this.disorderResponseCategories.map(category => {
                return this.store.disorderResponses.filter(
                    dR => dR.categories.includes(category.id)
                        && this.disorder.map(d => d.id).includes(dR.disorder)
                );
                // .map(dR => {
                //     console.log(category.id, dR.id);
                //     return this.selected_disorder_response.find(
                //         sDR => sDR.category === category.id && sDR.disorder_response === dR.id
                //     );
                //     return dR;
                // }).filter(dR => dR);
            });
        },
        customDisorderRespList: function () {
            return this.disorderResponseCategories.map(category => {
                return this.selected_disorder_response
                    .filter(s => s.custom_response.length > 0 && s.category === category.id)
                    .map(cS => {
                        return {
                            id: null,
                            disorder: this.disorder[0].id,
                            selected_disorder_response: cS,
                            response: cS.custom_response,
                        };
                    });
            });
        },
        selectedRespList: function () {
            return this.disorderResponseCategories.map((category, i) => {
                return this.customDisorderRespList[i]
                    .concat(this.selected_disorder_response.filter(sDR => sDR.category === category.id).map(sDR => {
                        return this.constDisorderRespList[i].find(disResp => sDR.disorder_response === disResp.id);
                    })).filter(sDR => sDR);
            });
        },
        notSelectedRespList: function () {
            return this.disorderResponseCategories.map((category, i) => {
                return this.constDisorderRespList[i]
                    .filter(r => {
                        const selected = this.selected_disorder_response
                            .find(sDR => sDR.disorder_response === r.id && sDR.category === category.id);
                        return selected === undefined;
                    });
            });
        },
        allDisorderRespList: function () {
            return this.disorderResponseCategories.map((category, i) => {
                return this.customDisorderRespList[i]
                    .concat(this.constDisorderRespList[i]);
            });
        }
    },
    methods: {
        updateDisorderResponse: function ($event) {
            this.$emit("update:disorder", $event);
        },
        removeDisorderResponse: function (disorderResponse, categoryId) {
            console.log(disorderResponse, categoryId);
            const sDRIndex = this.selected_disorder_response.findIndex(
                sDR => sDR.disorder_response === disorderResponse.id && sDR.category === categoryId
            );

            const removedResponse = this.selected_disorder_response.splice(sDRIndex, 1);

            if ("id" in removedResponse[0]) {
                this.deselected.push(removedResponse[0]);
            }
        },
        addDisorderResponse: function (disorderResponse, categoryId) {
            console.log(disorderResponse, categoryId);
            // Find an already removed response.
            const removedResponseIndex = this.deselected.findIndex(dR => dR.category === categoryId && dR.disorder_response === disorderResponse.id);
            if (removedResponseIndex >= 0) {
                this.selected_disorder_response.push(this.deselected.splice(removedResponseIndex, 1)[0]);
            }
            this.selected_disorder_response.push({
                disorder_care: this.disorderCareId,
                disorder_response: disorderResponse.id,
                category: categoryId,
                custom_response: "",
            });
        },
        showAddCustomResponse: function (category) {
            this.customResponseCategory = category;
            this.$bvModal.show("add-custom-response");
        },
        addCustomResponse: function (event) {
            if (this.customResponse.text.length === 0) {
                event.preventDefault();
                return;
            }

            const customResponse = {
                disorder_care: this.disorderCareId,
                category: this.customResponseCategory.id,
                disorder_response: null,
                custom_response: this.customResponse.text,
            };

            this.selected_disorder_response.push(customResponse);
            this.customResponse = { text: "" };
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
        this.loading = false;
    },
    components: {
        Multiselect,
        TextEditor,
    }
};
</script>

<style></style>
