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
                <b-form-group label="Date de l'absence :">
                    <b-form-input
                        type="date"
                        v-model="date_absence"
                        @change="loadAbsences"
                    />
                </b-form-group>
            </b-col>
            <b-col class="text-right">
                <b-btn
                    v-b-modal.tovalidate
                    :disabled="$store.state.changes.length == 0"
                >
                    Absences non validées
                </b-btn>
                <p v-if="onLine">
                    <icon
                        name="signal"
                        scale="1.2"
                        color="green"
                        class="align-baseline"
                    />Connecté
                </p>
                <p v-else>
                    <icon
                        name="ban"
                        scale="1.2"
                        color="red"
                        class="align-baseline"
                    />Déconnecté
                </p>
                <p v-if="$store.state.updating">
                    <icon
                        name="spinner"
                        color="green"
                        spin
                        class="align-baseline"
                    />Mise à jour des élèves
                </p>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group
                    v-if="date_absence.length > 0"
                    label="Recherche :"
                >
                    <multiselect
                        id="input-name"
                        :internal-search="false"
                        :options="searchOptions"
                        @search-change="getSearchOptions"
                        :loading="searchLoading"
                        placeholder="Rechercher un étudiant, une classe"
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
                        <span slot="noOptions" />
                    </multiselect>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-card v-if="classe">
                    <p>Nombre d'étudiants : {{ students.length }}.</p>
                    <b-dropdown text="Ajouter les élèves non modifiés comme présents">
                        <b-dropdown-item
                            v-for="period in $store.state.periods"
                            :key="period.id"
                            @click="addAllStudents(period.id)"
                        >
                            {{ period.name }}
                        </b-dropdown-item>
                    </b-dropdown>
                    <div
                        v-if="note.length > 0"
                        v-html="note"
                    />
                </b-card>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <add-absence-entry
                        v-for="s in students"
                        :key="s.matricule"
                        :student="s"
                        :date-absence="date_absence"
                        :period="$store.state.periods"
                    />
                </b-list-group>
            </b-col>
        </b-row>
        <b-modal
            size="lg"
            id="tovalidate"
            title="Changements non validées"
            cancel-title="Retour"
            @ok="sendChanges"
            :ok-disabled="disableValidation"
        >
            <b-tabs v-model="tabIndex">
                <b-tab :title="'Absences du ' + date_absence">
                    <div
                        v-for="cl in getAbsences(true, 'classe')"
                        :key="cl"
                        class="border-bottom pb-1 mb-1"
                    >
                        <strong>{{ cl.toUpperCase() }}</strong>
                        (absent(s) :
                        <b-badge variant="primary">
                            {{ getAbsences(true, "student", cl, true).length }}
                        </b-badge>
                        )
                        <b-form-group class="mt-2">
                            <b-form-checkbox
                                v-for="change in getAbsences(true, 'student', cl, true)"
                                :key="change.matricule + change.period"
                                :value="change"
                                v-model="selectedChanges"
                            >
                                {{ change.student.display }} ({{ getPeriod(change.period) }})
                            </b-form-checkbox>
                        </b-form-group> 
                        <b-button
                            href="#"
                            v-b-toggle="'present-' + cl"
                            variant="info"
                        >
                            Élèves présents
                            <b-badge variant="light">
                                {{ getAbsences(true, "student", cl, false).length }}
                            </b-badge>
                        </b-button>
                        <b-collapse :id="'present-' + cl">
                            <b-form-group class="mt-2">
                                <b-form-checkbox
                                    v-for="change in getAbsences(true, 'student', cl, false)"
                                    :key="change.matricule + change.period"
                                    :value="change"
                                    v-model="selectedChanges"
                                >
                                    {{ change.student.display }} ({{ getPeriod(change.period) }})
                                </b-form-checkbox>
                            </b-form-group>
                        </b-collapse>
                    </div>

                    <p
                        v-if="getAbsences(true, 'student').length > 0"
                        class="text-muted"
                    >
                        <small>
                            Pour supprimer des changements, sélectionnez les changements pour faire
                            apparaître le boutton de suppression.
                        </small>
                    </p>
                    <b-btn
                        variant="danger"
                        v-if="selectedChanges.length != 0"
                        @click="removeChanges()"
                        class="mt-1"
                    >
                        Supprimer les élements sélectionnés
                    </b-btn>
                </b-tab>
                <b-tab>
                    <template v-slot:title>
                        Autres absences non validées
                        <b-badge variant="primary">
                            {{ getAbsences(false, "student").length }}
                        </b-badge>
                    </template>
                    <div
                        v-for="cl in getAbsences(false, 'classe')"
                        :key="cl"
                        class="border-bottom"
                    >
                        <strong>{{ cl.toUpperCase() }}</strong>
                        (absent(s) :
                        <b-badge variant="primary">
                            {{ getAbsences(false, "student", cl, true).length }}
                        </b-badge>
                        )
                        <b-form-group class="mt-2">
                            <b-form-checkbox
                                v-for="change in getAbsences(false, 'student', cl, true)"
                                :key="change.matricule + change.period"
                                :value="change"
                                v-model="selectedOldChanges"
                            >
                                {{ change.student.display }}
                                (<strong>{{ change.date_absence }}</strong> - {{ getPeriod(change.period) }})
                            </b-form-checkbox>
                        </b-form-group> 
                        <b-button
                            href="#"
                            v-b-toggle="'present-' + cl"
                            variant="info"
                        >
                            Élèves présents
                            <b-badge variant="light">
                                {{ getAbsences(false, "student", cl, false).length }}
                            </b-badge>
                        </b-button>
                        <b-collapse :id="'present-' + cl">
                            <b-form-group class="mt-2">
                                <b-form-checkbox
                                    v-for="change in getAbsences(false, 'student', cl, false)"
                                    :key="change.matricule + change.period"
                                    :value="change"
                                    v-model="selectedOldChanges"
                                >
                                    {{ change.student.display }}
                                    (<strong>{{ change.date_absence }}</strong> - {{ getPeriod(change.period) }})
                                </b-form-checkbox>
                            </b-form-group>
                        </b-collapse>
                    </div>
                    <p
                        v-if="getAbsences(false, 'student').length > 0"
                        class="text-muted"
                    >
                        <small>
                            Pour supprimer des changements, sélectionnez les changements pour faire
                            apparaître le boutton de suppression.
                        </small>
                    </p>
                    <b-btn
                        variant="danger"
                        v-if="selectedOldChanges.length != 0"
                        @click="removeChanges('old')"
                        class="mt-1"
                    >
                        Supprimer les élements sélectionnés
                    </b-btn>
                </b-tab>
            </b-tabs>
            <template slot="modal-ok">
                <icon
                    v-if="sending"
                    name="spinner"
                    color="white"
                    spin
                    class="align-baseline"
                />
                {{ validateChange }}
            </template>
        </b-modal>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import axios from "axios";
