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
                <BFormGroup>
                    <BFormSelect
                        :options="activitySupports"
                        value-field="id"
                        v-model="currentActSuppId"
                        @update:model-value="updateCurrentActSupp"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BButtonGroup>
                    <BButton
                        variant="outline-secondary"
                        @click="copy"
                        :disabled="activitySupports.length === 0"
                    >
                        <IBiFiles />
                        Copier
                    </BButton>
                    <BButton
                        variant="success"
                        @click="add"
                    >
                        <IBiPlus />
                        Ajouter
                    </BButton>
                    <BButton
                        variant="danger"
                        @click="remove"
                        :disabled="activitySupports.length === 0"
                    >
                        <IBiTrash />
                        Supprimer
                    </BButton>
                </BButtonGroup>
            </BCol>
        </BRow>
        <BRow v-if="currentActSupp">
            <BCol>
                <BCard>
                    <BRow class="mb-1">
                        <BCol>
                            <strong>
                                <BForm inline>
                                    Du<BFormInput
                                        type="date"
                                        v-model="currentActSupp.date_start"
                                        class="mr-sm-2 ml-2"
                                    />
                                    au<BFormInput
                                        type="date"
                                        v-model="currentActSupp.date_end"
                                        class="ml-2"
                                    />
                                </BForm>
                            </strong>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BTableSimple v-if="!loading">
                            <BThead>
                                <BTr>
                                    <BTh>Jour</BTh>
                                    <BTh>Cours</BTh>
                                    <BTh>Prof</BTh>
                                </BTr>
                            </BThead>
                            <BTbody>
                                <BTr
                                    v-for="day in supportDays"
                                    :key="day"
                                >
                                    <BTd>{{ dayOfWeek[day] }}</BTd>
                                    <BTd>
                                        <multiselect
                                            :internal-search="false"
                                            :options="store.branches"
                                            placeholder="Choisir une matière"
                                            select-label=""
                                            selected-label="Sélectionné"
                                            deselect-label="Cliquer dessus pour enlever"
                                            v-model="currentActSupp.support_activities[day].branch"
                                            :show-no-options="false"
                                            label="branch"
                                            track-by="id"
                                            multiple
                                        >
                                            <template #noResult>
                                                Aucune branche trouvé.
                                            </template>
                                            <template #noOptions />
                                        </multiselect>
                                    </BTd>
                                    <BTd>
                                        <multiselect
                                            :id="`responsible-support-${day}`"
                                            :internal-search="false"
                                            :options="responsibleOptions"
                                            @search-change="getPeople"
                                            placeholder="Choisir un ou plusieurs profs"
                                            select-label=""
                                            selected-label="Sélectionné"
                                            deselect-label="Cliquer dessus pour enlever"
                                            v-model="currentActSupp.support_activities[day].teachers"
                                            label="display"
                                            track-by="matricule"
                                            :show-no-options="false"
                                            multiple
                                        >
                                            <template #noResult>
                                                Aucun responsable trouvé.
                                            </template>
                                            <template #noOptions />
                                        </multiselect>
                                    </BTd>
                                </BTr>
                            </BTbody>
                        </BTableSimple>
                    </BRow>
                </BCard>
            </BCol>
        </BRow>
        <BRow
            v-if="currentActSupp"
            class="mt-3"
        >
            <BCol>
                <BCard>
                    <BFormGroup>
                        <BFormRadioGroup
                            v-model="directedStudy"
                            :options="[{ text: 'Oui', value: true }, { text: 'Non', value: false }]"
                            name="has-directed-study"
                            button-variant="outline-primary"
                            buttons
                        />
                        <template #label>
                            <strong>Étude dirigée</strong>
                        </template>
                    </BFormGroup>
                    <BFormGroup
                        v-slot="{ ariaDescribedby }"
                        v-if="directedStudy"
                    >
                        <BFormCheckboxGroup
                            v-model="currentActSupp.directed_study.days"
                            :options="studyDays"
                            :aria-describedby="ariaDescribedby"
                            name="directed-study"
                        />
                    </BFormGroup>
                </BCard>
            </BCol>
        </BRow>
        <BRow class="mt-2">
            <BCol>
                <course-reinforcement
                    :pia="pia"
                    ref="reinforcement"
                />
            </BCol>
        </BRow>
    </BOverlay>
</template>

<script>
import axios from "axios";

import { getPeopleByName } from "@s:core/js/common/search.js";

import { piaStore } from "./stores/index.js";

import CourseReinforcement from "./course_reinforcement.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };


import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

