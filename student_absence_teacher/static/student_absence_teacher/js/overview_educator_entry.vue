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
    <BRow>
        <BCol
            v-for="(a, index) in status"
            :key="index"
        >
            <BOverlay :show="updating">
                <BForm class="d-flex justify-content-center flex-wrap">
                    <BFormCheckbox
                        switch
                        v-model="status[index]"
                        @update:model-value="updateRecord(index, $event)"
                    />
                    <span class="position-relative">
                        {{ status[index] ? "A" : "P" }}
                        <BBadge
                            v-if="absences[index].status !== null"
                            text-variant="success"
                            bg-variant="transparent"
                            placement="bottom-end"
                        >
                            <IBiCheck v-if="absences[index] !== null" />
                        </BBadge>
                    </span>
                </BForm>
            </BOverlay>
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";
import { useToastController } from "bootstrap-vue-next";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        absences: {
            type: Array,
            default: () => new Array()
        },
    },
    data: function () {
        return {
            status: [],
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
                    this.show({
                        body: "Une erreur est survenue lors de la mise à jour des données.",
                        title: "Erreur",
                        variant: "danger",
                        solid: true
                    });
                });
        }
    },
    mounted: function () {
        this.status = this.absences.map(a => a.status == "A");
    },
};
</script>

<style>
    table.BTable > thead > tr > :nth-child(1) {
        width: 25%;
    }
</style>
