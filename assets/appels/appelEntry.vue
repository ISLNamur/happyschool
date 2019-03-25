<template>
    <div>
        <transition appear name="fade">
            <b-card class="px-4 mt-2 current-card" no-body>
                <b-row>
                    <b-col>
                        <h5>
                            <a v-if="rowData.is_student" class="clickable" @click="$emit('showInfo')">{{ title }}</a>
                            <span v-else>{{ title }}</span>
                            <b-btn v-if="rowData.is_student" variant="link" size="sm" @click="filterStudent">
                                <icon name="eye" scale="1.2" class="align-text-middle"></icon>
                            </b-btn>
                        </h5>
                    </b-col>
                    <b-col sm="3" class="text-right">
                        <b-btn @click="$emit('processing')" v-if="!this.rowData.is_traiter" class="mr-2" size="sm">Traiter l'appel</b-btn>
                        <b-link @click="$emit('edit')"
                            class="card-link"><icon name="edit" scale="1.3" color="green"></icon></b-link>
                        <b-link @click="$emit('delete')"
                            class="card-link"><icon name="trash" scale="1.3" color="red"></icon></b-link>
                    </b-col>
                </b-row>
                <b-row class="entry-subtitle">
                    <em>{{ subtitle }}</em>
                </b-row>
                <b-row class="text-center">
                    <b-col md="2" class="current-data">{{ rowData.object.display }}</b-col>
                    <b-col md="2" class="current-data">{{ rowData.motive.display }}</b-col>
                    <b-col md="1" class="current-data">{{ motif_start }}</b-col>
                    <b-col md="1" class="current-data">{{ motif_end }}</b-col>
                    <b-col md="2" class="current-data">{{ appel }}</b-col>
                    <b-col class="current-data">{{ rowData.commentaire }}</b-col>
                </b-row>
            </b-card>
        </transition>
    </div>
</template>
<script>
    import Moment from 'moment';
    Moment.locale('fr');

    export default {
        props: {
            rowData : {type: Object},
            deleting: {type: Boolean, default: false}
        },
        computed: {
            title: function () {
                if (this.rowData.matricule) {
                    let student = this.rowData.matricule;
                    let title = student.last_name
                    title += " " + student.first_name;
                    title += " " + student.classe.year + student.classe.letter.toUpperCase();
                    title += " (" + student.teaching.display_name + ")";
                    return title;
                }
                // This is a responsible.
                return this.rowData.name;
            },
            subtitle: function () {
                if (!this.rowData.is_traiter)
                    return ""

                var subTitleStr = 'Traité ' + Moment(this.rowData.datetime_traitement).calendar();;
                return  subTitleStr;
            },
            motif_start: function() {
                if (this.rowData.datetime_motif_start) {
                    // Deprecated data.
                    return Moment(this.rowData.datetime_motif_start).format('hh:mm DD/MM');
                }
                let datetime_str = Moment(this.rowData.date_motif_start).format('DD/MM')
                if (this.rowData.time_motif_start) {
                    datetime_str = Moment(this.rowData.time_motif_start, 'hh:mm:ss').format('hh:mm ') + datetime_str;
                }
                return datetime_str;
            },
            motif_end: function() {
                if (this.rowData.datetime_motif_end) {
                    // Deprecated data.
                    return Moment(this.rowData.datetime_motif_end).format('hh:mm DD/MM');
                }

                let datetime_str = Moment(this.rowData.date_motif_end).format('DD/MM')
                if (this.rowData.time_motif_end) {
                    datetime_str = Moment(this.rowData.time_motif_end, 'hh:mm:ss').format('hh:mm ') + datetime_str;
                }
                return datetime_str;
            },
            appel: function() {
                return Moment(this.rowData.datetime_appel).calendar();
            }
        },
        methods: {
            filterStudent: function () {
                this.$emit('filterStudent', this.rowData.matricule_id);
            }
        }
    }
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
