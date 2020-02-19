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
        <app-menu :menu-info="menuInfo" />
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
                        <span v-if="$store.state.canSetSanction">
                            <b-badge>{{ askSanctionsCount }}</b-badge>
                            <b-badge variant="warning">{{ askSanctionsNotDoneCount }}</b-badge>
                        </span>
                    </b-nav-item>
                </b-nav>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-btn
                                variant="primary"
                                @click="openDynamicModal('add-modal')"
                            >
                                <icon
                                    name="plus"
                                    scale="1"
                                    class="align-middle"
                                />
                                Nouveau cas
                            </b-btn>
                            <b-btn
                                variant="secondary"
                                @click="openDynamicModal('export-modal')"
                            >
                                <icon
                                    name="file"
                                    scale="1"
                                />
                                Export
                            </b-btn>
                            <b-btn
                                variant="outline-secondary"
                                v-b-toggle.filters
                            >
                                <icon
                                    name="search"
                                    scale="1"
                                />
                                Ajouter des filtres
                            </b-btn>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-collapse
                        id="filters"
                        v-model="showFilters"
                    >
                        <b-card>
                            <filters
                                app="dossier_eleve"
                                model="cas_eleve"
                                ref="filters"
                                @update="applyFilter"
                            />
                        </b-card>
                    </b-collapse>
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
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @filterStudent="filterStudent($event)"
                @showInfo="showInfo(entry)"
            />
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
                size="lg"
                ref="infoModal"
                centered
                ok-only
                @hidden="currentEntry = null"
            >
                <info
                    v-if="currentEntry"
                    :matricule="currentEntry.matricule_id"
                    type="student"
                    no-news
                />
            </b-modal>
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
import BootstrapVue from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

import axios from "axios";
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import Info from "../annuaire/info.vue";

import Filters from "../common/filters.vue";
import {getFilters} from "../common/filters.js";
import Menu from "../common/menu.vue";
import CasEleveEntry from "./casEleveEntry.vue";
import AddModal from "./addModal.vue";
import ExportModal from "./exportModal.vue";

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
            ordering: "&ordering=-datetime_encodage",
            showFilters: false,
            loaded: false,
            askSanctionsCount: 0,
            askSanctionsNotDoneCount: 0,
        };
    },
    computed: {
        currentName: function () {
            if (this.currentEntry) {
                return this.currentEntry.matricule.display;
            }
            return "";
        },
        canAskSanction: function () {
            const enable = this.$store.state.settings.enable_submit_sanctions;
            const canAskSanction = this.$store.state.canAskSanction;
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
        showInfo: function (entry) {
            this.currentEntry = entry;
            this.$refs.infoModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {filterType: "matricule_id", tag: matricule, value: matricule}
            );
            this.applyFilter();
        },
        applyFilter: function () {
            this.filter = getFilters(this.$store.state.filters);
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
            this.openDynamicModal("add-modal");
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.delete("/dossier_eleve/api/cas_eleve/" + this.currentEntry.id + "/", token)
                .then(() => {
                    this.loadEntries();
                });

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
                this.$store.commit("addFilter", {filterType: "matricule_id", value: matricule, tag: matricule});
                this.showFilters = true;
            }
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;

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
        "add-modal": AddModal,
        "export-modal": ExportModal,
        "info": Info,
        "app-menu": Menu,
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
