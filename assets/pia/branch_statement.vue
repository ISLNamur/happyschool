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
        <b-card class="mt-1">
            <b-row>
                <b-col>
                    <strong>{{ branchStatement ? branchStatement.branch : "" }}</strong>
                </b-col>
                <b-col
                    cols="2"
                    class="text-right"
                >
                    <b-btn
                        variant="light"
                        size="sm"
                        @click="editing = true"
                        class="card-link mb-1"
                    >
                        <b-icon
                            icon="pencil-square"
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
            <b-row>
                <b-col>
                    <span class="text-muted">Ressources</span>
                    <div v-html="resources" />
                </b-col>
                <b-col>
                    <span class="text-muted">Difficultés</span>
                    <div v-html="difficulties" />
                </b-col>
                <b-col>
                    <span class="text-muted">Autres</span>
                    <div v-html="others" />
                </b-col>
            </b-row>
            <b-modal
                v-model="editing"
                size="xl"
                title="Éditer"
                ok-only
            >
                <b-form-row>
                    <b-col>
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
                                v-model="branchStatement"
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
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group label="Ressources">
                            <quill-editor
                                v-model="resources"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group label="Difficultés">
                            <quill-editor
                                v-model="difficulties"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group label="Autres">
                            <quill-editor
                                v-model="others"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
            </b-modal>
        </b-card>
    </b-overlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

/**
 * A branch statement from a class council.
 */
export default {
    props: {
        /** branch_statement data from database (read-only). */
        branch_statement: {
            type: Object,
            default: () => {},
        },
    },
    data: function () {
        return {
            /** Branch of the statement. */
            branchStatement: null,
            resources: "",
            difficulties: "",
            others: "",
            /** State if the editing modal is open. */
            loading: true,
            editing: false,
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
    methods: {
        initBranchStatement: function () {
            this.$store.dispatch("loadOptions")
                .then(() => {
                    this.branchStatement = this.$store.state.branches.filter(b => b.id == this.branch_statement.branch)[0];
                    this.loading = false;
                });
            this.resources = this.branch_statement.resources;
            this.difficulties = this.branch_statement.difficulties;
            this.others = this.branch_statement.others;
        },
        /** 
         * Submit new/changes branch statement.
         *  @param {String} classCouncilId The id of the class council parent.
         * */
        submit: function (classCouncilId) {
            const data = {
                class_council: classCouncilId,
                branch: this.branchStatement.id,
                resources: this.resources,
                difficulties: this.difficulties,
                others: this.others,
            };

            let url = "/pia/api/branch_statement/";
            if ("id" in this.branch_statement) url += this.branch_statement.id + "/";

            const send = "id" in this.branch_statement ? axios.put : axios.post;
            return send(url, data, token);
        },
    },
    mounted: function () {
        this.initBranchStatement();
    },
    components: {
        quillEditor,
        Multiselect,
    }
};
</script>
