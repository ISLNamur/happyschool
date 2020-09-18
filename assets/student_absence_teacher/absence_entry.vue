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
        <b-card>
            <strong>{{ absence.date_absence }}</strong>:
            <a :href="`/annuaire/#/person/student/${absence.student.matricule}/`">
                {{ displayStudent(absence.student) }}
            </a>
            <b-btn
                variant="link"
                size="sm"
                @click="filterStudent"
            >
                <b-icon icon="funnel" />
            </b-btn>
            <br>
            <strong>{{ status }}</strong>
            {{ absence.period.name }}
            {{ useCourse ? `(${absence.given_course.display})` : "" }}
            <p>{{ absence.comment }}</p>
        </b-card>
    </div>
</template>

<script>
import {displayStudent} from "../common/utilities.js";

const absenceLabel = {"presence": "Présence", "absence": "Absence", "lateness": "Retard"};

export default {
    props: {
        "absence": {
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
        };
    },
    computed: {
        useCourse: function () {
            return this.$store.state.settings.select_student_by === "GC";
        },
        status: function () {
            return absenceLabel[this.absence.status];
        }
    },
    methods: {
        filterStudent: function () {
            this.$emit("filterStudent", this.absence.student_id);
        },
        displayStudent
    },
};
</script>
