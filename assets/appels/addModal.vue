<template>
<div>
    <b-modal size="lg" title="Ajouter un appel"
        ok-title="Soumettre" cancel-title="Annuler"
        ref="addModal"
        @ok="addAppel" @hidden="resetModal"
        >
        <b-row>
            <b-col sm="4">
                <div>
                    <b-img rounded :src="photoPath" fluid alt="Responsive image" />
                </div>
            </b-col>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group label="Nom" label-for="input-name" :state="inputStates.name">
                                <!-- <b-form-input id="input-name" size="sm" type="text" placeholder="Nom et prénom"></b-form-input> -->
                                <multiselect id="input-name"
                                    :internal-search="false"
                                    :options="nameOptions"
                                    @search-change="getNameOptions"
                                    :loading="nameLoading"
                                    placeholder="Rechercher une personne…"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label=""
                                    label="display"
                                    track-by="matricule"
                                    v-model="name"
                                    >
                                    <span slot="noResult">Aucune personne trouvée.</span>
                                </multiselect>
                            </b-form-group>
                            <b-form-invalid-feedback id="nameFeedback">
                                {{ errorMsg('name') }}
                            </b-form-invalid-feedback>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Matricule" label-for="input-matricule">
                                <b-form-input id="input-matricule" type="text" v-model="name.matricule" readonly></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Objet" label-for="input-objet">
                                <b-form-select v-model="form.object" :options="objectOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un objet</option>
                                    </template>
                                </b-form-select>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Motif" label-for="input-motif">
                                <b-form-select v-model="form.motive" :options="motiveOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un motif</option>
                                    </template>
                                </b-form-select>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col sm="4">
                            <b-form-group label="Début du motif" label-for="input-date-motif-start">
                                <b-form-input id="input-date-motif-start" type="date" v-model="form.datetime_motif_start"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col sm="2">
                            <b-form-group label="(heure)" label-for="input-time-motif-start">
                                <b-form-input id="input-time-motif-start" type="time" :step="300" v-model="timeMotifStart"></b-form-input>
                            </b-form-group>
                        </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Fin du motif" label-for="input-date-motif-end">
                                <b-form-input id="input-date-motif-end" type="date" v-model="form.datetime_motif_end"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col sm="2">
                            <b-form-group label="(heure)" label-for="input-time-motif-end">
                                <b-form-input id="input-time-motif-end" type="time" :step="300" v-model="timeMotifEnd"></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Date de l'appel" label-for="input-date-appel">
                                <b-form-input id="input-date-appel" type="date" v-model="form.datetime_appel"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Heure de l'appel" label-for="input-time-appel">
                                <b-form-input id="input-time-appel" type="time" :step="60" v-model="timeAppel"></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Commentaires" label-for="input-comment">
                                <b-form-textarea id="input-comment" :rows="3" v-model="form.commentaire"></b-form-textarea>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-form>
            </b-col>
        </b-row>
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

export default {
    data: function () {
        return {
            form: {
                matricule_id: null,
                object_id: null,
                motive_id: null,
                datetime_motif_start: null,
                datetime_motif_end: null,
                datetime_appel: null,
                commentaire: "",
                is_student: false,
            },
            timeMotifStart: null,
            timeMotifEnd: null,
            timeAppel: null,
            objectOptions: [],
            motiveOptions: [],
            name: {matricule: null},
            nameOptions: [],
            nameLoading: false,
            searchId: 0,
            errors: {},
            inputStates: {
                name: null,
                object_id: null,
                motive_id: null,
            }
        };
    },
    computed: {
        photoPath: function () {
            //TODO photo path
            return "/static/photos/4721.jpg";
        }
    },
    watch: {
        name: function () {
            // Update form data.
            if (this.name.matricule) {
                if (this.name.matricule < 10000 && this.name.matricule > 999) {
                    // Student.
                    this.form.matricule_id = this.name.matricule;
                } else {
                    this.form.matricule_id = null;
                }
            }
        },
        errors: function (newErrors, oldErrors) {
            let inputs = ['name', 'object_id', 'motive_id'];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        }
    },
    methods: {
        show: function () {
            this.$refs.addModal.show();
        },
        hide: function () {
            this.$refs.addModal.hide();
        },
        resetModal: function () {
            //TODO resetModal()
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        addAppel: function (evt) {
            evt.preventDefault();

            // Add times if any.
            let data = this.form;
            if (this.timeMotifStart) data.datetime_motif_start += " " + this.timeMotifStart;
            if (this.timeMotifEnd) data.datetime_motif_end += " " + this.timeMotifEnd;
            if (this.timeAppel) data.datetime_appel += " " + this.timeAppel;

            // Set is_student.
            if (data.matricule_id) data.is_student = true;

            let modal = this;
            // Send data.
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.post('/appels/api/appel/', data, token)
            .then(response => {

            }).catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        getNameOptions(query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;
            axios.get("/annuaire/api/?query=" + query)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                this.nameOptions = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    if ('classe' in p) {
                        // It's a student.
                        entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                        entry.display += " – " + p.teaching.display_name;
                    } else {
                        // It's a responsible.
                        let teachings = " —";
                        for (let t in p.teaching) {
                            teachings += " " + p.teaching[t].display_name;
                        }
                        entry.display += teachings;
                    }
                    return entry;
                });
                this.nameLoading = false;
            })
            .catch(function (error) {
                this.nameLoading = false;
            });
        },
    },
    components: {Multiselect},
    mounted: function () {
        // Set motive options.
        axios.get('/appels/api/motive/')
        .then(response => {
            this.motiveOptions = response.data.results.map(m => {
                return {value: m.id, text: m.motive}
            });
        });
        // Set object options.
        axios.get('/appels/api/object/')
        .then(response => {
            this.objectOptions = response.data.results.map(m => {
                return {value: m.id, text: m.object}
            });
        });
    }
}
</script>

<style>
</style>
