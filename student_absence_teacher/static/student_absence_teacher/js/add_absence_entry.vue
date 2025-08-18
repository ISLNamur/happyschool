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
    <BListGroupItem>
        <BRow>
            <BCol
                cols="12"
                md="4"
                :class="isBold + ' mb-2 mb-md-0'"
            >
                {{ displayStudent(student) }} 
            </BCol>
            <BCol>
                <BRow>
                    <BCol
                        cols="12"
                        md="4"
                    >
                        <BFormSelect
                            @update:model-value="selectedStatus"
                            :options="options"
                            v-model="status"
                        />
                    </BCol>
                    <BCol>
                        <BFormInput
                            v-if="status != 'presence'"
                            maxlength="200"
                            @update="updateComment"
                            v-model="comment"
                            placeholder="Ajouter une remarque si nécessaire."
                            class="mt-1 mt-md-0"
                        />
                    </BCol>
                </BRow>
            </BCol>
        </BRow>
    </BListGroupItem>
</template>

<script>
import { displayStudent } from "@s:core/js/common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

export default {
    props: {
        "student": {
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
            options: [
                {value: "presence", text: "Présent"},
                {value: "lateness", text: "Retard"},
                {value: "absence", text: "Absence"},
                {value: "excluded", text: "Exclus"},
                {value: "exempted", text: "Dispensé"},
                {value: "internship", text: "Stage"},
                // {value: "other", text: "Autre remarque"}
            ],
            status: "presence",
            comment: "",
            store: studentAbsenceTeacherStore(),
        };
    },
    computed: {
        isBold: function () {
            return this.status != "presence" ? "font-weight-bold" : "";
        }
    },
    methods: {
        displayStudent,
        selectedStatus: function (status) {
            // Check if there is some changes.
            if ("saved" in this.student) {
                if (this.student.saved.status == status && this.comment == this.student.saved.comment) {
                    this.store.commit("removeChange", this.student.matricule);
                } else {
                    const change = {
                        matricule: this.student.matricule, "status": status, old_status: this.student.saved.status,
                        comment: this.comment, id: this.student.saved.id
                    };
                    this.store.setChange(change);
                }
            } else {
                const change = {
                    matricule: this.student.matricule, "status": status,
                    comment: this.comment, is_new: true
                };
                this.store.setChange(change);
            }
            this.$emit("update");
        },
        updateComment: function () {
            if (this.student.matricule in this.store.changes) {
                let change = this.store.changes[this.student.matricule];
                change.comment = this.comment;
                this.store.setChange(change);
            } else {
                const change = {
                    matricule: this.student.matricule, "status": this.status,
                    comment: this.comment, is_new: false, id: this.student.saved.id
                };
                if ("saved" in this.student) {
                    change.old_status = this.student.saved.status;
                }
                this.store.setChange(change);
                this.$emit("update");
            }
        }
    },
    mounted: function () {
        if ("saved" in this.student) {
            this.status = this.student.saved.status;
            this.comment = this.student.saved.comment;
        } else {
            const change = {
                matricule: this.student.matricule, "status": this.status,
                comment: this.comment, is_new: true
            };
            this.store.setChange(change);
            this.$emit("update");
        }
    }
};
</script>
