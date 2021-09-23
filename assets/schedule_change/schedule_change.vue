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
        <div
            class="loading"
            v-if="!loaded"
        />
        <app-menu
            v-if="!fullscreen"
            :menu-info="menu"
        />
        <b-container
            v-if="loaded"
            :fluid="fullscreen"
        >
            <b-row>
                <h2>Changement d'horaire</h2>
            </b-row>
            <b-row v-if="!fullscreen">
                <b-col
                    cols="12"
                    lg="3"
                >
                    <b-form-group>
                        <div>
                            <b-btn
                                v-if="$store.state.canAdd"
                                variant="outline-success"
                                @click="openModal('add-schedule-modal')"
                                class="w-100"
                            >
                                <icon
                                    name="plus"
                                    scale="1"
                                    color="green"
                                />
                                Ajouter un changement
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openModal('export-schedule-modal')"
                                class="w-100 mt-1"
                            >
                                <icon
                                    name="file"
                                    scale="1"
                                />
                                Sommaire
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
                <b-col>
                    <filters
                        app="schedule_change"
                        model="schedule_change"
                        ref="filters"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                    />
                </b-col>
            </b-row>
            <b-pagination
                v-if="!fullscreen"
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
                :per-page="30"
            />
            <div
                v-for="(group, index) in entriesGrouped"
                :key="index"
            >
                <hr><h5 class="day">
                    {{ calendar(group.day) }}
                </h5>
                <b-card
                    class="d-none d-md-block d-lg-block d-xl-block"
                    no-body
                >
                    <b-row
                        class="text-center"
                        v-if="!fullscreen"
                    >
                        <b-col :cols="fullscreen ? 3 : 2">
                            <strong>Changement</strong>
                        </b-col>
                        <b-col :cols="fullscreen ? 2 : 1">
                            <strong>Classes</strong>
                        </b-col>
                        <b-col :cols="fullscreen ? '' : 3">
                            <strong>Absent(s)/indisponible(s)</strong>
                        </b-col>
                    </b-row>
                    <table
                        v-else
                        width="100%"
                    >
                        <tr>
                            <td width="20%">
                                <strong>Changement</strong>
                            </td>
                            <td width="20%">
                                <strong>Classes</strong>
                            </td>
                            <td>
                                <strong>Absent(s)/indisponible(s)</strong>
                            </td>
                            <td />
                        </tr>
                    </table>
                </b-card>
                <div
                    v-for="(subGroup, idx) in group.sameDayEntries"
                    :key="idx"
                >
                    <hr class="smallhr"><strong>{{ time(subGroup) }}</strong>
                    <hr class="smallhr">
                    <b-overlay
                        v-if="$store.state.ready"
                        rounded="sm"
                    >
                        <schedule-change-entry
                            v-for="entry in subGroup.sameHourEntries"
                            :key="entry.id"
                            :row-data="entry"
                            @delete="askDelete(entry)"
                            @edit="editEntry(entry, false)"
                            @copy="editEntry(entry, true)"
                            @showInfo="showInfo(entry)"
                            :fullscreen="fullscreen"
                        />
                    </b-overlay>
                </div>
            </div>
        </b-container>
        <b-modal
            ref="deleteModal"
            cancel-title="Annuler"
            hide-header
            centered
            @ok="deleteEntry"
            @cancel="currentEntry = null"
            :no-close-on-backdrop="true"
            :no-close-on-esc="true"
        >
            Êtes-vous sûr de vouloir supprimer ce changement ?
        </b-modal>
        <add-schedule-modal
            ref="addScheduleModal"
            :entry="currentEntry"
            @update="loadEntries"
            @reset="currentEntry = null"
        />
        <export-schedule-modal ref="exportScheduleModal" />
    </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import Moment from "moment";
Moment.locale("fr");

import Filters from "../common/filters.vue";
import Menu from "../common/menu.vue";

import ScheduleChangeEntry from "./scheduleChangeEntry.vue";
import AddScheduleModal from "./addScheduleModal.vue";
import ExportScheduleModal from "./exportScheduleModal.vue";

import axios from "axios";
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";

