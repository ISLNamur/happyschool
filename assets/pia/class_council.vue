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
                        Date du conseil de classe <b-form-input type="date" v-model="date_council"></b-form-input>
                    </b-form>
                    </strong>
                </b-col>
                <b-col cols="4" align-self="end">
                    <b-btn @click="toggleExpand" variant="light">{{ expanded ? "Cacher" : "Voir" }}</b-btn>
                    <b-btn @click="$emit('remove')" variant="danger">Supprimer</b-btn>
                </b-col>
            </b-form-row>
            </b-col>
        </b-row>
        <b-collapse v-model="expanded" :id="Math.random().toString(36).substring(7)">
            <b-row>
                <b-col>
                    <b-btn @click="branch_statement.unshift({})" variant="info">Ajouter une branche</b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <branch-statement v-for="(branch, index) in branch_statement" :key="branch.id"
                        :branch_statement="branch" ref="statements" @remove="removeBranchStatement(index)">
                    </branch-statement>
                </b-col>
            </b-row>
        </b-collapse>
    </b-card>
</template>

<script>
import axios from 'axios';

import BranchStatement from "./branch_statement.vue";

const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

/**
 * Root component for showing class council.
 */
export default {
    props: {
        /** class_council data from database (read-only). id is -1 if new. */
        class_council: {
            type: Object,
        },
    },
    data: function () {
        return {
            /** Date of class council. */
            date_council: null,
            /** A list of branch statement. */
            branch_statement: [],
            /** State if the list of branch should be shown. */
            expanded: false,
        }
    },
    methods: {
        /** Toggle the visibility of the list of branch statement */
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
            }

            const isNew = this.class_council.id < 0;
            let url = '/pia/api/class_council/';
            if (!isNew) url += this.class_council.id + '/';

            const send = isNew ? axios.post : axios.put;
            return send(url, data, token);
        },
        /** 
         * Get all the promises of the branch statements of the class council.
         * 
         * @param {String} classCouncilId The current class council id.
        */
        submitBranchStatement: function (classCouncilId) {
            // Check if there is at least one branch statement.
            if (this.branch_statement.length == 0) return [];

            return this.$refs.statements.map(bs => bs.submit(classCouncilId));
        },
        /**
         * Assign data from the prop.
         */
        assignClassCouncil: function () {
            if (this.class_council.id < 0) return;

            this.date_council = this.class_council.date_council;
        },
        /**
         * Remove a branch statement.
         * 
         * @param
         */
        removeBranchStatement: function (branchStatementIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer cette branche ?", {
                okTitle: 'Oui',
                cancelTitle: 'Non',
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app.class_council.id < 0 || !('id' in app.branch_statement[branchStatementIndex])) {
                        app.branch_statement.splice(branchStatementIndex, 1);
                    } else {
                        axios.delete('/pia/api/branch_statement/' + app.branch_statement[branchStatementIndex].id + '/', token)
                        .then(ret => app.branch_statement.splice(branchStatementIndex, 1))
                        .catch(err => alert(err));
                    }
                    
                }
            })
        },
    },
    mounted: function () {
        if (this.class_council.id >= 0) {
            axios.get('/pia/api/branch_statement/?class_council=' + this.class_council.id)
            .then(resp => {
                this.branch_statement = resp.data.results;
            })
        }

        this.assignClassCouncil();
    },
    components: {
        BranchStatement,
    }
}
</script>
