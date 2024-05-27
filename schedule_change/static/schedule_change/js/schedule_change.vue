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
                            <b-dropdown
                                v-if="store.canAdd"
                                split
                                split-to="/schedule_form/-1/"
                                variant="success"
                                class="w-100"
                            >
                                <template #button-content>
                                    <b-icon
                                        icon="plus"
                                        scale="1.5"
                                    />
                                    Ajouter un changement
                                </template>
                                <b-dropdown-item
                                    to="/mass_schedule_change/"
                                    variant="success"
                                >
                                    <b-icon
                                        icon="list"
                                    />
                                    Génerer des changements
                                </b-dropdown-item>
                            </b-dropdown>
                            <b-btn
                                variant="secondary"
                                @click="openModal('export-schedule-modal')"
                                class="w-100 mt-1"
                            >
                                <b-icon
                                    icon="file-earmark"
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
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                    />
                </b-col>
            </b-row>
            <b-overlay :show="loading">
                <b-pagination-nav
                    v-if="!fullscreen"
                    class="mt-1"
                    :number-of-pages="numberOfPage"
                    :link-gen="pageLink"
                    use-router
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
                            v-if="store.ready"
                            rounded="sm"
                        >
                            <schedule-change-entry
                                v-for="entry in subGroup.sameHourEntries"
                                :key="entry.id"
                                :row-data="entry"
                                @delete="askDelete(entry)"
                                :fullscreen="fullscreen"
                            />
                        </b-overlay>
                    </div>
                </div>
                <b-pagination-nav
                    v-if="!fullscreen"
                    class="mt-1"
                    :number-of-pages="numberOfPage"
                    :link-gen="pageLink"
                    use-router
                />
            </b-overlay>
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

import { scheduleChangeStore } from "./stores/index.js";

import Filters from "@s:core/js/common/filters_form.vue";

import ScheduleChangeEntry from "./scheduleChangeEntry.vue";
import ExportScheduleModal from "./exportScheduleModal.vue";

import axios from "axios";

export default {
    props: {
        currentPage: {
            type: Number,
            default: 1
        }
    },
    data: function () {
        return {
            menu: {},
            loaded: false,
            loading: false,
            active: true,
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
            store: scheduleChangeStore(),
        };
    },
    watch: {
        currentPage: function () {
            this.loadEntries();
        }
    },
    computed: {
        numberOfPage: function () {
            return Math.ceil(this.entriesCount/this.entriesPerPage);
        }
    },
    methods: {
        /**
         * Generate link to other pages.
         * 
         * @param {Number} pageNum The page number
         */
        pageLink: function (pageNum) {
            return {
                path: `/page/${pageNum}/`,
            };
        },
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
        openModal: function (modal) {
            if (modal === "export-schedule-modal") this.$refs.exportScheduleModal.show();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.store.filters;
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
        loadEntries: function () {
            this.loading = true;
            axios.get(
                `/schedule_change/api/schedule_change/?page_size=${this.entriesPerPage}&page=${this.currentPage}${this.filter}${this.ordering}`
            )
                .then(response => {
                    this.entries = response.data.results;
                    // Set the first group of changes (group by dates).
                    this.entriesCount = response.data.count;
                    this.store.updatePage(this.currentPage);
                    if (this.entriesCount == 0) {
                        this.entriesGrouped = [];
                        this.loaded = true;
                        this.loading = false;
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
                        this.loading = false;
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
                    this.loading = false;
                })
                .catch((err) => {
                    // Page not found go to first page.
                    if (err.response.status === 404) {
                        this.$router.push("/page/1/");
                    }
                });
        },
        checkFullscreenMode: function () {
            const fullscreen = window.location.href.includes("fullscreen");
            if (fullscreen) {
                this.fullscreen = true;
                this.store.enableFullscreen();
                if (window.location.href.includes("show_for_students")) {
                    this.store.addFilter({filterType: "activate_show_for_students", tag: "Activer", value: true});
                }
                this.entriesPerPage = 15;
                if (this.numberOfPage > 1) {
                    setInterval(() => {
                        const newPage = (this.currentPage + 1) % 4 === 0 ? 1 : this.currentPage + 1;
                        this.$router.push(`/page/${newPage}/`);
                    }, 12000);
                }
            }
        },
    },
    mounted: function () {
        this.store.getChangeType();
        this.store.getChangeCategory();

        this.checkFullscreenMode();
        this.applyFilter();
    },
    components: {
        "filters": Filters,
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
