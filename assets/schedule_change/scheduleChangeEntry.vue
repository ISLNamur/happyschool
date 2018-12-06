<template>
    <transition appear name="fade">
        <b-card class="px-3 current-card" no-body>
            <b-row class="text-center">
                <b-col md="2" class="current-data"><em>{{ rowData.change }}</em></b-col>
                <b-col md="1" class="current-data">{{ rowData.classes }}</b-col>
                <b-col md="3" class="current-data">
                    {{ formatTeachers(rowData.teachers_replaced) }}
                    <span  v-if="rowData.teachers_substitute.length > 0">
                        <icon name="arrow-right" scale="1"></icon>
                        {{ formatTeachers(rowData.teachers_substitute) }}
                    </span>
                </b-col>
                <b-col md="2" class="current-data" v-if="rowData.place.length > 0">{{ rowData.place }}</b-col>
                <b-col class="current-data">{{ rowData.comment }}</b-col>
                <b-col md="1" v-if="$store.state.canAdd">
                    <a href="#" v-on:click="editEntry"
                        class="card-link"><icon name="edit" scale="1" color="green"></icon></a>
                    <a href="#" v-on:click="copyEntry"
                        class=""><icon name="copy" scale="1" color="blue"></icon></a>
                    <a href="#" v-on:click="deleteEntry"
                        class=""><icon name="remove" scale="1" color="red"></icon></a>
                </b-col>
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
        margin-top: .3rem;
    }

    .current-data {
        margin-left: .2rem;
        background-color: rgba(104, 104, 104, 0.1);
    }

    .fade-enter-active {
      transition: opacity .5s
    }
    .fade-enter, .fade-leave-to .fade-leave-active {
      opacity: 0
    }
</style>
