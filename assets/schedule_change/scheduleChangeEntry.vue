<template>
    <transition appear name="fade">
        <b-card :class="setCardClass()" no-body>
            <b-row class="text-center">
                <b-col md="2" class="current-data">
                    <icon v-if="rowData.category" :name="icon" v-b-tooltip.hover :title="category" class="align-text-bottom"></icon>
                    <em>{{ formatChange(rowData.change) }}</em>
                </b-col>
                <b-col :md="fullscreen ? 2 : 1" class="current-data">{{ rowData.classes }}</b-col>
                <b-col :md="fullscreen ? '' : 3" class="current-data">
                    <s v-if="rowData.teachers_substitute.length > 0">{{ formatTeachers(rowData.teachers_replaced) }}</s>
                    <span v-else>{{ formatTeachers(rowData.teachers_replaced) }}</span>
                    <span v-if="rowData.teachers_substitute.length > 0">
                        <icon name="arrow-right"></icon>
                        {{ formatTeachers(rowData.teachers_substitute) }}
                    </span>
                </b-col>
                <b-col md="2" class="current-data" v-if="rowData.place.length > 0">{{ rowData.place }}</b-col>
                <b-col v-if="!fullscreen" class="current-data">{{ rowData.comment }}</b-col>
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
            deleting: {type: Boolean, default: false},
            fullscreen: {type: Boolean, default: false},
        },
        computed: {
            icon: function () {
                if (this.rowData.category) return this.$store.state.changeCategory.filter(c => c.id == this.rowData.category)[0].icon;
                return "";
            },
            category: function () {
                if (this.rowData.category) return this.$store.state.changeCategory.filter(c => c.id == this.rowData.category)[0].category;
                return "";
            }
        },
        methods: {
            formatTeachers: function (teachers) {
                return teachers.map(t => t.display).join(", ");
            },
            formatChange: function (change) {
                return this.$store.state.changeType.filter(c => c.id == change)[0].name;
            },
            setCardClass: function () {
                let cat = "";
                if (this.rowData.category) cat += "category-" + this.rowData.category;
                return "px-3 current-card " + cat;
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
