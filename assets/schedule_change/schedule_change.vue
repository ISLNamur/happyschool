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
        <div class="loading" v-if="!loaded"></div>
        <app-menu :menu-info="menu"></app-menu>
        <b-container v-if="loaded">
            <b-row>
                <h2>Changement d'horaire</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-button v-if="$store.state.canAdd" variant="outline-success" @click="openModal(false)">
                                <icon name="plus" scale="1" color="green"></icon>
                                Ajouter un changement
                            </b-button>
                            <b-button variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-button>
                            <b-button :pressed.sync="active" variant="primary">
                                <span v-if="active">Afficher tous les changements</span>
                                <span v-else>Afficher les changements en cours</span>
                            </b-button>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                        <b-collapse id="filters" v-model=showFilters>
                            <b-card>
                                <filters app="schedule_change" model="schedule_change" ref="filters" @update="applyFilter"></filters>
                            </b-card>
                        </b-collapse>
                    </b-col>
            </b-row>
            <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
            </b-pagination>
            <div v-for="(group, index) in entriesGrouped"
                v-bind:key="index"
                >
                <hr><h5 class="day">{{ calendar(group.day) }}</h5> <hr>
                <schedule-change-entry
                    v-for="entry in group.entries"
                    v-bind:key="entry.id"
                    v-bind:row-data="entry"
                    @delete="askDelete(entry)"
                    @edit="editEntry(entry, false)"
                    @copy="editEntry(entry, true)"
                    @showInfo="showInfo(entry)"
                    >
                </schedule-change-entry>
            </div>
        </b-container>
        <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered
            @ok="deleteEntry" @cancel="currentEntry = null"
            :no-close-on-backdrop="true" :no-close-on-esc="true">
            Êtes-vous sûr de vouloir supprimer ce changement ?
        </b-modal>
        <add-schedule-modal ref="addScheduleModal" :entry="currentEntry"
            @update="loadEntries" @reset="currentEntry = null">
        </add-schedule-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

import Moment from 'moment';
Moment.locale('fr');

import Filters from '../common/filters.vue';
import Menu from '../common/menu.vue';

import ScheduleChangeEntry from './scheduleChangeEntry.vue';
import AddScheduleModal from './addScheduleModal.vue';

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'

Vue.component('icon', Icon);
Vue.use(BootstrapVue);
export default {
    data: function () {
        return {
            menu: {},
            loaded: false,
            active: true,
            currentPage: 1,
            showFilters: false,
            filter: "",
            ordering: "",
            currentEntry: null,
            entries: [],
            entriesGrouped: [],
            entriesCount: 0,
            inputStates: {
            },
        }
    },
    watch: {
        active: function (isActive) {
            if (isActive) {
                this.$store.commit('addFilter',
                    {filterType: 'activate_ongoing', tag: "Activer", value: true}
                );
            } else {
                this.$store.commit('removeFilter', 'activate_ongoing');
            }
            this.applyFilter();
        }
    },
    methods: {
        calendar: function(date) {
            return Moment(date).calendar().split(" à")[0];
        },
        changePage: function (page) {
            this.currentPage = page;
        },
        openModal: function () {
            this.$refs.addScheduleModal.show();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters
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
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/schedule_change/api/schedule_change/' + this.currentEntry.id, token)
            .then(response => {
                this.loadEntries();
            });

            this.currentEntry = null;
        },
        editEntry: function(entry, copy) {
            console.log(entry);
            console.log(copy);
            if (copy) {
                this.currentEntry = Object.assign({}, entry);
                delete this.currentEntry.id;
            } else {
                this.currentEntry = entry;
            }
            this.openModal();
        },
        loadEntries: function () {
            axios.get('/schedule_change/api/schedule_change/?page=' + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.entries = response.data.results;
                // Set the first group of changes (group by dates).
                this.entriesCount = response.data.count;
                if (this.entriesCount == 0) {
                    this.loaded = true;
                    return;
                }

                this.entriesGrouped = [{entries: [this.entries[0]], day: this.entries[0].date_change}];
                if (this.entriesCount == 1) {
                    this.loaded = true;
                    return;
                }

                for (let e = 1; e < this.entries.length; e++) {
                    if (this.entriesGrouped[this.entriesGrouped.length - 1].day == this.entries[e].date_change) {
                        this.entriesGrouped[this.entriesGrouped.length - 1].entries.push(this.entries[e]);
                    } else {
                        this.entriesGrouped.push({entries: [this.entries[e]], day: this.entries[e].date_change});
                    }
                }
                
                this.loaded = true;
            });
        },
    },
    mounted: function () {
        this.menu = menu;
        this.applyFilter();
    },
    components: {
        'filters': Filters,
        'app-menu': Menu,
        'add-schedule-modal': AddScheduleModal,
        'schedule-change-entry': ScheduleChangeEntry,
    },
}
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
</style>
