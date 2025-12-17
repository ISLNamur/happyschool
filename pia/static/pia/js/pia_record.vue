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
    <BContainer>
        <BRow>
            <h3>{{ advanced ? "PIA" : "Aide élève" }} : {{ id ? "Modifier" : "Nouveau" }}</h3>
        </BRow>
        <BRow class="sticky-top p-2 first-line">
            <BCol>
                <BButton @click="$router.back()">
                    Retour à la liste des élèves
                </BButton>
            </BCol>
            <BCol
                cols="5"
                align-self="end"
                class="text-end"
            >
                <BButtonGroup>
                    <BDropdown variant="outline-primary">
                        <template #button-content>
                            <IBiFileEarmarkPdf />
                            PDF
                        </template>
                        <BDropdownItem
                            :href="`/pia/report/${id}/1/`"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Année scolaire en cours
                        </BDropdownItem>
                        <BDropdownItem
                            :href="`/pia/report/${id}/0/`"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            Toutes années confondues
                        </BDropdownItem>
                    </BDropdown>
                    <BButton
                        @click="submit"
                        variant="primary"
                        :disabled="!form.student || sending"
                    >
                        <BSpinner
                            small
                            v-if="sending"
                        />
                        Sauver
                    </BButton>
                </BButtonGroup>
            </BCol>
        </BRow>
        <BOverlay :show="loading">
            <BTabs
                content-class="mt-3"
                justified
                class="mt-2"
            >
                <BTab
                    title="Élève et aménagements"
                    active
                >
                    <BRow>
                        <BCol>
                            <h3>Référents {{ advanced ? "PIA" : "" }}</h3>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol
                            v-if="form.student"
                            md="3"
                        >
                            <BImg
                                :src="`/static/photos/${form.student.matricule}.jpg`"
                                alt="Photo de l'élève"
                                rounded
                                fluid
                            />
                        </BCol>
                        <BCol>
                            <BFormRow>
                                <BCol md="4">
                                    <BFormGroup label="Élève">
                                        <multiselect
                                            id="student-0"
                                            :internal-search="false"
                                            :options="studentOptions"
                                            @search-change="getPeople($event, 'student')"
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
                                            <template #noResult>
                                                Aucun élève trouvé.
                                            </template>
                                            <template #noOptions />
                                        </multiselect>
                                    </BFormGroup>
                                </BCol>
                            </BFormRow>
                            <BFormRow>
                                <BCol>
                                    <BFormGroup
                                        label="Référent(s)"
                                        :state="inputStates.referent"
                                    >
                                        <multiselect
                                            id="responsible-0"
                                            :internal-search="false"
                                            :options="responsibleOptions"
                                            @search-change="getPeople($event, 'responsible')"
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
                                            <template #noResult>
                                                Aucun responsable trouvé.
                                            </template>
                                            <template #noOptions />
                                        </multiselect>
                                        <template #invalid-feedback>
                                            {{ errorMsg('referent') }}
                                        </template>
                                    </BFormGroup>
                                </BCol>
                            </BFormRow>
                            <BFormRow>
                                <BCol>
                                    <BFormGroup
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
                                            <template #noResult>
                                                Aucun responsable trouvé.
                                            </template>
                                            <template #noOptions />
                                        </multiselect>
                                        <template #invalid-feedback>
                                            {{ errorMsg('sponsor') }}
                                        </template>
                                    </BFormGroup>
                                </BCol>
                            </BFormRow>
                        </BCol>
                    </BRow>
                    <BRow class="mt-3">
                        <BCol>
                            <h3>{{ advanced ? "Aménagements" : "Activités de soutien" }}</h3>
                        </BCol>
                    </BRow>
                    <BRow
                        v-if="advanced"
                        class="mt-3"
                    >
                        <BCol>
                            <disorder-selection
                                :pia="Number(id)"
                                ref="disorder"
                            />
                        </BCol>
                    </BRow>
                    <schedule-adjustments
                        v-if="advanced"
                        :pia="Number(id)"
                        ref="adjustments"
                    />
                    <BRow v-else>
                        <BCol>
                            <activity-support
                                :pia="Number(id)"
                                ref="activitysupport"
                            />
                        </BCol>
                    </BRow>
                    <BRow class="mt-4">
                        <BCol>
                            <h3>Fichiers joints</h3>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <BFormGroup
                                description="Ajouter un ou des fichiers. Accepte uniquement des fichiers images et pdf."
                                label="Fichier(s)"
                            >
                                <BFormFile
                                    multiple
                                    accept=".pdf, .jpg, .png, jpeg"
                                    v-model="form.attachments"
                                    ref="attachments"
                                    placeholder="Attacher un ou des fichiers."
                                    choose-label="Attacher un ou des fichiers"
                                    drop-label="Déposer des fichiers ici"
                                    plain
                                    @update:model-value="addFiles"
                                />
                                <BListGroup
                                    v-for="(item, index) in uploadedFiles.filter(uF => uF.visible)"
                                    :key="index"
                                >
                                    <file-upload
                                        :id="item.id"
                                        :file="item.file"
                                        path="/pia/upload_file/"
                                        removestr="4"
                                        group-access
                                        @delete="deleteFile(index)"
                                        @setdata="setFileData(index, $event)"
                                        @unavailable="hideFile(index)"
                                    />
                                </BListGroup>
                            </BFormGroup>
                        </BCol>
                    </BRow>
                </BTab>
                <BTab
                    v-if="advanced"
                    title="Soutien"
                >
                    <BRow>
                        <BCol>
                            <h4>Activités de soutien</h4>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <activity-support
                                :pia="Number(id)"
                                ref="activitysupport"
                            />
                        </BCol>
                    </BRow>
                </BTab>
                <BTab>
                    <template #title>
                        <BOverlay :show="loadingOthers">
                            {{ advanced ? "Conseils de classe" : "Auto-évaluation" }}
                            <BBadge>{{ classCouncilCount }}</BBadge>
                        </BOverlay>
                    </template>
                    <class-council-list
                        ref="councils"
                        :advanced="advanced"
                        :pia="Number(id)"
                        @save="submit"
                        @count="classCouncilCount = $event"
                    />
                </BTab>
                <BTab>
                    <template #title>
                        <BOverlay :show="loadingOthers">
                            Objectifs {{ advanced ? "" : "du CCL" }}
                            <BBadge>{{ cross_goal.length + branch_goal.length }}</BBadge>
                        </BOverlay>
                    </template>
                    <BRow class="mt-2">
                        <BCol>
                            <h4>Objectifs du CCL</h4>
                        </BCol>
                        <BCol class="text-end">
                            <BButton
                                @click="copyGoalsSummary"
                                variant="outline-secondary"
                            >
                                <IBiCopy />
                                Copier objectifs
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow v-if="cross_goal.length + branch_goal.length > 0 && form.student">
                        <BCol>
                            <BTableSimple
                                id="goals-summary"
                                style="display: none;"
                            >
                                <BThead>
                                    <BTr>
                                        <BTh>NOM</BTh>
                                        <BTh>PRÉNOM</BTh>
                                        <BTh
                                            v-for="(g, i) in cross_goal.concat(branch_goal)"
                                            :key="g.id"
                                        >
                                            Objectif {{ i + 1 }}
                                        </BTh>
                                    </BTr>
                                </BThead>
                                <BTbody>
                                    <BTr>
                                        <BTd>
                                            {{ form.student.last_name }}
                                        </BTd>
                                        <BTd>
                                            {{ form.student.first_name }}
                                        </BTd>
                                        <BTd
                                            v-for="(g, i) in goalsList"
                                            :key="i"
                                        >
                                            <p
                                                v-for="(subGoal, j) in g.split(';')"
                                                :key="j"
                                            >
                                                {{ subGoal }}
                                            </p>
                                        </BTd>
                                    </BTr>
                                </BTbody>
                            </BTableSimple>
                        </BCol>
                    </BRow>
                    <BRow class="mt-2">
                        <BCol>
                            <BFormCheckbox
                                v-model="currentCrossGoal"
                                switch
                                @update:model-value="reloadCrossGoal"
                            >
                                Année scolaire en cours
                            </BFormCheckbox>
                        </BCol>
                        <BCol class="text-end">
                            <BButton
                                @click="cross_goal.unshift({ id: -1 })"
                                variant="outline-success"
                            >
                                <IBiPlus />
                                Ajouter
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
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
                        </BCol>
                    </BRow>
                    <BRow class="mt-2">
                        <h4>Objectifs de branche</h4>
                    </BRow>
                    <BRow>
                        <BCol>
                            <BFormCheckbox
                                v-model="currentBranchGoal"
                                switch
                                @update:model-value="reloadBranchGoal"
                            >
                                Année scolaire en cours
                            </BFormCheckbox>
                        </BCol>
                        <BCol class="text-end">
                            <BButton
                                @click="branch_goal.unshift({ id: -1 })"
                                variant="outline-success"
                            >
                                <IBiPlus />
                                Ajouter
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
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
                        </BCol>
                    </BRow>
                    <BRow />
                </BTab>
                <BTab>
                    <template #title>
                        <BOverlay :show="loadingOthers">
                            Projet et avis
                            <BBadge>{{ student_project.length + parents_opinion.length }}</BBadge>
                        </BOverlay>
                    </template>
                    <BRow>
                        <h4>Projet de l'élève</h4>
                    </BRow>
                    <BRow>
                        <BCol>
                            <BButton
                                @click="student_project.unshift({ id: -1 })"
                                variant="outline-secondary"
                            >
                                <IBiPlus />
                                Ajouter
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <pia-comment
                                class="mt-2"
                                v-for="(sP, index) in student_project"
                                :key="sP.id"
                                @remove="removeObject('student_project', index)"
                                comment-type="student_project"
                                :comment-object="sP"
                                ref="studentprojects"
                            />
                        </BCol>
                    </BRow>
                    <BRow>
                        <h4>Avis des parents</h4>
                    </BRow>
                    <BRow>
                        <BCol>
                            <BButton
                                @click="parents_opinion.unshift({ id: -1 })"
                                variant="outline-secondary"
                            >
                                <IBiPlus />
                                Ajouter
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <pia-comment
                                class="mt-2"
                                v-for="(pO, index) in parents_opinion"
                                :key="pO.id"
                                @remove="removeObject('parents_opinion', index)"
                                comment-type="parents_opinion"
                                :comment-object="pO"
                                ref="parentsopinions"
                            />
                        </BCol>
                    </BRow>
                </BTab>
                <BTab v-if="hasDossierApp">
                    <template #title>
                        <BOverlay :show="loadingOthers">
                            Autre infos
                            <BBadge>{{ dossier.length }}</BBadge>
                        </BOverlay>
                    </template>
                    <BRow>
                        <BCol>
                            <h4>Autre infos (<a href="/dossier_eleve/">Dossier de l'élève</a>)</h4>
                        </BCol>
                    </BRow>
                    <BRow class="mb-1">
                        <BCol>
                            <BButton
                                v-if="this.form.student"
                                :href="`/dossier_eleve/?matricule=${this.form.student.matricule}`"
                            >
                                <IBiArrowRight />
                                Vers le dossier de l'élève
                            </BButton>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <BCard
                                v-for="cas in dossier"
                                :key="cas.id"
                                no-body
                                class="mb-1"
                            >
                                <BCardSubtitle class="mt-1 pl-1">
                                    {{ cas.datetime_modified.slice(0, 10) }}
                                </BCardSubtitle>
                                <BcardBody>
                                    <span v-html="cas.explication_commentaire" />
                                </BcardBody>
                                <BcardFooter
                                    class="text-end"
                                >
                                    <BButton
                                        variant="warning"
                                        :href="`/dossier_eleve/#/edit/${cas.id}/`"
                                        class="mb-1 me-1"
                                    >
                                        <IBiPencilSquare />
                                        Modifier
                                    </BButton>
                                    <BButton
                                        v-for="(file, index) in cas.attachments"
                                        :key="file"
                                        :href="`/dossier_eleve/attachment/${file}`"
                                        class="mb-1 me-1"
                                        variant="outline-secondary"
                                    >
                                        <IBiPaperclip />
                                        Fichier {{ index + 1 }}
                                    </BButton>
                                </BcardFooter>
                            </BCard>
                        </BCol>
                    </BRow>
                </BTab>
            </BTabs>
        </BOverlay>
    </BContainer>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { getPeopleByName } from "@s:core/js/common/search.js";
import FileUpload from "@s:core/js/common/file_upload.vue";

import { piaStore } from "./stores/index.js";

import StudentGoal from "./student_goal.vue";
import ClassCouncilList from "./class_council_list.vue";
import PiaComment from "./pia_comment.vue";
import DisorderSelection from "./disorder_selection.vue";
import ScheduleAdjustments from "./schedule_adjustments.vue";

import ActivitySupport from "./activity_support.vue";
import { useModalController, useToastController } from "bootstrap-vue-next";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToastController();
        const { create } = useModalController();
        return { show, create };
    },
    props: {
        id: {
            type: String,
            default: null,
        },
        advanced: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            responsibleOptions: [],
            studentOptions: [],
            disorderResponseOptions: [],
            // eslint-disable-next-line no-undef
            disorderResponseCategories: disorderResponseCategories,
            selected_disorder_response: [],
            editDisorderResponse: false,
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
                support_activities: {},
            },
            uploadedFiles: [],
            cross_goal: [],
            currentCrossGoal: true,
            branch_goal: [],
            currentBranchGoal: true,
            student_project: [],
            parents_opinion: [],
            dossier: [],
            /** List of class council related to this PIA. */
            classCouncilCount: [],
            errors: {},
            /** List of input error states. */
            inputStates: {
                student: null,
                referent: null,
                sponsor: null,
                disorder: null,
                disorder_response: null,
                schedule_adjustment: null,
            },
            dayOfWeek: { 1: "Lundi", 2: "Mardi", 3: "Mercredi", 4: "Jeudi", 5: "Vendredi", 6: "Samedi", 7: "Dimanche" },
            store: piaStore(),
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
         * Get a simple list of goals.
         */
        goalsList: function () {
            if (this.cross_goal.filter(g => g.id > 0).length === 0 && this.branch_goal.filter(g => g.id > 0).length === 0) {
                return "";
            }

            return this.cross_goal.concat(this.branch_goal).filter(g => g.id > 0).map((goal) => {
                let goalText = "";
                if ("branch" in goal) {
                    const branch = this.store.branches.find(b => b.id === goal.branch);
                    goalText = `${branch.branch} : ${goal.branch_goals}`;
                } else {
                    goalText = goal.cross_goals;
                }

                return goalText;
            });
        },
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
            Object.keys(this.inputStates).forEach((key) => {
                if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
    },
    methods: {
        copyGoalsSummary: function () {
            const table = document.querySelector("#goals-summary");
            const htmlData = new ClipboardItem({ ["text/html"]: table.outerHTML });
            navigator.clipboard.write([htmlData])
                .then(() => {
                    this.show({
                        body: "Copié !",
                        variant: "success",
                        noCloseButton: true,
                    });
                });
        },
        addFiles: function () {
            this.uploadedFiles = this.uploadedFiles.concat(this.form.attachments.map((a) => {
                return { file: a, id: -1, visible: true };
            }));
            this.form.attachments.splice(0, this.form.attachments.length);
        },
        setFileData: function (index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
            this.uploadedFiles[index].visible = true;
        },
        deleteFile: function (index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        hideFile: function (index) {
            this.uploadedFiles[index].visible = false;
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
            this.create({
                body: "Cloner cet élément ?",
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then((resp) => {
                if (resp.ok) {
                    let clonedObject = Object.assign({}, app[objectType][objectIndex]);
                    if (app[objectType][objectIndex].id >= 0) {
                        // Remove the id from the object.
                        delete clonedObject.id;
                    }
                    axios.post(`/pia/api/${objectType}/`, clonedObject, token)
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
            this.create({
                body: "Êtes-vous sûr de vouloir supprimer l'élément ?",
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then((resp) => {
                if (resp.ok) {
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
        getPeople: function (searchQuery, person) {
            person = person.split("-")[0];
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
                    this[person + "Options"] = resp.data;
                    // this.searching = false;
                })
                .catch((err) => {
                    alert(err);
                    // this.searching = false;
                });
        },
        updateDisorderResponse: function (selected) {
            this.disorderResponseOptions = this.store.disorderResponses.filter((d) => {
                return this.form.disorder.map(x => x.id).includes(d.disorder);
            });

            if (selected.length == 0) return;

            // Keep disorder response related to only selected disorder.
            this.selected_disorder_response = this.selected_disorder_response.filter(
                sDR => this.disorderResponseOptions.includes(sDR.disorder_response),
            );
        },
        showSuccess: function (recordId) {
            let app = this;
            app.sending = false;
            if (app.id) {
                app.show({
                    body: "Les données ont bien été sauvegardées",
                    variant: "success",
                    noCloseButton: true,
                });
            } else {
                app.$router.replace(`/edit/${recordId}/${this.advanced}/`).then(() => {
                    app.show({
                        body: "Les données ont bien été sauvegardées",
                        variant: "success",
                        noCloseButton: true,
                    });
                });
            }
        },
        showFailure: function () {
            this.sending = false;
            this.show({
                body: "Un problème est survenu lors de l'enregistrement. Merci de vérifier que les données requises ont été complétées.",
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
            data.selected_disorder_response = this.selected_disorder_response.map(dr => dr.id);
            data.referent = data.referent.map(r => r.matricule);
            data.sponsor = data.sponsor.map(s => s.matricule);
            data.schedule_adjustment = data.schedule_adjustment.map(sa => sa.id);
            data.attachments = this.uploadedFiles.map(uF => uF.id);

            let send = this.id ? axios.put : axios.post;
            let url = "/pia/api/pia/";
            if (this.id) url += this.id + "/";
            send(url, data, token)
                .then((resp) => {
                    const recordId = resp.data.id;

                    const disorderPromise = this.advanced ? [app.$refs.disorder.save(recordId)] : [];
                    const scheduleAdjustPromise = this.advanced ? [app.$refs.adjustments.save(recordId)] : [];
                    const activitySupportPromise = [app.$refs.activitysupport.save(recordId)];
                    const crossGoalPromises = this.cross_goal.length != 0 ? this.$refs.crossgoals.map(g => g.submit(recordId)) : [];
                    const branchGoalPromises = this.branch_goal.length != 0 && this.$refs.branchgoals ? this.$refs.branchgoals.map(g => g.submit(recordId)) : [];
                    const sPPromises = this.student_project.length != 0 ? this.$refs.studentprojects.map(sP => sP.submit(recordId)) : [];
                    const pOPromises = this.parents_opinion.length != 0 ? this.$refs.parentsopinions.map(pO => pO.submit(recordId)) : [];
                    const classCouncilPromises = this.$refs.councils.save(recordId);
                    Promise.all(crossGoalPromises.concat(
                        disorderPromise, scheduleAdjustPromise, activitySupportPromise,
                        branchGoalPromises, classCouncilPromises, sPPromises, pOPromises,
                    ))
                        .then((resps) => {
                            // Update new component with response.
                            const components = ["cross_goal", "branch_goal", "student_project", "parents_opinion"];
                            components.forEach((comp) => {
                                const compResps = resps.filter(r => r && r.config.url.includes(`pia/api/${comp}/`));
                                app[comp] = compResps.map(r => r.data).sort((a, b) => a.datetime_creation < b.datetime_creation);
                            });

                            app.showSuccess(recordId);
                        })
                        .catch((err) => {
                            console.log(err);
                            app.showFailure();
                        });
                }).catch(function (error) {
                    console.log(error);
                    app.showFailure();
                    if ("response" in error) app.errors = error.response.data;
                });
        },
        reloadCrossGoal: function () {
            axios.get(`/pia/api/cross_goal/?pia_model=${this.id}&current_scholar_year=${this.currentCrossGoal}`)
                .then((resp) => {
                    this.cross_goal = resp.data.results;
                });
        },
        reloadBranchGoal: function () {
            axios.get(`/pia/api/branch_goal/?pia_model=${this.id}&current_scholar_year=${this.currentBranchGoal}`)
                .then((resp) => {
                    this.branch_goal = resp.data.results;
                });
        },
        /**
        * Assign record data from a request.
        *
        * @param {Number} newId The id of the record.
        */
        loadPIA: function (newId) {
            axios.get("/pia/api/pia/" + newId + "/")
                .then((resp) => {
                    this.form.student = resp.data.student;

                    resp.data.referent.map((r) => {
                        axios.get("/annuaire/api/responsible/" + r + "/")
                            .then(resp => this.form.referent.push(resp.data));
                    });
                    resp.data.sponsor.map((s) => {
                        axios.get("/annuaire/api/responsible/" + s + "/")
                            .then(resp => this.form.sponsor.push(resp.data));
                    });
                    this.form.disorder = this.store.disorders.filter(d => resp.data.disorder.includes(d.id));
                    // this.form.disorder_response = this.store.disorderResponses.filter(dr => resp.data.disorder_response.includes(dr.id));
                    this.form.schedule_adjustment = this.store.scheduleAdjustments.filter(sa => resp.data.schedule_adjustment.includes(sa.id));
                    this.form.other_adjustments = resp.data.other_adjustments;

                    this.loading = false;

                    axios.get(`/dossier_eleve/api/cas_eleve/?page_size=100&info__info=PIA&student__matricule=${resp.data.student.matricule}`)
                        .then((resp) => {
                            this.dossier = resp.data.results;
                        });

                    axios.get(`/annuaire/api/student/${resp.data.student.matricule}/`)
                        .then((resp) => {
                            this.store.setCourses(resp.data.courses);
                        });

                    this.form.selected_disorder_response = resp.data.selected_disorder_response;
                    this.selectedResponseLoading = true;
                    Promise.all(resp.data.selected_disorder_response.map(id => axios.get(`/pia/api/selected_disorder_response_new/${id}/`)))
                        .then((resps) => {
                            this.selected_disorder_response = resps.map(r => r.data);
                            this.selectedResponseLoading = false;
                        });

                    // Attachments
                    this.uploadedFiles = resp.data.attachments.map((a) => {
                        return { id: a, file: null, visible: true };
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
            this.store.loadOptions()
                .then(() => {
                    if (this.id) {
                        this.loadingOthers = true;
                        this.loadPIA(this.id);
                        const getAllData = [
                            axios.get(`/pia/api/cross_goal/?pia_model=${this.id}&current_scholar_year=${this.currentCrossGoal}`),
                            axios.get(`/pia/api/branch_goal/?pia_model=${this.id}&current_scholar_year=${this.currentBranchGoal}`),
                            axios.get("/pia/api/student_project/?pia_model=" + this.id),
                            axios.get("/pia/api/parents_opinion/?pia_model=" + this.id),
                        ];
                        Promise.all(getAllData)
                            .then((resps) => {
                                this.cross_goal = resps[0].data.results;
                                this.branch_goal = resps[1].data.results;
                                this.student_project = resps[2].data.results;
                                this.parents_opinion = resps[3].data.results;

                                this.loadingOthers = false;
                            });
                    } else {
                        this.loading = false;
                        this.loadingOthers = false;
                    }
                });
        },
    },
    mounted: function () {
        this.initApp();
    },
    components: {
        Multiselect,
        StudentGoal,
        ClassCouncilList,
        PiaComment,
        DisorderSelection,
        ScheduleAdjustments,
        FileUpload,
        ActivitySupport,
    },
};
</script>

<style>
.first-line {
    background-color: rgba(236, 236, 236, 0.8);
}

.scrollable {
    height: 300px;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>
