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
                <BButton to="/">
                    <IBiChevronLeft />
                    Retour
                </BButton>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup
                    label="Type de changement"
                >
                    <BFormSelect
                        v-model="form.change"
                        :options="store.changeType"
                        value-field="id"
                        text-field="name"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup
                    label="Catégorie"
                >
                    <BFormSelect
                        v-model="form.category"
                        :options="store.changeCategory"
                        value-field="id"
                        text-field="category"
                    >
                        <template #first>
                            <option :value="null" />
                        </template>
                    </BFormSelect>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol sm="4">
                <BFormGroup
                    id="date-start-input-group"
                    label="Date"
                    :state="inputStates.date_change"
                    label-cols="4"
                >
                    <BFormInput
                        type="date"
                        v-model="form.date_change"
                    />
                    <template #invalid-feedback>
                        {{ errorMsg('date_change') }}
                    </template>
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup
                    id="time-start-input-group"
                    label="Heure début"
                    :state="inputStates.time_start"
                    label-cols-sm="8"
                    label-class="text-end"
                >
                    <BFormInput
                        type="time"
                        v-model="form.time_start"
                    />
                    <template #invalid-feedback>
                        {{ errorMsg('time_start') }}
                    </template>
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup
                    id="time-end-input-group"
                    label="Heure fin"
                    :state="inputStates.time_end"
                    label-cols-sm="8"
                    label-class="text-end"
                >
                    <BFormInput
                        type="time"
                        v-model="form.time_end"
                    />
                    <template #invalid-feedback>
                        {{ errorMsg('time_end') }}
                    </template>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup
                    label="Classe(s) et/ou année(s) concernée(s)"
                >
                    <multiselect
                        :internal-search="false"
                        :options="classesOptions"
                        @search-change="getStudentsClassesYears"
                        :multiple="true"
                        :loading="classesLoading"
                        placeholder="Chercher une classe ou une année…"
                        select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.classes"
                    >
                        <template #noResult>
                            Aucune classe trouvée.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup
                    label="Prof/Educ(s) absent(s)/indisponible(s)/concerné(s)"
                >
                    <multiselect
                        :internal-search="false"
                        :options="teachersReplacedOptions"
                        @search-change="getTeachersReplaced"
                        :multiple="true"
                        placeholder="Ajouter un ou des prof/educ…"
                        :loading="teachersReplacedLoading"
                        select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.teachers_replaced"
                        label="display"
                        track-by="matricule"
                    >
                        <template #noResult>
                            Aucun professeur trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup
                    v-if="isReplacement"
                    label="Prof/Educ(s) remplacant(s)"
                >
                    <multiselect
                        :internal-search="false"
                        :options="teachersSubstituteOptions"
                        @search-change="getTeachersSubstitute"
                        :multiple="true"
                        placeholder="Ajouter un ou des professeurs…"
                        :loading="teachersReplacedLoading"
                        select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.teachers_substitute"
                        label="display"
                        track-by="matricule"
                    >
                        <template #noResult>
                            Aucun professeur trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup
                    label="Local/Lieu de subtitution"
                >
                    <multiselect
                        v-model="form.place"
                        tag-placeholder="Ajouter le local/lieu"
                        placeholder="Ajouter local/lieu"
                        :taggable="true"
                        :options="placesOptions"
                        @tag="addPlaces"
                        select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                    >
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup
                    label="Commentaire"
                >
                    <BFormTextarea
                        v-model="form.comment"
                        :rows="2"
                        placeholder="Un commentaire sur le changement"
                    />
                </BFormGroup>
                <BFormGroup>
                    <BFormCheckbox v-model="form.send_email_general">
                        Notifier par courriel les responsables des changements
                        <span
                            v-b-tooltip="store.settings.responsible_name"
                        >
                            <IBiQuestionCircle variant="primary" />
                        </span>
                    </BFormCheckbox>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BFormGroup>
                    <BFormCheckbox v-model="form.send_email_educ">
                        Notifier par courriel les educateurs
                    </BFormCheckbox>
                </BFormGroup>
                <BFormGroup v-if="form.teachers_replaced.length > 0">
                    <BFormCheckbox
                        v-model="form.send_email_replaced"
                    >
                        Notifier par courriel l'absent(s)/indisponible(s)/concerné(s)
                        <span
                            v-b-tooltip="form.teachers_replaced.map(t => t.display).join(', ')"
                        >
                            <IBiQuestionCircle variant="primary" />
                        </span>
                    </BFormCheckbox>
                </BFormGroup>
                <BFormGroup v-if="form.teachers_substitute.length > 0">
                    <BFormCheckbox
                        v-model="form.send_email_substitute"
                    >
                        Notifier le remplaçant par courriel
                        <span
                            v-b-tooltip="form.teachers_substitute.map(t => t.display).join(', ')"
                        >
                            <IBiQuestion-circle variant="primary" />
                        </span>
                    </BFormCheckbox>
                </BFormGroup>
                <BFormGroup>
                    <BFormCheckbox
                        v-model="form.hide_for_students"
                    >
                        Cacher aux étudiants
                    </BFormCheckbox>
                </BFormGroup>
            </BCol>
        </BRow>

        <BRow>
            <BCol>
                <BButton @click="copy">
                    <IBiFiles />
                    Copier
                </BButton>
            </BCol>
            <BCol class="text-end">
                <BButton
                    @click="submitForm"
                    :disabled="submitting"
                    variant="primary"
                >
                    <BSpinner
                        v-if="submitting"
                        small
                    />
                    Soumettre
                </BButton>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

