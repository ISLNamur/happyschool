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
    <BCard no-body>
        <template
            #header
        >
            <div class="d-flex justify-content-between align-items-center">
                <strong>Absences</strong>
            </div>
        </template>
        <BListGroup>
            <BListGroupItem class="d-flex justify-content-between align-items-center">
                Absences en attentes de justificatifs
                <BBadge :variant="pendingAbsences > 0 ? 'warning' : ''">
                    {{ pendingAbsences }}
                </BBadge>
            </BListGroupItem>

            <BListGroupItem
                variant="secondary"
            >
                <strong>Absences motivées:</strong>
            </BListGroupItem>
            <BListGroupItem
                v-for="justCount in justifiedAbsences"
                :key="justCount.justificationmodel__motive__short_name"
                class="d-flex justify-content-between align-items-center"
            >
                <span>
                    <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                    {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                    <span v-if="justCount.justificationmodel__motive__name.length > 50">…</span>
                </span>
                <BBadge
                    v-b-tooltip.hover="justCount.justificationmodel__motive__count > justCount.justificationmodel__motive__admissible_up_to ? `Max. ${justCount.justificationmodel__motive__admissible_up_to}` : ''"
                    :variant="justCount.justificationmodel__motive__count >= justCount.justificationmodel__motive__admissible_up_to ? 'danger' : 'secondary'"
                >
                    {{ justCount.justificationmodel__motive__count }}
                    <span v-if="justCount.justificationmodel__motive__admissible_up_to < 500">/ {{ justCount.justificationmodel__motive__admissible_up_to }}</span>
                </BBadge>
            </BListGroupItem>
            <BListGroupItem
                class="d-flex justify-content-between align-items-center"
            >
                <strong>Total justifiées / motivées:</strong>
                <span>
                    <BBadge variant="primary">
                        {{ totalAdmissibleCount }}
                    </BBadge>
                    /
                    <BBadge variant="primary">
                        {{ totalJustCount }}
                    </BBadge>
                </span>
            </BListGroupItem>
            <BListGroupItem
                variant="danger"
            >
                <strong>Absences non justifiées:</strong>
            </BListGroupItem>
            <BListGroupItem
                v-for="justCount in unjustifiedAbsences"
                :key="justCount.justificationmodel__motive__short_name"
                class="d-flex justify-content-between align-items-center"
            >
                <span>
                    <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                    {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                </span>
                <BBadge>
                    {{ justCount.justificationmodel__motive__count }}
                </BBadge>
            </BListGroupItem>
            <BListGroupItem
                class="d-flex justify-content-between align-items-center"
            >
                <strong>Total :</strong>
                <BBadge variant="danger">
                    {{ totalUnjustCount }}
                </BBadge>
            </BListGroupItem>
        </BListGroup>
    </BCard>
</template>

<script>
import axios from "axios";

export default {
    props: {
        studentId: {
            type: String,
            default: -1,
        },
    },
    data: function () {
        return {
            pendingAbsences: 0,
            justifiedAbsences: [],
            unjustifiedAbsences: [],
        };
    },
    watch: {
        studentId: function () {
            this.initData();
        },
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
        },
    },
    methods: {
        initData: function () {
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
        },
    },
    mounted: function () {
        this.initData();
    },
};
</script>
