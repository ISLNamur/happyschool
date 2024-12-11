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
        <BTableLite
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
                <div v-if="data.value">
                    {{ data.value[3] }}
                </div>
                <BLink
                    underline-variant="light"
                    v-if="data.value"
                    :to="`/overview/${data.value[0]}-${String(data.value[1]).padStart(2, '0')}-${String(data.value[2]).padStart(2, '0')}/student_view/${$route.params.studentId}/`"
                >
                    <span v-if="data.value[4]">
                        {{ data.value[4] }}
                    </span>
                    <span v-else>
                        _
                    </span>
                </BLink>
            </template>
            <template #cell(Mois)="data">
                <strong>{{ month[(firstDate.getMonth() + data.index) % 12] }}</strong>
            </template>
        </BTableLite>
    </div>
</template>

<script>
import axios from "axios";

import { getCurrentScholarYear } from "@s:core/js/common/utilities.js";

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
                { key: "Mois" }
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
    watch: {
        studentId: function () {
            this.initData();
        }
    },
    methods: {
        isToday: function (data) {
            const today = new Date();
            return data[0] === today.getFullYear() && data[1] === today.getMonth() + 1 && data[2] === today.getDate();
        },
        isCurrentDate: function (data) {
            return data[0] === parseInt(this.currentDate.slice(0, 4)) && data[1] === parseInt(this.currentDate.slice(5, 7)) && data[2] === parseInt(this.currentDate.slice(8, 10));
        },
        initData: function () {
            for (let d = 0; d < 31; d++) {
                this.fields.push(
                    {
                        key: String(d),
                        label: String(d + 1),
                    }
                );

            }

            const currentYear = getCurrentScholarYear();
            const from = `${currentYear}-08-02`;
            const to = `${currentYear + 1}-08-01`;
            Promise.all([
                axios.get("/core/api/scholar_calendar/"),
                axios.get(`/student_absence_teacher/api/absence_educ/?student__matricule=${this.studentId}&date_absence__gte=${from}&date_absence__lt=${to}&page_size=1000&ordering=period__start`),
                axios.get(`/student_absence_teacher/api/justification/?student__matricule=${this.studentId}&scholar_year=${currentYear}-${currentYear + 1}`)
            ])
                .then(resps => {
                    const firstDate = resps[0].data[0][0];
                    this.firstDate = new Date(firstDate[0], firstDate[1] - 1, firstDate[2]);
                    this.calendar = resps[0].data.map(month => {
                        return Object.assign({}, month);
                    });
                    this.calendar.forEach(month => Object.entries(month).forEach((dayData) => {
                        if (this.isToday(dayData[1])) {
                            if (month._cellVariants) {
                                month._cellVariants[dayData[0]] = "warning";
                            } else {
                                month._cellVariants = {[dayData[0]]: "warning"};
                            }
                        }
                        if (this.isCurrentDate(dayData[1])) {
                            if (month._cellVariants) {
                                month._cellVariants[dayData[0]] = "success";
                            } else {
                                month._cellVariants = {[dayData[0]]: "success"};
                            }
                        }

                        if (dayData[1][3] && ((dayData[1][3] == "Di") || (dayData[1][3] == "Sa"))) {
                            if (month._cellVariants) {
                                month._cellVariants[dayData[0]] = "danger";
                            } else {
                                month._cellVariants = {[dayData[0]]: "danger"};
                            }
                        }

                    }));
                    resps[1].data.results.forEach(abs => {
                        const rowIndex = ((11 - this.firstDate.getMonth()) + parseInt(abs.date_absence.slice(5, 7))) % 12;
                        const columnIndex = parseInt(abs.date_absence.slice(8, 10)) - 1;
                        const hasJustification = resps[2].data.results.find(just => just.absences.includes(abs.id));
                        this.calendar[rowIndex][String(columnIndex)][4] += hasJustification ? abs.status.toLowerCase() : abs.status;
                    });
                });
        }
        
    },
    mounted: function () {
        this.initData();
    }
};
</script>

<style>
.small-text {
    font-size: 0.85em;
}
</style>
