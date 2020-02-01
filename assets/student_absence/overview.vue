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
                    <template v-slot:cell(student)="data">
                        <a
                            href="#/list"
                            @click="filterStudent(data.item.student_id)"
                        >{{ data.value }}</a>
                    </template>
                    <template v-slot:cell(date_absence)="data">
                        {{ data.value }}
                    </template>
                    <template v-slot:cell(is_absent)="data">
                        {{ data.value }}
                    </template>
                </b-table>
            </b-card>
            <b-card title="Élèves absents (en ½ jours)" />
        </b-card-group>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

export default {
    data: function () {
        return {
            lastAbsences: [],
            fields: [
                {
                    key: "student",
                    label: "Élèves",
                    formatter: value => {
                        if (this.$store.state.settings.teachings.length == 1) {
                            return value.display.split(" – ")[0];
                        } else {
                            return value.display;
                        }
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
            }
        };
    },
    methods: {
        filterStudent(matricule) {
            this.$store.commit("addFilter", {"tag": matricule, "filterType": "student__matricule", "value":matricule});
        }
    },
    mounted: function () {
        let url = "/student_absence/api/student_absence/?ordering=-datetime_creation&page_size=15&is_absent=true";
        if (this.$store.state.forceAllAccess)
            url += "&forceAllAccess=1";
        axios.get(url)
            .then(response => {
                this.lastAbsences = response.data.results;
            });

        // axios.get('/student_absence/api/absence_count/')
        // .then(response => {
        //     this.absenceCount = response.data;
        // });

    }
};
</script>
