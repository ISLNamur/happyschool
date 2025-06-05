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
    <BOverlay :show="loading">
        <BRow>
            <BCol>
                <BCol sm="3">
                    <div class="text-center">
                        <BImg
                            v-if="justification.student"
                            rounded
                            :src="'/static/photos/' + justification.student + '.jpg'"
                            fluid
                            alt="Photo de l'élève"
                        />
                    </div>
                </BCol>
            </BCol>
            <BCol>
                <BFormGroup
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
                        :disabled="studentId > 0"
                        v-model="student"
                    >
                        <template #noResult>
                            Aucune personne trouvée.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup label="Début">
                    <BInputGroup>
                        <BFormInput
                            type="date"
                            v-model="justification.date_just_start"
                            @update:model-value="getRelatedAbsences"
                        />
                        <BFormSelect
                            :options="store.periodEduc"
                            :select-size="2"
                            text-field="name"
                            value-field="index"
                            v-model="justification.half_day_start"
                            @update:model-value="getRelatedAbsences"
                        />
                    </BInputGroup>
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup label="Fin">
                    <BInputGroup>
                        <BFormInput
                            type="date"
                            v-model="justification.date_just_end"
                            @update:model-value="getRelatedAbsences"
                        />
                        <BFormSelect
                            v-model="justification.half_day_end"
                            :options="store.periodEduc"
                            :select-size="2"
                            text-field="name"
                            value-field="index"
                            @update:model-value="getRelatedAbsences"
                        />
                    </BInputGroup>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup label="Motif">
                    <BFormSelect
                        v-model="justification.motive"
                        :options="motiveOptions"
                        value-field="id"
                        :select-size="4"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup label="Commentaire">
                    <text-editor v-model="justification.comment" />
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup label="Absences concernées">
                    <BListGroup>
                        <BListGroupItem
                            v-for="absence in relativeAbsences"
                            :key="absence.id"
                        >
                            {{ absence.date_absence }} – {{ store.periodEduc.find(p => p.id === absence.period).name }}
                        </BListGroupItem>
                    </BListGroup>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow v-if="justification.student">
            <BCol>
                <BOverlay :show="submitting">
                    <BButton
                        @click="submit"
                        variant="primary"
                    >
                        Soumettre
                    </BButton>
                </BOverlay>
            </BCol>
            <BCol
                v-if="justId !== '-1'"
                class="text-end"
            >
                <BButton
                    @click="remove"
                    variant="danger"
                >
                    Supprimer
                </BButton>
            </BCol>
        </BRow>
        <BRow
            class="mt-2"
            v-if="student"
        >
            <BCol>
                <absences-stat
                    :student-id="student.matricule"
                    ref="stat"
                />
            </BCol>
        </BRow>
    </BOverlay>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { useToastController, useModalController } from "bootstrap-vue-next";

import { studentAbsenceTeacherStore } from "./stores/index.js";
import AbsencesStat from "./AbsencesStat.vue";

