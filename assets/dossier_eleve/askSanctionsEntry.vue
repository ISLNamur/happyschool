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
        <transition appear name="fade">
            <b-card :class="'px-4 mt-2 current-card '" no-body>
                <b-row class="entry-title">
                    <b-col>
                        <h5>{{ title }}
                            <b-btn variant="link" size="sm" @click="filterStudent">
                                <icon name="filter" scale="1.2" class="align-text-middle"></icon>
                            </b-btn>
                        </h5>
                    </b-col>
                    <b-col sm="4">
                        <div class="text-right">
                            <b-form-checkbox v-if="date_sanction" @change="setSanctionDone">Sanction faite ? </b-form-checkbox>
                            <b-btn variant="light" size="sm" @click="editEntry"
                            class="card-link"><icon scale="1.3" name="edit" color="green" class="align-text-bottom"></icon></b-btn>
                            <b-btn variant="light" size="sm" @click="deleteEntry"
                            class="card-link"><icon scale="1.3" name="trash" color="red" class="align-text-bottom"></icon></b-btn>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="entry-subtitle"><em>{{ subtitle }}</em></b-row>
                <b-row class="text-center">
                    <b-col md="2" class="category">
                        {{ category }}
                    </b-col>
                    <b-col md="2">{{ date_council }}</b-col>
                    <b-col md="2">{{ date_sanction }}</b-col>
                    <b-col class="current-data mb-1 mr-1">
                        <p>
                            {{ comment }}
                            <b-btn size="sm" variant="light" v-if="comment.length > 100" @click="expand = !expand">
                                <icon
                                    color="grey"
                                    class="align-text-top"
                                    scale="1.7"
                                    :name="expand ? 'angle-double-up' : 'angle-double-down'"
                                    >
                                </icon>
                            </b-btn>
                        </p>
                    </b-col>
                </b-row>
            </b-card>
        </transition>
    </div>
</template>
<script>
    import Moment from 'moment';
    Moment.locale('fr');

    import axios from 'axios';

    export default {
        props: {
            rowData : {type: Object},
        },
        data: function () {
            return {
                expand: false,
            }
        },
        computed: {
            title: function () {
                let student = this.rowData.matricule;
                let title = student.last_name
                title += " " + student.first_name;
                title += " " + student.classe.year + student.classe.letter.toUpperCase();
                title += " (" + student.teaching.display_name + ")";
                return title;
            },
            subtitle: function () {
                return "Demandé par " + this.rowData.demandeur + " (" + Moment(this.rowData.datetime_encodage).calendar() + ")";
            },
            category: function () {
                return this.rowData.sanction_decision.sanction_decision;
            },
            date_sanction: function () {
                return this.rowData.datetime_sanction ? Moment(this.rowData.datetime_sanction).format('DD/MM/YY') : '';
            },
            date_council: function () {
                const datetime_conseil = this.rowData.datetime_conseil ? Moment(this.rowData.datetime_conseil).format('DD/MM/YY') : null
                if (datetime_conseil)
                    return datetime_conseil;
                if (!this.rowData.datetime_sanction) {
                    return 'À définir';
                } else {
                    return 'Hors-conseil'
                }
            },
            comment: function () {
                if (this.expand || this.rowData.explication_commentaire.length < 101) {
                    return this.rowData.explication_commentaire;
                } else {
                    return this.rowData.explication_commentaire.substring(0, 100) + "…";
                }
            }
        },
        methods: {
            deleteEntry: function () {
                this.$emit('delete');
            },
            editEntry: function () {
                this.$emit('edit');
            },
            filterStudent: function () {
                this.$emit('filterStudent', this.rowData.matricule_id);
            },
            setSanctionDone: function () {
                const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
                const path = '/dossier_eleve/api/ask_sanctions/' + this.rowData.id + '/';
                axios.patch(path, {sanction_faite: true}, token)
                .then(response => {
                    this.$emit('done');
                })
                .catch(function (error) {
                    alert(error);
                });

            }
        }
    }
</script>

<style>
    .current-card:hover {
        background-color: rgba(245, 245, 245, 0.5) !important;
    }

    .current-data {
        text-align: left;
        background-color: rgba(200, 200, 200, 0.1);
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
</style>
