<template>
    <transition appear name="fade">
        <b-card class="px-3 current-card" no-body>
            <b-row>
                <b-col sm="10"><strong>{{ time }}</strong></b-col>
                <b-col v-if="$store.state.canAdd">
                    <a href="#" v-on:click="editEntry"
                        class="card-link"><icon name="edit" scale="1" color="green"></icon></a>
                    <a href="#" v-on:click="copyEntry"
                        class="card-link"><icon name="copy" scale="1" color="blue"></icon></a>
                    <a href="#" v-on:click="deleteEntry"
                        class="card-link"><icon name="remove" scale="1" color="red"></icon></a>
                </b-col>
            </b-row>
            <b-row class="text-center">
                <b-col md="2" class="current-data"><em>{{ rowData.change }}</em></b-col>
                <b-col md="2" class="current-data">{{ rowData.classes }}</b-col>
                <b-col md="2" class="current-data">
                    <strong>Absent/indisponible</strong><br>{{ formatTeachers(rowData.teachers_replaced) }}
                </b-col>
                <b-col md="2" class="current-data" v-if="rowData.teachers_substitute.length > 0">
                    <strong>Remplacant</strong><br>{{ formatTeachers(rowData.teachers_substitute) }}
                </b-col>
                
                <b-col md="2" class="current-data" v-if="rowData.place.length > 0"><strong>Local/Lieu</strong><br>{{ rowData.place }}</b-col>
                <b-col class="current-data">{{ rowData.comment }}</b-col>
            </b-row>
        </b-card>
    </transition>
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
            time: function () {
                let result = "";
                if (this.rowData.time_start) {
                    result += this.rowData.time_start.slice(0,5);

                    if (this.rowData.time_end) {
                        result += " à ";
                    } else {
                        result = "À partir de " + result;
                    }
                }

                if (this.rowData.time_end) {
                    if (!this.rowData.time_start) {
                        result += "Jusqu'à "
                    }
                    result += this.rowData.time_end.slice(0,5);
                }

                if (result === "") {
                    result = "Toute la journée";
                }

                return result;
            }
        },
        methods: {
            formatTeachers: function (teachers) {
                return teachers.map(t => t.display).join(", ");
            },
            deleteEntry: function() {
                this.$emit('delete');
            },
            editEntry: function() {
                this.$emit('edit');
            },
            copyEntry: function() {
                this.$emit('copy');
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
</style>
