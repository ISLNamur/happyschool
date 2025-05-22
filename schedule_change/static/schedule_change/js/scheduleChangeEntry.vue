<template>
    <transition
        appear
        name="fade"
    >
        <BCard
            :class="setCardClass()"
            no-body
        >
            <BRow
                v-if="!fullscreen"
                class="text-center"
            >
                <BCol
                    :cols="fullscreen ? 3 : 2"
                    class="current-data"
                >
                    <component
                        :is="icon"
                    />
                    <em class="change">{{ formatChange(rowData.change) }}</em>
                </BCol>
                <BCol
                    :cols="fullscreen ? 2 : 1"
                    class="current-data"
                >
                    {{ rowData.classes }}
                </BCol>
                <BCol
                    :cols="fullscreen ? '' : 3"
                    class="current-data"
                >
                    <s v-if="rowData.teachers_substitute.length > 0">{{ formatTeachers(rowData.teachers_replaced) }}</s>
                    <span v-else>{{ formatTeachers(rowData.teachers_replaced) }}</span>
                    <span v-if="rowData.teachers_substitute.length > 0">
                        <IBiArrowRight />
                        {{ formatTeachers(rowData.teachers_substitute) }}
                    </span>
                </BCol>
                <BCol
                    cols="2"
                    class="current-data"
                    v-if="rowData.place.length > 0"
                >
                    {{ rowData.place }}
                </BCol>
                <BCol
                    v-if="!hide_comment"
                    class="current-data"
                >
                    {{ rowData.comment }}
                </BCol>
                <BCol
                    cols="1"
                    v-if="store.canAdd"
                >
                    <BButton
                        :to="`/schedule_form/${rowData.id}/`"
                        @click="editEntry"
                        class="card-link"
                        size="sm"
                        variant="outline-light"
                    >
                        <IBiPencilSquare
                            color="green"
                        />
                    </BButton>
                    <BButton
                        size="sm"
                        variant="outline-light"
                        @click="deleteEntry"
                    >
                        <IBiTrashFill
                            color="red"
                        />
                    </BButton>
                </BCol>
            </BRow>
            <table
                v-else
                width="100%"
            >
                <tr>
                    <td width="20%">
                        <component
                            v-if="rowData.category"
                            :is="icon"
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
                            <IBiArrowRight />
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
        </BCard>
    </transition>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import IBiPlus from "~icons/bi/plus";
import IBiBoxArrowRight from "~icons/bi/box-arrow-right";
import IBiArrowLeftRight from "~icons/bi/arrow-left-right";
import IBiRecycle from "~icons/bi/recycle";

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
        test: "plus",
        store: scheduleChangeStore(),
    }),
    computed: {
        icon: function () {
            if (this.rowData.category) {
                const categoryObj = this.store.changeCategory.find(c => c.id === this.rowData.category);
                if (categoryObj.icon) {
                    return categoryObj.icon;
                    // return `IBi${categoryObj.icon[0].toUpperCase() + categoryObj.icon.slice(1)}`;
                } else {
                    return "";
                }
            }
        
            return "";
        },
        category: function () {
            const categoryObj = this.store.changeCategory.find(c => c.id === this.rowData.category);
            if (categoryObj) {
                return categoryObj.category;
            }

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
    },
    components: {
        "place-move": IBiBoxArrowRight,
        "plus": IBiPlus,
        "exchange": IBiArrowLeftRight,
        "recycle": IBiRecycle,
    },
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

    .change {
        margin-left: 0.5em;
    }
</style>
