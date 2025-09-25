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
        <BModal
            size="xl"
            title="Nouvelle demande"
            ok-title="Soumettre"
            cancel-title="Annuler"
            :ok-disabled="!form.sanction_decision_id"
            ref="askModal"
            @ok="askSanction"
            @hidden="resetModal"
        >
            <BRow>
                <BCol sm="4">
                    <div>
                        <BImg
                            rounded
                            :src="'/static/photos/' + name.matricule + '.jpg'"
                            fluid
                            alt="Photo de l'élève"
                        />
                    </div>
                </BCol>
                <BCol>
                    <BForm>
                        <BFormRow>
                            <BCol sm="8">
                                <BFormGroup
                                    label="Nom"
                                    label-for="input-name"
                                    :state="inputStates.name"
                                >
                                    <multiselect
                                        id="input-name"
                                        :internal-search="false"
                                        :options="nameOptions"
                                        @search-change="getNameOptions"
                                        :loading="nameLoading"
                                        placeholder="Rechercher un étudiant…"
                                        select-label=""
                                        selected-label="Sélectionné"
                                        deselect-label=""
                                        label="display"
                                        track-by="matricule"
                                        v-model="name"
                                    >
                                        <template #noResult>
                                            Aucune personne trouvée.
                                        </template>
                                        <template #noOptions />
                                    </multiselect>
                                    <template #invalid-feedback>
                                        {{ errorMsg('name') }}
                                    </template>
                                </BFormGroup>
                            </BCol>
                            <BCol sm="4">
                                <BFormGroup
                                    label="Matricule"
                                    label-for="input-matricule"
                                >
                                    <BFormInput
                                        id="input-matricule"
                                        type="text"
                                        v-model="name.matricule"
                                        readonly
                                    />
                                </BFormGroup>
                            </BCol>
                        </BFormRow>
                        <BFormRow>
                            <BFormGroup
                                label="Demandeur"
                                label-for="input-demandeur"
                                :state="inputStates.demandeur"
                            >
                                <multiselect
                                    id="input-demandeur"
                                    :internal-search="false"
                                    :options="demandeurOptions"
                                    @search-change="getDemandeurOptions"
                                    :loading="demandeurLoading"
                                    placeholder="Rechercher un responsable…"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label=""
                                    label="display"
                                    track-by="display"
                                    v-model="demandeur"
                                >
                                    <template #noResult>
                                        Aucun responsable trouvée.
                                    </template>
                                    <template #noOptions />
                                </multiselect>
                                <template #invalid-feedback>
                                    {{ errorMsg('demandeur') }}
                                </template>
                            </BFormGroup>
                        </BFormRow>
                        <BFormRow v-if="store.canSetSanction">
                            <BFormGroup>
                                <BFormCheckbox v-model="form.important">
                                    Marquer comme important.
                                </BFormCheckbox>
                            </BFormGroup>
                        </BFormRow>
                        <BFormRow class="mt-2">
                            <BCol sm="7">
                                <BFormGroup
                                    label="Sanction disciplinaire"
                                    label-for="input-info"
                                    :state="inputStates.sanction_decision_id"
                                >
                                    <BFormSelect
                                        id="input-info"
                                        v-model="form.sanction_decision_id"
                                        :options="sanctionOptions"
                                    >
                                        <template #first>
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez un type de sanction
                                            </option>
                                        </template>
                                    </BFormSelect>
                                    <template #invalid-feedback>
                                        {{ errorMsg('sanction_decision_id') }}
                                    </template>
                                </BFormGroup>
                                <div v-if="store.canSetSanction">
                                    <BFormGroup
                                        v-if="store.settings.enable_disciplinary_council"
                                        label="Date du conseil"
                                        label-for="input-date-conseil"
                                        :state="inputStates.datetime_conseil"
                                    >
                                        <BFormInput
                                            id="input-date-conseil"
                                            type="date"
                                            v-model="form.datetime_conseil"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('datetime_conseil') }}
                                        </template>
                                    </BFormGroup>
                                    <BFormGroup
                                        label="Date de la sanction"
                                        label-for="input-date-sanction"
                                        :state="inputStates.date_sanction"
                                    >
                                        <BFormInput
                                            id="input-date-sanction"
                                            type="date"
                                            v-model="form.date_sanction"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('date_sanction') }}
                                        </template>
                                    </BFormGroup>
                                    <BFormGroup
                                        label="Date de fin de la sanction"
                                        label-for="input-date-sanction-end"
                                        :state="inputStates.date_sanction_end"
                                    >
                                        <BFormInput
                                            id="input-date-sanction-end"
                                            type="date"
                                            v-model="form.date_sanction_end"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('date_sanction_end') }}
                                        </template>
                                    </BFormGroup>
                                    <BFormGroup
                                        label="Heure de début de la sanction"
                                        label-for="input-time-sanction-start"
                                    >
                                        <BFormInput
                                            id="input-time-sanction-start"
                                            type="time"
                                            v-model="form.time_sanction_start"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('time_sanction_start') }}
                                        </template>
                                    </BFormGroup>
                                    <BFormGroup
                                        label="Heure de fin de la sanction"
                                        label-for="input-time-sanction-end"
                                        :state="inputStates.time_sanction_end"
                                    >
                                        <BFormInput
                                            id="input-time-sanction-end"
                                            type="time"
                                            v-model="form.time_sanction_end"
                                        />
                                        <template #invalid-feedback>
                                            {{ errorMsg('time_sanction_end') }}
                                        </template>
                                    </BFormGroup>
                                </div>
                            </BCol>
                            <BCol sm="5">
                                <BListGroup>
                                    <BListGroupItem
                                        class="d-flex justify-content-between align-items-center"
                                        v-for="(val, index) in stats"
                                        :key="index"
                                    >
                                        <strong>{{ val.display }} :</strong> {{ val.value }}
                                    </BListGroupItem>
                                </BListGroup>
                            </BCol>
                        </BFormRow>
                        <BFormRow>
                            <BCol>
                                <BFormGroup
                                    label="Commentaires"
                                    label-for="input-comment"
                                    :state="inputStates.explication_commentaire"
                                >
                                    <text-editor v-model="form.explication_commentaire" />
                                    <template #invalid-feedback>
                                        {{ errorMsg('explication_commentaire') }}
                                    </template>
                                </BFormGroup>
                                <BFormGroup
                                    description="Ajouter un ou des fichiers. Accepte uniquement des fichiers pdf."
                                    label="Fichier(s)"
                                >
                                    <BFormFile
                                        multiple
                                        accept=".pdf"
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
                                            path="/dossier_eleve/upload_file/"
                                            :removestr="5"
                                            @delete="deleteFile(index)"
                                            @setdata="setFileData(index, $event)"
                                        />
                                    </BListGroup>
                                </BFormGroup>
                            </BCol>
                        </BFormRow>
                        <BFormRow>
                            <BCol>
                                <BFormGroup
                                    v-if="visibilityOptions.length > 0"
                                    label="Donner la visibilité à :"
                                >
                                    <BFormCheckboxGroup
                                        stacked
                                        v-model="form.visible_by_groups"
                                        name="visible_by_groups"
                                        :options="visibilityOptions"
                                        value-field="id"
                                        text-field="text"
                                    />
                                </BFormGroup>
                            </BCol>
                        </BFormRow>
                    </BForm>
                </BCol>
            </BRow>
        </BModal>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import axios from "axios";

