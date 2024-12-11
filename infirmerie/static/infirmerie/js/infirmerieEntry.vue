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
    <div>
        <transition
            appear
            name="fade"
        >
            <BCard
                class="'px-4 mt-2"
                no-body
            >
                <BRow>
                    <BCol>
                        <h5>
                            <a
                                class="clickable"
                                :href="urlToStudentInfo"
                            >{{ title }}</a>
                            <BButton
                                variant="link"
                                size="sm"
                                @click="filterStudent"
                            >
                                <IBiFunnel />
                            </BButton>
                        </h5>
                    </BCol>
                    <BCol sm="2">
                        <div class="text-end">
                            <BButton
                                variant="light"
                                size="sm"
                                :to="'/edit/' + rowData.id + '/0'"
                                class="card-link"
                            >
                                <IBiPencilSquare color="green" />
                            </BButton>
                            <BButton
                                variant="light"
                                size="sm"
                                @click="deleteEntry"
                                class="card-link"
                            >
                                <IBiTrashFill color="red" />
                            </BButton>
                        </div>
                    </BCol>
                </BRow>
                <BRow class="text-center">
                    <BCol
                        md="2"
                        class="current-data"
                    >
                        <strong>Arrivée :</strong> {{ arrival }}
                    </BCol>
                    <BCol
                        md="2"
                        class="current-data"
                    >
                        <span v-if="rowData.datetime_sortie"><strong>Départ :</strong>{{ departure }}</span>
                        <BButton
                            v-else
                            class="mb-1"
                            size="sm"
                            :to="'/edit/' + rowData.id + '/1'"
                        >
                            Encoder départ
                        </BButton>
                    </BCol>
                    <BCol class="current-data">
                        {{ rowData.motifs_admission }}
                    </BCol>
                    <BCol class="current-data">
                        {{ rowData.remarques_sortie }}
                    </BCol>
                </BRow>
            </BCard>
        </transition>
    </div>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

export default {
    props: {
        rowData : {
            type: Object,
            default: () => {},
        },
    },
    data: function () {
        return {
        };
    },
    computed: {
        urlToStudentInfo:function(){
        /**
        * Gets called when the user clicks on the button to see student details
        */
            return `/annuaire/#/person/student/${this.rowData.matricule_id}/`;
        },
        title: function () {
            return this.rowData.matricule.display;
        },
        arrival: function () {
            return Moment(this.rowData.datetime_arrive).format("HH:mm DD/MM");
        },
        departure: function () {
            if (this.rowData.datetime_sortie) {
                return Moment(this.rowData.datetime_sortie).format("HH:mm DD/MM");
            } else {
                return "";
            }
        }
    },
    methods: {
        deleteEntry: function () {
            this.$emit("delete");
        },
        editEntry: function () {
            this.$emit("edit");
        },
        sortie: function () {
            this.$emit("sortie");
        },
        filterStudent: function () {
            this.$emit("filterStudent", this.rowData.matricule_id);
        }
    }
};
</script>

<style>
    .fade-enter-active {
      transition: opacity .7s
    }
    .fade-enter, .fade-leave-to .fade-leave-active {
      opacity: 0
    }
    .clickable {
        text-decoration: underline !important;
        color: #0069d9 !important;
    }

    .clickable:hover {
        cursor: pointer;
        color: rgb(0, 0, 150) !important;
    }

</style>
