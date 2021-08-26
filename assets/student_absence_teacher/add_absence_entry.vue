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
            <b-col
                cols="3"
                :class="isBold"
            >
                {{ student.last_name }} {{ student.first_name }}
            </b-col>
            <b-col>
                <b-row>
                    <b-col cols="4">
                        <b-select
                            @change="selectedStatus"
                            :options="options"
                            v-model="status"
                        />
                    </b-col>
                    <b-col>
                        <b-form-input
                            v-if="status != 'presence'"
                            maxlength="200"
                            @update="updateComment"
                            v-model="comment"
                            placeholder="Ajouter une remarque si nécessaire."
                        />
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-list-group-item>
</template>

<script>
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
                {value: "internship", text: "Stage"},
                // {value: "other", text: "Autre remarque"}
            ],
            status: "presence",
            comment: ""
        };
    },
    computed: {
        isBold: function () {
            return this.status != "presence" ? "font-weight-bold" : "";
        }
    },
    methods: {
        selectedStatus: function (status) {
            // Check if there is some changes.
            if ("saved" in this.student) {
                if (this.student.saved.status == status && this.comment == this.student.saved.comment) {
                    this.$store.commit("removeChange", this.student.matricule);
                } else {
                    const change = {
                        matricule: this.student.matricule, "status": status, old_status: this.student.saved.status,
                        comment: this.comment, id: this.student.saved.id
                    };
                    this.$store.commit("setChange", change);
                }
            } else {
                const change = {
                    matricule: this.student.matricule, "status": status,
                    comment: this.comment, is_new: true
                };
                this.$store.commit("setChange", change);
            }
            this.$emit("update");
        },
        updateComment: function () {
            if (this.student.matricule in this.$store.state.changes) {
                let change = this.$store.state.changes[this.student.matricule];
                change.comment = this.comment;
                this.$store.commit("setChange", change);
            } else {
                const change = {
                    matricule: this.student.matricule, "status": this.status,
                    comment: this.comment, is_new: false, id: this.student.saved.id
                };
                if ("saved" in this.student) {
                    change.old_status = this.student.saved.status;
                }
                this.$store.commit("setChange", change);
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
            this.$store.commit("setChange", change);
            this.$emit("update");
        }
    }
};
</script>
