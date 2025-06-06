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
        <BCard>
            <BRow>
                <BCol>
                    <strong>
                        <BForm class="d-flex flex-row align-items-center flex-wrap">
                            <label class="col-form-label me-2">Du</label>
                            <div class="col-lg-3 col-sm-12">
                                <BFormInput
                                    type="date"
                                    v-model="date_start"
                                    class="mr-sm-2 ml-2"
                                    :state="inputStates.date_start"
                                />
                            </div>
                            <label class="col-form-label ms-2 me-2">au</label>
                            <div class="col-lg-3 col-sm-12">
                                <BFormInput
                                    type="date"
                                    v-model="date_end"
                                    :state="inputStates.date_end"
                                />
                            </div>
                        </BForm>
                    </strong>
                </BCol>
                <BCol
                    cols="2"
                    sm="3"
                    v-if="branch"
                    class="text-start form-inline"
                >
                    <p><strong>{{ branch.branch }}</strong></p>
                </BCol>
                <BCol
                    cols="2"
                    align-self="end"
                    class="text-end"
                >
                    <IBiCheckCircleFill
                        v-if="goalState === 'OK'"
                        variant="success"
                    />
                    <IBiXCircleFill
                        v-if="goalState === 'NOK'"
                        variant="error"
                    />
                    <IBiSlashCircle
                        v-if="goalState === 'IP'"
                        variant="warning"
                    />
                    <BButtonGroup>
                        <BButton
                            @click="toggleExpand"
                            variant="light"
                        >
                            {{ expanded ? "Cacher" : "Voir" }}
                        </BButton>
                        <BButton
                            @click="$emit('clone')"
                            size="sm"
                            v-b-tooltip.hover="'Cloner'"
                        >
                            <IBiFiles />
                        </BButton>
                        <BButton
                            @click="$emit('remove')"
                            variant="danger"
                            size="sm"
                            v-b-tooltip.hover="'Supprimer'"
                        >
                            <IBiTrash />
                        </BButton>
                    </BButtonGroup>
                </BCol>
            </BRow>
            <BCollapse
                v-model="expanded"
                :id="Math.random().toString(36).substring(7)"
            >
                <BRow
                    v-if="useBranch"
                    class="mt-2"
                >
                    <BCol>
                        <BFormGroup
                            label="Branche"
                            label-cols="3"
                            :state="inputStates.branch"
                        >
                            <multiselect
                                :options="store.branches"
                                placeholder="Choisisser une branche"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="branch"
                                :show-no-options="false"
                                @update:model-value="updateBranchGoal"
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
                            <template #invalid-feedback>
                                {{ errorMsg('branch') }}
                            </template>
                        </BFormGroup>
                    </BCol>
                </BRow>
                <BFormRow :class="useBranch ? '' : 'mt-2'">
                    <BCol>
                        <BFormGroup
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
                                <template #option="props">
                                    {{ props.option.goal }}
                                    <span v-if="props.option.branch">
                                        ({{ store.branches.find(b => b.id === props.option.branch).branch }})
                                    </span>
                                </template>
                                <template #noResult>
                                    Aucun aménagements trouvé.
                                </template>
                                <template #noOptions />
                            </multiselect>
                            <template #invalid-feedback>
                                {{ errorMsg('cross_goals') }}{{ errorMsg('branch_goals') }}
                            </template>
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow v-if="advanced">
                    <BCol>
                        <BFormGroup
                            label="Indicateur(s)/Action(s)"
                            label-cols="2"
                        >
                            <text-editor v-model="indicatorAction" />
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow v-if="advanced">
                    <BCol>
                        <BFormGroup
                            label="Aide(s)"
                            label-cols="2"
                        >
                            <text-editor v-model="givenHelp" />
                        </BFormGroup>
                    </BCol>
                </BFormRow>

                <BFormRow v-if="advanced && useBranch">
                    <BCol>
                        <BFormGroup label="Évaluation intermédiaire">
                            <BTableSimple>
                                <BThead>
                                    <BTr>
                                        <BTh>Date</BTh>
                                        <BTh>Évaluation intermédiaire</BTh>
                                        <BTh />
                                    </BTr>
                                </BThead>
                                <BTbody>
                                    <BTr
                                        v-for="(intEval, index) in intermediateEvaluation"
                                        :key="intEval.id"
                                    >
                                        <BTd>
                                            <BFormInput
                                                type="date"
                                                v-model="intEval.date_evaluation"
                                            />
                                        </BTd>
                                        <BTd>
                                            <multiselect
                                                :options="store.assessments"
                                                placeholder="Choisisser une évaluation"
                                                tag-placeholder="Ajouter l'évaluation"
                                                select-label=""
                                                selected-label="Sélectionné"
                                                deselect-label="Cliquer dessus pour enlever"
                                                :show-no-options="false"
                                                label="assessment"
                                                track-by="id"
                                                v-model="evaluations[index]"
                                            >
                                                <template #noResult>
                                                    Aucune évaluation trouvée.
                                                </template>
                                                <template #noOptions />
                                            </multiselect>
                                        </BTd>
                                        <BTd>
                                            <BButton
                                                size="sm"
                                                variant="danger"
                                                @click="removeIntermediateEval(index)"
                                            >
                                                <IBiTrash />
                                            </BButton>
                                        </BTd>
                                    </BTr>
                                    <BTr>
                                        <BTd>
                                            <BButton
                                                variant="success"
                                                @click="addIntermediateEval"
                                            >
                                                <IBiPlus />
                                                Ajouter
                                            </BButton>
                                        </BTd>
                                    </BTr>
                                </BTbody>
                            </BTableSimple>
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow v-if="advanced">
                    <BCol v-if="!useBranch">
                        <BFormGroup label="Auto-évaluation">
                            <text-editor v-model="selfAssessment" />
                        </BFormGroup>
                    </BCol>
                    <BCol>
                        <BFormGroup label="Évaluation du CCL">
                            <multiselect
                                :options="store.assessments"
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
                                <template #noResult>
                                    Aucune évaluation trouvée.
                                </template>
                                <template #noOptions />
                            </multiselect>
                        </BFormGroup>
                    </BCol>
                </BFormRow>
                <BFormRow v-if="advanced">
                    <BCol>
                        <BFormGroup
                            description="Ajouter un ou des fichiers. Accepte uniquement des fichiers images et pdf."
                            label="Fichier(s)"
                        >
                            <BFormFile
                                multiple
                                accept=".pdf, .jpg, .png, jpeg"
                                v-model="attachments"
                                ref="attachments"
                                placeholder="Attacher un ou des fichiers."
                                choose-label="Attacher un ou des fichiers"
                                drop-label="Déposer des fichiers ici"
                                plain
                                @update:model-value="addFiles"
                            />
                            <BListGroup
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
                            </BListGroup>
                        </BFormGroup>
                    </BCol>
                </BFormRow>
            </BCollapse>
        </BCard>
    </div>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { useModalController } from "bootstrap-vue-next";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { piaStore } from "./stores/index.js";

