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
                <b-form-group
                    label="Date du jour"
                >
                    <b-input
                        type="date"
                        v-model="date"
                        @input="get_absence_count"
                    />
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-table
                    hover
                    bordered
                    :items="absence_count"
                    :fields="fields"
                />
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

export default {
    data: function () {
        return {
            date: Moment().format("YYYY-MM-DD"),
            absence_count: [],
            fields: [
                {key: "classe", }
            ]
        };
    },
    methods: {
        get_absence_count: function () {
            axios.get(`/student_absence_teacher/api/count_absence/${this.date}/`)
                .then(resp => {
                    this.absence_count = JSON.parse(resp.data).map(row => {
                        const emptyPeriods = Object.entries(row).filter(c => c[0].startsWith("period") && c[1] < 0);
                        row._cellVariants = emptyPeriods.reduce((acc, v) => {
                            acc[v[0]] = "warning";
                            return acc;
                        }, {});
                        return row;
                    });
                });
        },
        cellFormatting: function (value) {
            if (value >= 0) return value;

            return "-";
        }
    },
    mounted: function () {
        axios.get("/student_absence_teacher/api/period/")
            .then(resp => {
                this.fields = this.fields.concat(
                    resp.data.results.map(p => {
                        return {
                            key: `period-${p.id}`,
                            label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                            formatter: this.cellFormatting
                        };
                    })
                );
            });
        this.get_absence_count();
    }
};
</script>
