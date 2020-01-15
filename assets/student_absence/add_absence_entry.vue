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
                    <b-col
                        v-for="(p, index) in period"
                        :key="p.pk"
                    >
                        <b-form-checkbox
                            v-model="isAbsent[index]"
                            name="is-absent"
                            switch
                            @change="changeAbsence(index)"
                        >
                            <span :class="isSaved(index) ? 'font-italic' : ''">{{ p.name }}</span>
                            <span v-if="$store.state.periods.length > 2">
                                ({{ p.start.substr(0, 5) }}-{{ p.end.substr(0, 5) }})
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
        period: {
            type: Array,
            default: () => []
        }
    },
    data: function () {
        return {
            isAbsent: [],
            baseAbsences: [],
        };
    },
    methods: {
        isSaved: function (index) {
            return this.baseAbsences[index] && "id" in this.baseAbsences[index];
        },
        changeAbsence: function (index) {
            const checked = !this.isAbsent[index];
            let absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: this.period[index].id,
                is_absent: checked,
            };

            if (!this.baseAbsences[index] || checked != this.baseAbsences[index].is_absent) {
                if (this.baseAbsences[index] && "id" in this.baseAbsences[index]) absence.id = this.baseAbsences[index].id;
                this.$store.commit("setChange", absence);
            } else {
                this.$store.commit("removeChange", absence);
            }
        }
    },
    mounted: function () {
        for (let p in this.period) {
            const period = this.period[p];
            const absence = {
                matricule: this.student.matricule,
                date_absence: this.dateAbsence,
                student: this.student,
                period: period.id
            };
            
            this.baseAbsences[p] = this.$store.getters.change(absence);
            if (!this.baseAbsences[p]) {
                this.baseAbsences[p] = this.$store.getters.savedAbsence(absence);
            }
            this.isAbsent.splice(p, 1, this.baseAbsences[p] ? this.baseAbsences[p].is_absent : undefined);
        }
    }
};
</script>
