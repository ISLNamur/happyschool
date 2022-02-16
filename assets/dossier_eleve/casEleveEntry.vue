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
                                <b-icon icon="funnel" />
                            </b-btn>
                        </h5>
                    </b-col>
                    <b-col
                        v-if="$store.state.canAddCas"
                        sm="2"
                    >
                        <div class="text-right">
                            <b-btn
                                variant="light"
                                size="sm"
                                :to="`/edit/${rowData.id}/`"
                                class="card-link"
                            >
                                <b-icon
                                    icon="pencil-square"
                                    variant="success"
                                />
                            </b-btn>
                            <b-btn
                                variant="light"
                                size="sm"
                                @click="deleteEntry"
                                class="card-link"
                            >
                                <b-icon
                                    icon="trash-fill"
                                    variant="danger"
                                />
                            </b-btn>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="entry-subtitle">
                    <em>{{ subtitle }}</em>
                    <b-dropdown
                        size="sm"
                        variant="link"
                        toggle-class="text-decoration-none"
                        no-caret
                    >
                        <template #button-content>
                            <b-icon
                                icon="paperclip"
                                variant="primary"
                                v-if="rowData.attachments.length > 0"
                            />
                        </template>
                        <b-dropdown-item
                            v-for="a in attachments"
                            :key="a.id"
                            :href="`/dossier_eleve/attachment/${a.id}/`"
                        >
                            {{ a.filename }}
                        </b-dropdown-item>
                    </b-dropdown>
                </b-row>
                <b-row class="text-center">
                    <b-col
                        md="2"
                        class="category"
                    >
                        <b-icon
                            icon="info-circle-fill"
                            v-if="isInfo"
                            variant="primary"
                        />
                        <b-icon
                            icon="bell-fill"
                            v-else
                            variant="danger"
                        />
                        {{ category }}
                    </b-col>
                    <b-col class="current-data mb-1 mr-1">
                        <span v-html="comment" />
                        <b-btn
                            class="move-up"
                            size="sm"
                            variant="outline-primary"
                            v-if="comment.length > 150"
                            @click="expand = !expand"
                        >
                            <b-icon
                                :icon="expand ? 'chevron-double-up' : 'chevron-double-down'"
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

import axios from "axios";

import {displayStudent} from "../common/utilities.js";

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
            attachments: [],
        };
    },
    computed: {
        new: function () {
            // eslint-disable-next-line no-undef
            return Moment(this.rowData.datetime_modified) > Moment(dossierEleveLastAccess);
        },
        title: function () {
            return this.displayStudent(this.rowData.student);
        },
        subtitle: function () {
            let subtitle = "";
            if (this.rowData.date_sanction) {
                subtitle += "Sanction : " + Moment(this.rowData.date_sanction).format("DD/MM/YY") + ". ";
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
            const important = this.rowData.important ? "important" : "";
            const newCas = this.new ? "new" : "";
            return `${important} ${info_sanction} ${newCas}`;
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
            this.$emit("filterStudent", this.rowData.student_id);
        },
        displayStudent,
    },
    mounted: function () {
        const prom = this.rowData.attachments.map(a => {
            return axios.get(`/dossier_eleve/upload_file/${a}/`);
        });

        Promise.all(prom)
            .then(resp => {
                this.attachments = resp.map(r => r.data);
                this.attachments.forEach(a => {
                    const path = a.attachment.split("/");
                    a.filename = path[path.length - 1].substring(5, 60);
                });
            });

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

    .new {
        box-shadow: 0px 0px 5px #0069d9;
        border-color: #0069d9;
    }
</style>
