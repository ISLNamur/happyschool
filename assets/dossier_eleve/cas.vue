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
            <b-col>
                <h2>
                    {{ id &lt; 0 ? "Ajouter un cas" : "Modifier un cas" }}
                </h2>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-btn to="/">
                    Retour à la liste
                </b-btn>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col sm="3">
                <div class="text-center">
                    <b-img
                        v-if="name.matricule"
                        rounded
                        :src="'/static/photos/' + name.matricule + '.jpg'"
                        fluid
                        alt="Photo de l'élève"
                    />
                </div>
            </b-col>
            <b-col>
                <b-form
                    @submit="submit"
                >
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group
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
                                    <span slot="noResult">Aucune personne trouvée.</span>
                                    <span slot="noOptions" />
                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('name') }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group
                                label="Matricule"
                                label-for="input-matricule"
                            >
                                <b-form-input
                                    id="input-matricule"
                                    type="text"
                                    v-model="name.matricule"
                                    readonly
                                />
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group
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
                                    <span slot="noResult">Aucun responsable trouvée.</span>
                                    <span slot="noOptions" />
                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('demandeur') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row class="mb-2">
                        <b-col>
                            <b-form-checkbox v-model="form.important">
                                Marquer comme important.
                            </b-form-checkbox>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Type d'info">
                                <b-form-radio-group
                                    id="info-or-sanction"
                                    v-model="infoOrSanction"
                                    :disabled="id >= 0 ? true : false"
                                >
                                    <b-form-radio value="info">
                                        Non disciplinaire
                                    </b-form-radio>
                                    <b-form-radio
                                        value="sanction-decision"
                                        :disabled="!$store.state.canSetSanction"
                                    >
                                        Disciplinaire
                                    </b-form-radio>
                                </b-form-radio-group>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <div v-if="infoOrSanction == 'info'">
                        <b-form-row>
                            <b-col>
                                <b-form-group
                                    label="Info"
                                    label-for="input-info"
                                    :state="inputStates.info_id"
                                >
                                    <b-form-select
                                        id="input-info"
                                        v-model="form.info_id"
                                        :options="infoOptions"
                                    >
                                        <template slot="first">
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez un type d'info
                                            </option>
                                        </template>
                                    </b-form-select>
                                    <span slot="invalid-feedback">{{ errorMsg('info_id') }}</span>
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                    </div>
                    <div v-if="infoOrSanction == 'sanction-decision'">
                        <b-form-row>
                            <b-col sm="7">
                                <b-form-group
                                    label="Info disciplinaire"
                                    label-for="input-info"
                                    :state="inputStates.sanction_decision_id"
                                >
                                    <b-form-select
                                        id="input-info"
                                        v-model="form.sanction_decision_id"
                                        :options="sanctionDecisionOptions"
                                    >
                                        <template slot="first">
                                            <option
                                                :value="null"
                                                disabled
                                            >
                                                Choisissez dans la liste
                                            </option>
                                        </template>
                                    </b-form-select>
                                    <span slot="invalid-feedback">{{ errorMsg('sanction_decision_id') }}</span>
                                </b-form-group>
                                <b-form-group
                                    label="Date de la sanction"
                                    label-for="input-date-sanction"
                                    :state="inputStates.datetime_sanction"
                                >
                                    <b-form-input
                                        id="input-date-sanction"
                                        type="date"
                                        v-model="form.datetime_sanction"
                                    />
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_sanction') }}</span>
                                </b-form-group>
                                <b-form-group
                                    v-if="form.sanction_faite !== null"
                                    label-for="input-sanction-faite"
                                >
                                    <b-form-checkbox
                                        id="input-sanction-faite"
                                        v-model="form.sanction_faite"
                                    >
                                        Sanction faite ?
                                    </b-form-checkbox>
                                </b-form-group>
                            </b-col>
                            <b-col sm="5">
                                <b-list-group>
                                    <b-list-group-item
                                        class="d-flex justify-content-between align-items-center"
                                        v-for="(val, index) in stats"
                                        :key="index"
                                    >
                                        <strong>{{ val.display }} :</strong> {{ val.value }}
                                    </b-list-group-item>
                                </b-list-group>
                            </b-col>
                        </b-form-row>
                    </div>
                    <b-form-row v-if="infoOrSanction">
                        <b-col>
                            <b-form-group
                                label="Commentaires"
                                label-for="input-comment"
                                :state="inputStates.explication_commentaire"
                            >
                                <quill-editor
                                    v-model="form.explication_commentaire"
                                    :options="editorOptions"
                                />
                                <span slot="invalid-feedback">{{ errorMsg('explication_commentaire') }}</span>
                            </b-form-group>
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
                                        path="/dossier_eleve/upload_file/"
                                        :removestr="5"
                                        @delete="deleteFile(index)"
                                        @setdata="setFileData(index, $event)"
                                    />
                                </b-list-group>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row
                        v-if="infoOrSanction == 'info'"
                        class="mb-2"
                    >
                        <b-col>
                            <b-form-group
                                v-if="visibilityOptions.length > 0"
                                label="Donner la visibilité à :"
                            >
                                <b-form-checkbox-group
                                    stacked
                                    v-model="form.visible_by_groups"
                                    name="visible_by_groups"
                                    :options="visibilityOptions"
                                    value-field="id"
                                    text-field="text"
                                />
                            </b-form-group>
                            <b-form-checkbox
                                v-model="form.send_to_teachers"
                                :disabled="!$store.state.canSetSanction"
                            >
                                Envoyer l'info par courriel aux professeurs de la classe de l'élève (les fichiers seront joints).
                            </b-form-checkbox>
                        </b-col>
                    </b-form-row>
                    <b-btn
                        variant="primary"
                        v-if="form.info_id || form.sanction_decision_id"
                        type="submit"
                        :disabled="sending"
                    >
                        Soumettre
                    </b-btn>
                </b-form>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import Moment from "moment";
