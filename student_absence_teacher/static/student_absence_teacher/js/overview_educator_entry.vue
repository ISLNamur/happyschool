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
    <b-row>
        <b-col
            v-for="(a, index) in status"
            :key="index"
        >
            <b-overlay :show="updating">
                <b-checkbox
                    switch
                    v-model="status[index]"
                    @change="updateRecord(index, $event)"
                >
                    <template #default="">
                        <span>
                            {{ status[index] ? "A" : "P" }}
                        </span>
                        <b-iconstack>
                            <b-icon
                                stacked
                                icon="square"
                                variant="secondary"
                            />
                            <b-icon
                                stacked
                                v-if="absences[index].status !== null"
                                icon="check"
                                variant="success"
                            />
                        </b-iconstack>
                    </template>
                </b-checkbox>
            </b-overlay>
        </b-col>
    </b-row>
</template>

<script>
import axios from "axios";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        absences: {
            type: Array,
            default: () => new Array()
        },
    },
    data: function () {
        return {
            status: [false, false],
            updating: false,
        };
    },
    watch: {
        absences: function () {
            this.status = this.absences.map(a => a.status == "A");
        }
    },
    methods: {
        updateRecord: function (index, $event) {
            this.updating = true;
            let data = {
                status: $event ? "A" : "P",
                student_id: this.absences[index].student_id,
                period: this.absences[index].period,
                date_absence: this.absences[index].date_absence,
            };

            const isNew = !("id" in this.absences[index]);
            const url = `/student_absence_teacher/api/absence_educ/${ !isNew ? this.absences[index].id + "/" : ""}`;
            const method = isNew ? axios.post(url, [data], token) : axios.put(url, data, token);
            method.then(resp => {
                this.$emit("change", [isNew ? resp.data[0] : resp.data, index]);
                this.updating = false;
            })
                .catch(() => {
                    this.status[index] = this.absences[index].status;
                    this.updating = false;
                    this.$bvToast.toast("Une erreur est survenue lors de la mise à jour des données.", {
                        title: "Erreur",
                        variant: "danger",
                        solid: true
                    });
                });
        }
    },
    mounted: function () {
        this.status = this.absences.map(a => a.status == "A");
    }
};
</script>

<style>
    table.b-table > thead > tr > :nth-child(1) {
        width: 25%;
    }
</style>