import { getPeopleByName } from "@s:core/js/common/search.js";
import FileUpload from "@s:core/js/common/file_upload.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { create } = useModalController();
        return { create };
    },
    props: {
        goalObject: {
            type: Object,
            default: () => { },
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
        },
        advanced: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            date_start: null,
            date_end: null,
            goalOptions: [],
            goals: [],
            branch: null,
            branches: [],
            responsible: [],
            responsibleOptions: [],
            givenHelp: "",
            indicatorAction: "",
            selfAssessment: "",
            assessment: null,
            intermediateEvaluation: [],
            evaluations: [],
            attachments: [],
            uploadedFiles: [],
            expanded: false,
            searchId: -1,
            errors: {},
            inputStates: {
                "date_start": null,
                "date_end": null,
                "goals": null,
                "branch": null,
                "branches": null,
                "responsible": null
            },
            store: piaStore(),
        };
    },
    computed: {
        goalState: function () {
            if (!this.assessment) return null;

            return this.assessment.state;
        }
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
        addFiles: function () {
            this.uploadedFiles = this.attachments.map(a => { return { file: a, id: -1 }; });
            this.attachments.splice(0, this.attachments.length);
        },
        setFileData: function (index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
        },
        deleteFile: function (index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        getPeople: function (searchQuery) {
            const person = "responsible";
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, person)
                .then((resp) => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                    // this.searching = false;
                })
                .catch((err) => {
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
                this.assessment = this.store.assessments.filter(a => a.id == this.goalObject.assessment)[0];

                // Get intermediate evaluations.
                if (this.useBranch) {
                    axios.get(`/pia/api/intermediate_evaluation/?branch_goal=${this.goalObject.id}`)
                        .then((resp) => {
                            this.intermediateEvaluation = resp.data.results;
                            this.evaluations = resp.data.results.map(intEval => this.store.assessments.find(a => intEval.evaluation === a.id));
                        });
                }

                // Attachments
                this.uploadedFiles = this.goalObject.attachments.map(a => {
                    return { id: a, file: null };
                });

                // Responsibles
                const respProm = this.goalObject.responsible.filter(r => r !== null).map(r => axios.get("/annuaire/api/responsible/" + r + "/"));
                Promise.all(respProm)
                    .then(resps => {
                        this.responsible = resps.map(resp => resp.data);
                    });

                // Assign branch if necessary.
                if (this.useBranch) {
                    this.branch = this.store.branches.find(b => b.id == this.goalObject.branch);
                } else {
                    // For crossgoals
                    this.branches = this.store.branches.filter(b => this.goalObject.branches.includes(b.id));
                }

                // Assign goals
                let specificGoals = this.useBranch ? this.goalObject.branch_goals : this.goalObject.cross_goals;
                let goals = specificGoals.split(";");
                const options = this.useBranch ? this.store.branchGoalItems : this.store.crossGoalItems;
                this.goals = options.filter(cg => goals.includes(cg.goal));
                let newGoals = goals.filter(g => !this.goalOptions.map(cg => cg.goal).includes(g));
                newGoals.forEach(ng => this.addGoalTag(ng));
            }
        },
        addGoalTag: function (tag) {
            this.goals.push({ id: -1, goal: tag });
        },
        addIntermediateEval: function () {
            this.evaluations.push(null);
            this.intermediateEvaluation.push({ branch_goal: this.goalObject.id, date_evaluation: null, evaluation: null });
        },
        removeIntermediateEval: function (index) {
            this.create({
                body: "Êtes-vous sûr de vouloir supprimer cet élèment ?",
                title: "Confirmation",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Non",
            }).then((response) => {
                if (response.ok && "id" in this.intermediateEvaluation[index]) {
                    axios.delete(`/pia/api/intermediate_evaluation/${this.intermediateEvaluation[index].id}/`, token);
                }

                this.evaluations.splice(index, 1);
                this.intermediateEvaluation.splice(index, 1);
            });
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
                    branches: this.branches.map(b => b.id),
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
                const url = !isNew ? `/pia/api/${goalPath}/` + this.goalObject.id + "/" : `/pia/api/${goalPath}/`;
                const putOrPost = !isNew ? axios.put : axios.post;
                const goalsPromise = putOrPost(url, data, token);
                if (this.evaluations) {
                    goalsPromise.then((resp) => {
                        const branchGoalId = resp.data.id;
                        Promise.all(
                            this.intermediateEvaluation.map((iE, index) => {
                                const alreadyExists = "id" in iE;
                                iE.evaluation = this.evaluations[index].id;
                                iE.branch_goal = branchGoalId;
                                const send = alreadyExists ? axios.put : axios.post;
                                return send(`/pia/api/intermediate_evaluation/${alreadyExists ? iE.id + "/" : ""}`, iE, token);
                            })
                        );
                    });
                }
                return goalsPromise;
            }
        },
    },
    mounted: function () {
        if (this.goalObject.id < 0) this.expanded = true;

        this.store.loadOptions()
            .then(() => {
                if (this.useBranch) {
                    this.goalOptions = this.store.branchGoalItems.filter(
                        bGI => this.advanced ? bGI.advanced : bGI.basic
                    );
                } else {
                    this.goalOptions = this.store.crossGoalItems.filter(
                        cGI => this.advanced ? cGI.advanced : cGI.basic
                    );
                }
                this.assignGoal();
            });
    },
    components: {
        Multiselect,
        TextEditor,
        FileUpload,
    }
};
</script>
