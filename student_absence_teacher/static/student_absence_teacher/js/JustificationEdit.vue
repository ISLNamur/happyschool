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
    <b-overlay :show="loading">
        <b-row>
            <b-col>
                <b-col sm="3">
                    <div class="text-center">
                        <b-img
                            v-if="justification.student"
                            rounded
                            :src="'/static/photos/' + justification.student + '.jpg'"
                            fluid
                            alt="Photo de l'élève"
                        />
                    </div>
                </b-col>
            </b-col>
            <b-col>
                <b-form-group
                    label="Nom"
                    label-for="input-name"
                >
                    <multiselect
                        id="input-name"
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
                        :disabled="studentId"
                        v-model="student"
                    >
                        <template #noResult>
                            Aucune personne trouvée.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group label="Début">
                    <b-input-group>
                        <b-input
                            type="date"
                            v-model="justification.date_just_start"
                            @input="getRelatedAbsences"
                        />
                        <b-select
                            :options="store.periodEduc"
                            :select-size="2"
                            text-field="name"
                            value-field="index"
                            v-model="justification.half_day_start"
                            @input="getRelatedAbsences"
                        />
                    </b-input-group>
                </b-form-group>
            </b-col>
            <b-col>
                <b-form-group label="Fin">
                    <b-input-group>
                        <b-input
                            type="date"
                            v-model="justification.date_just_end"
                            @input="getRelatedAbsences"
                        />
                        <b-select
                            v-model="justification.half_day_end"
                            :options="store.periodEduc"
                            :select-size="2"
                            text-field="name"
                            value-field="index"
                            @input="getRelatedAbsences"
                        />
                    </b-input-group>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group label="Motif">
                    <b-select
                        v-model="justification.motive"
                        :options="motiveOptions"
                        value-field="id"
                        :select-size="4"
                    />
                </b-form-group>
            </b-col>
            <b-col>
                <b-form-group label="Commentaire">
                    <text-editor v-model="justification.comment" />
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group label="Absences concernées">
                    <b-list-group>
                        <b-list-group-item
                            v-for="absence in relativeAbsences"
                            :key="absence.id"
                        >
                            {{ absence.date_absence }} – {{ store.periodEduc.find(p => p.id === absence.period).name }}
                        </b-list-group-item>
                    </b-list-group>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row v-if="justification.student">
            <b-col>
                <b-overlay :show="submitting">
                    <b-btn
                        @click="submit"
                        variant="primary"
                    >
                        Soumettre
                    </b-btn>
                </b-overlay>
            </b-col>
            <b-col
                v-if="justId !== '-1'"
                class="text-right"
            >
                <b-btn
                    @click="remove"
                    variant="danger"
                >
                    Supprimer
                </b-btn>
            </b-col>
        </b-row>
        <b-row
            class="mt-2"
            v-if="student"
        >
            <b-col>
                <absences-stat :student-id="student.matricule" />
            </b-col>
        </b-row>
    </b-overlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { studentAbsenceTeacherStore } from "./stores/index.js";
import AbsencesStat from "./AbsencesStat.vue";

