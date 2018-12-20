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
        <b-row>
            <b-col>
                <b-form-group label="Date de l'absence :">
                    <b-form-input type="date" v-model="date_absence"
                        :disabled="$store.state.changes.length != 0 || !$store.state.onLine"
                        @change="loadAbsences"
                        >
                    </b-form-input>
                </b-form-group>
            </b-col>
            <b-col class="text-right">
                <b-btn v-b-modal.tovalidate :disabled="$store.state.changes.length == 0 || !$store.state.onLine">
                    Absences non validées
                </b-btn>
                <p v-if="$store.state.onLine"><icon name="signal" scale="1.2" color="green" class="align-baseline"></icon> Connecté</p>
                <p v-else><icon name="ban" scale="1.2" color="red" class="align-baseline"></icon> Déconnecté</p>
                <p v-if="$store.state.updating"><icon name="spinner" color="green" spin class="align-baseline"></icon>Mise à jour des élèves</p>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group v-if="date_absence.length > 0" label="Recherche :">
                        <multiselect id="input-name"
                            :internal-search="false"
                            :options="searchOptions"
                            @search-change="getSearchOptions"
                            :loading="searchLoading"
                            placeholder="Rechercher un étudiant, une classe, un professeur, …"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="id"
                            v-model="currentSearch"
                            @select="selected"
                            :disabled="$store.state.updating"
                            >
                            <span slot="noResult">Aucune personne trouvée.</span>

                        </multiselect>
                    </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <add-absence-entry v-for="s in students" :key="s.matricule"
                        v-bind:student="s" v-bind:date_absence="date_absence">
                    </add-absence-entry>
                </b-list-group>
            </b-col>
        </b-row>
        <b-modal size="lg" id="tovalidate" title="Changements non validées"
            cancel-title="Retour" ok-title="Valider les changements" @ok="sendChanges">
            <b-list-group v-for="change in $store.state.changes" :key="change.matricule">
                <b-list-group-item>
                    {{ change.student.display }} :
                    <strong v-if="'afternoon' in change">Après-midi ({{ change.afternoon ? "Absent" : "Présent" }})</strong>
                    <strong v-if="'morning' in change">Matin ({{ change.morning ? "Absent" : "Présent" }})</strong>
                </b-list-group-item>
            </b-list-group>
        </b-modal>
        <b-modal ref="offline" title="Hors-connexion">
            Attention, en mode hors-connexion seuls les absences du jour peuvent être prisent.
        </b-modal>
    </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import axios from 'axios';
import { openDB } from 'idb';

import Moment from 'moment';
Moment.locale('fr');

import AddAbsenceEntry from './add_absence_entry.vue';

