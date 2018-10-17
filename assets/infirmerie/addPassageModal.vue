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
    <b-modal size="lg" title="Passage"
        ok-title="Soumettre" cancel-title="Annuler" :ok-disabled="submitting"
        @ok="addPassage" @hidden="resetModal"
        ref="addPassageModal"
        >
        <b-row>
            <b-col sm="4">
                <div>
                    <b-img rounded :src="photoPath" fluid alt="Photo de l'élève" />
                </div>
            </b-col>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group label="Nom" label-for="input-name" :state="inputStates.name">
                                <multiselect id="input-name"
                                    :internal-search="false"
                                    :options="studentOptions"
                                    @search-change="getStudentOptions"
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

                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('name') }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Matricule" label-for="input-matricule">
                                <b-form-input id="input-matricule" type="text" v-model="form.matricule_id" readonly></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Motifs d'admissions :" label-for="input-admission">
                                <b-form-textarea id="input-admission" :rows="3" v-model="form.motifs_admission"></b-form-textarea>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                            <b-col>
                                <b-form-group label="Date de l'arrivée" label-for="input-date-arrive"  :state="inputStates.datetime_arrive">
                                    <b-form-input id="input-date-arrive" type="date" v-model="dateArrive"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_arrive') }}</span>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group label="Heure de l'arrivée" label-for="input-time-arrive"  :state="inputStates.datetime_arrive">
                                    <b-form-input id="input-time-arrive" type="time" v-model="timeArrive"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_arrive') }}</span>
                                </b-form-group>
                            </b-col>
                    </b-form-row>
                    <div v-if="form.datetime_sortie || sortie">
                        <b-form-row>
                            <b-col>
                                <b-form-group label="Remarques de sortie :" label-for="input-remarques" :state="inputStates.non_field_errors">
                                    <b-form-textarea id="input-remarque" :rows="3" v-model="form.remarques_sortie"></b-form-textarea>
                                    <span slot="invalid-feedback">{{ errorMsg('non_field_errors') }}</span>
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                        <b-form-row>
                                <b-col>
                                    <b-form-group label="Date de sortie" label-for="input-date-sortie"  :state="inputStates.datetime_sortie">
                                        <b-form-input id="input-date-sortie" type="date" v-model="dateSortie"></b-form-input>
                                        <span slot="invalid-feedback">{{ errorMsg('datetime_sortie') }}</span>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Heure de sortie" label-for="input-time-sortie"  :state="inputStates.datetime_sortie">
                                        <b-form-input id="input-time-sortie" type="time" v-model="timeSortie"></b-form-input>
                                        <span slot="invalid-feedback">{{ errorMsg('datetime_sortie') }}</span>
                                    </b-form-group>
                                </b-col>
                        </b-form-row>
                    </div>
                    <b-form-row>
                            <b-alert show>Un email sera envoyé aux différents responsables de l'élève.</b-alert>
                    </b-form-row>
                </b-form>
            </b-col>
        </b-row>
        <template slot="modal-ok">
            <icon v-if="submitting" name="spinner" scale="1" spin class="align-baseline"></icon>
            Soumettre
        </template>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Moment from 'moment';
Moment.locale('fr');

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

const nullForm = {
    matricule_id: null,
    name: "",
    datetime_arrive: null,
    datetime_sortie: null,
    motifs_admission: "",
    remarques_sortie: "",
    };

export default {
    props: ['entry'],
    data: function () {
        return {
            form: nullForm,
            dateArrive: null,
            timeArrive: null,
            dateSortie: null,
            timeSortie: null,
            name: null,
            nameLoading: false,
            submitting: false,
            studentOptions: [],
            sortie: false,
            searchId: 0,
            inputStates: {
                "name": null,
                "non_field_errors": null,
                "datetime_arrive": null,
                "datetime_sortie": null,
            },
            errors: {}
        }
    },
    computed: {
        photoPath: function () {
            if (this.name) {
                return '/static/photos/' + this.name.matricule + '.jpg';
            } else {
                return '/static/photos/unknown.jpg';
            }
        },
    },
    watch: {
        errors: function (newErrors, oldErrors) {
            const inputs = Object.keys(this.inputStates);
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
        name: function (newName, oldName) {
            if (newName) {
                this.form.matricule_id = newName.matricule;
                this.form.name = newName.display;
            }
        },
        entry: function (newEntry, oldEntry) {
            if (newEntry) {
                this.name = newEntry.matricule;
                this.form = {
                    id: newEntry.id,
                    matricule_id: newEntry.matricule_id,
                    name: newEntry.name,
                    datetime_arrive: newEntry.datetime_arrive,
                    datetime_sortie: newEntry.datetime_sortie,
                    motifs_admission: newEntry.motifs_admission,
                    remarques_sortie: newEntry.remarques_sortie,
                }
                this.dateArrive = Moment(newEntry.datetime_arrive).format('YYYY-MM-DD');
                this.timeArrive = Moment(newEntry.datetime_arrive).format('HH:mm');

                if (this.sortie && !newEntry.datetime_sortie) {
                    this.dateSortie = Moment().format('YYYY-MM-DD');
                    this.timeSortie = Moment().format('HH:mm');
                }
                if (newEntry.datetime_sortie) {
                    this.dateSortie = Moment(newEntry.datetime_sortie).format('YYYY-MM-DD');
                    this.timeSortie = Moment(newEntry.datetime_sortie).format('HH:mm');
                }

            } else {
                this.resetModal();
            }
        }
    },
    methods: {
        show: function (sortie) {
            this.sortie = sortie;
            if (!this.entry) {
                this.dateArrive = Moment().format('YYYY-MM-DD');
                this.timeArrive = Moment().format('HH:mm');
            }
            this.$refs.addPassageModal.show();
        },
        hide: function () {
            this.$refs.addPassageModal.hide();
        },
        resetModal: function () {
            this.form = nullForm;
            this.sortie = false;
            this.dateArrive = null;
            this.timeArrive = null;
            this.dateSortie = null;
            this.timeSortie = null;
            this.name = null;
            this.submitting = false;

            this.$emit('reset');
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        addPassage: function (evt) {
            evt.preventDefault();
            this.submitting = true;
            let modal = this;
            // Copy form data.
            let data = Object.assign({}, this.form);
            // Add times if any.
            data.datetime_arrive = this.dateArrive + " " + this.timeArrive;
            if (this.dateSortie) {
                data.datetime_sortie = this.dateSortie + " " + this.timeSortie;
            }

            // Send data.
            const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let path = '/infirmerie/api/passage/';
            if (this.entry) path += this.form.id + '/'
            const send = this.entry ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(response => {
                this.hide();
                this.errors = {};
                this.$emit('update');
                this.submitting = false;
            }).catch(function (error) {
                modal.submitting = false;
                modal.errors = error.response.data;
            });
        },
        getStudentOptions(query, people) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: "student",
                check_access: true,
            };
            axios.post('/annuaire/api/people/', data, token)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                const options = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.display, matricule: p.matricule};
                    return entry;
                });
                this.nameLoading = false;
                this.studentOptions = options;
            })
            .catch(function (error) {
                alert(error);
                app.nameLoading = false;
            });
        },
    },
    components: {Multiselect}
}
</script>

<style>

</style>
