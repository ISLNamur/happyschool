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
        <b-container v-if="loaded">
            <b-row>
                <h2>Demandes de sanction</h2>
            </b-row>
            <b-row>
                <b-tabs>
                    <template #tabs>
                        <b-nav-item href="/dossier_eleve/">
                            Dossier des élèves
                        </b-nav-item>
                        <b-nav-item
                            active
                            href="/dossier_eleve/ask_sanctions"
                        >
                            Demandes de sanction
                        </b-nav-item>
                    </template>
                </b-tabs>
            </b-row>
            <b-row>
                <b-col
                    cols="12"
                    lg="3"
                >
                    <b-form-group>
                        <div>
                            <b-btn
                                v-if="$store.state.canAskSanction"
                                variant="primary"
                                @click="openDynamicModal('ask-modal')"
                                class="w-100 mb-1"
                            >
                                <b-icon
                                    icon="plus"
                                    scale="1.5"
                                />
                                Nouvelle demande
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openDynamicModal('ask-export-modal')"
                                class="w-100"
                            >
                                <b-icon
                                    icon="file-earmark"
                                />
                                Export
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openMassActions"
                                class="w-100 mt-1"
                            >
                                <b-icon
                                    icon="list-check"
                                />
                                Actions de masse
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
                <b-col
                    cols="12"
                    lg="9"
                >
                    <filters
                        app="dossier_eleve"
                        model="ask_sanctions"
                        ref="filters"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                        class="mb-1"
                    />
                </b-col>
            </b-row>
            <b-row v-if="$store.state.canSetSanction">
                <b-col>
                    <b-list-group>
                        <b-list-group-item>Demandes de sanction en attente : <b-badge>{{ entriesCount }}</b-badge></b-list-group-item>
                        <b-list-group-item
                            button
                            @click="addFilter('activate_not_done', 'Activer', true)"
                        >
                            Sanctions non faites <strong>à traiter</strong> : <b-badge variant="danger">
                                {{ entriesNotDone }}
                            </b-badge>
                        </b-list-group-item>
                        <b-list-group-item
                            button
                            v-if="entriesWaiting > 0"
                            @click="addFilter('activate_waiting', 'Activer', true)"
                        >
                            En attentes de validations : <b-badge variant="warning">
                                {{ entriesWaiting }}
                            </b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-pagination
                        class="mt-1"
                        :total-rows="entriesCount"
                        v-model="currentPage"
                        @change="changePage"
                        :per-page="entriesPerPage"
                    />
                </b-col>
                <b-col>
                    <b-form-group
                        label="Sanctions par page"
                        label-cols
                        label-align-sm="right"
                    >
                        <b-select
                            class="mt-1"
                            v-model="entriesPerPage"
                            @input="loadEntries"
                            size="sm"
                        >
                            <option :value="2">
                                2
                            </option>
                            <option :value="20">
                                20
                            </option>
                            <option :value="50">
                                50
                            </option>
                            <option :value="100">
                                100
                            </option>
                            <option :value="200">
                                200
                            </option>
                        </b-select>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-card
                no-body
                class="current-card d-none d-md-block d-lg-block d-xl-block"
            >
                <b-row class="text-center">
                    <b-col cols="2">
                        <strong>Type de sanctions</strong>
                    </b-col>
                    <b-col
                        v-if="$store.state.settings.enable_disciplinary_council"
                        cols="2"
                    >
                        <strong>Conseil de discipline</strong>
                    </b-col>
                    <b-col cols="2">
                        <strong>Date de la sanction</strong>
                    </b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <ask-sanctions-entry
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                :light-display="lightDisplay"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @filterStudent="filterStudent($event)"
                @done="loadEntries"
                @update-sanction="updateSanction(entry, $event)"
            />
            <b-row>
                <b-col>
                    <b-pagination
                        class="mt-1"
                        :total-rows="entriesCount"
                        v-model="currentPage"
                        @change="changePage"
                        :per-page="entriesPerPage"
                    />
                </b-col>
                <b-col>
                    <b-form-group
                        label="Sanctions par page"
                        label-cols
                        label-align-sm="right"
                    >
                        <b-select
                            class="mt-1"
                            v-model="entriesPerPage"
                            @input="loadEntries"
                            size="sm"
                        >
                            <option :value="20">
                                20
                            </option>
                            <option :value="50">
                                50
                            </option>
                            <option :value="100">
                                100
                            </option>
                            <option :value="200">
                                200
                            </option>
                        </b-select>
                    </b-form-group>
                </b-col>
            </b-row>
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
                Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
            </b-modal>
            <b-modal
                :title="currentName"
                size="xl"
                ref="infoModal"
                centered
                ok-only
                @hidden="currentEntry = null"
                ok-title="Fermer"
            >
                <info
                    v-if="currentEntry"
                    :matricule="currentEntry.student_id"
                    type="student"
                />
            </b-modal>        
            <b-modal
                ref="massActions"
                scrollable
                size="xl"
                ok-only
                @hide="entriesPerPage = 20; loadEntries()"
                body-class="position-static"
                :busy="massActionsOverlay"
                :hide-header-close="massActionsOverlay"
                :no-close-on-esc="massActionsOverlay"
                :no-close-on-backdrop="massActionsOverlay"
            >
                <b-overlay :show="massActionsOverlay">
                    <template #overlay>
                        <div class="text-center">
                            <p>Modification en cours…</p>
                            <b-progress
                                :value="massActionsProgress"
                                :max="1"
                                show-progress
                                animated
                            />
                        </div>
                    </template>
                    <mass-actions
                        :sanctions="entries"
                        @loading="updateMassActionsLoading"
                    />
                </b-overlay>
            </b-modal>
            <component
                :is="currentModal"
                ref="dynamicModal"
                @update="loadEntries"
                @reset="currentEntry = null"
                :entry="currentEntry"
            />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import axios from "axios";

