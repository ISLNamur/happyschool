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
                {{ student.last_name }} {{ student.first_name }}
            </b-col>
            <b-col>
                <b-row>
                    <b-col class="text-center">
                        <b-form-checkbox
                            v-model="isAbsent"
                            name="is-absent"
                            switch
                            @change="changeAbsence()"
                            v-if="period"
                        >
                            <span :class="isSaved() ? 'font-italic' : ''">
                                {{ period.name }}
                            </span>
                            <span>
                                ({{ period.start.substr(0, 5) }}-{{ period.end.substr(0, 5) }})
                            </span>
                        </b-form-checkbox>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-list-group-item>
</template>

<script>
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
        periodId: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
        };
    },
    computed: {
        period: function () {
            return this.$store.state.periods.find(p => p.id === this.periodId);
        },
        baseAbsence: function () {
            const absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: this.periodId
            };
            const absInStore = this.$store.getters.change(absence);
            if (absInStore) return absInStore;

            return this.$store.getters.savedAbsence(absence);
        },
        isAbsent: function () {
            return this.baseAbsence ? this.baseAbsence.is_absent : undefined;
        },
    },
    methods: {
        isSaved: function () {
            return this.baseAbsence && "id" in this.baseAbsence;
        },
        changeAbsence: function () {
            const checked = !this.isAbsent;
            let absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: this.periodId,
                is_absent: checked,
            };

            if (!this.baseAbsence || checked != this.baseAbsence.is_absent) {
                if (this.baseAbsence && "id" in this.baseAbsence) absence.id = this.baseAbsence.id;
                this.$store.commit("setChange", absence);
            } else {
                this.$store.commit("removeChange", absence);
            }
        }
    },
};
</script>