export default {
    props: {
        pia: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
            loading: true,
            activitySupports: [],
            currentActSuppId: null,
            currentActSupp: null,
            directedStudy: false,
            responsibleOptions: [],
            branch: [],
            teachers: [],
            dayOfWeek: { 1: "Lundi", 2: "Mardi", 3: "Mercredi", 4: "Jeudi", 5: "Vendredi", 6: "Samedi", 7: "Dimanche" },
            searchId: 0,
            store: piaStore(),
        };
    },
    computed: {
        supportDays: function () {
            const seqDays = this.store.settings.weekday_support_activity.split(",");
            const days = seqDays.filter(d => d.length === 1).map(d => Number(d.trim()));
            const ranges = seqDays.filter(d => d.length === 3).map(d => d.trim()).filter(d => d[1] === "-");
            ranges.forEach(r => {
                const start = Number(r[0]);
                const end = Number(r[2]);
                if (start <= end) {
                    Array(end - start + 1).fill().map((_, i) => i + start).forEach(d => days.push(d));
                }
            });

            return days.sort();
        },
        studyDays: function () {
            return Object.entries(this.dayOfWeek).map((day) => {
                return { text: day[1], value: Number(day[0]) };
            }).filter(sD => sD.value < 6);
        }
    },
    methods: {
        add: function () {
            const newId = Math.min(Math.min(...this.activitySupports.map(sA => sA.id)), 0) - 1;

            const newActivitySupport = {
                support_activities: {}, id: newId, date_start: null, date_end: null, text: "Nouvel aménagement", directed_study: { days: [] }
            };
            this.supportDays.forEach(d => {
                newActivitySupport.support_activities[d] = { branch: [], teachers: [] };
            });
            this.activitySupports.push(newActivitySupport);

            this.currentActSupp = newActivitySupport;
            this.currentActSuppId = newId;
        },
        copy: function () {
            let copy = JSON.parse(JSON.stringify(this.currentActSupp));
            copy.id = Math.min(Math.min(...this.activitySupports.map(sA => sA.id)), 0) - 1;
            copy.text = `Copie de ${copy.text}`;
            this.activitySupports.push(copy);
            this.currentActSupp = copy;
            this.currentActSuppId = copy.id;

        },
        remove: function () {
            this.$bvModal.msgBoxConfirm(
                "Êtes-vous sûr de vouloir supprimer l'élément ?",
                {
                    title: "Attention !",
                    okVariant: "danger",
                    okTitle: "Oui",
                    cancelTitle: "Non",
                },
            ).then((confirm) => {
                if (confirm) {
                    const sAIndex = this.activitySupports.findIndex(
                        sA => sA.id === this.currentActSupp.id && sA.date_start === this.currentActSupp.date_start
                    );
                    const removedObj = this.activitySupports.splice(sAIndex, 1)[0];
                    this.currentActSupp = this.activitySupports[this.activitySupports.length - 1];
                    axios.delete(`/pia/api/activity_support/${removedObj.id}/`, token);
                }
            });
        },
        save: function (piaId) {
            return new Promise((resolve, reject) => {
                this.loading = true;
                const activitySupportProms = this.activitySupports.map(sA => {
                    const isNew = sA.id < 0;
                    const send = isNew ? axios.post : axios.put;
                    const url = `/pia/api/activity_support/${isNew ? "" : sA.id + "/"}`;

                    // Copy activity support for sending.
                    let data = Object.assign({}, sA);
                    data.pia_model = piaId;
                    return send(url, data, token);
                });
                const reinforcementProm = this.$refs.reinforcement.save(piaId);

                Promise.all(activitySupportProms.concat([reinforcementProm])).then((resps) => {
                    // Reinforcement prom return nothing, discard them.
                    const activitySupportResponses = resps.filter(r => r);
                    this.expandActivitySupport(activitySupportResponses.map(r => r.data));
                    this.loading = false;
                    resolve();
                }).catch((err) => {
                    console.log(err);
                    this.loading = false;
                    reject(err);
                });
            });
        },
        updateCurrentActSupp: function (selected) {
            this.currentActSupp = this.activitySupports.find(sA => sA.id === selected);

            // Update visibility of directed study
            this.directedStudy = this.currentActSupp.directed_study.days.length > 0;
        },
        expandActivitySupport: function (activitySupports) {
            this.activitySupports = activitySupports.sort((a, b) => a.date_start < b.date_start).map(sA => {
                sA.text = `Du ${sA.date_start} au ${sA.date_end}`;
                return sA;
            });

            if (this.activitySupports.length > 0) {
                this.currentActSupp = this.activitySupports[0];
                this.currentActSuppId = this.activitySupports[0].id;

                if (
                    "days" in this.currentActSupp.directed_study
                    && this.currentActSupp.directed_study.days.length > 0
                ) {
                    this.directedStudy = true;
                }
            }
        },
        getPeople: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "responsible")
                .then((resp) => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                    // this.searching = false;
                })
                .catch((err) => {
                    alert(err);
                    // this.searching = false;
                });
        },
        /**
         * Check and update support activities days if anything has changed.
         */
        checkSupportActivities: function () {
            this.activitySupports.forEach(aS => {
                // Add new support days.
                this.supportDays.forEach(sD => {
                    // Check
                    if (Number(sD) in aS.support_activities) {
                        return;
                    }

                    aS.support_activities[Number(sD)] = { branch: [], teachers: [] };
                });

                // Remove deleted support days.
                const removedDays = Object.keys(aS.support_activities)
                    .filter(sA => !this.supportDays.includes(Number(sA)));

                removedDays.forEach(rD => {
                    delete aS[rD];
                });
            });
        },
        checkDirectedStudy: function () {
            this.activitySupports.forEach(aS => {
                if ("days" in aS.directed_study) {
                    return;
                }

                aS.days = [];
            });
        }
    },
    components: {
        Multiselect,
        CourseReinforcement,
    },
    mounted: function () {
        this.store.loadOptions()
            .then(() => {
                if (this.pia) {
                    axios.get(`/pia/api/activity_support/?pia_model=${this.pia}`)
                        .then((resp) => {
                            this.expandActivitySupport(resp.data.results);
                            this.checkSupportActivities();
                            this.checkDirectedStudy();

                            this.loading = false;
                        });
                } else {
                    this.loading = false;
                }
            });
    }
};
</script>
