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
                :class="'px-4 mt-2 current-card '"
                no-body
            >
                <b-row :class="lightDisplay ? '' : 'entry-title'">
                    <b-col>
                        <span :class="lightDisplay ? '' : 'h5'">
                            <a
                                class="clickable"
                                :href="urlToStudentInfo"
                                target="_blank"
                                rel="noopener noreferrer"
                            >{{
                                title }}</a>
                            <b-btn
                                variant="link"
                                size="sm"
                                @click="filterStudent"
                            >
                                <b-icon icon="funnel" />
                            </b-btn>
                        </span>
                    </b-col>
                    <b-col
                        sm="12"
                        md="4"
                    >
                        <div class="text-right">
                            <span v-if="store.canSetSanction">
                                <b-icon
                                    icon="question-circle"
                                    variant="primary"
                                    v-if="!canSetSanctionDone"
                                    v-b-tooltip.hover
                                    title="La date de sanction doit être antérieure ou égale à aujourd'hui."
                                />
                                <b-form-checkbox
                                    :disabled="!canSetSanctionDone"
                                    @change="setSanctionDone"
                                >
                                    Sanction faite ?
                                </b-form-checkbox>
                            </span>
                        </div>
                    </b-col>
                    <b-col
                        sm="12"
                        md="5"
                    >
                        <div class="text-right">
                            <span v-if="canEditSanction">
                                <b-btn
                                    v-if="outdated"
                                    variant="light"
                                    size="sm"
                                    class="card-link"
                                    v-b-modal="`move-sanction-date-${rowData.id}`"
                                    v-b-tooltip.hover
                                    title="Déplacer la sanction (date et/ou type de sanction)"
                                >
                                    <b-icon icon="arrow-right-square" />
                                </b-btn>
                                <b-btn
                                    v-if="rowData.date_sanction"
                                    variant="light"
                                    size="sm"
                                    class="card-link"
                                    :to="`/warn/${rowData.id}/`"
                                >
                                    <b-iconstack>
                                        <b-icon
                                            icon="file-earmark-post-fill"
                                            stacked
                                        />
                                        <b-icon
                                            v-if="rowData.notified"
                                            icon="check"
                                            color="green"
                                            scale="1.8"
                                            stacked
                                        />
                                    </b-iconstack>
                                </b-btn>
                                <b-btn
                                    variant="light"
                                    size="sm"
                                    @click="editEntry"
                                    class="card-link"
                                ><b-icon
                                    icon="pencil-square"
                                    color="green"
                                    class="align-text-bottom"
                                /></b-btn>
                                <b-btn
                                    variant="light"
                                    size="sm"
                                    @click="deleteEntry"
                                    class="card-link"
                                ><b-icon
                                    icon="trash-fill"
                                    color="red"
                                    class="align-text-bottom"
                                /></b-btn>
                            </span>
                        </div>
                    </b-col>
                </b-row>
                <b-row
                    v-if="!lightDisplay"
                    class="entry-subtitle"
                >
                    <em>{{ subtitle }}</em>
                </b-row>
                <b-row>
                    <b-col
                        :md="lightDisplay ? '6' : '2'"
                        class="category"
                    >
                        {{ category }}
                    </b-col>
                    <b-col
                        v-if="store.settings.enable_disciplinary_council && !lightDisplay"
                        md="2"
                        class="text-center"
                    >
                        {{ date_council }}
                    </b-col>
                    <b-col
                        md="2"
                        class="text-center"
                    >
                        {{ date_sanction }}
                    </b-col>
                    <b-col
                        v-if="!lightDisplay"
                        class="current-data mb-1 mr-1"
                    >
                        <span v-html="comment" />
                        <b-btn
                            class="move-up"
                            size="sm"
                            variant="light"
                            v-if="comment.length > 100"
                            @click="expand = !expand"
                        >
                            <b-icon
                                class="align-text-top"
                                :icon="expand ? 'chevron-double-up' : 'chevron-double-down'"
                            />
                        </b-btn>
                    </b-col>
                </b-row>
                <b-modal
                    :id="`move-sanction-date-${rowData.id}`"
                    size="sm"
                    centered
                    title="Date de la sanction"
                    cancel-title="Annuler"
                    @ok="$emit('update-sanction', nextSanctionData)"
                >
                    <b-form-input
                        type="date"
                        v-model="nextDate"
                    />
                    <b-select
                        :options="sanctionOptions"
                        text-field="sanction_decision"
                        value-field="id"
                        v-model="nextSanction"
                    />
                </b-modal>
            </b-card>
        </transition>
    </div>