export default {
    data: function () {
        return {
            date_absence: "",
            searchOptions: [],
            searchLoading: false,
            currentSearch: null,
            students: [],
            savedAbsences: [],
            searchId: -1,
        }
    },
    computed: {
        onLine: function () {
            return this.$store.status;
        }
    },
    watch: {
        onLine: function (newValue, oldValue) {
            if (!newValue && this.date_absence != Moment().format("YYYY-MM-DD")) {
                this.$refs.offline.show();
                this.date_absence = Moment().format("YYYY-MM-DD");
            }
        }
    },
    methods: {
        cleanStudents: function () {
            this.students = [];
            this.currentSearch = null;
        },
        selected: function (option) {
            if (option.type == 'classe') {
                this.students = option.students.map(s => {
                    if (s.matricule in this.$store.state.todayAbsences) {
                        s.savedAbsence = this.$store.state.todayAbsences[s.matricule];
                        s.savedAbsence.student = s;
                    }
                    return s;
                }).sort((a, b) => a.display.localeCompare(b.display));
            } else {
                let saved = this.onLine ? this.savedAbsences : this.$store.state.todayAbsences;
                if (saved[option.matricule]) {
                    option.saved = this.saved[option.matricule];
                }
                this.students = [option];
            }
        },
        getSearchOptions: function (query) {
            if (query.length == 0)
                return;
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const dbPromise = openDB("annuaire", 1);

            if (isNaN(query[0])) {
                dbPromise.then(db => {
                    db.getAll("students").then(students => {
                        let options = students.filter(student => {
                            if (student.last_name.toLowerCase().startsWith(query.toLowerCase()))
                                return true;
                            
                            if (student.first_name.toLowerCase().startsWith(query.toLowerCase()))
                                return true;
                        }).slice(0, 50);
                        this.searchOptions = options.map(p => {
                            return {
                                display: p.display,
                                last_name: p.last_name,
                                first_name: p.first_name,
                                matricule: p.matricule,
                                id: p.matricule,
                                type: 'student',
                            }
                        })
                    });
                });
            } else {
                dbPromise.then(db => {
                    db.getAllKeys("classes").then(classes => {
                        let classeKeys = classes.filter(classe => {
                            if (classe.toLowerCase().startsWith(query.toLowerCase()))
                                return true;
                        });

                        let options = [];
                        for (let o in classeKeys) {
                            let students = [];
                            db.get("classes", classeKeys[o])
                            .then(studs => {
                                for (let s in studs) {
                                    db.get("students", studs[s])
                                    .then(student => {
                                        students.push(student);
                                    })
                                }
                                options.push({
                                    type: 'classe',
                                    students: students,
                                    display: classeKeys[o],
                                    id: classeKeys[o],
                                });
                            });
                        }
                        this.searchOptions = options.sort((a, b) => a.display.localeCompare(b.display));
                    });
                });
            }
        },
        sendChanges: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const apiUrl = "/student_absence/api/student_absence/";
            for (let c = this.$store.state.changes.length - 1; c >= 0; c--) {
                let change = this.$store.state.changes[c];
                const request = apiUrl + "?student=" + change.matricule + "&date_absence__gte=" + this.date_absence + '&date_absence__lte=' + this.date_absence;
                axios.get(request)
                .then(response => {
                    if (response.data.results.length > 0) {
                        let absence = Object.assign({}, response.data.results[0]);
                        if ('afternoon' in change) absence.afternoon = change.afternoon;
                        if ('morning' in change) absence.morning = change.morning;
                        axios.put(apiUrl + absence.id + '/', absence, token);
                        this.$store.commit('removeChange', change);
                        if (this.$store.state.changes.length == 0) this.loadAbsences(this.date_absence);
                    } else {
                        let absence = Object.assign({}, change);
                        delete Object.assign(absence, {["student_id"]: absence["matricule"] })["matricule"];
                        axios.post(apiUrl, absence, token)
                        .then(resp => {
                            this.$store.commit('removeChange', change);
                            if (this.$store.state.changes.length == 0) this.loadAbsences(this.date_absence);
                        })
                        .catch(function (error) {
                            alert(error);
                        });
                    }
                });    
            }
        },
        loadAbsences: function (date) {
            this.cleanStudents();
            this.date_absence = date;
            // Load absences from date_absence.
            if (this.date_absence.length == 0) return;

            this.savedAbsences = {};
            axios.get('/student_absence/api/student_absence/?date_absence__gte=' + this.date_absence + '&date_absence__lte=' + this.date_absence)
            .then(response => {
                this.savedAbsences = response.data.results.map(r => {
                    let abs = {matricule: r.student_id, date_absence: r.date_absence}
                    if (r.morning) abs.morning = true;
                    if (r.afternoon) abs.afternoon = true;
                    return abs;
                })
                this.savedAbsences = this.savedAbsences.reduce((obj, item) => {
                    obj[item.matricule] = item;
                    return obj;
                }, {});

                // Save absence to the store.
                if (date == Moment().format("YYYY-MM-DD")) {
                    this.$store.commit("setTodayAbsences", this.savedAbsences);
                }
            })
        }
    },
    mounted: function () {
        const now = Moment();
        this.loadAbsences(now.format("YYYY-MM-DD"));
    },
    components: {Multiselect, AddAbsenceEntry},
}
</script>