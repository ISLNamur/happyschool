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
import Moment from "moment";
import "moment/dist/locale/fr";
import { displayStudent } from "@s:core/js/common/utilities";
Moment.locale("fr");

export default {
    props: {
        rowData : {
            type: Object,
            default:null}
        ,
        deleting: {
            type: Boolean, 
            default: false}
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

            var subTitleStr = "Traité " + Moment(this.rowData.datetime_traitement).calendar();
            return  subTitleStr;
        },
        motif_start: function() {
            if (this.rowData.datetime_motif_start) {
                // Deprecated data.
                return Moment(this.rowData.datetime_motif_start).format("hh:mm DD/MM");
            }
            let datetime_str = Moment(this.rowData.date_motif_start).format("DD/MM");
            if (this.rowData.time_motif_start) {
                datetime_str = Moment(this.rowData.time_motif_start, "hh:mm:ss").format("hh:mm ") + datetime_str;
            }
            return datetime_str;
        },
        motif_end: function() {
            if (this.rowData.datetime_motif_end) {
                // Deprecated data.
                return Moment(this.rowData.datetime_motif_end).format("hh:mm DD/MM");
            }

            let datetime_str = Moment(this.rowData.date_motif_end).format("DD/MM");
            if (this.rowData.time_motif_end) {
                datetime_str = Moment(this.rowData.time_motif_end, "hh:mm:ss").format("hh:mm ") + datetime_str;
            }
            return datetime_str;
        },
        appel: function() {
            return Moment(this.rowData.datetime_appel).calendar();
        }
    },
    methods: {
        filterStudent: function () {
            this.$emit("filterStudent", this.rowData.matricule_id);
        }
    }
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
