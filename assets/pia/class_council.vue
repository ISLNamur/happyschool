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
        <b-row>
            <b-col>
                <b-form-row>
                    <b-col>
                        <strong>
                            <b-form inline>
                                {{ advanced ? "Semaine du conseil de classe" : "Date de l'auto-évaluation" }}
                                <b-form-input
                                    type="date"
                                    v-model="date_council"
                                    class="ml-1"
                                />
                            </b-form>
                        </strong>
                    </b-col>
                    <b-col
                        cols="2"
                        align-self="end"
                        class="text-right"
                    >
                        <b-btn
                            @click="toggleExpand"
                            variant="light"
                        >
                            {{ expanded ? "Cacher" : "Voir" }}
                        </b-btn>
                        <b-btn
                            @click="$emit('remove')"
                            variant="danger"
                            size="sm"
                            v-b-tooltip.hover
                            title="Supprimer"
                        >
                            <b-icon icon="trash" />
                        </b-btn>
                    </b-col>
                </b-form-row>
            </b-col>
        </b-row>
        <b-collapse
            v-model="expanded"
            :id="Math.random().toString(36).substring(7)"
        >
            <b-row>
                <b-col>
                    <b-btn
                        @click="council_statement.unshift({resources: [], difficulties: []})"
                        variant="info"
                    >
                        <b-icon icon="plus" />
                        Ajouter <span v-if="advanced">une branche</span>
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <council-statement
                        v-for="(statement, index) in council_statement"
                        :key="statement.id"
                        :council_statement="statement"
                        :advanced="advanced"
                        ref="councilstatements"
                        @remove="removeStatement(index, 'council_statement')"
                        @save="$emit('save')"
                        @update="updateStatement(index, $event)"
                    />
                </b-col>
            </b-row>
            <b-row
                v-if="council_statement.length > 0"
                class="mt-1"
            >
                <b-col>
                    <b-btn
                        @click="other_statement.unshift({})"
                        variant="outline-info"
                    >
                        <b-icon icon="plus" />
                        Autres ressources/difficultés
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <other-statement
                        v-for="(statement, index) in other_statement"
                        :key="statement.id"
                        :council_statement="statement"
                        ref="otherstatements"
                        @remove="removeStatement(index, 'other_statement')"
                    />
                </b-col>
            </b-row>
        </b-collapse>
    </b-card>
</template>

<script>
import axios from "axios";

import CouncilStatement from "./council_statement.vue";
import OtherStatement from "./other_statement.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

/**
 * Root component for showing class council.
 */
export default {
    props: {
        /** class_council data from database (read-only). id is -1 if new. */
        class_council: {
            type: Object,
            default: () => {},
        },
        /** Wether the council is advanced or not. */
        advanced: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            /** Date of class council. */
            date_council: null,
            /** A list of council statement. */
            council_statement: [],
            /** Other (free) statements.  */
            other_statement: [],
            /** State if the list of statements should be shown. */
            expanded: false,
        };
    },
    methods: {
        /** Update data for the new or updated council statement. */
        updateStatement: function (index, data) {
            this.council_statement.splice(index, 1, data);
        },
        /** Toggle the visibility of the list of council statement */
        toggleExpand: function () {
            this.expanded = !this.expanded;
        },
        /** 
         * Get promise for submitting the class council.
         * 
         * @param {String} piaId The id of the pia model it belgongs.
         */
        submit: function (piaId) {
            const data = {
                pia_model: piaId,
                date_council: this.date_council,
            };

            const isNew = this.class_council.id < 0;
            let url = "/pia/api/class_council/";
            if (!isNew) url += this.class_council.id + "/";

            const send = isNew ? axios.post : axios.put;
            return send(url, data, token);
        },
        /** 
         * Get all the promises of the council statements of the class council.
         * 
         * @param {String} classCouncilId The current class council id.
        */
        submitCouncilStatement: function (classCouncilId) {
            // Check if there is at least one council statement.
            if (this.council_statement.length === 0 && this.other_statement.length === 0) return [];

            let proms = [];
            if (this.$refs.councilstatements) {
                proms = proms.concat(this.$refs.councilstatements.map(bs => bs.submit(classCouncilId)));
            }
            if (this.$refs.otherstatements) {
                proms = proms.concat(this.$refs.otherstatements.map(s => s.submit(classCouncilId)));
            }
            return proms;
        },
        /**
         * Assign data from the prop.
         */
        assignClassCouncil: function () {
            if (this.class_council.id < 0) return;

            this.date_council = this.class_council.date_council;
        },
        /**
         * Remove a council statement.
         * 
         * @param
         */
        removeStatement: function (councilStatementIndex, statementType) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app.class_council.id < 0 || !("id" in app[statementType][councilStatementIndex])) {
                        app[statementType].splice(councilStatementIndex, 1);
                    } else {
                        axios.delete(`/pia/api/${statementType}/${app[statementType][councilStatementIndex].id}/`, token)
                            .then(() => app[statementType].splice(councilStatementIndex, 1))
                            .catch(err => alert(err));
                    }
                    
                }
            });
        },
    },
    mounted: function () {
        if (this.class_council.id >= 0) {
            axios.get(`/pia/api/council_statement/?class_council=${this.class_council.id}`)
                .then(resp => {
                    this.council_statement = resp.data.results;
                });
            axios.get(`/pia/api/other_statement/?class_council=${this.class_council.id}`)
                .then(resp => {
                    this.other_statement = resp.data.results;
                });
        } else {
            this.expanded = true;
        }

        this.assignClassCouncil();
    },
    components: {
        CouncilStatement,
        OtherStatement
    }
};
</script>
