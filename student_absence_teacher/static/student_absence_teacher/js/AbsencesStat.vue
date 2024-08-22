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
    <b-card no-body>
        <template
            #header
        >
            <div class="d-flex justify-content-between align-items-center">
                <strong>Absences</strong>
            </div>
        </template>
        <b-list-group>
            <b-list-group-item class="d-flex justify-content-between align-items-center">
                Absences en attentes de justificatifs
                <b-badge :variant="pendingAbsences > 0 ? 'warning' : ''">
                    {{ pendingAbsences }}
                </b-badge>
            </b-list-group-item>

            <b-list-group-item
                variant="secondary"
            >
                <strong>Absences motivées:</strong>
            </b-list-group-item>
            <b-list-group-item
                v-for="justCount in justifiedAbsences"
                :key="justCount.justificationmodel__motive__short_name"
                class="d-flex justify-content-between align-items-center"
            >
                <span>
                    <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                    {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                    <span v-if="justCount.justificationmodel__motive__name.length > 50">…</span>
                </span>
                <b-badge
                    :id="`just-count-badge-${justCount.justificationmodel__motive__short_name}`"
                    :variant="justCount.justificationmodel__motive__count > justCount.justificationmodel__motive__admissible_up_to ? 'danger' : ''"
                >
                    {{ justCount.justificationmodel__motive__count }}
                </b-badge>
                <b-tooltip
                    v-if="justCount.justificationmodel__motive__count > justCount.justificationmodel__motive__admissible_up_to"
                    :target="`just-count-badge-${justCount.justificationmodel__motive__short_name}`"
                    triggers="hover"
                >
                    Max. {{ justCount.justificationmodel__motive__admissible_up_to }}
                </b-tooltip>
            </b-list-group-item>
            <b-list-group-item
                class="d-flex justify-content-between align-items-center"
            >
                <strong>Total justifiées / motivées:</strong>
                <span>
                    <b-badge variant="primary">
                        {{ totalAdmissibleCount }}
                    </b-badge>
                    /
                    <b-badge variant="primary">
                        {{ totalJustCount }}
                    </b-badge>
                </span>
            </b-list-group-item>
            <b-list-group-item
                variant="danger"
            >
                <strong>Absences non justifiées:</strong>
            </b-list-group-item>
            <b-list-group-item
                v-for="justCount in unjustifiedAbsences"
                :key="justCount.justificationmodel__motive__short_name"
                class="d-flex justify-content-between align-items-center"
            >
                <span>
                    <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                    {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                </span>
                <b-badge>
                    {{ justCount.justificationmodel__motive__count }}
                </b-badge>
            </b-list-group-item>
            <b-list-group-item
                class="d-flex justify-content-between align-items-center"
            >
                <strong>Total :</strong>
                <b-badge variant="danger">
                    {{ totalUnjustCount }}
                </b-badge>
            </b-list-group-item>
        </b-list-group>
    </b-card>
</template>

<script>
import axios from "axios";

export default {
    props: {
        studentId: {
            type: String,
            default: -1
        }
    },
    data: function () {
        return {
            pendingAbsences: 0,
            justifiedAbsences: [],
            unjustifiedAbsences: [],
        };
    },
    computed: {
        totalJustCount: function () {
            return this.justifiedAbsences.reduce((p, c) => p + c.justificationmodel__motive__count, 0);
        },
        totalAdmissibleCount: function () {
            return this.justifiedAbsences.reduce((p, c) => {
                if (c.justificationmodel__motive__count > c.justificationmodel__motive__admissible_up_to) {
                    return p + c.justificationmodel__motive__admissible_up_to;
                }
                return p + c.justificationmodel__motive__count;
            }, 0);
        },
        totalUnjustCount: function () {
            return this.unjustifiedAbsences.reduce((p, c) => p + c.justificationmodel__motive__count, 0);
        }
    },
    mounted: function () {
        if (parseInt(this.studentId) < 1) {
            return;
        }

        axios.get(`/student_absence_teacher/api/count_no_justification/${this.studentId}/`)
            .then((resp) => {
                this.pendingAbsences = resp.data.count;
            });
        axios.get(`/student_absence_teacher/api/count_justification/${this.studentId}/`)
            .then((resp) => {
                this.justifiedAbsences = resp.data.justified;
                this.unjustifiedAbsences = resp.data.unjustified;
            });
    }
};
</script>
