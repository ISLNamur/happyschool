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
                    <strong>
                        <b-form inline>
                            Du<b-form-input
                                type="date"
                                v-model="date_start"
                                class="mr-sm-2 ml-2"
                                :state="inputStates.date_start"
                            />
                            au<b-form-input
                                type="date"
                                v-model="date_end"
                                class="ml-2"
                                :state="inputStates.date_end"
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
            <b-collapse
                v-model="expanded"
                :id="Math.random().toString(36).substring(7)"
            >
                <b-form-row
                    v-if="useBranch"
                    class="mt-2"
                >
                    <b-col>
                        <b-form-group
                            label="Branche"
                            label-cols="3"
                            :state="inputStates.branch"
                        >
                            <multiselect
                                :options="$store.state.branches"
                                placeholder="Choisisser une branche"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="branch"
                                :show-no-options="false"
                                @input="updateBranchGoal"
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
                            <span slot="invalid-feedback">{{ errorMsg('branch') }}</span>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row :class="useBranch ? '' : 'mt-2'">
                    <b-col>
                        <b-form-group
                            :label="goalLabel"
                            label-cols="3"
                            :state="inputStates.goals"
                        >
                            <multiselect
                                :options="goalOptions"
                                placeholder="Choisisser un ou des objectifs"
                                tag-placeholder="Ajouter un nouvel objectif"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="goals"
                                :show-no-options="false"
                                @tag="addGoalTag"
                                label="goal"
                                track-by="goal"
                                multiple
                                taggable
                            >
                                <template
                                    slot="option"
                                    slot-scope="props"
                                >
                                    {{ props.option.goal }}
                                    <span v-if="props.option.branch">
                                        ({{ $store.state.branches.find(b => b.id === props.option.branch).branch }})
                                    </span>
                                </template>
                                <span slot="noResult">Aucun aménagements trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('cross_goals') }}{{ errorMsg('branch_goals') }}</span>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            label="Intervenant(s)"
                            label-cols="2"
                            :state="inputStates.responsible"
                        >
                            <multiselect
                                id="responsible"
                                :internal-search="false"
                                :options="responsibleOptions"
                                @search-change="getPeople"
                                placeholder="Rechercher un intervenants"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="responsible"
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                                multiple
                            >
                                <span slot="noResult">Aucun intervenant trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('responsible') }}</span>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            label="Indicateur(s)/Action(s)"
                            label-cols="2"
                        >
                            <quill-editor
                                v-model="indicatorAction"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            label="Aide(s)"
                            label-cols="2"
                        >
                            <quill-editor
                                v-model="givenHelp"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group label="Auto-évaluation">
                            <quill-editor
                                v-model="selfAssessment"
                                :options="editorOptions"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group label="Évaluation">
                            <multiselect
                                :options="$store.state.assessments"
                                placeholder="Choisisser une ou des évaluations"
                                tag-placeholder="Ajouter l'évaluation"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="assessment"
                                :show-no-options="false"
                                label="assessment"
                                track-by="id"
                            >
                                <span slot="noResult">Aucune évaluation trouvée.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col>
                        <b-form-group
                            description="Ajouter un ou des fichiers. Accepte uniquement des fichiers images et pdf."
                            label="Fichier(s)"
                        >
                            <b-form-file
                                multiple
                                accept=".pdf, .jpg, .png, jpeg"
                                v-model="attachments"
                                ref="attachments"
                                placeholder="Attacher un ou des fichiers."
                                choose-label="Attacher un ou des fichiers"
                                drop-label="Déposer des fichiers ici"
                                plain
                                @input="addFiles"
                            />
                            <b-list-group
                                v-for="(item, index) in uploadedFiles"
                                :key="index"
                            >
                                <file-upload
                                    :id="item.id"
                                    :file="item.file"
                                    path="/pia/upload_file/"
                                    removestr="4"
                                    @delete="deleteFile(index)"
                                    @setdata="setFileData(index, $event)"
                                />
                            </b-list-group>
                        </b-form-group> 
                    </b-col>
                </b-form-row>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import {getPeopleByName} from "../common/search.js";
