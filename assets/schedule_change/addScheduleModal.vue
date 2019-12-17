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
    <b-modal
        size="lg"
        title="Ajouter un changement"
        cancel-title="Annuler"
        :ok-disabled="!form.change || submitting || !$store.state.canAdd"
        ref="addModal"
        @ok="submitForm"
        @hidden="resetData"
    >
        <b-form>
            <b-form-row>
                <b-form-group
                    label="Type de changement"
                >
                    <b-form-select
                        v-model="form.change"
                        :options="$store.state.changeType"
                        value-field="id"
                        text-field="name"
                    />
                </b-form-group>
            </b-form-row>
            <b-form-row>
                <b-form-group
                    label="Catégorie"
                >
                    <b-form-select
                        v-model="form.category"
                        :options="categoryOptions"
                        value-field="id"
                        text-field="category"
                    >
                        <template slot="first">
                            <option :value="null" />
                        </template>
                    </b-form-select>
                </b-form-group>
            </b-form-row>
            <b-form-row>
                <b-form-group
                    id="date-start-input-group"
                    label="Date"
                    :state="inputStates.date_change"
                >
                    <b-form-input
                        type="date"
                        v-model="form.date_change"
                    />
                    <span slot="invalid-feedback">{{ errorMsg('date_change') }}</span>
                </b-form-group>
            </b-form-row>
            <b-form-row>
                <b-form-group
                    id="time-start-input-group"
                    label="Heure début"
                    :state="inputStates.time_start"
                >
                    <b-form-input
                        type="time"
                        v-model="form.time_start"
                    />
                    <span slot="invalid-feedback">{{ errorMsg('time_start') }}</span>
                </b-form-group>
                <b-form-group
                    id="time-end-input-group"
                    label="Heure fin"
                    :state="inputStates.time_end"
                >
                    <b-form-input
                        type="time"
                        v-model="form.time_end"
                    />
                    <span slot="invalid-feedback">{{ errorMsg('time_end') }}</span>
                </b-form-group>
            </b-form-row>
            <b-form-group
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
                    <span slot="noResult">Aucune classe trouvée.</span>
                    <span slot="noOptions" />
                </multiselect>
            </b-form-group>
            <b-form-group
                label="Prof/Educ(s) absent(s) et/ou indisponible(s)"
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
                    <span slot="noResult">Aucun professeur trouvé.</span>
                    <span slot="noOptions" />
                </multiselect>
            </b-form-group>
            <b-form-group
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
                    <span slot="noResult">Aucun professeur trouvé.</span>
                    <span slot="noOptions" />
                </multiselect>
            </b-form-group>
            <b-form-group
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
                    <span slot="noOptions" />
                </multiselect>
            </b-form-group>
            <b-form-group
                label="Commentaire"
            >
                <b-form-textarea
                    v-model="form.comment"
                    :rows="2"
                    placeholder="Un commentaire sur le changement"
                />
            </b-form-group>
            <b-form-group>
                <b-form-checkbox v-model="form.send_email_general">
                    Notifier le changement par courriel
                </b-form-checkbox>
            </b-form-group>
            <b-form-group>
                <b-form-checkbox
                    v-if="form.teachers_substitute.length > 0"
                    v-model="form.send_email_substitute"
                >
                    Notifier le remplaçant par courriel
                </b-form-checkbox>
            </b-form-group>
        </b-form>
        <template slot="modal-ok">
            <icon
                v-if="submitting"
                name="spinner"
                scale="1"
                spin
                class="align-baseline"
            />
            Soumettre
        </template>
    </b-modal>
</template>

<script>
import Moment from "moment";
Moment.locale("fr");

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import axios from "axios";

export default {
    props: {
        entry: {
            type: Object,
            default: () => null,
        }
    },
    data: function () {
        return {
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
                send_email_substitute: false,
            },
            classesOptions: [],
            classesLoading: false,
            categoryOptions: [],
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
            } else {
                this.resetData();
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
            for (let ct in this.$store.state.changeType) {
                if (this.$store.state.changeType[ct].name == "Remplacement"
                    && this.$store.state.changeType[ct].id == this.form.change) return true;
            }
            return false;
        }
    },
    methods: {
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
        resetData: function () {
            const places = this.placesOptions;
            Object.assign(this.$data, this.$options.data.call(this));
            this.placesOptions = places;
            this.categoryOptions = this.$store.state.changeCategory;
            this.$emit("reset");
        },
        show: function () {
            this.categoryOptions = this.$store.state.changeCategory;
            this.$refs.addModal.show();
        },
        hide: function() {
            this.$refs.addModal.hide();
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        getPlaces() {
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.get("/schedule_change/api/schedule_change_place/", token)
                .then(resp => {
                    this.placesOptions = resp.data.results.map(p => p.name);
                });
        },
        getStudentsClassesYears(query) {
            this.classesLoading = true;

            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
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
                teachings: this.$store.state.settings.teachings,
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
            // Send data.
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let path = "/schedule_change/api/schedule_change/";
            const isPut = this.entry && this.entry.id;
            if (isPut) path += this.form.id + "/";
            const send = isPut ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(() => {
                this.hide();
                this.errors = {};
                this.$emit("update");
                this.submitting = false;
            }).catch(function (error) {
                modal.submitting = false;
                modal.errors = error.response.data;
            });
        }
    },
    components: {Multiselect},
    mounted: function () {
        this.getPlaces();
    }
};
</script>
