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
        <BCard
            no-body
            class="mt-1"
            border-variant="info"
        >
            <BCardHeader>
                <BRow>
                    <BCol v-if="!editMode && advanced">
                        <strong>{{ branch ? branch.branch : "Ne concerne pas une branche en particulier" }}</strong>
                    </BCol>
                    <BCol v-else-if="advanced">
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
                                v-model="branch"
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
                    <BCol
                        cols="2"
                        class="text-end"
                    >
                        <BButton
                            variant="light"
                            size="sm"
                            @click="editMode = !editMode; if (!editMode) $emit('save')"
                            class="card-link mb-1"
                        >
                            <IBiCheck2Square
                                color="green"
                                v-if="editMode"
                            />
                            <IBiPencilSquare
                                v-else
                                color="green"
                            />
                        </BButton>
                        <BButton
                            variant="light"
                            size="sm"
                            @click="$emit('remove')"
                            class="card-link"
                        >
                            <IBiTrashFill color="red" />
                        </BButton>
                    </BCol>
                </BRow>
                <BRow v-if="editMode">
                    <BCol>
                        <p class="text-info">
                            <IBiInfoCircle />
                            Il n'est <strong>pas nécessaire</strong> de statuer sur chacune des ressources et
                            difficultés.
                        </p>
                    </BCol>
                </BRow>
                <BRow v-if="editMode">
                    <BCol>
                        <BInputGroup>
                            <template
                                #prepend
                            >
                                <BInputGroupText><IBiSearch /></BInputGroupText>
                            </template>
                            <BFormInput
                                placeholder="Filtrer les ressources et difficultés"
                                v-model="filter"
                            />
                        </BInputGroup>
                    </BCol>
                </BRow>
            </BCardHeader>
            <BListGroup
                flush
                v-if="editMode"
            >
                <resource-difficulty
                    v-for="resDif in resourcesDifficulties"
                    :key="resDif.id"
                    :resource-difficulty="resDif"
                    v-model="statements[store.resourceDifficulty.findIndex(rD => rD.id === resDif.id)]"
                    :edit-mode="editMode"
                />
                <BListGroupItem class="text-end">
                    <BButton
                        @click="editMode = false; $emit('save')"
                        variant="outline-primary"
                    >
                        <IBiBoxArrowInRight />
                        Sauver
                    </BButton>
                </BListGroupItem>
            </BListGroup>
            <BcardBody v-else>
                <BRow>
                    <BCol>
                        <BListGroup>
                            <BListGroupItem>
                                <strong>Ressources</strong>
                            </BListGroupItem>
                            <resource-difficulty
                                v-for="res in resources"
                                :key="res.id"
                                :resource-difficulty="res"
                                :edit-mode="editMode"
                                :model-value="true"
                            />
                        </BListGroup>
                    </BCol>
                    <BCol>
                        <BListGroup>
                            <BListGroupItem>
                                <strong>Difficultés</strong>
                            </BListGroupItem>
                            <resource-difficulty
                                v-for="res in difficulties"
                                :key="res.id"
                                :resource-difficulty="res"
                                :edit-mode="editMode"
                                :model-value="false"
                            />
                        </BListGroup>
                    </BCol>
                </BRow>
            </BcardBody>
        </BCard>
    </BOverlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { piaStore } from "./stores/index.js";

import ResourceDifficulty from "./resource_difficulty.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

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
                    difficulties: [],
                };
            },
        },
        /** Wether the statement is advanced or not. */
        advanced: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            loading: false,
            /** Edit mode status. */
            editMode: false,
            /** The related branch if any. */
            branch: null,
            statements: [],
            filter: "",
            store: piaStore(),
        };
    },
    computed: {
        resourcesDifficulties: function () {
            if (this.editMode) {
                return this.store.resourceDifficulty
                    .filter(rD => rD.advanced === this.advanced)
                    .filter(rD => rD.difficulty.includes(this.filter) || rD.resource.includes(this.filter));
            }

            return this.store.resourceDifficulty.filter(
                (_, idx) => this.statements[idx] !== null,
            );
        },
        resources: function () {
            return this.store.resourceDifficulty.filter((_, idx) => this.statements[idx]);
        },
        difficulties: function () {
            return this.store.resourceDifficulty.filter((_, idx) => this.statements[idx] === false);
        },
    },
    methods: {
        initCouncilStatement: function () {
            this.loading = true;
            // Directly set edit mode when creating a new statement.
            if (!("id" in this.council_statement)) {
                this.editMode = true;
            }
            this.store.loadOptions()
                .then(() => {
                    this.branch = this.store.branches.find(b => b.id == this.council_statement.branch);
                    this.loading = false;
                });
            this.statements = this.store.resourceDifficulty.filter(rD => rD.advanced === this.advanced)
                .map((s) => {
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
            return send(url, data, token)
                .then((resp) => {
                    this.$emit("update", resp.data);
                });
        },
    },
    mounted: function () {
        this.initCouncilStatement();
    },
    components: {
        Multiselect,
        ResourceDifficulty,
    },
};
</script>
