<template>
<div>
    <b-modal size="lg" :title="(processing ? 'Traiter' : 'Ajouter') + ' un appel'"
        :ok-title="processing ? 'Traiter' : 'Soumettre'" cancel-title="Annuler"
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
                        <b-col>
                            <b-form-group label="Objet" label-for="input-object" :state="inputStates.object_id">
                                <b-form-select id="input-object" v-model="form.object_id" :options="objectOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un objet</option>
                                    </template>
                                </b-form-select>
                                <span slot="invalid-feedback">{{ errorMsg('object_id') }}</span>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Motif" label-for="input-motif" :state="inputStates.motive_id">
                                <b-form-select v-model="form.motive_id" :options="motiveOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un motif</option>
                                    </template>
                                </b-form-select>
                                <span slot="invalid-feedback">{{ errorMsg('motive_id') }}</span>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <div v-if="!processing || form.is_traiter">
                        <b-form-row>
                            <b-col>
                                <b-form-group label="Début du motif" label-for="input-date-motif-start" :state="inputStates.datetime_motif_start">
                                    <b-form-input id="input-date-motif-start" type="date" v-model="form.datetime_motif_start"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_motif_start') }}</span>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group label="(heure)" label-for="input-time-motif-start">
                                    <b-form-input id="input-time-motif-start" type="time" v-model="timeMotifStart"></b-form-input>
                                </b-form-group>
                            </b-form-group>
                            </b-col>
                        </b-form-row>
                        <b-form-row>
                            <b-col>
                                <b-form-group label="Fin du motif" label-for="input-date-motif-end" :state="inputStates.datetime_motif_end">
                                    <b-form-input id="input-date-motif-end" type="date" v-model="form.datetime_motif_end"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_motif_end') }}</span>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group label="(heure)" label-for="input-time-motif-end">
                                    <b-form-input id="input-time-motif-end" type="time" v-model="timeMotifEnd"></b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                        <b-form-row>
                            <b-col>
                                <b-form-group label="Date de l'appel" label-for="input-date-appel"  :state="inputStates.datetime_appel">
                                    <b-form-input id="input-date-appel" type="date" v-model="form.datetime_appel"></b-form-input>
                                    <span slot="invalid-feedback">{{ errorMsg('datetime_appel') }}</span>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group label="Heure de l'appel" label-for="input-time-appel">
                                    <b-form-input id="input-time-appel" type="time" :step="60" v-model="timeAppel"></b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-form-row>
                    </div>
                    <b-form-row v-if="processing || form.is_traiter">
                        <b-form-group label="Destinataire(s) : ">
                            <b-form-checkbox-group id="emails" stacked
                                v-model="form.emails"
                                :options="$store.state.emails"
                                value-field="id" text-field="display">
                            </b-form-checkbox-group>
                        </b-form-group>
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
    props: ['entry', 'processing'],
    data: function () {
        return {
            form: {
                name: "",
                matricule_id: null,
                object_id: null,
                motive_id: null,
                datetime_motif_start: null,
                datetime_motif_end: null,
                datetime_appel: null,
                commentaire: "",
                emails: [],
                is_student: false,
                is_traiter: false,
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
                datetime_motif_start: null,
                datetime_motif_end: null,
                datetime_appel: null,
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
                // First update form name data.
                this.form.name = this.name.display;
                if (!('is_teacher' in this.name)) {
                    // Student.
                    this.form.matricule_id = this.name.matricule;
                } else {
                    this.form.matricule_id = null;
                }
            }
        },
        errors: function (newErrors, oldErrors) {
            let inputs = ['name', 'object_id', 'motive_id',
                'datetime_motif_start', 'datetime_motif_end', 'datetime_appel'];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
        entry: function (entry, oldEntry) {
            if (entry) {
                this.setEntry(entry);
                // Precheck emails.
                if (this.processing && this.form.is_student) {
                    this.form.emails = this.$store.state.emails.filter(email => {
                        if (this.name.teaching.id == email.teaching
                            && email.years.includes(this.name.classe.year)) {
                            return true;
                        }
                        return false;
                    }).map(email => email.id);
                }
            } else {
                this.resetModal();
            }
        },
    },
    methods: {
        show: function () {
            if (!this.entry) {
                const nowDate = Moment().format('YYYY-MM-DD');
                const nowTime = Moment().format('HH:mm');
                this.form.datetime_appel = nowDate;
                this.timeAppel = nowTime;
                this.form.datetime_motif_start = nowDate;
                this.form.datetime_motif_end = nowDate;
            }
            this.$refs.addModal.show();
        },
        hide: function () {
            this.$refs.addModal.hide();
        },
        resetModal: function () {
            this.$emit('reset');

            this.form = {
                name: "",
                matricule_id: null,
                object_id: null,
                motive_id: null,
                datetime_motif_start: null,
                datetime_motif_end: null,
                datetime_appel: null,
                commentaire: "",
                emails: [],
                is_student: false,
                is_traiter: false,
            };

            this.name = {matricule: null};
            this.timeMotifStart = null;
            this.timeMotifEnd = null;
            this.timeAppel = null;
        },
        setEntry: function (entry) {
            this.name = entry.matricule;
            this.form = {
                id: entry.id,
                name: entry.name,
                matricule_id: entry.matricule_id,
                object_id: entry.object.id,
                motive_id: entry.motive.id,
                datetime_motif_start: Moment(entry.datetime_motif_start).format('YYYY-MM-DD'),
                datetime_motif_end: Moment(entry.datetime_motif_end).format('YYYY-MM-DD'),
                datetime_appel: Moment(entry.datetime_appel).format('YYYY-MM-DD'),
                commentaire: entry.commentaire,
                emails: entry.emails,
                is_student: entry.is_student,
                is_traiter: entry.is_traiter,
            };
            this.timeMotifStart = Moment(entry.datetime_motif_start).format('HH:mm');
            this.timeMotifEnd = Moment(entry.datetime_motif_end).format('HH:mm');
            this.timeAppel = Moment(entry.datetime_appel).format('HH:mm');
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

            let data = this.form;
            // Add times if any.
            let time = this.timeMotifStart ? " " + this.timeMotifStart : " 12:00";
            data.datetime_motif_start += time;
            time = this.timeMotifEnd ? " " + this.timeMotifEnd : " 12:00";
            data.datetime_motif_end += time;
            time = this.timeAppel ? " " + this.timeAppel : " 12:00";
            data.datetime_appel += time;

            // Set is_student.
            if (data.matricule_id) data.is_student = true;

            let modal = this;
            // Send data.
            const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let path = '/appels/api/appel/';
            if (this.entry) path += this.form.id + '/'
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
            let app = this;
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: 'all',
                check_access: false,
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
                        entry.is_student = false;
                    } else {
                        // It's a student.
                        entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                        entry.display += " – " + p.teaching.display_name;
                        entry.is_student = true;
                    }
                    return entry;
                });
                this.nameLoading = false;
                this.nameOptions = options;
            })
            .catch(function (error) {
                alert(error);
                app.nameLoading = false;
            });
        },
    },
    components: {Multiselect},
    mounted: function () {
        // Set motive options.
        axios.get('/appels/api/motive/')
        .then(response => {
            this.motiveOptions = response.data.results.map(m => {
                return {value: m.id, text: m.display};
            });
        });
        // Set object options.
        axios.get('/appels/api/object/')
        .then(response => {
            this.objectOptions = response.data.results.map(m => {
                return {value: m.id, text: m.display};
            });
        });
    }
}
</script>

<style>
</style>
