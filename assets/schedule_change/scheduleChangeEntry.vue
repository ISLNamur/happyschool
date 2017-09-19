<template>
    <transition appear name="fade">
        <b-card :title="title" :sub-title="subtitle" class="current-card">
            <b-row align-h="end">
                <a href="#" v-on:click="editEntry"
                class="card-link"><icon name="edit" scale="1" color="green"></icon></a>
                <a href="#" v-on:click="deleteEntry"
                class="card-link"><icon name="remove" scale="1" color="red"></icon></a>
            </b-row>
            <b-row class="text-center">
                <b-col md="2" class="current-data">{{ rowData.classes }}</b-col>
                <b-col md="2" class="current-data">{{ rowData.activity }}</b-col>
                <b-col md="2" class="current-data">{{ rowData.teachers }}</b-col>
                <b-col md="2" class="current-data">{{ rowData.place }}</b-col>
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
            title: function () {
                var titleStr = 'Début : ' + Moment(this.rowData.date_start).format('dddd D MMMM');
                if (this.rowData.time_start)
                    titleStr += ' à ' + Moment(this.rowData.time_start, 'HH:mm').format('H:mm');
                return  titleStr;
            },
            subtitle: function () {
                if (!this.rowData.date_end)
                    return ""

                var subTitleStr = 'Fin : ' + Moment(this.rowData.date_end).format('dddd D MMMM');
                if (this.rowData.time_end)
                    subTitleStr += ' à ' + Moment(this.rowData.time_end, 'HH:mm').format('H:mm');
                return  subTitleStr;
            }
        },
        methods: {
            deleteEntry: function() {
                this.$emit('delete');
            },
            editEntry: function() {
                this.$emit('edit');
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
