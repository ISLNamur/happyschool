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
                <h3>Passage infirmerie : {{ this.id ? "Modification" : "Ajout" }}</h3>
            </b-row>
            <b-row>
                <b-btn @click="$router.go(-1)"> Retour à la liste des passages</b-btn>
            </b-row>
            <b-row>
                <b-col sm="4">
                    <b-img rounded :src="photoPath" fluid alt="Photo de l'élève" />
                </b-col>
                <b-col>
                    <b-form @submit="submit" @reset="reset">
                        <b-form-row>
                        <b-col sm="8">
                        <b-form-group label="Nom" label-for="input-name" :state="inputStates.name">
                            <multiselect
                                :internal-search="false"
                                :options="studentOptions"
                                @search-change="getStudentOptions"
                                placeholder="Rechercher un étudiant…"
                                :loading="searching"
                                select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                label="display"
                                track-by="matricule"
                                v-model="name"
                                >
                                <span slot="noResult">Aucun étudiant trouvé.</span>
                                <span slot="noOptions"></span>
                            </multiselect>
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
                    <div v-if="form.datetime_sortie || this.sortie!=='0'">
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
                        <b-button type="submit" variant="primary" :disabled="sending">Soumettre</b-button>
                    </b-form>
                </b-col>
            </b-row>
    </b-container>
</template>

<script>
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.min.css';
import VueRouter from 'vue-router'
import Vue from 'vue'
Vue.use(VueRouter)
import {getPeopleByName} from '../common/search.js';

const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

export default {
    props: {
        sortie:{
            type: String,
            default: "0",
        },
        id: {
            type: String,
            default: null,
        }
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
        id: function (newVal, oldVal) {
            if (newVal) {
                this.loadAbsence(newVal);
            } else {
                this.reset();
            }
        },
        name: function (newName, oldName) {
            if (newName) {
                this.form.matricule_id = newName.matricule;
                this.form.name = newName.display;
                console.log(newName)
            }
        }
    },
    data: function () {
        return {
            errors: {},
            dateArrive: null,
            timeArrive: null,
            dateSortie: null,
            timeSortie: null,
            inputStates: {
                "name": null,
                "non_field_errors": null,
                "datetime_arrive": null,
                "datetime_sortie": null,
            },
            studentOptions: [],
            motifOptions: [],
            searching: false,
            form: {
                name: '',
                matricule_id: null,
                datetime_arrive: null,
                datetime_sortie: null,
                motifs_admission: "",
                remarques_sortie: "",
            },
            name: [],
            person: [],
            searchId: -1,
            sending: false,
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
    methods: {
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
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
                check_access: false,
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
        updateEnd: function (value) {
            if (!this.form.date_absence_end) this.form.date_absence_end = value;
        },
        loadAbsence: function () {
            axios.get(`/infirmerie/api/passage/${this.id}/`, token)
            .then(resp => {
                if (resp.data) {
                    console.log(resp.data);
                    this.form.matricule_id= resp.data.matricule.matricule;
                    this.name=resp.data.matricule;
                    console.log(resp.data);
                    this.dateArrive = resp.data.datetime_arrive.split("T")[0];
                    this.timeArrive = resp.data.datetime_arrive.split("T")[1].split("+")[0];
                    this.form.motifs_admission= resp.data.motifs_admission;
                    this.form.remarques_sortie= resp.data.remarques_sortie;
                    this.form.id_person = resp.data.id_person;
                    this.form.motif = resp.data.motif;
                    this.form.name = resp.data.name;
                    this.form.date_absence_start = resp.data.date_absence_start;
                    this.form.comment = resp.data.comment;
                }
            })
            .catch(err => {
                alert(err);
            })
        },
        reset: function () {

        },
        submit: function (evt) {

            evt.preventDefault();

            this.sending = true;
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
            let url = '/infirmerie/api/passage/';
            if (this.id) url += this.id + "/";
            if (this.entry) path += this.form.id + '/'
            const send = this.id ? axios.put(url, data, token) : axios.post(url, data, token);
            send.then(response => {
                this.errors = {};
                this.$emit('update');
                this.sending = false;
                this.$router.push('/',() => {
                    this.$root.$bvToast.toast(`Les données ont bien été envoyées`, {
                        variant: 'success',
                        noCloseButton: true,
                    })
                });
            }).catch(function (error) {
                alert("Une erreur est survenue lors de la soumission : " + error);
                modal.sending = false;
            });
        },
        getResponsibles: function (query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.searching = true;

            getPeopleByName(query, this.$store.state.settings.teachings, 'responsible')
            .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                this.responsibleOptions = resp.data;
                this.searching = false;
            })
            .catch( (err) => {
                alert(err);
                this.searching = false;
            })
        }
    },
    mounted: function () {
        const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
        axios.get('/absence_prof/api/motif/', token)
        .then(resp => {
            this.motifOptions = resp.data.results.map(v => {return {value: v.motif, text: v.motif}});
        })
        .catch(err => {
            alert("Unable to get motives");
        })

        if (this.id) this.loadAbsence();
    },
    components: {
        Multiselect
    }
}
</script>
