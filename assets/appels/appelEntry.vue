<template>
    <div>
        <transition appear name="fade">
            <b-card :title="title" :sub-title="subtitle" class="current-card">
                <b-row align-h="end">
                    <a href="#" v-on:click="editEntry"
                    class="card-link"><icon name="edit" scale="1" color="green"></icon></a>
                    <a href="#" v-on:click="deleteEntry"
                    class="card-link"><icon name="remove" scale="1" color="red"></icon></a>
                </b-row>
                <b-row class="text-center">
                    <b-col md="2" class="current-data">{{ rowData.objet }}</b-col>
                    <b-col md="2" class="current-data">{{ rowData.motif }}</b-col>
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
                return  this.rowData.name;
            },
            subtitle: function () {
                if (!this.rowData.is_traiter)
                    return ""

                var subTitleStr = 'Traiter le ' + Moment(this.rowData.datetime_traitement).calendar();;
                return  subTitleStr;
            },
            motif_start: function() {
                return Moment(this.rowData.datetime_motif_start).format('hh:mm DD/MM');
            },
            motif_end: function() {
                return Moment(this.rowData.datetime_motif_end).format('hh:mm DD/MM');
            },
            appel: function() {
                return Moment(this.rowData.datetime_appel).calendar();
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
