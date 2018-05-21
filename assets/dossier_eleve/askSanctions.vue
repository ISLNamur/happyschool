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
        <b-container v-if="loaded">
            <b-row>
                <h2>Demande de sanctions</h2>
            </b-row>
            <b-row class="mb-2">
                <b-tabs>
                    <template slot="tabs">
                        <b-nav-item href="/dossier_eleve/">Dossier des élèves</b-nav-item>
                    </template>
                </b-tabs>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-btn variant="primary" @click="openDynamicModal('ask-modal')">
                                <icon name="plus" scale="1" class="align-middle"></icon>
                                Nouvelle demande
                            </b-btn>
                            <b-btn variant="secondary" @click="openDynamicModal('ask-export-modal')">
                                <icon name="file" scale="1" ></icon>
                                Export
                            </b-btn>
                            <b-btn variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-collapse id="filters" v-model=showFilters>
                        <b-card>
                            <filters app="dossier_eleve" model="ask_sanctions" ref="filters" @update="applyFilter"></filters>
                        </b-card>
                    </b-collapse>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-list-group>
                        <b-list-group-item>Demandes de sanction en attentes : <b-badge>{{ entriesCount }}</b-badge></b-list-group-item>
                        <b-list-group-item button @click="addFilter('activate_not_done', 'Activer', true)">
                            Non faites : <b-badge variant="danger">{{ entriesNotDone }}</b-badge>
                        </b-list-group-item>
                        <b-list-group-item button @click="addFilter('activate_waiting', 'Activer', true)">
                            En attentes de validations : <b-badge variant="warning">{{ entriesWaiting }}</b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
            <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
            </b-pagination>
            <b-card no-body class="current-card d-none d-md-block d-lg-block d-xl-block">
                <b-row class="text-center">
                    <b-col cols="2"><strong>Type de sanctions</strong></b-col>
                    <b-col cols="2"><strong>Conseil de discipline</strong></b-col>
                    <b-col cols="2"><strong>Date de la sanction</strong></b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <ask-sanctions-entry
                v-for="(entry, index) in entries"
                v-bind:key="entry.id"
                v-bind:row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @filterStudent="filterStudent($event)"
                @done="loadEntries"
                >
            </ask-sanctions-entry>
            <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered
                @ok="deleteEntry" @cancel="currentEntry = null">
                Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
            </b-modal>
            <component
                v-bind:is="currentModal" ref="dynamicModal"
                @update="loadEntries" @reset="currentEntry = null"
                :entry="currentEntry">
            </component>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import AskSanctionsEntry from './askSanctionsEntry.vue'
import AskModal from './askModal.vue'
import AskExportModal from './askExportModal.vue'
import Filters from '../common/filters.vue'

export default {
    data: function () {
        return {
            showFilters: false,
            filter: '',
            ordering: '&ordering=datetime_sanction',
            entriesCount: 0,
            currentPage: 1,
            entries: [],
            entriesNotDone: 0,
            entriesWaiting: 0,
            currentEntry: null,
            currentModal: 'ask-modal',
            loaded: false,
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            return;
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            this.$refs.dynamicModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit('addFilter',
                {filterType: 'matricule_id', tag: matricule, value: matricule}
            );
            this.applyFilter()
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.$store.state.filters
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
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
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
            this.openDynamicModal('ask-modal');
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/dossier_eleve/api/ask_sanctions/' + this.currentEntry.id + '/', token)
            .then(response => {
                this.loadEntries();
            });

            this.currentEntry = null;
        },
        addFilter: function(filterType, tag, value) {
            this.showFilters = true;
            this.$store.commit('addFilter',
                {'filterType': filterType, 'tag': tag, 'value': value}
            );
            this.applyFilter()
        },
        loadEntries: function () {
            axios.get('/dossier_eleve/api/ask_sanctions/?page=' + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.entriesCount = response.data.count;
                this.entries = response.data.results;
                this.loaded = true;

                // Get other counts.
                this.getEntriesNotDone();
                this.getEntriesWaiting();
            });
        },
        getEntriesNotDone: function () {
            axios.get('/dossier_eleve/api/ask_sanctions/?page=' + this.currentPage + this.filter + this.ordering + '&activate_not_done=true')
            .then(response => {
                this.entriesNotDone = response.data.count;
            })
        },
        getEntriesWaiting: function () {
            axios.get('/dossier_eleve/api/ask_sanctions/?page=' + this.currentPage + this.filter + this.ordering + '&activate_waiting=true')
            .then(response => {
                this.entriesWaiting = response.data.count;
            })
        }
    },
    mounted: function () {
        this.applyFilter();
        this.loadEntries();
    },
    components: {
        'filters': Filters,
        'ask-sanctions-entry': AskSanctionsEntry,
        'ask-modal': AskModal,
        'ask-export-modal': AskExportModal,
    }
}
</script>

<style>
</style>
