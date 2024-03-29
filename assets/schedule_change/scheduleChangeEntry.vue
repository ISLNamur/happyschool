<template>
    <transition
        appear
        name="fade"
    >
        <b-card
            :class="setCardClass()"
            no-body
        >
            <b-row
                v-if="!fullscreen"
                class="text-center"
            >
                <b-col
                    :cols="fullscreen ? 3 : 2"
                    class="current-data"
                >
                    <b-icon
                        v-if="rowData.category"
                        :icon="icon"
                        v-b-tooltip.hover
                        :title="category"
                    />
                    <em>{{ formatChange(rowData.change) }}</em>
                </b-col>
                <b-col
                    :cols="fullscreen ? 2 : 1"
                    class="current-data"
                >
                    {{ rowData.classes }}
                </b-col>
                <b-col
                    :cols="fullscreen ? '' : 3"
                    class="current-data"
                >
                    <s v-if="rowData.teachers_substitute.length > 0">{{ formatTeachers(rowData.teachers_replaced) }}</s>
                    <span v-else>{{ formatTeachers(rowData.teachers_replaced) }}</span>
                    <span v-if="rowData.teachers_substitute.length > 0">
                        <b-icon icon="arrow-right" />
                        {{ formatTeachers(rowData.teachers_substitute) }}
                    </span>
                </b-col>
                <b-col
                    cols="2"
                    class="current-data"
                    v-if="rowData.place.length > 0"
                >
                    {{ rowData.place }}
                </b-col>
                <b-col
                    v-if="!hide_comment"
                    class="current-data"
                >
                    {{ rowData.comment }}
                </b-col>
                <b-col
                    cols="1"
                    v-if="store.canAdd"
                >
                    <a
                        :href="`#/schedule_form/${rowData.id}/`"
                        @click="editEntry"
                        class="card-link"
                    ><b-icon
                        icon="pencil-square"
                        variant="success"
                    /></a>
                    <a
                        href="#"
                        @click="deleteEntry"
                        class=""
                    ><b-icon
                        icon="trash-fill"
                        variant="danger"
                    /></a>
                </b-col>
            </b-row>
            <table
                v-else
                width="100%"
            >
                <tr>
                    <td width="20%">
                        <b-icon
                            v-if="rowData.category"
                            :icon="icon"
                            v-b-tooltip.hover
                            :title="category"
                        />
                        <em>{{ formatChange(rowData.change) }}</em>
                    </td>
                    <td width="20%">
                        {{ rowData.classes }}
                    </td>
                    <td>
                        <s v-if="rowData.teachers_substitute.length > 0">{{ formatTeachers(rowData.teachers_replaced) }}</s>
                        <span v-else>{{ formatTeachers(rowData.teachers_replaced) }}</span>
                        <span v-if="rowData.teachers_substitute.length > 0">
                            <b-icon icon="arrow-right" />
                            {{ formatTeachers(rowData.teachers_substitute) }}
                        </span>
                    </td>
                    <td align="right">
                        {{ rowData.place }}
                    </td>
                    <td
                        align="right"
                        v-if="!hide_comment"
                    >
                        {{ rowData.comment }}
                    </td>
                </tr>
            </table>
        </b-card>
    </transition>
</template>

<script>
import Moment from "moment";
Moment.locale("fr");

import { scheduleChangeStore } from "./stores/index.js";

export default {
    props: {
        rowData : {
            type: Object,
            default: () => {}
        },
        deleting: {type: Boolean, default: false},
        fullscreen: {type: Boolean, default: false},
    },
    data: () => ({
        store: scheduleChangeStore(),
    }),
    computed: {
        icon: function () {
            if (this.rowData.category) return this.store.changeCategory.filter(c => c.id === this.rowData.category)[0].icon;
            return "";
        },
        category: function () {
            if (this.rowData.category) return this.store.changeCategory.filter(c => c.id === this.rowData.category)[0].category;
            return "";
        },
        hide_comment: function () {
            return this.store.filters.find(f => f.filterType == "activate_show_for_students") !== undefined;
        }
    },
    methods: {
        formatTeachers: function (teachers) {
            return teachers.map(t => t.display).join(", ");
        },
        formatChange: function (change) {
            for (var c = 0; c < this.store.changeType.length; c++) {
                if (this.store.changeType[c].id == change) {
                    return this.store.changeType[c].name;
                }
            }
            // return this.store.changeType.filter(c => c.id == change)[0].name;
            return "";
        },
        setCardClass: function () {
            let cat = "";
            if (this.rowData.category) cat += "category-" + this.rowData.category;
            return "px-3 current-card " + cat;
        },
        deleteEntry: function() {
            this.$emit("delete");
        },
        editEntry: function() {
            this.$emit("edit");
        },
        copyEntry: function() {
            this.$emit("copy");
        }
    }
};
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