Moment.locale("fr");

import axios from "axios";
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import FileUpload from "../common/file_upload.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
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
                matricule_id: null,
                info_id: null,
                sanction_decision_id: null,
                explication_commentaire: "",
                important: false,
                demandeur: "",
                visible_by_groups: [],
                datetime_sanction: null,
                sanction_faite: null,
                send_to_teachers: false,
                attachments: [],
            },
            attachments: [],
            uploadedFiles: [],
            infoOrSanction: null,
            infoOptions: [],
            sanctionDecisionOptions: [],
            name: {matricule: null},
            nameOptions: [],
            nameLoading: false,
            demandeur: {},
            demandeurOptions: [],
            demandeurLoading: false,
            searchId: 0,
            stats: {},
            timeSanction: null,
            errors: {},
            inputStates: {
                name: null,
                info_id: null,
                sanction_decision_id: null,
                demandeur: null,
                explication_commentaire: null,
            },
            visibilityOptions: [],
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
            sending: false,
        };
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                // First update form name data.
                this.form.name = this.name.display;
                this.form.matricule_id = this.name.matricule;
                // Get statistics.
                axios.get("dossier_eleve/api/statistics/" + this.name.matricule + "/")
                    .then(response => {
                        this.stats = JSON.parse(response.data);
                    })
                    .catch(function (error) {
                        alert(error);
                    });
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
        addFiles: function() {
            for (let a in this.attachments) {
                this.uploadedFiles.push({file: this.attachments[a], id: -1});
            }
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
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        setCas: function () {
            if (this.casObject) {
                // The name will update form.name and form.matricule_id
                this.name = {
                    display: this.casObject.name,
                    matricule: this.casObject.matricule_id,
                };
                this.demandeur = {
                    display: this.casObject.demandeur,
                };
                this.form.explication_commentaire = this.casObject.explication_commentaire;
                this.form.info_id = this.casObject.info_id;
                this.form.important = this.casObject.important;
                this.form.sanction_decision_id = this.casObject.sanction_decision_id;
                if (this.casObject.datetime_sanction) {
                    let datetime = Moment(this.casObject.datetime_sanction);
                    this.form.datetime_sanction = datetime.format("YYYY-MM-DD");
                    this.timeSanction = datetime.format("HH:MM");
                }
                this.form.sanction_faite = this.casObject.sanction_faite;

                this.infoOrSanction = this.casObject.info_id ? "info" : "sanction-decision";
                if (this.casObject.info_id) {
                    const forcedGroups = this.visibilityOptions.filter(o => o.disabled).map(o => o.id);
                    this.form.visible_by_groups = this.casObject.visible_by_groups.concat(forcedGroups);
                }

                this.setSanctionDecisionOptions();

                if (this.casObject.attachments.length > 0) {
                    for (let a in this.casObject.attachments) {
                        this.uploadedFiles.push({id: this.casObject.attachments[a], file: null});
                    }
                }
            }
        },
        submit: function (evt) {
            evt.preventDefault();

            this.form.demandeur = this.demandeur.display;
            let data = this.form;
            // Set visibility for all if it's sanction_decision.
            if (this.infoOrSanction == "sanction-decision") {
                // Set visibility to all.
                // eslint-disable-next-line no-undef
                data.visible_by_groups = Object.keys(groups).map(x => groups[x].id);
            }
            // Add times if any.
            if (data.datetime_sanction) {
                let time = this.timeSanction ? " " + this.timeSanction : " 12:00";
                data.datetime_sanction += time;
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
                this.$router.push("/",() => {
                    this.$root.$bvToast.toast("Les données ont bien été envoyées", {
                        variant: "success",
                        noCloseButton: true,
                    });
                });
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

            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: people,
                check_access: true,
                tenure_class_only: this.$store.state.settings.filter_teacher_entries_by_tenure,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data.map(p => {
                    // Format entries.
                        let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                        // Append teachings if necessary.
                        if ("is_secretary" in p) {
                            if (this.$store.state.settings.teachings.length > 1) {
                                // It's a responsible.
                                let teachings = " —";
                                for (let t in p.teaching) {
                                    teachings += " " + p.teaching[t].display_name;
                                }
                                entry.display += teachings;
                            }
                        } else {
                        // It's a student.
                            entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                            if (this.$store.state.settings.teachings.length > 1) entry.display += " – " + p.teaching.display_name;
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
        setSanctionDecisionOptions: function() {
            // Set sanctions and decisions options.
            axios.get("/dossier_eleve/api/sanction_decision/")
                .then(response => {
                    this.sanctionDecisionOptions = response.data.results.map(m => {
                        let entry = {value: m.id, text: m.sanction_decision};
                        if (this.$store.state.settings.enable_submit_sanctions) {
                            entry["disabled"] = m.can_ask;
                        }
                        return entry;
                    });

                    // Keep sanction decision entry.
                    if (this.$store.state.settings.enable_submit_sanctions) {
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
            let settings = this.$store.state.settings;
            // eslint-disable-next-line no-undef
            const groupSet = groups;
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
                return {
                    group: g,
                    isAllowed: settings[allowedGroupSetting],
                    isForced: settings[forcedGroupSetting],
                };
            });

            const allowedGroups = [...new Set(concernedSettings.map(s => s.isAllowed).reduce((acc, curValue) => {
                return curValue.concat(acc);
            }, []))];
            this.visibilityOptions = allowedGroups.map(aG => {
                let group = Object.values(groupSet).find(g => g.id === aG);
                // Is the group forced?
                // First check if a group allows it but is not forced. In this case, this group permission prevails
                // and it is not forced.
                if (concernedSettings.find(uG => uG.isAllowed.includes(aG) && !uG.isForced.includes(aG))) {
                    return group;
                // Check if the group is simultaneously forced and allowed in the remaining settings.
                } else if (concernedSettings.find(uG => uG.isAllowed.includes(aG) && uG.isForced.includes(aG))) {
                    // Append the group to pre-selectioned options.
                    this.form.visible_by_groups.push(aG);
                    group.disabled = true;
                    return group;
                }
                return group;
            });
        },
    },
    components: {Multiselect, quillEditor, FileUpload},
    mounted: function () {
        // Set policies.
        this.setVisibilityGroups();

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
                    if (this.$store.state.settings.teachings.length > 1) {
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
                    return {value: m.id, text: m.info};
                });
            })
            .catch(function (error) {
                alert(error);
            });

        this.setSanctionDecisionOptions();
    }
};
</script>
