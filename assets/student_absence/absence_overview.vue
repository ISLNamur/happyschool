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
        <b-card-group class="mt-2">
            <b-card title="Dernières absences">
                <b-table
                    striped
                    hover
                    :items="lastAbsences"
                    :fields="fields"
                >
                    <template #cell(student)="data">
                        <a
                            href="#/list"
                            @click="filterStudent(data.item.student_id)"
                        >{{ data.value }}</a>
                    </template>
                    <template #cell(date_absence)="data">
                        {{ data.value }}
                    </template>
                    <template #cell(is_absent)="data">
                        {{ data.value }}
                    </template>
                    <template #cell(is_processed)="data">
                        <b-form-checkbox
                            :checked="data.value"
                            @change="updateProcessed(!data.value, data.item.id, data.index)"
                        />
                    </template>
                </b-table>
                <b-overlay v-show="!loading">
                    <b-btn @click="getMoreAbsences">
                        <b-icon icon="chevron-double-down" />
                        Afficher plus
                    </b-btn>
                </b-overlay>
            </b-card>
            <!-- <b-card title="Élèves absents (en ½ jours)" /> -->
        </b-card-group>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import {displayStudent} from "../common/utilities.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            /**
             * The list of the 25 last absences.
             */
            lastAbsences: [],
            /**
             * The fields of the last absences table.
             */
            fields: [
                {
                    key: "student",
                    label: "Élèves",
                    formatter: value => {
                        return this.displayStudent(value);
                    }
                },
                {
                    key: "date_absence",
                    label: "Date",
                    formatter: value => {
                        return Moment(value).calendar().split(" à ")[0];
                    }
                },
                {
                    key: "is_absent",
                    label: "Absence",
                    formatter: (value, key, item) => {
                        const period = this.$store.state.periods.find(p => p.id == item.period).name;
                        return value ? period : "";
                    }
                },
                {
                    key: "is_processed",
                    label: "",
                },
            ],
            absenceCount: [],
            absenceCountFields: {
                "student": {
                    label: "Élèves",
                },
                "half_day_diff": {
                    label: "Non just.",
                },
                "half_day_just": {
                    label: "Just."
                },
                "half_day_miss": {
                    label: "Total",
                }
            },
            /** The next page url for absences. */
            absenceNextPage: null,
            /** Is the page loading? */
            loading: false,
        };
    },
    methods: {
        displayStudent,
        /** Update processed status for an absence.
         * 
         * @param {Boolean} event The processed status.
         * @param {Number} id The unique id of the related object
         * @param {Number} index Position of the related absence object.
        */
        updateProcessed(event, id, index) {
            axios.patch(`/student_absence/api/student_absence/${id}/`, {is_processed: event}, token)
                .then(resp => {
                    this.lastAbsences[index] = resp.data;
                });
        },
        /**
         * Add a filter for a specific student for the list component.
         * @param {Number} matricule The matricule of the student.
         */
        filterStudent(matricule) {
            this.$store.commit("addFilter", {"tag": matricule, "filterType": "student__matricule", "value":matricule});
        },
        /**
         * Get more absences.
         */
        getMoreAbsences() {
            if (!this.absenceNextPage) return;

            this.loading = true;
            axios.get(this.absenceNextPage)
                .then(resp => {
                    this.lastAbsences = this.lastAbsences.concat(resp.data.results);
                    this.absenceNextPage = this.cleanUrlStr(resp.data.next);
                    this.loading = false;
                })
                .catch(() => {
                    this.loading = false;
                });
        },
        /** Remove protocol and domain for url string. */
        cleanUrlStr(urlStr) {
            return urlStr.substr(urlStr.indexOf("/", 8));
        }
    },
    mounted: function () {
        let url = "/student_absence/api/student_absence/?ordering=-datetime_creation&page_size=15&is_absent=true";
        if (this.$store.state.forceAllAccess)
            url += "&forceAllAccess=1";
        axios.get(url)
            .then(response => {
                this.lastAbsences = response.data.results;
                this.absenceNextPage = this.cleanUrlStr(response.data.next);
            });
    }
};
</script>
