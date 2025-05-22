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
            <BCol>
                <h2>
                    {{ id < 0 ? "Ajouter un cas" : "Modifier un cas" }}
                </h2>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BButton to="/">
                    Retour à la liste
                </BButton>
            </BCol>
        </BRow>
        <BRow class="mt-2">
            <BCol sm="3">
                <div class="text-center">
                    <BImg
                        v-if="name.matricule"
                        rounded
                        :src="'/static/photos/' + name.matricule + '.jpg'"
                        fluid
                        alt="Photo de l'élève"
                    />
                </div>
            </BCol>
            <BCol>
                <BForm @submit="submit">
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
                        <BCol>
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
                        </BCol>
                    </BFormRow>
                    <BFormRow class="mb-2">
                        <BCol>
                            <BFormGroup
                                description="Mettre en évidence les informations importantes sur le long terme (décès d'un parent, dyslexie, anorexie, idées noires...)."
                            >
                                <BFormCheckbox v-model="form.important">
                                    Marquer comme important.
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup label="Type d'info">
                                <BFormRadioGroup
                                    id="info-or-sanction"
                                    v-model="infoOrSanction"
                                    :disabled="id >= 0 ? true : false"
                                >
                                    <BFormRadio value="info">
                                        Non disciplinaire
                                    </BFormRadio>
                                    <BFormRadio
                                        value="sanction-decision"
                                        :disabled="!store.canSetSanction"
                                    >
                                        Disciplinaire
                                    </BFormRadio>
                                </BFormRadioGroup>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <div v-if="infoOrSanction == 'info'">
                        <BFormRow>
                            <BCol>
                                <BFormGroup
                                    label="Info"
                                    label-for="input-info"
                                    :state="inputStates.info_id"
                                >
                                    <BFormSelect
                                        id="input-info"
                                        v-model="form.info_id"
                                        :options="infoOptions"
                                    >
                                        <template #first>
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez un type d'info
                                            </option>
                                        </template>
                                    </BFormSelect>
                                    <template #invalid-feedback>
                                        {{ errorMsg('info_id') }}
                                    </template>
                                </BFormGroup>
                            </BCol>
                        </BFormRow>
                    </div>
                    <div v-if="infoOrSanction == 'sanction-decision'">
                        <BFormRow>
                            <BCol sm="7">
                                <BFormGroup
                                    label="Info disciplinaire"
                                    label-for="input-info"
                                    :state="inputStates.sanction_decision_id"
                                >
                                    <BFormSelect
                                        id="input-info"
                                        v-model="form.sanction_decision_id"
                                        :options="sanctionDecisionOptions"
                                    >
                                        <template #first>
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez dans la liste
                                            </option>
                                        </template>
                                    </BFormSelect>
                                    <template #invalid-feedback>
                                        {{ errorMsg('sanction_decision_id') }}
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
                                    v-if="form.sanction_faite !== null"
                                    label-for="input-sanction-faite"
                                >
                                    <BFormCheckbox
                                        id="input-sanction-faite"
                                        v-model="form.sanction_faite"
                                    >
                                        Sanction faite ?
                                    </BFormCheckbox>
                                </BFormGroup>
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
                    </div>
                    <BFormRow v-if="infoOrSanction">
                        <BCol>
                            <BFormGroup
                                label="Commentaires"
                                label-for="input-comment"
                                :state="inputStates.explication_commentaire"
                            >
                                <text-editor
                                    v-model="form.explication_commentaire"
                                    div-block
                                />
                                <template #invalid-feedback>
                                    {{ errorMsg('explication_commentaire') }}
                                </template>
                            </BFormGroup>
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
                                        path="/dossier_eleve/upload_file/"
                                        :removestr="5"
                                        @delete="deleteFile(index)"
                                        @setdata="setFileData(index, $event)"
                                        remove-media
                                    />
                                </BListGroup>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow class="mb-2">
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
                            <BFormCheckbox
                                v-model="form.send_to_teachers"
                                :disabled="!store.canSetSanction"
                            >
                                Envoyer l'info par courriel aux professeurs de la classe de l'élève (les fichiers seront
                                joints).
                            </BFormCheckbox>
                        </BCol>
                    </BFormRow>
                    <BButton
                        variant="primary"
                        v-if="form.info_id || form.sanction_decision_id"
                        type="submit"
                        :disabled="sending"
                    >
                        Soumettre
                    </BButton>
                </BForm>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

