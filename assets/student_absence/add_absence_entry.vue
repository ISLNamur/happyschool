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
    <b-list-group-item>
        <b-row>
            <b-col cols="3">
                {{ displayStudent(student) }}
            </b-col>
            <b-col>
                <b-row>
                    <b-col
                        v-for="(p, idx) in periodIds"
                        :key="p"
                        class="text-center"
                    >
                        <b-form-checkbox
                            v-model="isAbsent[idx]"
                            name="is-absent"
                            switch
                            @change="changeAbsence(idx)"
                            v-if="period(p)"
                        >
                            <span :class="isSaved() ? 'font-italic' : ''">
                                {{ period(p).name }}
                            </span>
                        </b-form-checkbox>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-list-group-item>
</template>

<script>
import {displayStudent} from "../common/utilities.js";

export default {
    props: {
        dateAbsence: {
            type: String,
            default: ""
        },
        student: {
            type: Object,
            default: () => {}
        },
        periodIds: {
            type: Array,
            default: () => []
        }
    },
    data: function () {
        return {
            isAbsent: []
        };
    },
    watch: {
        periodIds: function () {
            this.initAbsence();
        }
    },
    methods: {
        displayStudent,
        baseAbsence: function (index) {
            const absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: this.periodIds[index]
            };
            const absInStore = this.$store.getters.change(absence);
            if (absInStore) return absInStore;

            return this.$store.getters.savedAbsence(absence);
        },
        checkData: function (index) {
            return this.baseAbsence(index) ? this.baseAbsence(index).is_absent : undefined;
        },
        period: function (periodId) {
            return this.$store.state.periods.find(p => p.id === periodId);
        },
        isSaved: function () {
            return this.baseAbsence && "id" in this.baseAbsence;
        },
        changeAbsence: function (index) {
            const checked = !this.checkData(index);
            let absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: this.periodIds[index],
                is_absent: checked,
            };

            if (!this.baseAbsence(index) || checked != this.baseAbsence(index).is_absent) {
                if (this.baseAbsence(index) && "id" in this.baseAbsence(index)) absence.id = this.baseAbsence(index).id;
                this.$store.commit("setChange", absence);
            } else {
                this.$store.commit("removeChange", absence);
            }
        },
        initAbsence: function () {
            this.isAbsent = this.periodIds.map((p, i) => this.baseAbsence(i) ? this.baseAbsence(i).is_absent : undefined);
        }
    },
    mounted: function () {
        this.initAbsence();
    }
};
</script>
