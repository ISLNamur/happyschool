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
        <BCard class="mt-1">
            <BRow>
                <BCol>
                    <strong>{{ councilStatement ? councilStatement.branch : "" }}</strong>
                </BCol>
                <BCol
                    cols="2"
                    class="text-end"
                >
                    <BButton
                        variant="light"
                        size="sm"
                        @click="editing = true"
                        class="card-link mb-1"
                    >
                        <IBiPencilSquare
                            variant="success"
                        />
                    </BButton>
                    <BButton
                        variant="light"
                        size="sm"
                        @click="$emit('remove')"
                        class="card-link"
                    >
                        <IBiTrashFill variant="danger" />
                    </BButton>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <span class="text-muted">Ressources</span>
                    <div v-html="resources" />
                </BCol>
                <BCol>
                    <span class="text-muted">Difficultés</span>
                    <div v-html="difficulties" />
                </BCol>
                <BCol>
                    <span class="text-muted">Autres</span>
                    <div v-html="others" />
                </BCol>
            </BRow>
            <b-modal
                v-model="editing"
                size="xl"
                title="Éditer"
                ok-only
            >
                <BFormRow>
                    <BCol>
                        <BFormGroup
                            label="Branche"
                            label-cols="2"
                        >
                            <multiselect
                                :options="store.branches"
                                placeholder="Choisisser une branche"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="councilStatement"
                                :show-no-options="false"
                                label="branch"
                                track-by="id"
                            >
                                <template #singleLabel="props">
                                    <strong>{{ props.option.branch }}</strong>
                                </template>
                                <template #noResult>
                                    Aucune branche trouvée.
                                </template>
                                <template #noOptions />
                            </multiselect>
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow>
                    <BCol>
                        <BFormGroup label="Ressources">
                            <text-editor v-model="resources" />
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow>
                    <BCol>
                        <BFormGroup label="Difficultés">
                            <text-editor v-model="difficulties" />
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow>
                    <BCol>
                        <BFormGroup label="Autres">
                            <text-editor v-model="others" />
                        </BFormGroup>
                    </BCol>
                </BFormRow>
            </b-modal>
        </BCard>
    </BOverlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { piaStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

/**
 * A council statement from a class council.
 */
export default {
    props: {
        /** council_statement data from database (read-only). */
        council_statement: {
            type: Object,
            default: () => { },
        },
    },
    data: function () {
        return {
            /** A statement. */
            councilStatement: null,
            resources: "",
            difficulties: "",
            others: "",
            /** State if the editing modal is open. */
            loading: true,
            editing: false,
            store: piaStore(),
        };
    },
    methods: {
        initCouncilStatement: function () {
            this.store.loadOptions()
                .then(() => {
                    this.councilStatement = this.store.branches.filter(b => b.id == this.council_statement.branch)[0];
                    this.loading = false;
                });
            this.resources = this.council_statement.resources;
            this.difficulties = this.council_statement.difficulties;
            this.others = this.council_statement.others;
        },
        /**
         * Submit new/changes branch statement.
         *  @param {String} classCouncilId The id of the class council parent.
         * */
        submit: function (classCouncilId) {
            const data = {
                class_council: classCouncilId,
                branch: this.councilStatement.id,
                resources: this.resources,
                difficulties: this.difficulties,
                others: this.others,
            };

            let url = "/pia/api/other_statement/";
            if ("id" in this.council_statement) url += this.council_statement.id + "/";

            const send = "id" in this.council_statement ? axios.put : axios.post;
            return send(url, data, token);
        },
    },
    mounted: function () {
        this.initCouncilStatement();
    },
    components: {
        TextEditor,
        Multiselect,
    },
};
</script>
