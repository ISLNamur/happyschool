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
        <BContainer
            v-if="loaded"
            :fluid="fullscreen"
        >
            <BRow>
                <h2>Changement d'horaire</h2>
            </BRow>
            <BRow v-if="!fullscreen">
                <BCol
                    cols="12"
                    lg="3"
                >
                    <BFormGroup>
                        <div>
                            <BDropdown
                                v-if="store.canAdd"
                                split
                                split-to="/schedule_form/-1/"
                                variant="success"
                                class="w-100"
                            >
                                <template #button-content>
                                    <IBiPlus
                                        scale="1.5"
                                    />
                                    Ajouter un changement
                                </template>
                                <BDropdownItem
                                    to="/mass_schedule_change/"
                                    variant="success"
                                >
                                    <IBiList />
                                    Génerer des changements
                                </BDropdownItem>
                            </BDropdown>
                            <BButton
                                variant="secondary"
                                @click="openModal('export-schedule-modal')"
                                class="w-100 mt-1"
                            >
                                <IBiFileEarmark scale="1" />
                                Sommaire
                            </BButton>
                        </div>
                    </BFormGroup>
                </BCol>
                <BCol>
                    <filters
                        app="schedule_change"
                        model="schedule_change"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggle-search="showFilters = !showFilters"
                    />
                </BCol>
            </BRow>
            <BOverlay :show="loading">
                <div
                    v-for="(group, index) in entriesGrouped"
                    :key="index"
                >
                    <hr><h5 class="day">
                        {{ calendar(group.day) }}
                    </h5>
                    <BCard
                        class="d-none d-md-block d-lg-block d-xl-block"
                        no-body
                    >
                        <BRow
                            class="text-center"
                            v-if="!fullscreen"
                        >
                            <BCol :cols="fullscreen ? 3 : 2">
                                <strong>Changement</strong>
                            </BCol>
                            <BCol :cols="fullscreen ? 2 : 1">
                                <strong>Classes</strong>
                            </BCol>
                            <BCol :cols="fullscreen ? '' : 3">
                                <strong>Absent(s)/indisponible(s)</strong>
                            </BCol>
                        </BRow>
                        <table
                            v-else
                            width="100%"
                        >
                            <tbody>
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
                            </tbody>
                        </table>
                    </BCard>
                    <div
                        v-for="(subGroup, idx) in group.sameDayEntries"
                        :key="idx"
                    >
                        <hr class="smallhr"><strong>{{ time(subGroup) }}</strong>
                        <hr class="smallhr">
                        <BOverlay
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
                        </BOverlay>
                    </div>
                </div>
                <BPagination
                    v-if="!fullscreen"
                    :value="currentPage"
                    :total-rows="entriesCount"
                    :per-page="entriesPerPage"
                    @update:model-value="changePage"
                    class="mt-1"
                />
            </BOverlay>
        </BContainer>
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
import Moment from "moment";
import "moment/dist/locale/fr";
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
            default: 1,
        },
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
        },
    },
    methods: {
        /**
         * Move to another page.
         *
         * @param {Number} pageNum The page number
         */
        changePage: function (pageNum) {
            this.$router.push(`/page/${pageNum}/`);
            scroll(0, 0);
        },
        calendar: function (date) {
            return Moment(date).calendar().split(" à")[0];
        },
        time: function (entry) {
            let result = "";
            if (entry.time_start) {
                result += entry.time_start.slice(0, 5);

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
                result += entry.time_end.slice(0, 5);
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
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            axios.delete("/schedule_change/api/schedule_change/" + this.currentEntry.id, token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        loadEntries: function () {
            this.loading = true;
            axios.get(
                `/schedule_change/api/schedule_change/?page_size=${this.entriesPerPage}&page=${this.currentPage}${this.filter}${this.ordering}`,
            )
                .then((response) => {
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
                        { sameDayEntries: [
                            { sameHourEntries: [
                                this.entries[0]], time_start: this.entries[0].time_start, time_end: this.entries[0].time_end },
                        ], day: this.entries[0].date_change },
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
                                sameDay.sameDayEntries.push({ sameHourEntries: [
                                    this.entries[e]], time_start: this.entries[e].time_start, time_end: this.entries[e].time_end });
                            }
                        } else {
                            this.entriesGrouped.push({ sameDayEntries: [
                                { sameHourEntries: [
                                    this.entries[e],
                                ], time_start: this.entries[e].time_start, time_end: this.entries[e].time_end },
                            ], day: this.entries[e].date_change });
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
                    this.store.addFilter({ filterType: "activate_show_for_students", tag: "Activer", value: true });
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