import { scheduleChangeStore } from "./stores/index.js";

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        id: {
            type: Number,
            default: -1,
        }
    },
    data: function () {
        return {
            entry: null,
            searchId: -1,
            form: {
                change: null,
                category: null,
                date_change: "",
                time_start: null,
                time_end: null,
                classes: [],
                teachers_replaced: [],
                teachers_replaced_id: [],
                teachers_substitute: [],
                teachers_substitute_id: [],
                place: "",
                comment: "",
                send_email_general: false,
                send_email_educ: false,
                send_email_substitute: false,
                send_email_replaced: false,
                hide_for_students: false,
            },
            classesOptions: [],
            classesLoading: false,
            teachersReplacedOptions: [],
            teachersReplacedLoading: false,
            teachersSubstituteOptions: [],
            teachersSubstituteLoading: false,
            placesOptions: [],
            submitting: false,
            errors: {},
            inputStates: {
                date_change: null,
                time_start: null,
                time_end: null,
            },
            store: scheduleChangeStore(),
        };
    },
    watch: {
        entry: function (newEntry) {
            if (newEntry) {
                Object.assign(this.form, newEntry);
                if (this.form.time_start) this.form.time_start = this.form.time_start.slice(0, 5);
                if (this.form.time_end) this.form.time_end = this.form.time_end.slice(0, 5);
                this.form.classes = this.initArray(this.form.classes);
                this.form.teachers_replaced_id = this.form.teachers_replaced;
                this.form.teachers_substitute_id = this.form.teachers_substitute;
            }
        },
        errors: function (newErrors) {
            let inputs = Object.keys(this.inputStates);
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
    },
    computed: {
        isReplacement: function () {
            for (let ct in this.store.changeType) {
                if (this.store.changeType[ct].name == "Remplacement"
                    && this.store.changeType[ct].id == this.form.change) return true;
            }
            return false;
        }
    },
    methods: {
        copy: function () {
            delete this.form.id;
            delete this.entry.id;
            this.$router.push("/schedule_form/-1/");
            this.show( {
                body: "Ceci est une copie de l'entrée, vous pouvez maintenant modifier les données sans changer la précédente.",
                variant: "info",
                noCloseButton: true,
            });
        },
        addPlaces: function (newPlace) {
            this.placesOptions.push(newPlace);
            this.form.place = newPlace;
        },
        initArray: function (toArray) {
            if (toArray.length > 0) {
                return toArray.split(", ");
            } else {
                return [];
            }
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        getStudentsClassesYears(query) {
            this.classesLoading = true;

            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                check_access: false,
                years: true,
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data.map(p => {
                        return p.display;
                    });
                    this.classesLoading = false;
                    this.classesOptions = options;
                })
                .catch(function (error) {
                    alert(error);
                    app.classesLoading = false;
                });
        },
        getTeachersReplaced(query) {
            this.getTeachers(query, "replaced");
        },
        getTeachersSubstitute(query) {
            this.getTeachers(query, "substitute");
        },
        getTeachers(query, teacherType) {
            if (teacherType == "replaced") {
                this.teachersReplacedLoading = true;
            } else {
                this.teachersSubstituteLoading = true;
            }
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: "responsible",
                check_access: false,
                active: false,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data;
                    if (teacherType == "replaced") {
                        this.teachersReplacedLoading = false;
                        this.teachersReplacedOptions = options;
                    } else {
                        this.teachersSubstituteLoading = false;
                        this.teachersSubstituteOptions = options;
                    }
                })
                .catch(function (error) {
                    alert(error);
                    if (teacherType == "replaced") {
                        app.teachersReplacedLoading = false;
                    } else {
                        app.teachersSubstituteLoading = false;
                    }
                });
        },
        submitForm: function (evt) {
            evt.preventDefault();

            this.submitting = true;
            let modal = this;
            // Copy form data.
            let data = Object.assign({}, this.form);
            data.teachers_replaced_id = data.teachers_replaced.map(t => t.matricule);
            data.teachers_substitute_id = data.teachers_substitute.map(t => t.matricule);
            if (data.time_start == "") data.time_start = null;
            if (data.time_end == "") data.time_end = null;
            if (data.place == null) data.place = "";
            // Send data.
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let path = "/schedule_change/api/schedule_change/";
            const isPut = this.entry && this.entry.id;
            if (isPut) path += this.form.id + "/";
            const send = isPut ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(() => {
                this.errors = {};
                const nextPage = this.store.lastPage ? `/page/${this.store.lastPage}/` : "/";
                this.$router.push(nextPage).then(() => {
                    this.show( {
                        body: "Les données ont bien été envoyées.",
                        variant: "success",
                        noCloseButton: true,
                    });
                });
                this.submitting = false;
            }).catch(function (error) {
                console.log(error);
                modal.submitting = false;
                modal.errors = error.response.data;
            });
        },
        loadEntry: function () {
            if (this.id > 0) {
                axios.get(`/schedule_change/api/schedule_change/${this.id}/`)
                    .then((resp) => {
                        this.entry = resp.data;
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            }
        }
    },
    components: {Multiselect},
    mounted: function () {
        this.loadEntry();
        this.store.getPlaces()
            .then(() => {
                this.placesOptions = this.store.places;
            });
    }
};
</script>
