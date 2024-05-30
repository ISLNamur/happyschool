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
                <h2>Dossier des élèves</h2>
            </b-row>
            <b-row
                class="mb-2"
                v-if="canAskSanction"
            >
                <b-nav tabs>
                    <b-nav-item
                        active
                        href="/dossier_eleve/"
                    >
                        Dossier des élèves
                    </b-nav-item>
                    <b-nav-item href="/dossier_eleve/ask_sanctions">
                        <span class="text-danger">Demandes de sanction</span>
                        <span v-if="store.canSetSanction">
                            <b-badge>{{ askSanctionsCount }}</b-badge>
                            <b-badge variant="warning">{{ askSanctionsNotDoneCount }}</b-badge>
                        </span>
                    </b-nav-item>
                </b-nav>
            </b-row>
            <b-row>
                <b-col
                    cols="12"
                    lg="3"
                >
                    <b-form-group>
                        <div>
                            <b-btn
                                variant="primary"
                                to="/new/"
                                class="w-100"
                                v-if="store.canAddCas"
                            >
                                <b-icon icon="plus" />
                                Nouveau cas
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openDynamicModal('export-modal')"
                                class="w-100 mt-1"
                            >
                                <b-icon icon="file-earmark-text" />
                                Export
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
                <b-col>
                    <filters
                        app="dossier_eleve"
                        model="cas_eleve"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                    />
                </b-col>
            </b-row>
            <b-pagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
                :per-page="20"
            />
            <cas-eleve-entry
                v-for="entry in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @filterStudent="filterStudent($event)"
            />
            <component
                :is="currentModal"
                ref="dynamicModal"
                @update="loadEntries"
                @reset="currentEntry = null"
                :entry="currentEntry"
                :entries-count="entriesCount"
            />
            <b-pagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
                :per-page="20"
            />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import axios from "axios";

import Filters from "@s:core/js/common/filters_form.vue";
import {getFilters} from "@s:core/js/common/filters.js";
import CasEleveEntry from "./casEleveEntry.vue";
import ExportModal from "./exportModal.vue";

import { dossierEleveStore } from "./stores/dossier_eleve.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
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
        }
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
                {filterType: "student__matricule", tag: matricule, value: matricule}
            );
            this.applyFilter();
        },
        applyFilter: function () {
            this.filter = getFilters(this.store.filters);
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer l'entrée ?",{
                centered: true,
                buttonSize: "sm",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Annuler",
            })
                .then(remove => {
                    if (!remove) return;

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
                .then(response => {
                    this.entriesCount = response.data.count;
                    this.entries = response.data.results;
                    this.loaded = true;
                });
        },
        checkMatriculeFilter: function () {
            // const fullscreen = window.location.href.includes("matricule");
            const matricule = (new URL(document.location)).searchParams.get("matricule");
            if (matricule) {
                this.store.addFilter({filterType: "student__matricule", value: matricule, tag: matricule});
                this.showFilters = true;
            }
        }
    },
    mounted: function () {
        this.checkMatriculeFilter();
        this.applyFilter();
        this.loadEntries();

        axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.askSanctionsCount = response.data.count;
            });
        axios.get("/dossier_eleve/api/ask_sanctions/?page=" + this.currentPage + this.filter + this.ordering + "&activate_not_done=true")
            .then(response => {
                this.askSanctionsNotDoneCount = response.data.count;
            });
    },
    components: {
        "filters": Filters,
        "cas-eleve-entry": CasEleveEntry,
        "export-modal": ExportModal,
    }
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
