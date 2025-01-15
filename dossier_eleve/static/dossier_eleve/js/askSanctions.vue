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
        <BContainer v-if="loaded">
            <BRow>
                <h2>Demandes de sanction</h2>
            </BRow>
            <BRow>
                <BTabs>
                    <template #tabs>
                        <BNavItem href="/dossier_eleve/">
                            Dossier des élèves
                        </BNavItem>
                        <BNavItem
                            active
                            href="/dossier_eleve/ask_sanctions"
                        >
                            Demandes de sanction
                        </BNavItem>
                    </template>
                </BTabs>
            </BRow>
            <BRow>
                <BCol
                    cols="12"
                    lg="3"
                >
                    <BFormGroup>
                        <div>
                            <BButton
                                v-if="store.canAskSanction"
                                variant="primary"
                                @click="openDynamicModal('ask-modal')"
                                class="w-100 mb-1"
                            >
                                <IBiPlus
                                    scale="1.5"
                                />
                                Nouvelle demande
                            </BButton>
                            <BButton
                                variant="secondary"
                                @click="openDynamicModal('ask-export-modal')"
                                class="w-100"
                            >
                                <IBiFileEarmark />
                                Export
                            </BButton>
                            <BButton
                                variant="secondary"
                                @click="openMassActions"
                                class="w-100 mt-1"
                            >
                                <IBiListCheck />
                                Actions de masse
                            </BButton>
                        </div>
                    </BFormGroup>
                </BCol>
                <BCol
                    cols="12"
                    lg="9"
                >
                    <filters
                        app="dossier_eleve"
                        model="ask_sanctions"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggle-search="showFilters = !showFilters"
                        class="mb-1"
                    />
                </BCol>
            </BRow>
            <BRow v-if="store.canSetSanction">
                <BCol>
                    <BListGroup>
                        <BListGroupItem>
                            Demandes de sanction en attente : <BBadge>
                                {{ entriesCount
                                }}
                            </BBadge>
                        </BListGroupItem>
                        <BListGroupItem
                            button
                            @click="addFilter('activate_not_done', 'Activer', true)"
                        >
                            Sanctions non faites <strong>à traiter</strong> : <BBadge variant="danger">
                                {{ entriesNotDone }}
                            </BBadge>
                        </BListGroupItem>
                        <BListGroupItem
                            button
                            v-if="entriesWaiting > 0"
                            @click="addFilter('activate_waiting', 'Activer', true)"
                        >
                            En attentes de validations : <BBadge variant="warning">
                                {{ entriesWaiting }}
                            </BBadge>
                        </BListGroupItem>
                    </BListGroup>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BPagination
                        class="mt-1"
                        :total-rows="entriesCount"
                        v-model="currentPage"
                        @update:model-value="changePage"
                        :per-page="entriesPerPage"
                    />
                </BCol>
                <BCol>
                    <BFormGroup
                        label="Sanctions par page"
                        label-cols
                        label-align-sm="right"
                    >
                        <BFormSelect
                            class="mt-1"
                            v-model="entriesPerPage"
                            @update:model-value="loadEntries"
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
                        </BFormSelect>
                    </BFormGroup>
                </BCol>
            </BRow>
            <BCard
                no-body
                class="current-card d-none d-md-block d-lg-block d-xl-block"
            >
                <BRow class="text-center">
                    <BCol cols="2">
                        <strong>Type de sanctions</strong>
                    </BCol>
                    <BCol
                        v-if="store.settings.enable_disciplinary_council"
                        cols="2"
                    >
                        <strong>Conseil de discipline</strong>
                    </BCol>
                    <BCol cols="2">
                        <strong>Date de la sanction</strong>
                    </BCol>
                    <BCol><strong>Commentaire(s)</strong></BCol>
                </BRow>
            </BCard>
            <ask-sanctions-entry
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                :light-display="lightDisplay"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @filter-student="filterStudent($event)"
                @done="loadEntries"
                @update-sanction="updateSanction(entry, $event)"
            />
            <BRow>
                <BCol>
                    <BPagination
                        class="mt-1"
                        :total-rows="entriesCount"
                        v-model="currentPage"
                        @update:model-value="changePage"
                        :per-page="entriesPerPage"
                    />
                </BCol>
                <BCol>
                    <BFormGroup
                        label="Sanctions par page"
                        label-cols
                        label-align-sm="right"
                    >
                        <BFormSelect
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
                        </BFormSelect>
                    </BFormGroup>
                </BCol>
            </BRow>
            <BModal
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
            </BModal>
            <BModal
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
                <BOverlay :show="massActionsOverlay">
                    <template #overlay>
                        <div class="text-center">
                            <p>Modification en cours…</p>
                            <BProgress
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
                </BOverlay>
            </BModal>
            <component
                :is="currentModal"
                ref="dynamicModal"
                @update="loadEntries"
                @reset="currentEntry = null"
                :entry="currentEntry"
            />
        </BContainer>
    </div>
</template>

<script>
import axios from "axios";

import { useModalController } from "bootstrap-vue-next";

import AskSanctionsEntry from "./askSanctionsEntry.vue";
import AskModal from "./ask_form.vue";
import AskExportModal from "./askExportModal.vue";
import MassActions from "./massActions.vue";
import Filters from "@s:core/js/common/filters_form.vue";
import Menu from "@s:core/js/common/menu_bar.vue";

import { askSanctionsStore } from "./stores/ask_sanctions.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { confirm } = useModalController();
        return { confirm };
    },
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
            store: askSanctionsStore(),
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
            if (this.store.filters.find(f => f.filterType === "activate_today")) {
                return "&ordering=student__last_name";
            } else {
                return "&ordering=date_sanction,student__last_name";
            }
        },
    },
    watch: {
        retenues_mode: function (mode) {
            if (mode) {
                this.store.removeFilter("activate_own_classes");
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
            this.store.addFilter(
                { filterType: "student__matricule", tag: matricule, value: matricule }
            );
            this.applyFilter();
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
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        editEntry: function (index) {
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
        addFilter: function (filterType, tag, value) {
            this.showFilters = true;
            this.store.addFilter(
                { "filterType": filterType, "tag": tag, "value": value }
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

<style></style>