import FileUpload from "../common/file_upload.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        goalObject: {
            type: Object,
            default: () => {},
        },
        pia_model: {
            type: Number,
            default: -1,
        },
        showExpanded: {
            type: Boolean,
            default: false,
        },
        goalLabel: {
            type: String,
            default: "Objectif"
        },
        itemModel: {
            type: String,
            default: "goal_item"
        },
        useBranch: {
            type: Boolean,
            default: false
        }
    },
    data: function () {
        return {
            date_start: null,
            date_end: null,
            goalOptions: [],
            goals: [],
            branch: null,
            responsible: [],
            responsibleOptions: [],
            givenHelp: "",
            indicatorAction: "",
            selfAssessment: "",
            assessment: null,
            attachments: [],
            uploadedFiles: [],
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
            expanded: false,
            searchId: -1,
            errors: {},
            inputStates: {
                "date_start": null,
                "date_end": null,
                "goals": null,
                "branch": null,
                "responsible": null
            },
        };
    },
    watch: {
        errors: function (newErrors) {
            const goalKey = this.useBranch ? "branch_goals" : "cross_goals";
            Object.keys(this.inputStates).forEach(key => {
                if (key.includes("goals") && goalKey in newErrors) {
                    this.inputStates.goals = newErrors[goalKey].length == 0;
                } else if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
    },
    methods: {
        /** 
         * Assign text error if any.
         * 
         * @param {String} err Field name.
         */
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        toggleExpand: function () {
            this.expanded = !this.expanded;
        },
        updateBranchGoal: function (branch) {
            this.goalOptions = this.goalOptions.sort((a, b) => {
                if (a.branch == branch.id && b.branch != a.branch) return -1;
                if (b.branch == branch.id && b.branch != a.branch) return 1;
                return 1;
            });
        },
        addFiles: function() {
            this.uploadedFiles = this.attachments.map(a => { return {file: a, id: -1};});
            this.attachments.splice(0, this.attachments.length);
        },
        setFileData: function(index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
        },
        deleteFile: function(index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        getPeople: function (searchQuery) {
            const person = "responsible";
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.$store.state.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, person)
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
        assignGoal: function () {
            if (this.goalObject.id >= 0) {
                this.date_start = this.goalObject.date_start;
                this.date_end = this.goalObject.date_end;
                this.indicatorAction = this.goalObject.indicator_action;
                this.givenHelp = this.goalObject.given_help;
                this.selfAssessment = this.goalObject.self_assessment;
                this.assessment = this.$store.state.assessments.filter(a => a.id == this.goalObject.assessment)[0];

                // Attachments
                this.uploadedFiles = this.goalObject.attachments.map(a => {
                    return {id: a, file: null};
                });

                // Responsibles
                const respProm =this.goalObject.responsible.filter(r => r !== null).map(r => axios.get("/annuaire/api/responsible/" + r + "/"));
                Promise.all(respProm)
                    .then(resps => {
                        this.responsible = resps.map(resp => resp.data);
                    });

                // Assign branch if necessary.
                if (this.useBranch) {
                    this.branch = this.$store.state.branches.find(b => b.id == this.goalObject.branch);
                }

                // Assign goals
                let specificGoals = this.useBranch ? this.goalObject.branch_goals : this.goalObject.cross_goals;
                let goals = specificGoals.split(";");
                const options = this.useBranch ? this.$store.state.branchGoalItems : this.$store.state.crossGoalItems;
                this.goals = options.filter(cg => goals.includes(cg.goal));
                let newGoals = goals.filter(g => !this.goalOptions.map(cg => cg.goal).includes(g));
                newGoals.forEach(ng => this.addGoalTag(ng));
            }
        },
        addGoalTag: function (tag) {
            this.goals.push({id: -1, goal: tag});
        },
        submit: function (piaId) {
            if (this.goals) {
                // Reset errors.
                this.errors = {};

                const goals = this.goals.reduce((acc, cg) => acc + ";" + cg.goal, "");
                const goalPath = this.useBranch ? "branch_goal" : "cross_goal";
                const goalField = goalPath + "s";
                let data = {
                    pia_model: piaId,
                    date_start: this.date_start,
                    date_end: this.date_end,
                    indicator_action: this.indicatorAction,
                    given_help: this.givenHelp,
                    self_assessment: this.selfAssessment,
                    assessment: this.assessment ? this.assessment.id : null,
                    [goalField]: this.goals.length > 0 ? goals.slice(1) : null,
                    responsible: this.responsible.map(r => r.matricule),
                    attachments: Array.from(this.uploadedFiles.map(u => u.id)),
                };

                if (this.useBranch && this.branch) data["branch"] = this.branch.id;

                const isNew = this.goalObject.id < 0;
                const url =  !isNew ? `/pia/api/${goalPath}/` + this.goalObject.id + "/" : `/pia/api/${goalPath}/`;
                const putOrPost = !isNew ? axios.put : axios.post;
                return putOrPost(url, data, token)
                    .catch(error => {
                        this.errors = error.response.data;
                        throw "Erreur lors de l'envoi des données.";
                    });
            }
        },
    },
    mounted: function () {
        if (this.goalObject.id < 0) this.expanded = true;

        this.$store.dispatch("loadOptions")
            .then(() => {
                if (this.useBranch) {
                    this.goalOptions = this.$store.state.branchGoalItems;
                } else {
                    this.goalOptions = this.$store.state.crossGoalItems;
                }
                this.assignGoal();
            });
    },
    components: {
        Multiselect,
        quillEditor,
        FileUpload,
    }
};
</script>
