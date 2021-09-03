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
            v-for="(a, index) in is_absent"
            :key="index"
        >
            <b-overlay :show="updating">
                <b-checkbox
                    switch
                    v-model="is_absent[index]"
                    @change="updateRecord(index, $event)"
                >
                    <template v-slot="first">
                        <b-iconstack>
                            <b-icon
                                stacked
                                icon="square"
                                variant="secondary"
                            />
                            <b-icon
                                stacked
                                v-if="is_absent[index] !== null"
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
            is_absent: [],
            updating: false,
        };
    },
    methods: {
        updateRecord: function (index, $event) {
            this.updating = true;
            let data = {
                is_absent: $event,
                student_id: this.absences[index].student_id,
                period: this.absences[index].period,
                date_absence: this.absences[index].date_absence,
            };

            const isNew = !("id" in this.absences[index]);
            const url = `/student_absence/api/student_absence/${ !isNew ? this.absences[index].id + "/" : ""}`;
            const method = isNew ? axios.post(url, [data], token) : axios.put(url, data, token);
            method.then(resp => {
                this.$emit("change", resp.data);
                this.updating = false;
            })
                .catch(() => {
                    this.is_absent[index] = this.absences[index].is_absent;
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
        this.is_absent = this.absences.map(a => a.is_absent);
    }
};
</script>

<style>
    table.b-table > thead > tr > :nth-child(1) {
        width: 25%;
    }
</style>
