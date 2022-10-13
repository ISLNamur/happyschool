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
    <b-container>
        <b-row>
            <h3>{{ advanced ? "PIA" : "Aide élève" }} : {{ id ? "Modifier" : "Nouveau" }}</h3>
        </b-row>
        <b-row class="sticky-top p-2 first-line">
            <b-col>
                <b-btn @click="$router.back()">
                    Retour à la liste des élèves
                </b-btn>
            </b-col>
            <b-col
                cols="4"
                align-self="end"
                class="text-left"
            >
                <b-btn
                    :href="`/pia/report/${id}/`"
                >
                    PDF
                </b-btn>
                <b-overlay
                    :show="sending"
                    rounded="sm"
                    class="d-inline-block"
                >
                    <b-btn
                        @click="submit"
                        variant="primary"
                        :disabled="!form.student"
                    >
                        Sauver
                    </b-btn>
                </b-overlay>
            </b-col>
        </b-row>
        <b-overlay
            :show="loading"
        >
            <b-tabs
                content-class="mt-3"
                justified
                class="mt-2"
            >
                <b-tab
                    title="Élève et aménagements"
                    active
                >
                    <b-row>
                        <b-col>
                            <h4>Référents {{ advanced ? "PIA" : "" }}</h4>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col
                            v-if="form.student"
                            md="3"
                        >
                            <b-img
                                :src="`/static/photos/${form.student.matricule}.jpg`"
                                alt="Photo de l'élève"
                                fluid
                            />
                        </b-col>
                        <b-col>
                            <b-form-row>
                                <b-col md="4">
                                    <b-form-group label="Élève">
                                        <multiselect
                                            id="student-0"
                                            :internal-search="false"
                                            :options="studentOptions"
                                            @search-change="getPeople"
                                            placeholder="Rechercher un élève"
                                            select-label=""
                                            selected-label="Sélectionné"
                                            deselect-label="Cliquer dessus pour enlever"
                                            v-model="form.student"
                                            label="display"
                                            track-by="matricule"
                                            :show-no-options="false"
                                            :disabled="parseInt(id) >= 0"
                                        >
                                            <span slot="noResult">Aucun élève trouvé.</span>
                                            <span slot="noOptions" />
                                        </multiselect>
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                            <b-form-row>
                                <b-col>
                                    <b-form-group
                                        label="Référent(s)"
                                        :state="inputStates.referent"
                                    >
                                        <multiselect
                                            id="responsible-0"
                                            :internal-search="false"
                                            :options="responsibleOptions"
                                            @search-change="getPeople"
                                            placeholder="Choisir un ou plusieurs référents"
                                            select-label=""
                                            selected-label="Sélectionné"
                                            deselect-label="Cliquer dessus pour enlever"
                                            v-model="form.referent"
                                            label="display"
                                            track-by="matricule"
                                            :show-no-options="false"
                                            multiple
                                        >
                                            <span slot="noResult">Aucun responsable trouvé.</span>
                                            <span slot="noOptions" />
                                        </multiselect>
                                        <span slot="invalid-feedback">{{ errorMsg('referent') }}</span>
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                            <b-form-row>
                                <b-col>
                                    <b-form-group
                                        label="Parrain(s)/Marraine(s)"
                                        :state="inputStates.referent"
                                    >
                                        <multiselect
                                            id="responsible-1"
                                            :internal-search="false"
                                            :options="responsibleOptions"
                                            @search-change="getPeople"
                                            placeholder="Choisir un ou plusieurs parrains/marraines"
                                            select-label=""
                                            selected-label="Sélectionné"
                                            deselect-label="Cliquer dessus pour enlever"
                                            v-model="form.sponsor"
                                            label="display"
                                            track-by="matricule"
                                            :show-no-options="false"
                                            multiple
                                        >
                                            <span slot="noResult">Aucun responsable trouvé.</span>
                                            <span slot="noOptions" />
                                        </multiselect>
                                        <span slot="invalid-feedback">{{ errorMsg('sponsor') }}</span>
                                    </b-form-group>
                                </b-col>
                            </b-form-row>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <h4>{{ advanced ? "Aménagements" : "Activités de soutien" }}</h4>
                        </b-col>
                    </b-row>
                    <b-row v-if="advanced">
                        <b-col>
                            <b-form-group
                                label="Trouble d'apprentissage"
                                label-cols="3"
                                :state="inputStates.disorder"
                            >
                                <multiselect
                                    :options="$store.state.disorders"
                                    placeholder="Sélectionner le ou les différents troubles"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.disorder"
                                    :show-no-options="false"
                                    track-by="id"
                                    label="disorder"
                                    @input="updateDisorderResponse"
                                    multiple
                                >
                                    <span slot="noResult">Aucun trouble trouvé.</span>
                                    <span slot="noOptions" />
                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('disorder') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row v-if="advanced">
                        <b-col>
                            <b-form-group
                                label="Aménagements raisonnables liés au trouble"
                                label-cols="3"
                                :state="inputStates.disorder_response"
                            >
                                <multiselect
                                    :options="disorderResponseOptions"
                                    placeholder="Sélectionner le ou les différents aménagements"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.disorder_response"
                                    :show-no-options="false"
                                    track-by="id"
                                    label="response"
                                    multiple
                                >
                                    <span slot="noResult">Aucun aménagements trouvé.</span>
                                    <span slot="noOptions" />
                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('disorder_response') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row v-if="advanced">
                        <b-col>
                            <b-form-group
                                label="Aménagements d'horaire"
                                label-cols="3"
                                :state="inputStates.schedule_adjustment"
                            >
                                <multiselect
                                    :options="$store.state.scheduleAdjustments"
                                    placeholder="Sélectionner le ou les différents adaptations"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.schedule_adjustment"
                                    track-by="id"
                                    label="schedule_adjustment"
                                    :show-no-options="false"
                                    multiple
                                >
                                    <span slot="noResult">Aucun aménagements trouvé.</span>
                                    <span slot="noOptions" />
                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('schedule_adjustment') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row v-if="advanced">
                        <b-col>
                            <b-form-group
                                label="Autres aménagements"
                            >
                                <quill-editor
                                    v-model="form.other_adjustments"
                                    :options="editorOptions"
                                />
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row v-else>
                        <b-col>
                            <b-table-simple v-if="!loading">
                                <b-thead>
                                    <b-tr>
                                        <b-th>Jour</b-th>
                                        <b-th>Cours</b-th>
                                        <b-th>Prof</b-th>
                                    </b-tr>
                                </b-thead>
                                <b-tbody>
                                    <b-tr
                                        v-for="day in supportDays"
                                        :key="day"
                                    >
                                        <b-td>{{ dayOfWeek[day] }}</b-td>
                                        <b-td>
                                            <multiselect
                                                :internal-search="false"
                                                :options="$store.state.branches"
                                                placeholder="Choisir une matière"
                                                select-label=""
                                                selected-label="Sélectionné"
                                                deselect-label="Cliquer dessus pour enlever"
                                                v-model="form.support_activities[day].branch"
                                                :show-no-options="false"
                                                label="branch"
                                                track-by="id"
                                                multiple
                                            >
                                                <span slot="noResult">Aucune branche trouvé.</span>
                                                <span slot="noOptions" />
                                            </multiselect>
                                        </b-td>
                                        <b-td>
                                            <multiselect
                                                :id="`responsible-support-${day}`"
                                                :internal-search="false"
                                                :options="responsibleOptions"
                                                @search-change="getPeople"
                                                placeholder="Choisir un ou plusieurs profs"
                                                select-label=""
                                                selected-label="Sélectionné"
                                                deselect-label="Cliquer dessus pour enlever"
                                                v-model="form.support_activities[day].teachers"
                                                label="display"
                                                track-by="matricule"
                                                :show-no-options="false"
                                                multiple
                                            >
                                                <span slot="noResult">Aucun responsable trouvé.</span>
                                                <span slot="noOptions" />
                                            </multiselect>
                                        </b-td>
                                    </b-tr>
                                </b-tbody>
                            </b-table-simple>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <h4>Attachements</h4>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group
                                description="Ajouter un ou des fichiers. Accepte uniquement des fichiers images et pdf."
                                label="Fichier(s)"
                            >
                                <b-form-file
                                    multiple
                                    accept=".pdf, .jpg, .png, jpeg"
                                    v-model="form.attachments"
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
                    </b-row>
                </b-tab>
                <b-tab>
                    <template #title>
                        <b-overlay :show="loadingOthers">
                            {{ advanced ? "Conseils de classe" : "Auto-évaluation" }}
                            <b-badge>{{ class_council.length }}</b-badge>
                        </b-overlay>
                    </template>
                    <b-row>
                        <h4 v-if="advanced">
                            Conseil de classe
                        </h4>
                        <h4 v-else>
                            Auto-évaluation
                        </h4>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-btn
                                @click="class_council.unshift({id: -1})"
                                variant="outline-secondary"
                            >
                                <b-icon icon="plus" />
                                Ajouter
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <class-council
                                v-for="(council, index) in class_council"
                                :key="council.id"
                                :class_council="council"
                                :advanced="advanced"
                                ref="councils"
                                class="mt-2"
                                @remove="removeClassCouncil(index)"
                                @save="submit"
                            />
                        </b-col>
                    </b-row>
                </b-tab>
                <b-tab>
                    <template #title>
                        <b-overlay :show="loadingOthers">
                            Objectifs {{ advanced ? "" : "du CCL" }}
                            <b-badge>{{ cross_goal.length + branch_goal.length }}</b-badge>
                        </b-overlay>
                    </template>
                    <b-row class="mt-2">
                        <h4>Objectifs {{ advanced ? "transversaux" : "du CCL" }}</h4>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-btn
                                @click="cross_goal.unshift({id: -1})"
                                variant="outline-secondary"
                            >
                                <b-icon icon="plus" />
                                Ajouter
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <student-goal
                                class="mt-2"
                                v-for="(goal, index) in cross_goal"
                                :key="'cg-' + goal.id"
                                :goal-object="goal"
                                :advanced="advanced"
                                ref="crossgoals"
                                @remove="removeObject('cross_goal', index)"
                                @clone="cloneObject('cross_goal', index)"
                                goal-label="Objectifs transversaux"
                                item-model="cross_goal_item"
                            />
                        </b-col>
                    </b-row>
                    <b-row
                        class="mt-2"
                    >
                        <h4>Objectifs de branche</h4>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-btn
                                @click="branch_goal.unshift({id: -1})"
                                variant="outline-secondary"
                            >
                                <b-icon icon="plus" />
                                Ajouter
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <student-goal
                                class="mt-2"
                                v-for="(goal, index) in branch_goal"
                                :key="'bg-' + goal.id"
                                :goal-object="goal"
                                :advanced="advanced"
                                ref="branchgoals"
                                @remove="removeObject('branch_goal', index)"
                                @clone="cloneObject('branch_goal', index)"
                                goal-label="Objectifs de branche"
                                item-model="branch_goal_item"
                                use-branch
                            />
                        </b-col>
                    </b-row>
                    <b-row />
                </b-tab>
                <b-tab>
                    <template #title>
                        <b-overlay :show="loadingOthers">
                            Projet et avis
                            <b-badge>{{ student_project.length + parents_opinion.length }}</b-badge>
                        </b-overlay>
                    </template>
                    <b-row>
                        <h4>Projet de l'élève</h4>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-btn
                                @click="student_project.unshift({id: -1})"
                                variant="outline-secondary"
                            >
                                <b-icon icon="plus" />
                                Ajouter
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <pia-comment
                                class="mt-2"
                                v-for="(sP, index) in student_project"
                                :key="sP.id"
                                @remove="removeObject('student_project', index)"
                                comment-type="student_project"
                                :comment-object="sP"
                                ref="studentprojects"
                            />
                        </b-col>
                    </b-row>
                    <b-row>
                        <h4>Avis des parents</h4>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-btn
                                @click="parents_opinion.unshift({id: -1})"
                                variant="outline-secondary"
                            >
                                <b-icon icon="plus" />
                                Ajouter
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <pia-comment
                                class="mt-2"
                                v-for="(pO, index) in parents_opinion"
                                :key="pO.id"
                                @remove="removeObject('parents_opinion', index)"
                                comment-type="parents_opinion"
                                :comment-object="pO"
                                ref="parentsopinions"
                            />
                        </b-col>
                    </b-row>
                </b-tab>
                <b-tab v-if="hasDossierApp">
                    <template #title>
                        <b-overlay :show="loadingOthers">
                            Autre infos
                            <b-badge>{{ dossier.length }}</b-badge>
                        </b-overlay>
                    </template>
                    <b-row>
                        <b-col>
                            <h4>Autre infos (<a href="/dossier_eleve/">Dossier de l'élève</a>)</h4>
                        </b-col>
                    </b-row>
                    <b-row class="mb-1">
                        <b-col>
                            <b-btn
                                v-if="this.form.student"
                                :href="`/dossier_eleve/?matricule=${this.form.student.matricule}`"
                            >
                                <b-icon icon="arrow-right" />
                                Vers le dossier de l'élève
                            </b-btn>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-card
                                v-for="cas in dossier"
                                :key="cas.id"
                                no-body
                                class="mb-1"
                            >
                                <b-card-sub-title class="mt-1 pl-1">
                                    {{ cas.datetime_modified.slice(0, 10) }}
                                </b-card-sub-title>
                                <b-card-body>
                                    <span v-html="cas.explication_commentaire" />
                                </b-card-body>
                                <b-card-footer class="text-right">
                                    <b-btn
                                        variant="warning"
                                        :href="`/dossier_eleve/#/edit/${cas.id}/`"
                                    >
                                        <b-icon icon="pencil-square" />
                                        Modifier
                                    </b-btn>
                                </b-card-footer>
                            </b-card>
                        </b-col>
                    </b-row>
                </b-tab>
            </b-tabs>
        </b-overlay>
    </b-container>
</template>

<script>
import axios from "axios";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {getPeopleByName} from "../common/search.js";
import FileUpload from "../common/file_upload.vue";

import StudentGoal from "./student_goal.vue";
import ClassCouncil from "./class_council.vue";
import PiaComment from "./pia_comment.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        id: {
            type: String,
            default: null,
        },
        advanced: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            responsibleOptions: [],
            studentOptions: [],
            disorderResponseOptions: [],
            searchId: -1,
            sending: false,
            loading: true,
            loadingOthers: true,

            form: {
                id: null,
                student: null,
                referent: [],
                sponsor: [],
                disorder: [],
                disorder_response: [],
                schedule_adjustment: [],
                attachments: [],
                other_adjustments: "",
                support_activities: {}
            },
            uploadedFiles: [],
            cross_goal: [],
            branch_goal: [],
            student_project: [],
            parents_opinion: [],
            dossier: [],
            /** List of class council related to this PIA. */
            class_council: [],
            errors: {},
            /** List of input error states. */
            inputStates: {
                "student": null,
                "referent": null,
                "sponsor": null,
                "disorder": null,
                "disorder_response": null,
                "schedule_adjustment": null
            },
            /** Options for the text editor. */
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
            dayOfWeek: {1: "Lundi", 2: "Mardi", 3: "Mercredi", 4: "Jeudi", 5: "Vendredi", 6: "Samedi", 7: "Dimanche"}
        };
    },
    computed: {
        /**
         * State if HappySchool use the dossier_eleve app.
         */
        hasDossierApp: function () {
            // eslint-disable-next-line no-undef
            return menu.apps.some(a => a.app === "dossier_eleve");
        },
        /**
         * A list of supported days from settings.
         */
        supportDays: function () {
            const seqDays = this.$store.state.settings.weekday_support_activity.split(",");
            const days = seqDays.filter(d => d.length === 1).map(d => Number(d.trim()));
            const ranges = seqDays.filter(d => d.length === 3).map(d => d.trim()).filter(d => d[1] === "-");
            ranges.forEach(r => {
                const start = Number(r[0]);
                const end = Number(r[2]);
                if (start <= end) {
                    Array(end - start + 1).fill().map((_, i) => i + start).forEach(d => days.push(d));
                }
            });

            return days.sort();
        }
    },
    watch: {
        id: function (newVal) {
            if (newVal) {
                // Reset data.
                Object.assign(this.$data, this.$options.data());
                this.initApp();
            } else {
                this.reset();
            }
        },
        /**
         * Handle returned errors states.
         * 
         * @param {Object} newErrors Errors states with error message.
         */
        errors: function (newErrors) {
            Object.keys(this.inputStates).forEach(key => {
                if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
    },
    methods: {
        addFiles: function() {
            this.uploadedFiles = this.uploadedFiles.concat(this.form.attachments.map(a => { return {file: a, id: -1};}));
            this.form.attachments.splice(0, this.form.attachments.length);
        },
        setFileData: function(index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
        },
        deleteFile: function(index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
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
        /**
         * Clone an object from the list.
         * 
         * @param {String} objectType The type of the goal (cross_goal, branch_goal).
         * @param {Number} objectIndex The index of the goal in the associated goal list.
         */
        cloneObject: function (objectType, objectIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Cloner cet élément ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    let clonedObject = Object.assign({}, app[objectType][objectIndex]);
                    if (app[objectType][objectIndex].id >= 0) {
                        // Remove the id from the object.
                        delete clonedObject.id;
                    }
                    axios.post(`/pia/api/${objectType}/`, clonedObject,token)
                        .then(resp => app[objectType].splice(objectIndex + 1, 0, resp.data))
                        .catch(err => alert(err));
                }
            });
        },
        /**
         * Remove a object from the list.
         * 
         * @param {String} objectType The type of the goal (cross_goal, branch_goal, student_project or parents_opinion).
         * @param {Number} objectIndex The index of the goal in the associated goal list.
         */
        removeObject: function (objectType, objectIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer l'élément ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app[objectType][objectIndex].id >= 0) {
                        axios.delete(`/pia/api/${objectType}/` + app[objectType][objectIndex].id + "/", token)
                            .then(() => app[objectType].splice(objectIndex, 1))
                            .catch(err => alert(err));
                    } else {
                        app[objectType].splice(objectIndex, 1);
                    }
                }
            });
        },
        /**
         * Remove a class council.
         * 
         * @param: {String} councilIndex The index of the class council.
         */
        removeClassCouncil: function (councilIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer ce conseil de classe ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app.class_council[councilIndex].id >= 0) {
                        axios.delete("/pia/api/class_council/" + app.class_council[councilIndex].id + "/", token)
                            .then(() => app.class_council.splice(councilIndex, 1))
                            .catch(err => alert(err));
                    } else {
                        app.class_council.splice(councilIndex, 1);
                    }
                }
            });
        },
        getPeople: function (searchQuery, person) {
            person = person.split("-")[0];
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
                    this[person + "Options"] = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
        updateDisorderResponse: function (selected) {
            this.disorderResponseOptions = this.$store.state.disorderResponses.filter(d => {
                return this.form.disorder.map(x => x.id).includes(d.disorder);
            });

            if (selected.length == 0) return;

            // Append corresponding disorder response.
            const lastDisorder = selected[selected.length -1];
            const newDisorderResponse = this.$store.state.disorderResponses.filter(d => {
                const matchDisorder = d.disorder == lastDisorder.id;
                const alreadySelected = this.form.disorder_response.map(dr => dr.id).includes(d.id);
                return matchDisorder && !alreadySelected;
            });
            this.form.disorder_response = this.form.disorder_response.concat(newDisorderResponse);
        },
        showSuccess: function (recordId) {
            let app = this;
            app.sending = false;
            if (app.id) {
                app.$root.$bvToast.toast("Les données ont bien été sauvegardées", {
                    variant: "success",
                    noCloseButton: true,
                });
            } else {
                app.$router.replace(`/edit/${recordId}/${this.advanced}/`,() => {
                    app.$root.$bvToast.toast("Les données ont bien été sauvegardées", {
                        variant: "success",
                        noCloseButton: true,
                    });
                });
            }
        },
        showFailure: function () {
            this.sending = false;
            this.$root.$bvToast.toast("Un problème est survenu lors de l'enregistrement. Merci de vérifier que les données requises ont été complétées.", {
                variant: "danger",
                noCloseButton: true,
            });
        },
        submit: function (evt) {
            if (evt) evt.preventDefault();

            let app = this;
            this.sending = true;
            const data = Object.assign({}, this.form);
            data.advanced = this.advanced;
            data.student_id = data.student.matricule;
            data.disorder = data.disorder.map(d => d.id);
            data.disorder_response = data.disorder_response.map(dr => dr.id);
            data.referent = data.referent.map(r => r.matricule);
            data.sponsor = data.sponsor.map(s => s.matricule);
            data.schedule_adjustment = data.schedule_adjustment.map(sa => sa.id);
            data.attachments = this.uploadedFiles.map(uF => uF.id);

            let send = this.id ? axios.put : axios.post;
            let url = "/pia/api/pia/";
            if (this.id) url += this.id + "/";
            send(url, data, token)
                .then(resp => {
                    const recordId = resp.data.id;
                    // No goals, no promises.
                    if (this.cross_goal.length == 0 && this.branch_goal.length == 0
                        && this.class_council.length == 0 && this.student_project.length == 0
                        && this.parents_opinion.length == 0) {
                        this.showSuccess(recordId);
                        return;
                    }

                    const crossGoalPromises = this.cross_goal.length != 0 ? this.$refs.crossgoals.map(g => g.submit(recordId)) : [];
                    const branchGoalPromises = this.branch_goal.length != 0 && this.$refs.branchgoals ? this.$refs.branchgoals.map(g => g.submit(recordId)) : [];
                    const sPPromises = this.student_project.length != 0 ? this.$refs.studentprojects.map(sP => sP.submit(recordId)) : [];
                    const pOPromises = this.parents_opinion.length != 0 ? this.$refs.parentsopinions.map(pO => pO.submit(recordId)) : [];
                    const classCouncilPromises = this.class_council.length != 0 ? this.$refs.councils.map(c => c.submit(recordId)) : [];
                    Promise.all(crossGoalPromises.concat(branchGoalPromises, classCouncilPromises, sPPromises, pOPromises))
                        .then(resps => {
                            // Update new component with response.
                            const components = ["cross_goal", "branch_goal", "student_project", "parents_opinion", "class_council"];
                            components.forEach(comp => {
                                const compResps = resps.filter(r =>r && r.config.url.includes(`pia/api/${comp}/`));
                                app[comp] = compResps.map(r => r.data).sort((a, b) => a.datetime_creation < b.datetime_creation);
                            });

                            // Save class_council subcomponents.
                            const subPromises = [];
                            const councilResponses = resps.filter(r =>r && r.config.url.includes("/pia/api/class_council/"));

                            if (councilResponses.length == 0) {
                                app.showSuccess(recordId);
                                return;
                            }
                            // Get council statement promises.
                            councilResponses.forEach((r, i) => {
                                if (!("id" in app.$refs.councils[i])) {
                                    app.class_council.splice(i, 1, r.data);
                                    subPromises.concat(app.$refs.councils[i].submitCouncilStatement(app.class_council[i].id));
                                }
                            });

                            Promise.all(subPromises)
                                .then(() => {
                                    app.showSuccess(recordId);
                                })
                                .catch(err => {
                                    console.log(err);
                                    app.showFailure();
                                });
                        })
                        .catch(err => {
                            console.log(err);
                            app.showFailure();
                        });

                }).catch(function (error) {
                    console.log(error);
                    app.showFailure();
                    if ("response" in error) app.errors = error.response.data;
                });
        },
        /**
        * Assign record data from a request.
        * 
        * @param {Number} newId The id of the record.
        */
        loadPIA: function (newId) {
            axios.get("/pia/api/pia/" + newId + "/")
                .then(resp => {
                    this.form.student = resp.data.student;
                    
                    resp.data.referent.map(r => {
                        axios.get("/annuaire/api/responsible/" + r + "/")
                            .then(resp => this.form.referent.push(resp.data));
                    });
                    resp.data.sponsor.map(s => {
                        axios.get("/annuaire/api/responsible/" + s + "/")
                            .then(resp => this.form.sponsor.push(resp.data));
                    });
                    this.form.disorder = this.$store.state.disorders.filter(d => resp.data.disorder.includes(d.id));
                    this.form.disorder_response = this.$store.state.disorderResponses.filter(dr => resp.data.disorder_response.includes(dr.id));
                    this.form.schedule_adjustment = this.$store.state.scheduleAdjustments.filter(sa => resp.data.schedule_adjustment.includes(sa.id));
                    this.form.other_adjustments = resp.data.other_adjustments;
                    this.form.support_activities = resp.data.support_activities;

                    this.loading = false;

                    axios.get(`/dossier_eleve/api/cas_eleve/?page_size=100&info__info=PIA&student__matricule=${resp.data.student.matricule}`)
                        .then(resp => {
                            this.dossier = resp.data.results;
                        });
                    
                    axios.get(`/annuaire/api/student/${resp.data.student.matricule}/`)
                        .then(resp => {
                            this.$store.commit("setCourses", resp.data.courses);
                        });

                    // Attachments
                    this.uploadedFiles = resp.data.attachments.map(a => {
                        return {id: a, file: null};
                    });
                });
        },
        /**
         * Initialize the component.
         * 
         * It will request options for the select inputs and if editing, call
         * the retrieval of the current data record (goals, comments and council included).
         */
        initApp: function () {
            this.supportDays.forEach(d => {
                this.form.support_activities[d] = {branch: [], teachers: []};
            });
            this.$store.dispatch("loadOptions")
                .then(() => {
                    if (this.id) {
                        this.loadingOthers = true;
                        this.loadPIA(this.id);
                        const getAllData = [
                            axios.get("/pia/api/cross_goal/?pia_model=" + this.id),
                            axios.get("/pia/api/branch_goal/?pia_model=" + this.id),
                            axios.get("/pia/api/student_project/?pia_model=" + this.id),
                            axios.get("/pia/api/parents_opinion/?pia_model=" + this.id),
                            axios.get("/pia/api/class_council/?pia_model=" + this.id),
                        ];
                        Promise.all(getAllData)
                            .then(resps => {
                                this.cross_goal = resps[0].data.results;
                                this.branch_goal = resps[1].data.results;
                                this.student_project = resps[2].data.results;
                                this.parents_opinion = resps[3].data.results;
                                this.class_council = resps[4].data.results;

                                this.loading = false;
                                this.loadingOthers = false;
                            });
                    } else {
                        this.loading = false;
                        this.loadingOthers = false;
                    }
                });
        }
    },
    mounted: function () {
        this.initApp();
    },
    components: {
        Multiselect,
        StudentGoal,
        ClassCouncil,
        PiaComment,
        FileUpload,
        quillEditor,
    }
};
</script>

<style>
.first-line {
    background-color: rgba(236, 236, 236, 0.8);
}
</style>
