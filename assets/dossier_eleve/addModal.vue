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
    <b-modal size="lg" title="Nouveau cas"
        ok-title="Soumettre" cancel-title="Annuler"
        :ok-disabled="!(form.info_id || form.sanction_decision_id) || (!coord && !educ)"
        ref="addModal"
        @ok="addCas" @hidden="resetModal"
        >
        <b-row>
            <b-col sm="4">
                <div>
                    <b-img rounded :src="'/static/photos/' + name.matricule + '.jpg'" fluid alt="Photo de l'élève" />
                </div>
            </b-col>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group label="Nom" label-for="input-name" :state="inputStates.name">
                                <multiselect id="input-name"
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

                                </multiselect>
                                <span slot="invalid-feedback">{{ errorMsg('name') }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Matricule" label-for="input-matricule">
                                <b-form-input id="input-matricule" type="text" v-model="name.matricule" readonly></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-form-group label="Demandeur" label-for="input-demandeur" :state="inputStates.demandeur">
                            <multiselect id="input-demandeur"
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

                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('demandeur') }}</span>
                        </b-form-group>
                    </b-form-row>
                    <b-form-row>
                        <b-form-checkbox v-model="form.important">
                            Marquer comme important.
                        </b-form-checkbox>
                    </b-form-row>
                    <b-form-row>
                        <b-form-group label="Type d'info">
                            <b-form-radio-group id="info-or-sanction" v-model="infoOrSanction" :disabled="entry ? true : false">
                                <b-form-radio value="info">Non disciplinaire</b-form-radio>
                                <b-form-radio value="sanction-decision" :disabled="!coord && !educ">Disciplinaire</b-form-radio>
                            </b-form-radio-group>
                        </b-form-group>
                    </b-form-row>
                    <div v-if="infoOrSanction == 'info'">
                        <b-form-row>
                            <b-col>
                                <b-form-group label="Info" label-for="input-info" :state="inputStates.info_id">
                                    <b-form-select id="input-info" v-model="form.info_id" :options="infoOptions">
                                        <template slot="first">
                                            <option :value="null" disabled>Choisissez un type d'info</option>
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
                                <b-form-group label="Info disciplinaire" label-for="input-info" :state="inputStates.sanction_decision_id">
                                    <b-form-select id="input-info" v-model="form.sanction_decision_id" :options="sanctionDecisionOptions">
                                        <template slot="first">
                                            <option :value="null" disabled>Choisissez dans la liste</option>
                                        </template>
                                    </b-form-select>
                                    <span slot="invalid-feedback">{{ errorMsg('sanction_decision_id') }}</span>
                                </b-form-group>
                                <b-form-group label="Date de la sanction" label-for="input-date-sanction" :state="inputStates.datetime_sanction">
                                    <b-form-input id="input-date-sanction" type="date" v-model="form.datetime_sanction"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_sanction') }}</span>
                                </b-form-group>
                                <b-form-group v-if="form.sanction_faite !== null" label-for="input-sanction-faite">
                                    <b-form-checkbox id="input-sanction-faite"
                                        v-model="form.sanction_faite">
                                        Sanction faite ?
                                    </b-form-checkbox>
                                </b-form-group>
                            </b-col>
                            <b-col sm="5">
                                <b-list-group>
                                    <b-list-group-item class="d-flex justify-content-between align-items-center"
                                        v-for="(val, index) in stats" :key="index">
                                        <strong>{{ val.display }} :</strong> {{ val.value }}
                                    </b-list-group-item>
                                </b-list-group>
                            </b-col>
                        </b-form-row>
                    </div>
                    <b-form-row v-if="infoOrSanction">
                        <b-col>
                            <b-form-group label="Commentaires" label-for="input-comment" :state="inputStates.explication_commentaire">
                                <b-form-textarea id="input-comment" :rows="3" v-model="form.explication_commentaire"></b-form-textarea>
                                <span slot="invalid-feedback">{{ errorMsg('explication_commentaire') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row v-if="infoOrSanction == 'info'">
                        <b-form-group label="Visibilité">
                                <b-form-checkbox v-model="form.visible_by_educ" :disabled="!coord">
                                    Visible par les éducateurs
                                </b-form-checkbox>
                                <b-form-checkbox v-model="form.visible_by_tenure" :disabled="!educ && !coord">
                                    Visible par les titulaires
                                </b-form-checkbox>
                        </b-form-group>
                        <b-form-checkbox v-model="form.send_to_teachers" :disabled="!educ && !coord">
                            Envoyer l'info par email aux professeurs de la classe de l'élève.
                        </b-form-checkbox>

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
    props: ['entry'],
    data: function () {
        return {
            form: {
                name: "",
                matricule_id: null,
                info_id: null,
                sanction_decision_id: null,
                explication_commentaire: "",
                important: false,
                demandeur: "",
                visible_by_educ: false,
                visible_by_tenure: false,
                datetime_sanction: null,
                sanction_faite: null,
                send_to_teachers: false,
            },
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
                demandeur: null,
                explication_commentaire: null,
            },
            coord: false,
            educ: false,
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
                axios.get('dossier_eleve/api/statistics/' + this.name.matricule + '/')
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
            if (newChoice == 'info') {
                this.form.sanction_decision_id = null;
            } else {
                this.form.info_id = null;
            }
        },
        errors: function (newErrors, oldErrors) {
            let inputs = ['name', 'info_id', 'sanction_decision_id', 'demandeur', 'explication_commentaire'];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
        entry: function (entry, oldEntry) {
            this.setEntry(entry);
        },
    },
    methods: {
        show: function () {
            this.$refs.addModal.show();
        },
        hide: function () {
            this.$refs.addModal.hide();
        },
        resetModal: function () {
            this.$emit('reset');

            this.name = {matricule: null};
            this.infoOrSanction = null;
            this.demandeur = {};
            this.stats = {};

            this.form.name = "";
            this.form.matricule_id = null;
            this.form.info_id = null;
            this.form.sanction_decision_id = null;
            this.form.explication_commentaire = "";
            this.form.important = false;
            this.form.demandeur = "";
            this.form.visible_by_educ = !this.coord;
            this.form.visible_by_tenure = !this.educ && !this.coord;
            this.form.datetime_sanction = null;
            this.form.sanction_faite = null;
            this.form.send_to_teachers = false;
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        setEntry: function (entry) {
            if (entry) {
                // The name will update form.name and form.matricule_id
                this.name = {
                    display: entry.name,
                    matricule: entry.matricule_id,
                }
                this.demandeur = {
                    display: entry.demandeur,
                }
                this.form.explication_commentaire = entry.explication_commentaire;
                this.form.info_id = entry.info_id;
                this.form.important = entry.important;
                this.form.visible_by_educ = entry.visible_by_educ;
                this.form.visible_by_tenure = entry.visible_by_tenure;

                this.form.sanction_decision_id = entry.sanction_decision_id;
                if (entry.datetime_sanction) {
                    let datetime = Moment(entry.datetime_sanction);
                    this.form.datetime_sanction = datetime.format('YYYY-MM-DD');
                    this.timeSanction = datetime.format('HH:MM');
                }
                this.form.sanction_faite = entry.sanction_faite;

                this.infoOrSanction = entry.info_id ? 'info' : 'sanction-decision';

                // Set sanctions and decisions options.
                axios.get('/dossier_eleve/api/sanction_decision/')
                .then(response => {
                    this.sanctionDecisionOptions = response.data.results.map(m => {
                        let entry = {value: m.id, text: m.sanction_decision};
                        if (this.$store.state.settings.enable_submit_sanctions) {
                            entry['disabled'] = m.can_ask;
                        }
                        return entry;
                    })

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
            } else {
                this.resetModal();
            }
        },
        addCas: function (evt) {
            evt.preventDefault();

            this.form.demandeur = this.demandeur.display;
            let data = this.form;
            // Add times if any.
            if (data.datetime_sanction) {
                let time = this.timeSanction ? " " + this.timeSanction : " 12:00";
                data.datetime_sanction += time;
            }

            let modal = this;
            // Send data.
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

            let path = '/dossier_eleve/api/cas_eleve/'
            if (this.entry) path += this.entry.id + '/'
            const send = this.entry ? axios.put(path, data, token) : axios.post(path, data, token);

            send.then(response => {
                this.hide();
                this.errors = {};
                this.$emit('update');
            }).catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        getNameOptions(query) {
            return this.getPeopleOptions(query, 'student');
        },
        getDemandeurOptions(query) {
            return this.getPeopleOptions(query, 'responsible');
        },
        getPeopleOptions(query, people) {
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            if (people == 'student') this.nameLoading = true;
            if (people == 'responsible') this.demandeurLoading = true;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: people,
                check_access: true,
            };
            axios.post('/annuaire/api/people/', data, token)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                const options = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    if ('is_secretary' in p) {
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
                if (people == 'student') {
                    this.nameLoading = false;
                    this.nameOptions = options;
                } else if (people == 'responsible') {
                    this.demandeurLoading = false;
                    this.demandeurOptions = options;
                }
            })
            .catch(function (error) {
                alert(error);
                app.nameLoading = false;
            });
        },
    },
    components: {Multiselect},
    mounted: function () {
        // Set policies.
        this.coord = this.$store.state.is_coord;
        this.educ = this.$store.state.is_educ;
        this.form.visible_by_educ = !this.coord;
        this.form.visible_by_tenure = !this.educ && !this.coord;

        if (this.entry) this.setEntry(this.entry);

        this.show();

        // Set info options.
        axios.get('/dossier_eleve/api/info/')
        .then(response => {
            this.infoOptions = response.data.results.map(m => {
                return {value: m.id, text: m.info};
            });
        })
        .catch(function (error) {
            alert(error);
        });
    }
}
</script>

<style>
</style>