import TextEditor from "@s:core/js/common/text_editor.vue";
import {getPeopleByName} from "@s:core/js/common/search.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        "justId": {
            type: String,
            default: ""
        },
        "studentId": {
            type: String,
            default: -1
        },
    },
    data: function () {
        return {
            loading: true,
            submitting: false,
            justification: {
                student: null,
                date_just_start: null,
                date_just_end: null,
                half_day_start: null,
                half_day_end: null,
            },
            student: null,
            relativeAbsences: [],
            nameOptions: [],
            searchId: -1,
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        motiveOptions: function () {
            return this.store.motives.map(m => {
                const motiveWithLabel = Object.assign({}, m);
                motiveWithLabel.text = `${m.short_name} – ${m.name}`;
                return motiveWithLabel;
            });
        }
    },
    watch: {
        student: function () {
            this.justification.student = this.student.matricule;
        }
    },
    methods: {
        getNameOptions: function (query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.searching = true;

            getPeopleByName(query, this.store.settings.teachings, "student")
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.nameOptions = resp.data;
                    this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                    this.searching = false;
                });
        },
        getRelatedAbsences: function () {
            // Auto-complete date end.
            if (this.justification.date_just_start && !this.justification.date_just_end
                || this.justification.date_just_start > this.justification.date_just_end
            ) {
                this.justification.date_just_end = this.justification.date_just_start;
            }

            // Range must be set.
            if (
                !this.justification.date_just_start
                || !this.justification.date_just_end
                || this.justification.half_day_start === null
                || this.justification.half_day_start === null
            ) {
                return;
            }

            axios.get(`/student_absence_teacher/api/absence_educ/?status=A&student=${this.justification.student}&date_absence__gte=${this.justification.date_just_start}&date_absence__lte=${this.justification.date_just_end}&page_size=1000`)
                .then((resp) => {
                    const just_on_one_period = this.justification.date_just_start === this.justification.date_just_end && this.justification.half_day_start === this.justification.half_day_end;
                    this.relativeAbsences = resp.data.results.filter(absence => {
                        const periodAbsenceOrder = this.store.periodEduc.find(p => p.id === absence.period).index;

                        if (!just_on_one_period) {
                            if (absence.date_absence === this.justification.date_just_start && periodAbsenceOrder >= this.justification.half_day_start) {
                                return true;
                            }
                            if (absence.date_absence === this.justification.date_just_end && periodAbsenceOrder <= this.justification.half_day_end) {
                                return true;
                            }
                            if (absence.date_absence > this.justification.date_just_start && absence.date_absence < this.justification.date_just_end) {
                                return true;
                            }
                            return false;
                        } else {
                            return absence.date_absence === this.justification.date_just_start && periodAbsenceOrder === this.justification.half_day_start;
                        }
                    });

                    this.relativeAbsences.sort((a, b) => a.date_absence > b.date_absence);
                });
        },
        submit: function () {
            this.submitting = true;

            const data = Object.assign({}, this.justification);
            data.absences = this.relativeAbsences.map(a => a.id);
            const newJust = parseInt(this.justId) <= 0;
            if (!newJust) {
                data.id = this.justId;
            }
            const send = newJust ? axios.post : axios.put;
            const url = `/student_absence_teacher/api/justification/${newJust ? "" : this.justId + "/"}`;

            send(url, data, token)
                .then(() => {
                    this.$router.push(`/overview/${data.date_just_start}/student_view/${data.student}/`,() => {
                        this.submitting = false;
                        this.$root.$bvToast.toast("Les données ont bien été envoyées", {
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch(() =>  {
                    this.submitting = false;
                });

        },
        remove: function () {
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer cette justification",{
                centered: true,
                buttonSize: "sm",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Annuler",
            })
                .then(remove => {
                    if (!remove) return;

                    const dateJustStart = this.justification.date_just_start;
                    const studentMatricule = this.justification.student;
                    axios.delete(`/student_absence_teacher/api/justification/${this.justId}/`, token)
                        .then(() => {
                            this.$router.push(`/overview/${dateJustStart}/student_view/${studentMatricule}/`,() => {
                                this.submitting = false;
                                this.$root.$bvToast.toast("Les données ont bien été supprimées", {
                                    variant: "success",
                                    noCloseButton: true,
                                });
                            });
                        });
                });
        }
    },
    mounted: function () {
        this.store.getOptions();

        if (parseInt(this.studentId) > 0) {
            this.justification.student = this.studentId;
            axios.get(`/annuaire/api/student/${this.studentId}/`)
                .then((resp) => {
                    this.student = resp.data;
                });
        }

        if (!this.justId || parseInt(this.justId) < 0) {
            this.loading = false;
            return;
        }

        axios.get(`/student_absence_teacher/api/justification/${this.justId}`)
            .then((resp) => {
                this.justification = resp.data;
                axios.get(`/annuaire/api/student/${this.justification.student}`)
                    .then((resp) => {
                        this.student = resp.data;
                    });
                this.getRelatedAbsences();
                this.loading = false;
            });
    },
    components: {
        TextEditor,
        Multiselect,
        AbsencesStat,
    }
};
</script>