import { openDB } from "idb";

import Moment from "moment";
Moment.locale("fr");

import AddAbsenceEntry from "./add_absence_entry.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

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
            selectedOldChanges: [],
            selectedChanges: [],
            tabIndex: 0,
            sending: false,
            classe: null,
            note: "",
        };
    },
    computed: {
        onLine: function () {
            return this.$store.state.onLine;
        },
        validateChange: function () {
            if (this.tabIndex == 0) return "Valider les changements du " + this.date_absence;
            return "Valider les autres changements";
        },
        disableValidation: function () {
            return this.getAbsences(this.tabIndex == 0, "students").length == 0;
        }

    },
    methods: {
        getPeriod: function (period) {
            return this.$store.state.periods.find(p => p.id == period).name;
        },
        addAllStudents: function (period) {
            const savedStudents = this.$store.state.savedAbsences.filter(sA => {
                return sA.period == period && sA.date_absence == this.date_absence;
            }).map(sA => sA.student_id);
            const currentChanges = this.$store.state.changes.filter(c => {
                return c.period == period && c.date_absence == this.date_absence;
            }).map(c => c.matricule);
    
            this.students.filter(student => {
                // Check if there is already an saved absence or current changes.
                return !currentChanges.includes(student.matricule) && !savedStudents.includes(student.matricule);
            }).forEach(student => {
                const absence = {
                    date_absence: this.date_absence,
                    matricule: student.matricule,
                    student: student,
                    period: period,
                    is_absent: false,
                };
                this.$store.commit("setChange", absence);
            });
        },
        cleanStudents: function () {
            this.students = [];
            this.classe = null;
            this.currentSearch = null;
        },
        getAbsences: function (isCurrentDate, outputType, classe, isAbsent) {
            let changes = this.$store.state.changes
                .filter(c => isCurrentDate ? c.date_absence == this.date_absence : c.date_absence != this.date_absence);

            if (outputType == "classe") {
                return [...new Set(changes.map(c => c.student.classe.year + c.student.classe.letter))].sort();
            } else {
                if (classe) changes = changes.filter(c => c.student.classe.year + c.student.classe.letter == classe);
                if (isAbsent != undefined) changes = changes.filter(c => c.is_absent == isAbsent);
                return changes.sort((c1, c2) => {
                    if (c1.student.classe.year < c2.student.classe.year) {
                        return -1;
                    } else if (c1.student.classe.year == c2.student.classe.year) {
                        if (c1.student.classe.letter < c2.student.classe.letter) {
                            return -1;
                        } else if (c1.student.classe.letter == c2.student.classe.letter) {
                            return 0;
                        } else {
                            return 1;
                        }
                    } else {
                        return 1;
                    }
                });
            }
        },
        removeChanges: function (changeType) {
            const selected = changeType == "old" ? this.selectedOldChanges : this.selectedChanges;
            for (let rmch in selected) {
                this.$store.commit("removeChange", selected[rmch]);
            }
            if (changeType == "old") {
                this.selectedOldChanges = [];
            } else {
                this.selectedChanges = [];
                this.cleanStudents();
            }
        },
        selected: function (option) {
            if (option.type == "classe") {
                this.classe = option.id;
                this.students = option.students.sort((a, b) => a.display.localeCompare(b.display));
                // Get notes if any.
                if (this.classe in this.$store.state.notes) {
                    this.note = this.$store.state.notes[this.classe].note;
                }
                console.log(option);
            } else {
                this.classe = null;
                axios.get("/annuaire/api/student/" + option.matricule + "/")
                    .then(response => {
                        console.log(option);
                        console.log(response.data);
                        // option.student = response.data;
                        this.students = [option];
                    })
                    .catch(() => {
                        alert("Impossible de trouver l'élève sur le serveur.");
                    });
            }
        },
        getSearchOptions: function (query) {
            if (query.length == 0)
                return;
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
                            p.type = "student";
                            p.id = p.matricule;
                            return p;
                        });
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
                                    for (let s in studs.students) {
                                        db.get("students", studs.students[s])
                                            .then(student => {
                                                students.push(student);
                                            });
                                    }
                                    options.push({
                                        type: "classe",
                                        students: students,
                                        display: classeKeys[o],
                                        id: studs.id,
                                    });
                                });
                        }
                        this.searchOptions = options.sort((a, b) => a.display.localeCompare(b.display));
                    });
                });
            }
        },
        sendChanges: function (evt) {
            evt.preventDefault();
            this.sending = true;
            let app = this;
            const apiUrl = "/student_absence/api/student_absence/";
            // Is it old absences or absences of today?
            const changesToSend = this.tabIndex == 0 ? this.getAbsences(true, "student") : this.getAbsences(false, "student");

            const updateAbsences = changesToSend.filter(change => "id" in change);
            const newAbsences = changesToSend.filter(change => !("id" in change))
                .map(change => {
                    change.student_id = change.matricule;
                    return change;
                });

            const absencePromises = updateAbsences.map(change => {
                return axios.put(apiUrl + change.id + "/", change, token);
            });

            if (newAbsences.length > 0) absencePromises.push(axios.post(apiUrl, newAbsences, token));

            Promise.all(absencePromises)
                .then(responses => {
                    for (let r in responses) {
                        console.log(responses[r]);
                        if (responses[r].config.method == "put") {
                            responses[r].data.matricule = responses[r].data.student_id;
                            this.$store.commit("removeChange", responses[r].data);
                        } else if (responses[r].config.method == "post") {
                            responses[r].data.forEach(absence => {
                                absence.matricule = absence.student_id;
                                this.$store.commit("removeChange", absence);
                            });
                        }
                    }
                    app.$bvModal.hide("tovalidate");
                    app.loadAbsences(app.date_absence);
                    app.sending = false;
                })
                .catch(function (error) {
                    app.sending = false;
                    app.loadAbsences(app.date_absence);
                    alert(error);
                });
        },
        loadAbsences: function (date) {
            this.cleanStudents();
            this.date_absence = date;
            // Load absences from date_absence.
            if (this.date_absence.length == 0) return;

            this.$store.commit("updateSavedAbsences", date);
        }
    },
    mounted: function () {
        const now = Moment();

        this.loadAbsences(now.format("YYYY-MM-DD"));
    },
    components: {Multiselect, AddAbsenceEntry},
};
</script>
