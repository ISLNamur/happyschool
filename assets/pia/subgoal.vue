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
    <div>
        <b-card>
            <b-form-row>
                <b-col>
                    <b-form-group label="Branche">
                        <multiselect
                            :options="branchOptions"
                            placeholder="Choisisser une branche"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="branch"
                            :showNoOptions="false"
                            @input="updateBranchGoal"
                            label="branch"
                            track-by="id"
                            >
                            <span slot="noResult">Aucune branche trouvée.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Objectif spécifique">
                        <multiselect
                            :options="branchGoalOptions"
                            placeholder="Choisisser un ou des objectifs"
                            tag-placeholder="Ajouter un nouvel objectif"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="branchGoal"
                            :showNoOptions="false"
                            @tag="addBranchGoalTag"
                            @input="updateAssessment"
                            label="goal"
                            track-by="goal"
                            multiple taggable
                            >
                            <span slot="noResult">Aucun objectif trouvé.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Aide(s)">
                        <quill-editor v-model="givenHelp" :options="editorOptions">
                        </quill-editor>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Auto-évaluation">
                        <quill-editor v-model="selfAssessment" :options="editorOptions">
                        </quill-editor>
                    </b-form-group>
                </b-col>
                <b-col>
                    <b-form-group label="Évaluation">
                        <multiselect
                            :options="assessmentOptions"
                            placeholder="Choisisser une ou des évaluations"
                            tag-placeholder="Ajouter l'évaluation"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="assessment"
                            :showNoOptions="false"
                            label="assessment"
                            track-by="id"
                            multiple
                            >
                            <span slot="noResult">Aucune évaluation trouvée.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-form-row>
        </b-card>
    </div>
</template>

<script>
import axios from 'axios';

import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';

import {quillEditor} from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'

export default {
    props: [],
    data: function () {
        return {
            branchOptions: [],
            branch: null,
            branchGoalAll: [],
            branchGoalOptions: [],
            branchGoal: [],
            givenHelp: "",
            selfAssessment: "",
            assessmentAll: [],
            assessmentOptions: [],
            assessment: [],
            editorOptions: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote'],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'indent': '-1'}, { 'indent': '+1' }],
                        [{ 'align': [] }],
                        ['clean']
                    ]
                },
                placeholder: ""
            },
        }
    },
    methods: {
        addBranchGoalTag: function (tag) {
            this.branchGoal.push({id: -1, goal: tag})
        },
        updateBranchGoal: function () {
            this.branchGoalOptions = this.branchGoalAll.filter(bg => bg.branch == this.branch.id);
        },
        updateAssessment: function () {
            this.assessmentOptions = this.assessmentAll.filter(a => {
                return a.branches.includes(this.branch.id);
                // Check intersection between branch.id and assessment.branches.
                // return this.branch.map(x => x.id).filter(g => a.branches.includes(g));
            });
        }
    },
    mounted: function () {
        axios.get('/pia/api/branch/')
        .then(resp => {
            this.branchOptions = resp.data.results;
        })
        axios.get('/pia/api/branch_goal/')
        .then(resp => {
            this.branchGoalAll = resp.data.results;
        })
        axios.get('/pia/api/assessment/')
        .then(resp => {
            this.assessmentAll = resp.data.results;
        })
    },
    components: {
        Multiselect,
        quillEditor,
    }
}
</script>