import AskSanctionsEntry from "./askSanctionsEntry.vue";
import AskModal from "./ask_form.vue";
import AskExportModal from "./askExportModal.vue";
import MassActions from "./massActions.vue";
import Filters from "../common/filters_form.vue";
import Menu from "../common/menu_bar.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            menuInfo: {},
            showFilters: false,
            filter: "",
            entriesCount: 0,
            currentPage: 1,
            entries: [],
            entriesNotDone: 0,
            entriesWaiting: 0,
            currentEntry: null,
            currentModal: "ask-modal",
            retenues_mode: false,
            loaded: false,
            entriesPerPage: 20,
            massActionsOverlay: false,
            massActionsProgress: 0,
            lightDisplay: false,
        };
    },
    computed: {
        currentName: function () {
            if (this.currentEntry) {
                return this.currentEntry.student.display;
            }
            return "";
        },
        ordering: function () {
            if (this.$store.state.filters.find(f => f.filterType === "activate_today")) {
                return "&ordering=student__last_name";
            } else {
                return "&ordering=date_sanction,student__last_name";
            }
        },
    },
    watch: {
        retenues_mode: function (mode) {
            if (mode) {
                this.$store.commit("removeFilter", "activate_own_classes");
                this.applyFilter();
            } else {
                this.addFilter("activate_own_classes", "Activer", true);
            }
        }
    },
    methods: {
        updateMassActionsLoading: function (progress) {
            this.massActionsProgress = progress;
            this.massActionsOverlay = progress < 1;
            if (this.massActionsProgress === 1) {
                this.$refs.massActions.hide();
            }
        },
        openMassActions: function () {
            this.loaded = true;
            this.entriesPerPage = 200;
            this.loadEntries()
                .then(() => {
                    this.$refs.massActions.show();
                });
        },
        updateSanction: function (entry, newData) {
            if (entry.date_sanction != newData.date) {
                entry.explication_commentaire += `<p>Report de la sanction du ${entry.date_sanction} au ${newData.date}</p>`;
                entry.date_sanction = newData.date;
            }

            if (entry.sanction_decision_id !== newData.sanction.id) {
                entry.explication_commentaire += `<p>Changement de sanction: ${newData.sanction.sanction_decision}</p>`;
                entry.sanction_decision_id = newData.sanction.id;
                entry.sanction_decision = newData.sanction;
            }
            axios.put(`/dossier_eleve/api/ask_sanctions/${entry.id}/`, entry, token);
        },
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
            this.$store.commit("addFilter",
                {filterType: "student__matricule", tag: matricule, value: matricule}
            );
            this.applyFilter();
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
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
            this.openDynamicModal("ask-modal");
        },
        deleteEntry: function () {
            axios.delete("/dossier_eleve/api/ask_sanctions/" + this.currentEntry.id + "/", token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        addFilter: function(filterType, tag, value) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {"filterType": filterType, "tag": tag, "value": value}
            );
            this.applyFilter();
        },
        loadEntries: function () {
            return new Promise(resolve => {
                axios.get(`/dossier_eleve/api/ask_sanctions/?page=${this.currentPage}${this.filter}${this.ordering}&page_size=${this.entriesPerPage}`)
                    .then(response => {
                        this.entriesCount = response.data.count;
                        this.entries = response.data.results;
                        this.loaded = true;

                        // Get other counts.
                        this.getEntriesNotDone();
                        this.getEntriesWaiting();
                        resolve();
                    });
            });
        },
        getEntriesNotDone: function () {
            axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_not_done=true")
                .then(response => {
                    this.entriesNotDone = response.data.count;
                });
        },
        getEntriesWaiting: function () {
            axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_waiting=true")
                .then(response => {
                    this.entriesWaiting = response.data.count;
                });
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;

        this.applyFilter();
        this.loadEntries();
    },
    components: {
        "filters": Filters,
        "ask-sanctions-entry": AskSanctionsEntry,
        "ask-modal": AskModal,
        "ask-export-modal": AskExportModal,
        "app-menu": Menu,
        "mass-actions": MassActions,
    }
};
</script>

<style>
</style>
