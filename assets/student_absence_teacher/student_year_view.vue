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
        <b-table-lite
            :items="calendar"
            sticky-header="650px"
            :fields="fields"
            striped
            small
            class="small-text"
            bordered
            hover
            foot-clone
            stacked="sm"
            head-variant="dark"
        >
            <template #cell()="data">
                {{ data.value[3] }}
                <a
                    v-if="data.value[3]"
                    :href="`#/student_view/${$route.params.studentId}/${data.value[0]}-${String(data.value[1]).padStart(2, '0')}-${String(data.value[2]).padStart(2, '0')}`"
                >
                    <span v-if="data.value[4]">
                        {{ data.value[4] }}
                    </span>
                    <span v-else>
                        _
                    </span>
                </a>
            </template>
            <template #cell(Mois)="data">
                <strong>{{ month[(firstDate.getMonth() + data.index) % 12] }}</strong>
            </template>
        </b-table-lite>
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: {
        studentId: {
            type: Number,
            default: -1,
        },
        currentDate: {
            type: String,
            default: "1970-01-01"
        }
    },
    data: function () {
        return {
            calendar: [],
            fields: [
                {key: "Mois"}
            ],
            firstDate: null,
            month: [
                "Jan.",
                "Fév.",
                "Mars",
                "Avril",
                "Mai",
                "Juin",
                "Juil.",
                "Août",
                "Sept.",
                "Oct.",
                "Nov.",
                "Déc.",
            ],
        };
    },
    methods: {
        isToday: function (data) {
            const today = new Date();
            return data[0] === today.getFullYear() && data[1] === today.getMonth() + 1 && data[2] === today.getDate();
        },
        isCurrentDate: function (data) {
            return data[0] === parseInt(this.currentDate.slice(0, 4)) && data[1] === parseInt(this.currentDate.slice(5, 7)) && data[2] === parseInt(this.currentDate.slice(8, 10));
        }
    },
    mounted: function () {
        let app = this;
        for (let d = 0; d < 31; d++) {
            this.fields.push(
                {
                    key: String(d),
                    label: String(d + 1),
                    tdClass: function (value, key, item) {
                        return [app.isToday(value) ? "today" : "", app.isCurrentDate(value) ? "currentdate" : ""];
                    }
                }
            );
        }

        const from = "2021-08-01";
        const to = "2022-08-31";
        Promise.all([
            axios.get("/core/api/scholar_calendar/"),
            axios.get(`/student_absence/api/student_absence/?student__matricule=${this.studentId}&date_absence__gte=${from}&date_absence__lt=${to}&page_size=1000&ordering=period__start`),
        ])
            .then(resps => {
                const firstDate = resps[0].data[0][0];
                this.firstDate = new Date(firstDate[0], firstDate[1] - 1, firstDate[2]);
                this.calendar = resps[0].data;
                resps[1].data.results.forEach(abs => {
                    const rowIndex = ((11 - this.firstDate.getMonth()) + parseInt(abs.date_absence.slice(5,7))) % 12;
                    const columnIndex = parseInt(abs.date_absence.slice(8, 10)) - 1;
                    this.calendar[rowIndex][columnIndex][4] += abs.is_absent ? "A" : "P";
                });
            });
    }
};
</script>

<style>
    .small-text {
        font-size: 0.85em;
    }
    .today {
        background-color: lightseagreen;
    }
    .currentdate {
        font-weight: bold;
        background-color: lightblue;
    }
</style>
