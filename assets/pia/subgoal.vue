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
        <b-card bg-variant="light">
            <b-form-row>
                <b-col>
                    <b-form-group label="Branche" label-cols="2">
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
                            <template slot="singleLabel" slot-scope="props"><strong>{{ props.option.branch }}</strong></template>
                            <span slot="noResult">Aucune branche trouvée.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
                <b-col cols="2">
                    <b-btn @click="$emit('remove')" variant="danger">Supprimer</b-btn>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Objectif spécifique" label-cols="2">
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
                    <b-form-group label="Indicateur(s)/Action(s)" label-cols="2">
                        <quill-editor v-model="indicatorAction" :options="editorOptions">
                        </quill-editor>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Aide(s)" label-cols="2">
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
                            >
                            <span slot="noResult">Aucune évaluation trouvée.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group label="Aide en engagement des parents">
                        <quill-editor v-model="parentCommitment" :options="editorOptions">
                        </quill-editor>
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

const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

export default {
    props: {
        subgoal: {
            type: Object,
            default: {},
        },
    },
    data: function () {
        return {
            branchOptions: [],
            branch: null,
            branchGoalAll: [],
            branchGoalOptions: [],
            branchGoal: [],
            indicatorAction: "",
            givenHelp: "",
            selfAssessment: "",
            assessmentOptions: [],
            assessment: null,
            parentCommitment: "À completer",
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
        assignSubgoal: function () {
            if ('id' in this.subgoal) {
                this.branch = this.branchOptions.filter(b => b.id == this.subgoal.branch)[0];
                this.indicatorAction = this.subgoal.indicator_action;
                this.givenHelp = this.subgoal.given_help;
                this.selfAssessment = this.subgoal.self_assessment;
                this.parentCommitment = this.subgoal.parent_commitment;
                this.assessment = this.assessmentOptions.filter(a => a.id == this.subgoal.assessment)[0];

                const subgoals = this.subgoal.branch_goals.split(";");
                this.branchGoal = this.branchGoalAll.filter(bg => subgoals.includes(bg.goal));
                const newSubgoals = subgoals.filter(sg => !this.branchGoalAll.map(bg => bg.goal).includes(sg));
                newSubgoals.forEach(nsg => this.addBranchGoalTag(nsg));
            }
        },
        addBranchGoalTag: function (tag) {
            this.branchGoal.push({id: -1, goal: tag})
        },
        updateBranchGoal: function (branch) {
            this.branchGoalOptions = this.branchGoalAll.filter(bg => bg.branch == branch.id);
        },
        submit: function(goalId) {
            const data = {
                goal: goalId,
                branch: this.branch.id,
                branch_goals: this.branchGoal.length > 0 ? this.branchGoal.reduce((acc, bg) => acc + ";" + bg.goal, "").slice(1) : "",
                indicator_action: this.indicatorAction,
                given_help: this.givenHelp,
                self_assessment: this.selfAssessment,
                assessment: this.assessment.id,
                parent_commitment: this.parentCommitment,
            };
            let url = '/pia/api/subgoal/';
            if ('id' in this.subgoal) url += this.subgoal.id + '/';
            if ('id' in this.subgoal) return axios.put(url, data, token);

            return axios.post(url, data, token);
        },
    },
    mounted: function () {
        const promises = [
            axios.get('/pia/api/branch/'),
            axios.get('/pia/api/branch_goal/'),
            axios.get('/pia/api/assessment/'),
        ]

        Promise.all(promises)
        .then(resps => {
            this.branchOptions = resps[0].data.results;
            this.branchGoalAll = resps[1].data.results;
            this.assessmentOptions = resps[2].data.results;

            this.assignSubgoal();
        });
    },
    components: {
        Multiselect,
        quillEditor,
    }
}
</script>