import { askSanctionsStore } from "./stores/ask_sanctions.js";

import FileUpload from "@s:core/js/common/file_upload.vue";

export default {
    props: {
        "entry": {
            type: Object,
            default: () => { }
        }
    },
    data: function () {
        return {
            form: {
                name: "",
                student_id: null,
                sanction_decision_id: null,
                explication_commentaire: "",
                important: false,
                demandeur: "",
                date_sanction: null,
                date_sanction_end: null,
                time_sanction_start: null,
                time_sanction_end: null,
                datetime_conseil: null,
                visible_by_groups: [],
            },
            attachments: [],
            uploadedFiles: [],
            sanctionOptions: [],
            name: { matricule: null },
            nameOptions: [],
            nameLoading: false,
            demandeur: {},
            demandeurOptions: [],
            demandeurLoading: false,
            searchId: 0,
            stats: [],
            timeSanction: null,
            visibilityOptions: [],
            errors: {},
            inputStates: {
                name: null,
                sanction_decision_id: null,
                demandeur: null,
                explication_commentaire: null,
                time_sanction_start: null,
                time_sanction_end: null,
            },
            store: askSanctionsStore(),
        };
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                // First update form name data.
                this.form.name = this.name.display;
                this.form.student_id = this.name.matricule;
                // Get statistics.
                axios.get("/dossier_eleve/api/statistics/" + this.name.matricule + "/")
                    .then(response => {
                        this.stats = response.data.filter(s => s.type === "sanction-decision");
                    })
                    .catch(function (error) {
                        alert(error);
                    });
            }
        },
        errors: function (newErrors) {
            let inputs = ["name", "sanction_decision_id", "demandeur", "explication_commentaire",
                "datetime_conseil", "date_sanctionl", "time_sanction_start", "time_sanction_end"];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
        entry: function (entry) {
            if (entry) {
                // The name will update form.name and form.matricule_id
                this.name = {
                    display: entry.name,
                    matricule: entry.student_id,
                };
                this.demandeur = {
                    display: entry.demandeur,
                };
                this.form.explication_commentaire = entry.explication_commentaire;
                this.form.important = entry.important;

                this.form.sanction_decision_id = entry.sanction_decision_id;
                this.form.date_sanction = entry.date_sanction;
                this.form.date_sanction_end = entry.date_sanction_end;
                this.form.time_sanction_start = entry.time_sanction_start ? entry.time_sanction_start : null;
                this.form.time_sanction_end = entry.time_sanction_end ? entry.time_sanction_end.slice(0, 5) : null;
                this.form.visible_by_groups = entry.visible_by_groups;
                if (entry.visible_by_tenure) {
                    this.form.visible_by_groups.push(-1);
                }

                if (entry.datetime_conseil) {
                    this.form.datetime_conseil = Moment(entry.datetime_conseil).format("YYYY-MM-DD");
                }
                if (entry.attachments.length > 0) {
                    for (let a in entry.attachments) {
                        this.uploadedFiles.push({ id: entry.attachments[a], file: null });
                    }
                }
            } else {
                this.resetModal();
            }
        },
    },
    methods: {
        show: function () {
            this.$refs.askModal.show();
        },
        hide: function () {
            this.$refs.askModal.hide();
        },
        resetModal: function () {
            this.$emit("reset");

            this.name = { matricule: null };
            this.demandeur = {};
            this.stats = {};
            if (this.$refs.attachments) this.$refs.attachments.reset();
            this.uploadedFiles.splice(0, this.uploadedFiles.length);

            this.form.name = "";
            this.form.student_id = null;
            this.form.sanction_decision_id = null;
            this.form.explication_commentaire = "";
            this.form.important = false;
            this.form.demandeur = "";
            this.form.date_sanction = null;
            this.form.date_sanction_end = null;
            this.form.datetime_conseil = null;
            this.form.time_sanction_start = null;
            this.form.time_sanction_end = null;
            this.form.visible_by_groups = this.visibilityOptions.map(g => g.id);
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        addFiles: function () {
            for (let a in this.attachments) {
                this.uploadedFiles.push({ file: this.attachments[a], id: -1 });
            }
            if (this.attachments) {
                this.attachments.splice(0, this.attachments.length);
            }
        },
        setFileData: function (index, data) {
            this.uploadedFiles[index].id = data.id;
            this.uploadedFiles[index].link = data.attachment;
        },
        deleteFile: function (index) {
            this.uploadedFiles.splice(index, 1);
            this.$refs.attachments.reset();
        },
        askSanction: function (evt) {
            evt.preventDefault();

            this.form.demandeur = this.demandeur.display;
            let data = this.form;

            // Tenure is not a group, remove from groups and add proper setting.
            const tenureGroupIndex = data.visible_by_groups.findIndex(g => g === -1);
            if (tenureGroupIndex >= 0) {
                data.visible_by_groups.splice(tenureGroupIndex, 1);
                data.visible_by_tenure = true;
            } else {
                data.visible_by_tenure = false;
            }

            // Add times if any.
            if (!data.date_sanction) {
                data.date_sanction = null;
            }
            if (!data.time_sanction_start) {
                data.time_sanction_start = null;
            }
            if (!data.time_sanction_end) {
                data.time_sanction_end = null;
            }
            if (data.datetime_conseil) {
                data.datetime_conseil += " 12:00";
            }
            if (this.uploadedFiles.length > 0) {
                data.attachments = Array.from(this.uploadedFiles.map(u => u.id));
            } else if (this.entry) {
                data.attachments = [];
            }

            let modal = this;
            // Send data.
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

            let path = "/dossier_eleve/api/ask_sanctions/";
            if (this.entry) path += this.entry.id + "/";
            const send = this.entry ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(() => {
                this.hide();
                this.errors = {};
                this.$emit("update");
            }).catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        getNameOptions(query) {
            return this.getPeopleOptions(query, "student");
        },
        getDemandeurOptions(query) {
            return this.getPeopleOptions(query, "responsible");
        },
        getPeopleOptions(query, people) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            if (people == "student") this.nameLoading = true;
            if (people == "responsible") this.demandeurLoading = true;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: people,
                check_access: this.store.filters.find(f => f.filterType === "activate_own_classes") ? true : false,
                educ_by_years: "both",
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data.map(p => {
                        // Format entries.
                        let entry = { display: p.last_name + " " + p.first_name, matricule: p.matricule };
                        if ("is_secretary" in p) {
                            // It's a responsible.
                            let teachings = " —";
                            for (let t in p.teaching) {
                                teachings += " " + p.teaching[t].display_name;
                            }
                            entry.display += teachings;
                        } else {
                            // It's a student.
                            entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                            entry.display += " – " + p.teaching.display_name;
                        }
                        return entry;
                    });
                    if (people == "student") {
                        this.nameLoading = false;
                        this.nameOptions = options;
                    } else if (people == "responsible") {
                        this.demandeurLoading = false;
                        this.demandeurOptions = options;
                    }
                })
                .catch(function (error) {
                    alert(error);
                    app.nameLoading = false;
                });
        },
        setVisibilityGroups: function () {
            let settings = this.store.settings;
            // eslint-disable-next-line no-undef
            const groupSet = Object.assign({}, groups);
            groupSet.tenure = {
                id: -1, text: "Titulaire(s)"
            };
            // eslint-disable-next-line no-undef
            if (user_groups.find(g => g.id == groupSet.sysadmin.id)) {
                this.visibilityOptions = Object.values(groupSet).filter(g => g.id !== groupSet.sysadmin.id);
                return;
            }
            // Match between groups and settings name.
            const groupSettingsMatch = {
                direction: "dir",
                educateur: "educ",
                professeur: "teacher",
                pms: "pms",
                coordonateur: "coord",
            };
            const consideredGroups = Object.keys(groupSettingsMatch);
            // eslint-disable-next-line no-undef
            const userGroups = user_groups.filter(g => consideredGroups.includes(g.name));
            const concernedSettings = userGroups.map(g => {
                const allowedGroupSetting = groupSettingsMatch[g.name] + "_allow_visibility_to";
                const forcedGroupSetting = groupSettingsMatch[g.name] + "_force_visibility_to";
                let groupSetting = {
                    group: g.id,
                    isAllowed: new Set(settings[allowedGroupSetting]),
                    isForced: new Set(settings[forcedGroupSetting]),
                };
                // Add tenure "group".
                if (settings.tenure_force_visibility_from.includes(g.id)) {
                    groupSetting.isForced.add(-1);
                }
                if (settings.tenure_allow_visibility_from.includes(g.id)) {
                    groupSetting.isAllowed.add(-1);
                }
                return groupSetting;
            });

            // eslint-disable-next-line no-undef
            if (user_properties.tenure.includes(this.name.classe)) {
                concernedSettings.push({
                    group: -1,
                    isAllowed: new Set(settings.tenure_allow_visibility_to),
                    isForced: new Set(settings.tenure_force_visibility_to),
                });
            }

            const allowedGroups = [...new Set(concernedSettings.map(s => s.isAllowed).reduce((acc, curValue) => {
                return new Set([...curValue, ...acc]);
            }, new Set()))];

            this.visibilityOptions = allowedGroups.map(aG => {
                let group = Object.values(groupSet).find(g => g.id === aG);
                // Is the group forced?
                // First check if a group allows it but is not forced. In this case, this group permission prevails
                // and it is not forced.
                if (concernedSettings.find(uG => [...uG.isAllowed].includes(aG) && ![...uG.isForced].includes(aG))) {
                    group.disabled = false;
                    return group;
                    // Check if the group is simultaneously forced and allowed in the remaining settings.
                } else if (concernedSettings.find(uG => [...uG.isAllowed].includes(aG) && [...uG.isForced].includes(aG))) {
                    // Append the group to pre-selectioned options.
                    this.form.visible_by_groups.push(aG);
                    group.disabled = true;
                    return group;
                }
                return group;
            });
            
        },
    },
    mounted: function () {
        // Set sanctions and decisions options.
        this.store.getSanctions()
            .then(() => {
                this.sanctionOptions = this.store.sanctions.map(m => {
                    return { value: m.id, text: m.sanction_decision };
                });
            })
            .catch(function (error) {
                alert(error);
            });
        
        this.setVisibilityGroups();
        this.form.visible_by_groups = this.visibilityOptions.map(g => g.id);
    },
    components: { Multiselect, TextEditor, FileUpload },
};
</script>

<style></style>
