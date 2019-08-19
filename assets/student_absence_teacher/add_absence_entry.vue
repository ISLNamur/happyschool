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
        <b-col cols="3" :class="isBold">{{ student.last_name }} {{ student.first_name }}</b-col>
        <b-col>
            <b-row>
                <b-col cols="4">
                    <b-select @change="selectedChoice" :options="options" v-model="choice"></b-select>
                </b-col>
                <b-col>
                    <b-form-input v-if="choice != 'presence'" maxlength="200" @update="updateComment"
                        v-model="comment" placeholder="Ajouter une remarque si nécessaire.">
                    </b-form-input>
                </b-col>
            </b-row>
        </b-col>
        </b-row>
    </b-list-group-item>
</template>

<script>
export default {
    props: ['student',],
    data: function () {
        return {
            options: [
                {value: "presence", text: "Présent"},
                {value: "lateness", text: "Retard"},
                {value: "absence", text: "Absence"},
                // {value: "other", text: "Autre remarque"}
            ],
            choice: "presence",
            comment: ""
        }
    },
    computed: {
        isBold: function () {
            return this.choice != "presence" ? "font-weight-bold" : "";
        }
    },
    methods: {
        selectedChoice: function (choice) {
            // Check if there is some changes.
            if ('saved' in this.student) {
                if (this.student.saved.choice == choice && this.comment == this.student.saved.comment) {
                    this.$store.commit('removeChange', this.student.matricule);
                } else {
                    const change = {
                        matricule: this.student.matricule, 'choice': choice, old_choice: this.student.saved.choice,
                        comment: this.comment, is_new: this.student.saved.choice != choice, id: this.student.saved.id
                    };
                    this.$store.commit('setChange', change);
                }
            } else {
                if (choice == 'presence') {
                    this.$store.commit('removeChange', this.student.matricule);
                    this.comment = "";
                } else {
                    const change = {
                        matricule: this.student.matricule, 'choice': choice,
                        comment: this.comment, is_new: true
                    };
                    this.$store.commit('setChange', change);
                }
            }
            this.$emit('update');
        },
        updateComment: function (value) {
            if (this.student.matricule in this.$store.state.changes) {
                let change = this.$store.state.changes[this.student.matricule]
                change.comment = this.comment;
                this.$store.commit('setChange', change);
            } else {
                const change = {
                    matricule: this.student.matricule, 'choice': this.choice,
                    comment: this.comment, is_new: false, id: this.student.saved.id
                };
                if ('saved' in this.student) {
                    change.old_choice = this.student.saved.choice;
                }
                this.$store.commit('setChange', change);
                this.$emit('update');
            }
        }
    },
    mounted: function () {
        if ('saved' in this.student) {
            this.choice = this.student.saved.choice;
            this.comment = this.student.saved.comment;
        }
    }
}
</script>