Vue.component("icon", Icon);
export default {
    data: function () {
        return {
            menu: {},
            loaded: false,
            active: true,
            currentPage: 1,
            entriesPerPage: 30,
            showFilters: false,
            filter: "",
            ordering: "",
            currentEntry: null,
            entries: [],
            entriesGrouped: [],
            entriesCount: 0,
            inputStates: {
            },
            fullscreen: false,
        };
    },
    methods: {
        calendar: function(date) {
            return Moment(date).calendar().split(" à")[0];
        },
        time: function (entry) {
            let result = "";
            if (entry.time_start) {
                result += entry.time_start.slice(0,5);

                if (entry.time_end) {
                    result += " à ";
                } else {
                    result = "À partir de " + result;
                }
            }

            if (entry.time_end) {
                if (!entry.time_start) {
                    result += "Jusqu'à ";
                }
                result += entry.time_end.slice(0,5);
            }

            if (result === "") {
                result = "Toute la journée";
            }

            return result;
        },
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
        },
        openModal: function (modal) {
            if (modal === "add-schedule-modal") this.$refs.addScheduleModal.show();
            if (modal === "export-schedule-modal") this.$refs.exportScheduleModal.show();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters;
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gte=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lte=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.delete("/schedule_change/api/schedule_change/" + this.currentEntry.id, token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        editEntry: function(entry, copy) {
            if (copy) {
                this.currentEntry = Object.assign({}, entry);
                delete this.currentEntry.id;
            } else {
                this.currentEntry = entry;
            }
            this.openModal("add-schedule-modal");
        },
        loadEntries: function () {
            axios.get(
                `/schedule_change/api/schedule_change/?page_size=${this.entriesPerPage}&page=${this.currentPage}${this.filter}${this.ordering}`
            )
                .then(response => {
                    this.entries = response.data.results;
                    // Set the first group of changes (group by dates).
                    this.entriesCount = response.data.count;
                    if (this.entriesCount == 0) {
                        this.entriesGrouped = [];
                        this.loaded = true;
                        return;
                    }

                    this.entriesGrouped = [
                        {sameDayEntries: [
                            {sameHourEntries: [
                                this.entries[0]], time_start: this.entries[0].time_start, time_end: this.entries[0].time_end},
                        ], day: this.entries[0].date_change}
                    ];
                    if (this.entriesCount == 1) {
                        this.loaded = true;
                        return;
                    }

                    for (let e = 1; e < this.entries.length; e++) {
                        if (this.entriesGrouped[this.entriesGrouped.length - 1].day == this.entries[e].date_change) {
                            let sameDay = this.entriesGrouped[this.entriesGrouped.length - 1];
                            let entryCount = sameDay.sameDayEntries.length;
                            if (sameDay.sameDayEntries[entryCount - 1].time_start == this.entries[e].time_start
                            && sameDay.sameDayEntries[entryCount - 1].time_end == this.entries[e].time_end) {
                                sameDay.sameDayEntries[entryCount - 1].sameHourEntries.push(this.entries[e]);
                            } else {
                                sameDay.sameDayEntries.push({sameHourEntries: [
                                    this.entries[e]], time_start: this.entries[e].time_start, time_end: this.entries[e].time_end});
                            }
                        } else {
                            this.entriesGrouped.push({sameDayEntries: [
                                {sameHourEntries: [
                                    this.entries[e]
                                ], time_start: this.entries[e].time_start, time_end: this.entries[e].time_end},
                            ], day: this.entries[e].date_change});
                        }
                    }
                    this.loaded = true;
                });
        },
        checkFullscreenMode: function () {
            const fullscreen = window.location.href.includes("fullscreen");
            // const fullscreen = url.searchParams.get("fullscreen");
            if (fullscreen) {
                this.fullscreen = true;
                this.$store.commit("enableFullscreen");
                if (window.location.href.includes("show_for_students")) {
                    this.$store.commit("addFilter", {filterType: "activate_show_for_students", tag: "Activer", value: true});
                }
                this.entriesPerPage = 15;
                setInterval(() => {
                    this.currentPage = this.currentPage === 1 ? 2 : 1;
                    this.loadEntries();
                }, 15000);
            }
        },
    },
    mounted: function () {
        this.checkFullscreenMode();
        // eslint-disable-next-line no-undef
        this.menu = menu;
        this.applyFilter();
    },
    components: {
        "filters": Filters,
        "app-menu": Menu,
        "add-schedule-modal": AddScheduleModal,
        "export-schedule-modal": ExportScheduleModal,
        "schedule-change-entry": ScheduleChangeEntry,
    },
};
</script>

<style>
.loading {
    content: " ";
    display: block;
    position: absolute;
    width: 80px;
    height: 80px;
    background-image: url(/static/img/spin.svg);
    background-size: cover;
    left: 50%;
    top: 50%;
}

.day {
    text-align: center;
}

.smallhr {
    margin-top: 0.2rem;
    margin-bottom: 0.2rem;
}
</style>