import TextEditor from "@s:core/js/common/text_editor.vue";
import {getPeopleByName} from "@s:core/js/common/search.js";
import moment from "moment";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        const { create } = useModalController();
        return { show, create };
    },
    props: {
        "justId": {
            type: String,
            default: ""
        },
        "studentId": {
            type: String,
            default: -1
        },
        "endDate": {
            type: String,
            default: "",
        },
        "absencesCount": {
            type: Number,
            default: 0,
        }
    },
    data: function () {
        return {
            loading: true,
            submitting: false,
            justification: {
                student: null,
                motive: null,
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
        checkAdmissibility: function () {
            return new Promise((resolve, reject) => {
                // Check admissible justification.
                const justMotive = this.$refs.stat.justifiedAbsences.find(m => m.justificationmodel__motive === this.justification.motive);
                if (justMotive) {
                    // No further justification should be admissible.
                    if (justMotive.justificationmodel__motive__count >= justMotive.justificationmodel__motive__admissible_up_to) {
                        this.create({
                            body: `L'étudiant a atteint la limite maximum de justificatif (${justMotive.justificationmodel__motive__count}). Êtes-vous sûr de vouloir continuer ?`,
                            centered: true,
                            buttonSize: "sm",
                            okVariant: "danger",
                            okTitle: "Oui",
                            cancelTitle: "Annuler",
                        }).then((proceed) => {
                            if (proceed.ok) {
                                resolve();
                            } else {
                                reject();
                            }
                        });
                    } else if (justMotive.justificationmodel__motive__count +2 >= justMotive.justificationmodel__motive__admissible_up_to) {
                        this.create({
                            body: `L'étudiant a bientôt atteint la limite des justificatifs pour le motif ${justMotive.justificationmodel__motive__short_name}. Merci de prendre les dispositions nécessaire.`,
                            okOnly: true,
                        }).then(() => {
                            resolve();
                        });
                    } else {
                        resolve();
                    }
                } else {
                    resolve();
                }
            });
        },
        submit: function () {
            this.submitting = true;

            this.checkAdmissibility()
                .then(() => {
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
                            this.$router.push(`/overview/${data.date_just_start}/student_view/${data.student}/`)
                                .then(() => {
                                    this.submitting = false;
                                    this.show( {
                                        body: "Les données ont bien été envoyées",
                                        variant: "success",
                                        noCloseButton: true,
                                    });
                                });
                        })
                        .catch((err) =>  {
                            this.submitting = false;
                            let additionalInfo = "";
                            if ("response" in err && err.response.data.non_field_errors) {
                                additionalInfo = err.response.data.non_field_errors.join(" ");
                            }
                            const errorMessage = `Une erreur est survenue lors de l'envoi des données. ${additionalInfo}`;
                            this.show({
                                body: errorMessage,
                                variant: "danger",
                                noCloseButton: true,
                            });
                        });
                })
                .catch(() => {
                    this.submitting = false;
                });
        },
        remove: function () {
            this.create({
                body: "Êtes-vous sûr de vouloir supprimer cette justification",
                centered: true,
                buttonSize: "sm",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Annuler",
            })
                .then(remove => {
                    if (!remove.ok) return;

                    const dateJustStart = this.justification.date_just_start;
                    const studentMatricule = this.justification.student;
                    axios.delete(`/student_absence_teacher/api/justification/${this.justId}/`, token)
                        .then(() => {
                            this.$router.push(`/overview/${dateJustStart}/student_view/${studentMatricule}/`)
                                .then(() => {
                                    this.submitting = false;
                                    this.show({
                                        body: "Les données ont bien été supprimées",
                                        variant: "success",
                                        noCloseButton: true,
                                    });
                                });
                        });
                });
        }
    },
    mounted: function () {
        this.store.getOptions().then(() => {
            if (parseInt(this.studentId) > 0) {
                this.justification.student = this.studentId;
                axios.get(`/annuaire/api/student/${this.studentId}/`)
                    .then((resp) => {
                        this.student = resp.data;
                    });

                if (this.endDate) {
                    this.justification.date_just_end = this.endDate;
                    // Estimate from unjustified count (with a margin of two days).
                    const startDate = moment(this.endDate).subtract(Math.round(this.absencesCount / this.store.periodEduc.length) + 2, "days").format("YYYY-MM-DD");

                    axios.get(
                        `/student_absence_teacher/api/absence_educ/?student__matricule=${this.studentId}&status=A&date_absence__lte=${this.endDate}&date_absence__gte=${startDate}&ordering=date_absence,period__start`
                    ).then((resp) => {
                        this.justification.date_just_start = resp.data.results[0].date_absence;
                        this.justification.half_day_start = this.store.periodEduc.find(p => p.id === resp.data.results[0].period).index;
                        this.justification.half_day_end = this.store.periodEduc.find(p => p.id === resp.data.results[resp.data.count - 1].period).index;

                        this.getRelatedAbsences();
                    });
                }
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
        });
    },
    components: {
        TextEditor,
        Multiselect,
        AbsencesStat,
    }
};
</script>