import FileUpload from "@s:core/js/common/file_upload.vue";

import { dossierEleveStore } from "./stores/dossier_eleve.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        "id": {
            type: String,
            default: "-1"
        }
    },
    data: function () {
        return {
            casObject: null,
            form: {
                name: "",
                student_id: null,
                info_id: null,
                sanction_decision_id: null,
                explication_commentaire: "",
                important: false,
                demandeur: "",
                visible_by_groups: [],
                date_sanction: null,
                sanction_faite: null,
                send_to_teachers: false,
                attachments: [],
            },
            attachments: [],
            uploadedFiles: [],
            infoOrSanction: null,
            infoOptions: [],
            sanctionDecisionOptions: [],
            name: { matricule: null },
            nameOptions: [],
            nameLoading: false,
            demandeur: {},
            demandeurOptions: [],
            demandeurLoading: false,
            searchId: 0,
            stats: {},
            errors: {},
            inputStates: {
                name: null,
                info_id: null,
                sanction_decision_id: null,
                demandeur: null,
                explication_commentaire: null,
            },
            visibilityOptions: [],
            sending: false,
            store: dossierEleveStore(),
        };
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                // First update form name data.
                this.form.name = `${this.name.fullname}`;
                this.form.student_id = this.name.matricule;
                // Get statistics.
                axios.get("/dossier_eleve/api/statistics/" + this.name.matricule + "/")
                    .then(response => {
                        this.stats = JSON.parse(response.data);
                    })
                    .catch(function (error) {
                        alert(error);
                    });
                // Set policies.
                this.setVisibilityGroups();
            }
        },
        infoOrSanction: function (newChoice) {
            // Reset other part of the form (sanction_decision or info).
            if (newChoice == "info") {
                this.form.sanction_decision_id = null;
            } else {
                this.form.info_id = null;
            }
        },
        errors: function (newErrors) {
            let inputs = ["name", "info_id", "sanction_decision_id", "demandeur", "explication_commentaire"];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
    },
    methods: {
        addFiles: function () {
            for (let a in this.attachments) {
                this.uploadedFiles.push({ file: this.attachments[a], id: -1 });
            }
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
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        setCas: function () {
            if (this.casObject) {
                // The name will update form.name and form.student_id
                this.name = {
                    display: this.casObject.student.display,
                    fullname: `${this.casObject.student.last_name} ${this.casObject.student.first_name}`,
                    matricule: this.casObject.student_id,
                    classe: this.casObject.student.classe.id,
                };
                this.demandeur = {
                    display: this.casObject.demandeur,
                };
                this.form.explication_commentaire = this.casObject.explication_commentaire;
                this.form.info_id = this.casObject.info_id;
                this.form.important = this.casObject.important;
                this.form.sanction_decision_id = this.casObject.sanction_decision_id;
                this.form.date_sanction = this.casObject.date_sanction;
                this.form.sanction_faite = this.casObject.sanction_faite;

                this.infoOrSanction = this.casObject.info_id ? "info" : "sanction-decision";
                // Set policies.
                this.form.visible_by_groups = this.casObject.visible_by_groups;
                if (this.casObject.visible_by_tenure) {
                    this.form.visible_by_groups.push(-1);
                }

                this.setSanctionDecisionOptions();

                if (this.casObject.attachments.length > 0) {
                    for (let a in this.casObject.attachments) {
                        this.uploadedFiles.push({ id: this.casObject.attachments[a], file: null });
                    }
                }
            }
        },
        submit: function (evt) {
            evt.preventDefault();

            this.sending = true;
            this.form.demandeur = this.demandeur.display;
            let data = JSON.parse(JSON.stringify(this.form));

            // Tenure is not a group, remove from groups and add proper setting.
            const tenureGroupIndex = data.visible_by_groups.findIndex(g => g === -1);
            if (tenureGroupIndex >= 0) {
                data.visible_by_groups.splice(tenureGroupIndex, 1);
                data.visible_by_tenure = true;
            } else {
                data.visible_by_tenure = false;
            }

            if (this.uploadedFiles.length > 0) {
                data.attachments = Array.from(this.uploadedFiles.map(u => u.id));
            } else if (this.casObject) {
                data.attachments = [];
            }

            let modal = this;
            // Send data.
            let path = "/dossier_eleve/api/cas_eleve/";
            if (this.casObject) path += this.id + "/";
            const send = this.casObject ? axios.put(path, data, token) : axios.post(path, data, token);

            send.then(() => {
                this.sending = false;
                this.$router.push("/").then(() => {
                    this.show( {
                        body: "Les données ont bien été envoyées",
                        variant: "success",
                        noCloseButton: true,
                    });
                });
            }).catch(function (error) {
                this.sending = false;
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

            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: people,
                check_access: true,
                tenure_class_only: this.store.settings.filter_teacher_entries_by_tenure,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data.map(p => {
                        // Format entries.
                        let entry = { display: p.last_name + " " + p.first_name, matricule: p.matricule };
                        // Append teachings if necessary.
                        if ("is_secretary" in p) {
                            if (this.store.settings.teachings.length > 1) {
                                // It's a responsible.
                                let teachings = " —";
                                for (let t in p.teaching) {
                                    teachings += " " + p.teaching[t].display_name;
                                }
                                entry.display += teachings;
                            }
                        } else {
                            // It's a student.
                            entry.fullname = entry.display;
                            entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                            entry.classe = p.classe.id;
                            if (this.store.settings.teachings.length > 1) entry.display += " – " + p.teaching.display_name;
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
        setSanctionDecisionOptions: function () {
            // Set sanctions and decisions options.
            axios.get("/dossier_eleve/api/sanction_decision/")
                .then(response => {
                    this.sanctionDecisionOptions = response.data.results.map(m => {
                        let entry = { value: m.id, text: m.sanction_decision };
                        if (this.store.settings.enable_submit_sanctions) {
                            entry["disabled"] = m.can_ask;
                        }
                        return entry;
                    });

                    // Keep sanction decision entry.
                    if (this.store.settings.enable_submit_sanctions) {
                        this.sanctionDecisionOptions = this.sanctionDecisionOptions.filter(s => {
                            if (this.form.sanction_decision_id === s.value || !s.disabled) {
                                return true;
                            } else {
                                return false;
                            }
                        });
                    }
                })
                .catch(function (error) {
                    alert(error);
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
    components: { Multiselect, TextEditor, FileUpload },
    mounted: function () {
        if (this.id >= 0) {
            axios.get(`/dossier_eleve/api/cas_eleve/${this.id}`)
                .then(resp => {
                    this.casObject = resp.data;
                    this.setCas();
                });
        } else {
            // Prefill demandeur.
            // eslint-disable-next-line no-undef
            axios.get(`/annuaire/api/responsible/${user_properties.matricule}`)
                .then(resp => {
                    this.demandeur = resp.data;
                    if (this.store.settings.teachings.length > 1) {
                        let teachings = " —";
                        for (let t in this.demandeur.teaching) {
                            teachings += " " + this.demandeur.teaching[t].display_name;
                        }
                        this.demandeur.display += teachings;
                    }
                });
        }

        // Set info options.
        axios.get("/dossier_eleve/api/info/")
            .then(response => {
                this.infoOptions = response.data.results.map(m => {
                    return { value: m.id, text: m.info };
                });
            })
            .catch(function (error) {
                alert(error);
            });

        this.setSanctionDecisionOptions();
    }
};
</script>
