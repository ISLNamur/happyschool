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
                <h3>PIA : Nouveau</h3>
            </b-row>
            <b-row class="sticky-top">
                <b-col>
                    <b-btn to="/">Retour à la liste des PIA</b-btn>
                </b-col>
                <b-col cols="2" align-self="end">
                    <b-btn @click="submit" variant="primary">Sauver</b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <h4>Référents PIA</h4>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-row>
                        <b-col md="4">
                            <b-form-group label="Élève">
                                <multiselect
                                    id="student-0"
                                    :internal-search="false"
                                    :options="studentOptions"
                                    @search-change="getPeople"
                                    placeholder="Référent"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.student"
                                    label="display"
                                    track-by="matricule"
                                    :showNoOptions="false"
                                    >
                                    <span slot="noResult">Aucun responsable trouvé.</span>
                                    <span slot="noOptions"></span>
                                </multiselect>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col md="6">
                            <b-form-group label="Référent(s)">
                                <multiselect
                                    id="responsible-0"
                                    :internal-search="false"
                                    :options="responsibleOptions"
                                    @search-change="getPeople"
                                    placeholder="Référent"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.referent"
                                    label="display"
                                    track-by="matricule"
                                    :showNoOptions="false"
                                    multiple
                                    >
                                    <span slot="noResult">Aucun responsable trouvé.</span>
                                    <span slot="noOptions"></span>
                                </multiselect>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Parrain/Marraine">
                                <multiselect
                                    id="responsible-1"
                                    :internal-search="false"
                                    :options="responsibleOptions"
                                    @search-change="getPeople"
                                    placeholder="Parrain/Marraine"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label="Cliquer dessus pour enlever"
                                    v-model="form.sponsor"
                                    label="display"
                                    track-by="matricule"
                                    :showNoOptions="false"
                                    multiple
                                    >
                                    <span slot="noResult">Aucun responsable trouvé.</span>
                                    <span slot="noOptions"></span>
                                </multiselect>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-col>
            </b-row>
            <b-row>
                <h4>Aménagements</h4>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group label="Trouble d'apprentissage">
                        <multiselect
                            :options="disorderOptions"
                            placeholder="Sélectionner le ou les différents troubles"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="form.disorder"
                            :showNoOptions="false"
                            track-by="id"
                            label="disorder"
                            @input="updateDisorderResponse"
                            multiple
                            >
                            <span slot="noResult">Aucun trouble trouvé.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group label="Aménagements raisonnables liés au trouble">
                        <multiselect
                            :options="disorderResponseOptions"
                            placeholder="Sélectionner le ou les différents aménagements"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="form.disorder_response"
                            :showNoOptions="false"
                            track-by="id"
                            label="response"
                            multiple
                            >
                            <span slot="noResult">Aucun aménagements trouvé.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group label="Aménagements d'horaire">
                        <multiselect
                            :options="scheduleOptions"
                            placeholder="Sélectionner le ou les différents adaptations"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="form.schedule"
                            :showNoOptions="false"
                            multiple
                            >
                            <span slot="noResult">Aucun aménagements trouvé.</span>
                            <span slot="noOptions"></span>
                        </multiselect>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <h4>Objectifs</h4>
            </b-row>
            <b-row>
                <b-col>
                    <goal :goal="-1" :pia="-1"></goal>
                </b-col>
            </b-row>
            <b-row>

            </b-row>
    </b-container>
</template>

<script>
import axios from 'axios';

import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';

import {getPeopleByName} from '../common/search.js';
import Goal from './goal.vue';

const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

export default {
    props: {
        id: {
            type: String,
            default: null,
        }
    },
    watch: {
        id: function (newVal, oldVal) {
            if (newVal) {
                // Reset data.
                Object.assign(this.$data, this.$options.data());
                this.loadPIA(newVal);
            } else {
                this.reset();
            }
        },
    },
    data: function () {
        return {
            responsibleOptions: [],
            studentOptions: [],
            disorderOptions: [],
            disorderResponseOptions: [],
            scheduleOptions: [],
            disorderResponseAll: [],
            searchId: -1,
            sending: false,
            form: {
                id: null,
                student: null,
                referent: [],
                sponsor: [],
                disorder: [],
                disorder_response: [],
                schedule: [],
            }
        }
    },
    methods: {
        reset: function () {

        },
        submit: function (evt) {
            evt.preventDefault();
        },
        getPeople: function (searchQuery, person) {
            person = person.split("-")[0];
            this.searchId += 1;
            let currentSearch = this.searchId;
            // this.searching = true;

            getPeopleByName(searchQuery, this.$store.state.settings.teachings, person)
            .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                this[person + 'Options'] = resp.data;
                // this.searching = false;
            })
            .catch( (err) => {
                alert(err);
                // this.searching = false;
            })
        },
        updateDisorderResponse: function () {
            this.disorderResponseOptions = this.disorderResponseAll.filter(d => {
                return this.form.disorder.map(x => x.id).includes(d.disorder);
            });
        },
        submit: function (evt) {
            evt.preventDefault();

            let app = this;
            this.sending = true;
            const data = Object.assign({}, this.form);
            data.student = data.student.matricule;
            data.disorder = data.disorder.map(d => d.id);
            data.disorder_response = data.disorder_response.map(dr => dr.id);
            data.referent = data.referent.map(r => r.matricule);
            data.sponsor = data.sponsor.map(s => s.matricule);

            let send = this.id ? axios.put : axios.post;
            let url = '/pia/api/pia/';
            if (this.id) url += this.id + "/";
            send(url, data, token)
            .then(resp => {
                this.sending = false;
                if (this.id) {
                    app.$root.$bvToast.toast(`Les données ont bien été sauvegardée`, {
                        variant: 'success',
                        noCloseButton: true,
                    })
                } else {
                    app.$router.push('/edit/' + this.id + '/',() => {
                        app.$root.$bvToast.toast(`Les données ont bien été sauvegardée`, {
                            variant: 'success',
                            noCloseButton: true,
                        })
                    });
                }
            }).catch(function (error) {
                app.sending = false;
                alert(error);
            });
        },
        loadPIA: function (newId) {
            axios.get('/pia/api/pia/' + newId + '/')
            .then(resp => {
                this.form.student = resp.data.student;
                resp.data.referent.map(r => {
                    axios.get('/annuaire/api/responsible/' + r + '/')
                    .then(resp => this.form.referent.push(resp.data));
                })
                resp.data.sponsor.map(s => {
                    axios.get('/annuaire/api/responsible/' + s + '/')
                    .then(resp => this.form.sponsor.push(resp.data));
                })
                this.form.disorder = this.disorderOptions.filter(d => resp.data.disorder.includes(d.id));
                this.form.disorder_response = this.disorderResponseAll.filter(dr => resp.data.disorder_response.includes(dr.id));
            });
        }
    },
    mounted: function () {
        const promises = [axios.get('/pia/api/disorder/'), axios.get('/pia/api/disorder_response/')]
        Promise.all(promises)
        .then(resps => {
            this.disorderOptions = resps[0].data.results;
            this.disorderResponseAll = resps[1].data.results;
            if (this.id) this.loadPIA(this.id);
        });
    },
    components: {
        Multiselect,
        Goal
    }
}
</script>