</template>
<script>
import Moment from "moment";
import "moment/dist/locale/fr";

import axios from "axios";

import { displayStudent } from "@s:core/js/common/utilities.js";

import { askSanctionsStore } from "./stores/ask_sanctions.js";

export default {
    props: {
        rowData: {
            type: Object,
            default: () => { },
        },
        lightDisplay: {
            type: Boolean,
            default: false,
        }
    },
    data: function () {
        return {
            expand: false,
            nextDate: this.nextWeek(),
            nextSanction: null,
            sanctionOptions: [],
            store: askSanctionsStore()
        };
    },
    computed: {
        urlToStudentInfo: function () {
            /**
            * Gets called when the user clicks on the button to see student details
            */
            return `/annuaire/#/person/student/${this.rowData.student_id}/`;
        },
        nextSanctionData: function () {
            return {
                date: this.nextDate,
                sanction: this.sanctionOptions.find(s => s.id === this.nextSanction)
            };
        },
        outdated: function () {
            return Moment(this.rowData.date_sanction) < Moment();
        },
        title: function () {
            return this.displayStudent(this.rowData.student);
        },
        subtitle: function () {
            return "Demandé par " + this.rowData.demandeur + " (" + Moment(this.rowData.datetime_encodage).calendar() + ")";
        },
        category: function () {
            return this.rowData.sanction_decision.sanction_decision;
        },
        date_sanction: function () {
            return this.rowData.date_sanction ? Moment(this.rowData.date_sanction).format("DD/MM/YY") : "";
        },
        date_council: function () {
            const datetime_conseil = this.rowData.datetime_conseil ? Moment(this.rowData.datetime_conseil).format("DD/MM/YY") : null;
            if (datetime_conseil)
                return datetime_conseil;
            if (!this.rowData.date_sanction) {
                return "À définir";
            } else {
                return "Hors-conseil";
            }
        },
        comment: function () {
            const regex = /(<([^>]+)>)/ig;
            const commentLength = this.rowData.explication_commentaire.replace(regex, "").length;
            if (this.expand || commentLength < 101) {
                return this.rowData.explication_commentaire;
            } else {
                const diffLength = this.rowData.explication_commentaire.length - commentLength;
                let comment = this.rowData.explication_commentaire.substring(0, 100 + diffLength) + "…";
                if (comment.startsWith("<p>"))
                    comment += "</p>";
                return comment;
            }
        },
        canSetSanctionDone: function () {
            if (this.date_sanction === "") {
                return false;
            } else {
                // Check that sanction date is today or older.
                return Moment(this.rowData.date_sanction).isSameOrBefore(Moment(), "day");
            }
        },
        canEditSanction: function () {
            if (this.store.canSetSanction)
                return true;

            // eslint-disable-next-line no-undef
            if (this.rowData.user == user)
                return true;

            return false;
        }
    },
    methods: {
        nextWeek: function () {
            const sanctionDay = Moment(this.rowData.date_sanction).day();
            const nextDay = Moment().day() >= sanctionDay ? sanctionDay + 7 : sanctionDay;
            return Moment().day(nextDay).format("YYYY-MM-DD");
        },
        deleteEntry: function () {
            this.$emit("delete");
        },
        editEntry: function () {
            this.$emit("edit");
        },
        filterStudent: function () {
            this.$emit("filterStudent", this.rowData.student_id);
        },
        setSanctionDone: function () {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            const path = `/dossier_eleve/api/ask_sanctions/${this.rowData.id}/`;
            axios.patch(path, { sanction_faite: true }, token)
                .then(() => {
                    this.$emit("done");
                })
                .catch(function (error) {
                    alert(error);
                });
        },
        displayStudent
    },
    mounted: function () {
        this.store.getSanctions()
            .then(() => {
                this.sanctionOptions = this.store.sanctions;
                this.nextSanction = this.rowData.sanction_decision.id;
            });
    }
};
</script>

<style>
.current-card:hover {
    background-color: rgba(245, 245, 245, 0.5) !important;
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

.fade-enter,
.fade-leave-to .fade-leave-active {
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
