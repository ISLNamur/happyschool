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
    <b-overlay
        :show="loading"
    >
        <b-card
            no-body
            class="mt-1"
            border-variant="info"
        >
            <b-card-header>
                <b-row>
                    <b-col v-if="!editMode && advanced">
                        <strong>{{ branch ? branch.branch : "Ne concerne pas une branche en particulier" }}</strong>
                    </b-col>
                    <b-col v-else-if="advanced">
                        <b-form-group
                            label="Branche"
                            label-cols="2"
                        >
                            <multiselect
                                :options="$store.state.branches"
                                placeholder="Choisisser une branche"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="branch"
                                :show-no-options="false"
                                label="branch"
                                track-by="id"
                            >
                                <template
                                    slot="singleLabel"
                                    slot-scope="props"
                                >
                                    <strong>{{ props.option.branch }}</strong>
                                </template>
                                <span slot="noResult">Aucune branche trouvée.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                    <b-col
                        cols="2"
                        class="text-right"
                    >
                        <b-btn
                            variant="light"
                            size="sm"
                            @click="editMode = !editMode; if (!editMode) $emit('save')"
                            class="card-link mb-1"
                        >
                            <b-icon
                                :icon="editMode ? 'check2-square' : 'pencil-square'"
                                variant="success"
                            />
                        </b-btn>    
                        <b-btn
                            variant="light"
                            size="sm"
                            @click="$emit('remove')"
                            class="card-link"
                        >
                            <b-icon
                                variant="danger"
                                icon="trash-fill"
                            />
                        </b-btn>
                    </b-col>
                </b-row>
                <b-row v-if="editMode">
                    <b-col>
                        <p class="text-info">
                            <b-icon icon="info-circle" />
                            Il n'est <strong>pas nécessaire</strong> de statuer sur chacune des ressources et difficultés.
                        </p>
                    </b-col>
                </b-row>
            </b-card-header>
            <b-list-group
                flush
                v-if="editMode"
            >
                <resource-difficulty
                    v-for="resDif in resourcesDifficulties"
                    :key="resDif.id"
                    :resource-difficulty="resDif"
                    v-model="statements[$store.state.resourceDifficulty.findIndex(rD => rD.id === resDif.id)]"
                    :edit-mode="editMode"
                />
                <b-list-group-item class="text-right">
                    <b-btn
                        @click="editMode = false; $emit('save')"
                        variant="outline-primary"
                    >
                        <b-icon icon="box-arrow-in-right" />
                        Sauver
                    </b-btn>
                </b-list-group-item>
            </b-list-group>
            <b-card-body v-else>
                <b-row>
                    <b-col>
                        <b-list-group>
                            <b-list-group-item>
                                <strong>Ressources</strong>
                            </b-list-group-item>
                            <resource-difficulty
                                v-for="res in resources"
                                :key="res.id"
                                :resource-difficulty="res"
                                :edit-mode="editMode"
                                :value="true"
                            />
                        </b-list-group>
                    </b-col>
                    <b-col>
                        <b-list-group>
                            <b-list-group-item>
                                <strong>Difficultés</strong>
                            </b-list-group-item>
                            <resource-difficulty
                                v-for="res in difficulties"
                                :key="res.id"
                                :resource-difficulty="res"
                                :edit-mode="editMode"
                                :value="false"
                            />
                        </b-list-group>
                    </b-col>
                </b-row>
            </b-card-body>
        </b-card>
    </b-overlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import ResourceDifficulty from "./resource_difficulty.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

/**
 * A council statement from a class council.
 */
export default {
    props: {
        /** council_statement data from database (read-only). */
        council_statement: {
            type: Object,
            default: () => {
                return {
                    resources: [],
                    difficulties: []
                };
            }
        },
        /** Wether the statement is advanced or not. */
        advanced: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            loading: false,
            /** Edit mode status. */
            editMode: false,
            /** The related branch if any. */
            branch: null,
            statements: [],
            /** Configuration of the quill editor. */
            editorOptions: {
                modules: {
                    toolbar: [
                        ["bold", "italic", "underline", "strike"],
                        ["blockquote"],
                        [{ "list": "ordered"}, { "list": "bullet" }],
                        [{ "indent": "-1"}, { "indent": "+1" }],
                        [{ "align": [] }],
                        ["clean"]
                    ]
                },
                placeholder: ""
            },
        };
    },
    computed: {
        resourcesDifficulties: function () {
            if (this.editMode) {
                return this.$store.state.resourceDifficulty.filter(rD => rD.advanced === this.advanced);
            }

            return this.$store.state.resourceDifficulty.filter(
                (_, idx) => this.statements[idx] !== null
            );
        },
        resources: function () {
            return this.$store.state.resourceDifficulty.filter((_, idx) => this.statements[idx]);
        },
        difficulties: function () {
            return this.$store.state.resourceDifficulty.filter((_, idx) => this.statements[idx] === false);
        }
    },
    methods: {
        initCouncilStatement: function () {
            this.loading = true;
            // Directly set edit mode when creating a new statement.
            if (!("id" in this.council_statement)) {
                this.editMode = true;
            }
            this.$store.dispatch("loadOptions")
                .then(() => {
                    this.branch = this.$store.state.branches.find(b => b.id == this.council_statement.branch);
                    this.loading = false;
                });
            this.statements = this.$store.state.resourceDifficulty.filter(rD => rD.advanced === this.advanced)
                .map(s => {
                    const isResource = this.council_statement.resources.includes(s.id);
                    if (isResource) return true;
                    const isDifficulty = this.council_statement.difficulties.includes(s.id);
                    if (isDifficulty) return false;
                    return null;
                });
        },
        /** 
         * Submit new/changes council statement.
         *  @param {String} classCouncilId The id of the class council parent.
         * */
        submit: function (classCouncilId) {
            this.editMode = false;

            const data = {
                class_council: classCouncilId,
                branch: this.branch ? this.branch.id : null,
                resources: this.resources.map(rD => rD.id),
                difficulties: this.difficulties.map(rD => rD.id),
            };

            let url = "/pia/api/council_statement/";
            if ("id" in this.council_statement) url += this.council_statement.id + "/";

            const send = "id" in this.council_statement ? axios.put : axios.post;
            return send(url, data, token);
        },
    },
    mounted: function () {
        this.initCouncilStatement();
    },
    components: {
        Multiselect,
        ResourceDifficulty,
    }
};
</script>
