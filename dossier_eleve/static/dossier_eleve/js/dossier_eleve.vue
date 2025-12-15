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
                <h2>Dossier des élèves</h2>
            </BRow>
            <BRow
                class="mb-2"
                v-if="canAskSanction"
            >
                <BNav tabs>
                    <BNavItem
                        active
                        href="/dossier_eleve/"
                    >
                        Dossier des élèves
                    </BNavItem>
                    <BNavItem href="/dossier_eleve/ask_sanctions">
                        <span class="text-danger">Demandes de sanction</span>
                        <span v-if="store.canSetSanction">
                            <BBadge>{{ askSanctionsCount }}</BBadge>
                            <BBadge variant="warning">{{ askSanctionsNotDoneCount }}</BBadge>
                        </span>
                    </BNavItem>
                </BNav>
            </BRow>
            <BRow>
                <BCol
                    cols="12"
                    lg="3"
                >
                    <BFormGroup>
                        <div>
                            <BButton
                                variant="primary"
                                to="/new/"
                                class="w-100"
                                v-if="store.canAddCas"
                            >
                                <IBiPlus />
                                Nouveau cas
                            </BButton>
                            <BButton
                                variant="secondary"
                                @click="openDynamicModal('export-modal')"
                                class="w-100 mt-1"
                            >
                                <IBiFileEarmarkText />
                                Export
                            </BButton>
                        </div>
                    </BFormGroup>
                </BCol>
                <BCol>
                    <filters
                        app="dossier_eleve"
                        model="cas_eleve"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggle-search="showFilters = !showFilters"
                    />
                </BCol>
            </BRow>
            <BPagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @update:model-value="changePage"
                :per-page="20"
            />
            <cas-eleve-entry
                v-for="entry in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @filter-student="filterStudent($event)"
            />
            <component
                :is="currentModal"
                ref="dynamicModal"
                @update="loadEntries"
                @reset="currentEntry = null"
                :entry="currentEntry"
                :entries-count="entriesCount"
            />
            <BPagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @update:model-value="changePage"
                :per-page="20"
            />
        </BContainer>
    </div>
</template>

<script>
import axios from "axios";

import { useModalController } from "bootstrap-vue-next";

import Filters from "@s:core/js/common/filters_form.vue";
import { getFilters } from "@s:core/js/common/filters.js";
import CasEleveEntry from "./casEleveEntry.vue";
import ExportModal from "./exportModal.vue";

import { dossierEleveStore } from "./stores/dossier_eleve.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { create } = useModalController();
        return { create };
    },
    data: function () {
        return {
            menuInfo: {},
            entriesCount: 0,
            currentPage: 1,
            entries: [],
            currentEntry: null,
            currentModal: null,
            filter: "",
            ordering: "&ordering=",
            showFilters: false,
            loaded: false,
            askSanctionsCount: 0,
            askSanctionsNotDoneCount: 0,
            store: dossierEleveStore(),
        };
    },
    computed: {
        currentName: function () {
            if (this.currentEntry) {
                return this.currentEntry.student.display;
            }
            return "";
        },
        canAskSanction: function () {
            const enable = this.store.settings.enable_submit_sanctions;
            const canAskSanction = this.store.canAskSanction;
            return enable && canAskSanction;
        },
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            if ("dynamicModal" in this.$refs) this.$refs.dynamicModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.store.addFilter(
                { filterType: "student__matricule", tag: matricule, value: matricule },
            );
            this.applyFilter();
        },
        applyFilter: function () {
            this.filter = getFilters(this.store.filters);
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.create({
                body: "Êtes-vous sûr de vouloir supprimer l'entrée ?",
                centered: true,
                buttonSize: "sm",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Annuler",
            })
                .then((remove) => {
                    if (!remove.ok) return;

                    axios.delete(`/dossier_eleve/api/cas_eleve/${entry.id}/`, token)
                        .then(() => {
                            this.loadEntries();
                        });
                });
        },
        deleteEntry: function () {
            this.currentEntry = null;
        },
        loadEntries: function () {
            axios.get("/dossier_eleve/api/cas_eleve/?page=" + this.currentPage + this.filter + this.ordering)
                .then((response) => {
                    this.entriesCount = response.data.count;
                    this.entries = response.data.results;
                    this.loaded = true;
                });
        },
        checkMatriculeFilter: function () {
            // const fullscreen = window.location.href.includes("matricule");
            const matricule = (new URL(document.location)).searchParams.get("matricule");
            if (matricule) {
                this.store.addFilter({ filterType: "student__matricule", value: matricule, tag: matricule });
                this.showFilters = true;
            }
        },
    },
    mounted: function () {
        this.checkMatriculeFilter();
        this.applyFilter();
        this.loadEntries();

        axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering)
            .then((response) => {
                this.askSanctionsCount = response.data.count;
            });
        axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_not_done=true")
            .then((response) => {
                this.askSanctionsNotDoneCount = response.data.count;
            });
    },
    components: {
        "filters": Filters,
        "cas-eleve-entry": CasEleveEntry,
        "export-modal": ExportModal,
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
</style>
