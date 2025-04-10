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
    <BContainer>
        <BRow>
            <BCol>
                <h2>Préparer les changements</h2>
            </BCol>
        </BRow>

        <BOverlay :show="loading">
            <BRow>
                <BCol>
                    <BFormGroup
                        label="Prof(s) absent(s)/indisponible(s)/concerné(s)"
                    >
                        <multiselect
                            :internal-search="false"
                            :options="teacherOptions"
                            @search-change="getTeachers"
                            placeholder="Chercher un prof"
                            select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="teacher"
                            label="display"
                            track-by="matricule"
                        >
                            <template #noResult>
                                Aucun professeur trouvé.
                            </template>
                            <template #noOptions />
                        </multiselect>
                    </BFormGroup>
                </BCol>
            </BRow>

            <BRow>
                <BCol>
                    <BFormGroup
                        id="date-start-input-group"
                        label="À partir de"
                        label-cols="12"
                        label-cols-sm="4"
                    >
                        <BFormInput
                            type="date"
                            v-model="dateStart"
                            @update:model-value="updateEnd"
                        />
                    </BFormGroup>
                </BCol>
                <BCol>
                    <BFormGroup
                        id="date-end-input-group"
                        label="Jusqu'à"
                        label-cols="12"
                        label-cols-sm="4"
                    >
                        <BFormInput
                            type="date"
                            v-model="dateEnd"
                            :min="dateStart"
                        />
                    </BFormGroup>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BFormGroup
                        label="Type par défaut"
                        label-cols="12"
                        label-cols-md="5"
                    >
                        <BFormSelect
                            v-model="defaultType"
                            :options="store.changeType"
                            value-field="id"
                            text-field="name"
                        />
                    </BFormGroup>
                </BCol>
                <BCol>
                    <BFormGroup
                        label="Catégorie par défaut"
                        label-cols="12"
                        label-cols-md="5"
                    >
                        <BFormSelect
                            v-model="defaultCategory"
                            :options="store.changeCategory"
                            value-field="id"
                            text-field="category"
                        />
                    </BFormGroup>
                </BCol>
            </BRow>
            <BRow class="text-end">
                <BCol>
                    <BButton
                        variant="outline-primary"
                        @click="prepareSchedule"
                    >
                        <IBiReceipt />
                        Générer les changements
                    </BButton>
                </BCol>
            </BRow>
            <BRow class="mt-2">
                <BCol>
                    <BTable
                        :items="scheduleChanges"
                        :fields="tableFields"
                    >
                        <template #cell(change)="data">
                            <BFormSelect
                                v-model="scheduleChanges[data.index].change"
                                :options="store.changeType"
                                value-field="id"
                                text-field="name"
                            />
                        </template>
                        <template #cell(category)="data">
                            <BFormSelect
                                v-model="scheduleChanges[data.index].category"
                                :options="store.changeCategory"
                                value-field="id"
                                text-field="category"
                            />
                        </template>
                        <template #cell(time_start)="data">
                            <BFormInput
                                type="time"
                                v-model="scheduleChanges[data.index].time_start"
                            />
                        </template>
                        <template #cell(time_end)="data">
                            <BFormInput
                                type="time"
                                v-model="scheduleChanges[data.index].time_end"
                            />
                        </template>
                        <template #cell(place)="data">
                            <multiselect
                                v-model="scheduleChanges[data.index].place"
                                tag-placeholder=""
                                placeholder="Local/Lieu"
                                :taggable="true"
                                :options="placesOptions"
                                @tag="addPlaces($event, data.index)"
                                select-label=""
                                selected-label=""
                                deselect-label=""
                            >
                                <template #noOptions />
                            </multiselect>
                        </template>
                        <template #cell(classes)="data">
                            <multiselect
                                :internal-search="false"
                                :options="classesOptions"
                                @search-change="getStudentsClassesYears"
                                :multiple="true"
                                :show-no-options="false"
                                placeholder="classe ou année"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="scheduleChanges[data.index].classes"
                            >
                                <template #noResult>
                                    Aucune classe trouvée.
                                </template>
                                <template #noOptions />
                            </multiselect>
                        </template>
                        <template #cell(remove)="data">
                            <BButton
                                size="sm"
                                variant="danger"
                                @click="removeChange(data.index)"
                            >
                                <IBiTrash />
                            </BButton>
                        </template>
                    </BTable>
                </BCol>
            </BRow>
            <BRow class="text-end">
                <BCol>
                    <BButton
                        variant="success"
                        @click="submitScheduleChanges"
                    >
                        Créer les changements
                    </BButton>
                </BCol>
            </BRow>
        </BOverlay>
    </BContainer>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

import { scheduleChangeStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            dateStart: null,
            dateEnd: null,
            searchId: 0,
            teacher: null,
            teacherOptions: [],
            placesOptions: [],
            classesOptions: [],
            defaultType: null,
            defaultCategory: null,
            scheduleChanges: [],
            tableFields: [
                {
                    key: "change",
                    label: "Type"
                },
                {
                    key: "category",
                    label: "Catégorie"
                },
                {
                    key: "date_change",
                    label: "Date"
                },
                {
                    key: "time_start",
                    label: "Heure début"
                },
                {
                    key: "time_end",
                    label: "Heure fin"
                },
                {
                    key: "classes",
                    label: "Classes",
                    formatter: (value) => value.join(", ")
                },
                {
                    key: "teachers_replaced_id",
                    label: "Prof concerné",
                    formatter: () => this.teacher.display
                },
                {
                    key: "place",
                    label: "Local",
                },
                {
                    key: "remove",
                    label: ""
                }
            ],
            loading: false,
            store: scheduleChangeStore(),
        };
    },
    methods: {
        updateEnd: function () {
            if (!this.dateEnd && this.dateStart) {
                this.dateEnd = this.dateStart;
            }

            if (Moment(this.dateStart).isAfter(Moment(this.dateEnd))) {
                this.dateEnd = this.dateStart;
            }
        },
        removeChange: function (changeIndex) {
            this.scheduleChanges.splice(changeIndex, 1);
        },
        addPlaces: function (newPlace, schedIndex) {
            this.placesOptions.push(newPlace);
            this.scheduleChanges[schedIndex].place = newPlace;
        },
        getTeachers(query) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: "responsible",
                check_access: false,
                active: false,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.teacherOptions = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        getStudentsClassesYears(query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                check_access: false,
                years: true,
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    const options = response.data.map(p => {
                        return p.display;
                    });
                    this.classesOptions = options;
                })
                .catch(function (error) {
                    alert(error);
                });
        },
        prepareSchedule: function () {
            if (!this.teacher || !this.dateStart || !this.dateEnd) {
                return;
            }

            if (this.scheduleChanges.length > 0) {
                this.$bvModal.msgBoxConfirm(
                    "Génerer de nouveaux changements vont supprimés ceux déjà présents, voulez-vous continuer ?", {
                        cancelTitle: "Annuler",
                        title: "Êtes-vous sûr de vouloir continuer ?",
                        okVariant: "warning",
                        okTitle: "Continuer"
                    }
                )
                    .then((value) => {
                        if (value) {
                            this.makeSchedules();
                        }
                    });
            } else {
                this.makeSchedules();
            }
        },
        makeSchedules: function () {
            this.loading = true;
            Promise.all([
                axios.get(`/core/api/course_schedule/?responsible=${this.teacher.matricule}`),
                axios.get("/core/api/period/")
            ])
                .then((resp) => {
                    this.scheduleChanges = [];

                    const periods = resp[1].data.results;
                    const startDay = Moment(this.dateStart);
                    const endDay = Moment(this.dateEnd);
                    let currentDay = startDay;
                    while (currentDay.isSameOrBefore(endDay)) {
                        this.scheduleChanges = this.scheduleChanges.concat(
                            resp[0].data.results
                                .filter(courseSchedule => courseSchedule.day_of_week === currentDay.day() - 1)
                                .map(courseSchedule => {
                                    return {
                                        change: this.defaultType,
                                        category: this.defaultCategory,
                                        date_change: currentDay.format("YYYY-MM-DD"),
                                        time_start: periods.find(p => p.id === courseSchedule.period).start,
                                        time_end: periods.find(p => p.id === courseSchedule.period).end,
                                        classes: courseSchedule.related_classes ? courseSchedule.related_classes.split(", ") : [],
                                        teachers_replaced_id: [this.teacher.matricule],
                                    };
                                })
                        );
                        currentDay.add(1, "days");
                    }
                    this.loading = false;
                });
        },
        submitScheduleChanges: function () {
            this.loading = true;
            const data = this.scheduleChanges.map(sC => {
                if (sC.time_end === "") {
                    sC.time_end = null;
                }
                return sC;
            });
            axios.post("/schedule_change/api/schedule_change/", data, token)
                .then(() => {
                    this.$router.push("/").then(() => {
                        this.show({props: {
                            body: "Les changements ont bien été créés.",
                            variant: "success",
                            noCloseButton: true,
                        }});
                    });
                    this.loading = false;
                })
                .catch(err => {
                    this.loading = false;
                    console.log(err);
                    alert("Erreur lors de l'envoi");
                });
        }
    },
    mounted: function () {
        this.store.getChangeType();
        this.store.getPlaces()
            .then(() => {
                this.placesOptions = this.store.places;
            });
    },
    components: {
        Multiselect
    }
};
</script>
