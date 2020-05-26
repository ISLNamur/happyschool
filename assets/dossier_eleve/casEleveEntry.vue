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
            <b-card
                :class="'px-4 mt-2 current-card ' + cardClass"
                no-body
            >
                <b-row class="entry-title">
                    <b-col>
                        <h5>
                            <a
                                class="clickable"
                                @click="$emit('showInfo')"
                            >{{ title }}</a>
                            <b-btn
                                variant="link"
                                size="sm"
                                @click="filterStudent"
                            >
                                <icon
                                    name="eye"
                                    scale="1.2"
                                    class="align-text-middle"
                                />
                            </b-btn>
                        </h5>
                    </b-col>
                    <b-col sm="2">
                        <div class="text-right">
                            <b-btn
                                variant="light"
                                size="sm"
                                :to="`/edit/${rowData.id}/`"
                                class="card-link"
                            >
                                <icon
                                    scale="1.3"
                                    name="edit"
                                    color="green"
                                    class="align-text-bottom"
                                />
                            </b-btn>
                            <b-btn
                                variant="light"
                                size="sm"
                                @click="deleteEntry"
                                class="card-link"
                            >
                                <icon
                                    scale="1.3"
                                    name="trash"
                                    color="red"
                                    class="align-text-bottom"
                                />
                            </b-btn>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="entry-subtitle">
                    <em>{{ subtitle }}</em>
                    <icon
                        name="paperclip"
                        color="blue"
                        v-if="rowData.attachments.length > 0"
                    />
                </b-row>
                <b-row class="text-center">
                    <b-col
                        md="2"
                        class="category"
                    >
                        <icon
                            name="info"
                            scale="1.2"
                            v-if="isInfo"
                            color="blue"
                            class="align-text-bottom"
                        />
                        <icon
                            name="bell"
                            scale="1.2"
                            v-else
                            color="red"
                            class="align-text-bottom"
                        />
                        {{ category }}
                    </b-col>
                    <b-col class="current-data mb-1 mr-1">
                        <span v-html="comment" />
                        <b-btn
                            class="move-up"
                            size="sm"
                            variant="light"
                            v-if="comment.length > 150"
                            @click="expand = !expand"
                        >
                            <icon
                                color="grey"
                                class="align-text-top"
                                scale="1.1"
                                :name="expand ? 'angle-double-up' : 'angle-double-down'"
                            />
                        </b-btn>
                    </b-col>
                </b-row>
            </b-card>
        </transition>
    </div>
</template>
<script>
import Moment from "moment";
Moment.locale("fr");

export default {
    props: {
        rowData : {
            type: Object,
            default: () => {}
        },
    },
    data: function () {
        return {
            expand: false,
        };
    },
    computed: {
        title: function () {
            let student = this.rowData.matricule;
            let title = student.last_name;
            title += " " + student.first_name;
            title += " " + student.classe.year + student.classe.letter.toUpperCase();
            title += " (" + student.teaching.display_name + ")";
            return title;
        },
        subtitle: function () {
            let subtitle = "";
            if (this.rowData.datetime_sanction) {
                subtitle += "Sanction : " + Moment(this.rowData.datetime_sanction).format("DD/MM/YY") + ". ";
            }
            subtitle += "Demandé par " + this.rowData.demandeur + " (" + Moment(this.rowData.datetime_encodage).calendar() + ")";
            return subtitle;
        },
        category: function() {
            if (this.rowData.info)
                return this.rowData.info.info ;

            if (this.rowData.sanction_decision)
                return this.rowData.sanction_decision.sanction_decision;
            
            return "";
        },
        cardClass: function () {
            const info_sanction = this.isInfo ? "info" : "sanction_decision";
            const important = this.rowData.important ? "important " : "";
            return important + info_sanction;
        },
        isInfo: function () {
            return this.rowData.info ? true : false;
        },
        comment: function () {
            const regex = /(<([^>]+)>)/ig;
            const commentLength = this.rowData.explication_commentaire.replace(regex, "").length;
            if (this.expand || commentLength < 151) {
                return this.rowData.explication_commentaire;
            } else {
                const diffLength = this.rowData.explication_commentaire.length - commentLength;
                let comment = this.rowData.explication_commentaire.substring(0, 150 + diffLength) + "…";
                if (comment.startsWith("<p>"))
                    comment += "</p>";
                return comment;
            }
        },
    },
    methods: {
        deleteEntry: function () {
            this.$emit("delete");
        },
        filterStudent: function () {
            this.$emit("filterStudent", this.rowData.matricule_id);
        }
    }
};
</script>

<style>
    .current-card:hover {
        background-color: rgba(255, 255, 255, 1) !important;
    }

    .category {
        text-align: left;
    }

    .current-data {
        text-align: left;
        background-color: rgba(180, 180, 180, 0.25);
    }

    .entry-subtitle {
        color: grey;
    }

    .fade-enter-active {
      transition: opacity .7s
    }
    .fade-enter, .fade-leave-to .fade-leave-active {
      opacity: 0
    }

    .info {
        background-color: rgba(191, 221, 255, 0.1) !important;
    }

    .sanction_decision {
        background-color: rgba(180, 255, 123, 0.05) !important;
    }

    .important {
        background-color: rgba(255, 0, 0, 0.3) !important;
    }

    .clickable {
        text-decoration: underline !important;
        color: #0069d9 !important;
    }

    .clickable:hover {
        cursor: pointer;
        color: rgb(0, 0, 150) !important;
    }

    .move-up {
        margin-top: -25px;
    }
</style>
