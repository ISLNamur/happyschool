<template>
    <div>
        <transition
            appear
            name="fade"
        >
            <BCard
                class="px-4 mt-2 current-card"
                no-body
            >
                <BRow>
                    <BCol>
                        <h5>
                            <a
                                v-if="rowData.is_student"
                                class="clickable"
                                @click="$emit('showInfo')"
                            >{{ title }}</a>
                            <span v-else>{{ title }}</span>
                            <BButton
                                v-if="rowData.is_student"
                                variant="link"
                                size="sm"
                                @click="filterStudent"
                            >
                                <IBiFunnel />
                            </BButton>
                        </h5>
                    </BCol>
                    <BCol
                        sm="3"
                        class="text-end"
                    >
                        <BButton
                            @click="$emit('processing')"
                            :to="'/edit/' + rowData.id + '/1'"
                            v-if="!this.rowData.is_traiter"
                            class="mr-2"
                            size="sm"
                        >
                            Traiter l'appel
                        </BButton>
                        <BLink
                            :to="'/edit/' + rowData.id + '/0'"
                            class="card-link"
                        >
                            <IBiPencilSquare color="green" />
                        </BLink>
                        <BLink
                            @click="$emit('delete')"
                            class="card-link"
                        >
                            <IBiTrashFill color="red" />
                        </BLink>
                    </BCol>
                </BRow>
                <BRow class="entry-subtitle">
                    <em>{{ subtitle }}</em>
                </BRow>
                <BRow class="text-center">
                    <BCol
                        md="2"
                        class="current-data"
                    >
                        {{ rowData.object.display }}
                    </BCol>
                    <BCol
                        md="2"
                        class="current-data"
                    >
                        {{ rowData.motive.display }}
                    </BCol>
                    <BCol
                        md="1"
                        class="current-data"
                    >
                        {{ motif_start }}
                    </BCol>
                    <BCol
                        md="1"
                        class="current-data"
                    >
                        {{ motif_end }}
                    </BCol>
                    <BCol
                        md="2"
                        class="current-data"
                    >
                        {{ appel }}
                    </BCol>
                    <BCol class="current-data">
                        {{ rowData.commentaire }}
                    </BCol>
                </BRow>
            </BCard>
        </transition>
    </div>
</template>
<script>
import { DateTime } from "luxon";

import { displayStudent } from "@s:core/js/common/utilities";

export default {
    props: {
        rowData: {
            type: Object,
            default: null },
        deleting: {
            type: Boolean,
            default: false },
    },
    computed: {
        title: function () {
            if (this.rowData.matricule) {
                let student = this.rowData.matricule;
                return displayStudent(student, this);
            }
            // This is a responsible.
            return this.rowData.name;
        },
        subtitle: function () {
            if (!this.rowData.is_traiter)
                return "";

            const subTitleStr = `Traité ${DateTime.fromISO(this.rowData.datetime_traitement).toLocaleString()}`;
            return subTitleStr;
        },
        motif_start: function () {
            if (this.rowData.datetime_motif_start) {
                // Deprecated data.
                return DateTime.fromISO(this.rowData.datetime_motif_start).toFormat("HH:mm DD/MM");
            }
            let datetimeStr = DateTime.fromISO(this.rowData.date_motif_start).toFormat("dd/MM");
            if (this.rowData.time_motif_start) {
                datetimeStr = DateTime.fromFormat(this.rowData.time_motif_start, "hh:mm:ss").toFormat("HH:mm ") + datetimeStr;
            }
            return datetimeStr;
        },
        motif_end: function () {
            if (this.rowData.datetime_motif_end) {
                // Deprecated data.
                return DateTime.fromISO(this.rowData.datetime_motif_end).toFormat("HH:mm DD/MM");
            }

            let datetimeStr = DateTime.fromISO(this.rowData.date_motif_end).toFormat("dd/MM");
            if (this.rowData.time_motif_end) {
                datetimeStr = DateTime.fromFormat(this.rowData.time_motif_end, "hh:mm:ss").toFormat("HH:mm ") + datetimeStr;
            }
            return datetimeStr;
        },
        appel: function () {
            return DateTime.fromISO(this.rowData.datetime_appel).toLocaleString();
        },
    },
    methods: {
        filterStudent: function () {
            this.$emit("filterStudent", this.rowData.matricule_id);
        },
    },
};
</script>

<style>
    .current-card {
        margin-top: 5px;
    }

    .current-data {
        margin-left: 3px;
        background-color: rgba(200, 200, 200, 0.1);
    }

    .fade-enter-active {
      transition: opacity .7s
    }
    .fade-enter, .fade-leave-to .fade-leave-active {
      opacity: 0
    }

    .entry-subtitle {
        color: grey;
    }
    .clickable {
        text-decoration: underline !important;
        color: #0069d9 !important;
    }

    .clickable:hover {
        cursor: pointer;
    }
</style>
