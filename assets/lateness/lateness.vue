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
            v-if="loaded"
            :menu-info="menuInfo"
        />
        <b-container v-if="loaded">
            <h1>Retards des élèves</h1>
            <b-row class="mb-1">
                <b-col
                    sm="12"
                    :md="$store.state.settings.enable_camera_scan ? '8' : '10' "
                >
                    <multiselect
                        ref="input"
                        :show-no-options="false"
                        :internal-search="false"
                        :options="searchOptions"
                        @search-change="getSearchOptions"
                        :loading="searchLoading"
                        placeholder="Rechercher un étudiant"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label=""
                        label="display"
                        track-by="matricule"
                        v-model="search"
                    >
                        <span slot="noResult">Aucune personne trouvée.</span>
                    </multiselect>
                </b-col>
                <b-col
                    cols="3"
                    sm="2"
                    class="mt-1 mt-md-0"
                >
                    <b-button
                        :disabled="!search || addingStudent"
                        @click="addStudent"
                    >
                        <icon
                            v-if="addingStudent"
                            name="spinner"
                            scale="1"
                            spin
                            class="align-baseline"
                        />
                        Ajouter
                    </b-button>
                </b-col>
                <b-col
                    v-if="$store.state.settings.enable_camera_scan"
                    cols="3"
                    sm="2"
                    class="mt-1 mt-md-0"
                >
                    <b-btn @click="scanCode">
                        Scanner
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col
                    v-if="$store.state.settings.printer.length > 0"
                    cols="5"
                    md="4"
                >
                    <b-card
                        bg-variant="light"
                        no-body
                        class="p-2"
                    >
                        <b-form-checkbox v-model="printing">
                            Imprimer le retard
                        </b-form-checkbox>
                    </b-card>
                </b-col>
                <b-col
                    cols="5"
                    md="4"
                >
                    <b-card
                        bg-variant="light"
                        no-body
                        class="p-2"
                    >
                        <b-form-checkbox v-model="justified">
                            Retard justifié
                        </b-form-checkbox>
                    </b-card>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <filters
                        app="lateness"
                        model="lateness"
                        ref="filters"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                    />
                </b-col>
                <b-col
                    v-if="$store.state.hasSettingsPerm"
                    cols="12"
                    md="5"
                    class="text-right"
                >
                    <b-dropdown
                        text="Export"
                        variant="outline-secondary"
                        class="mt-1"
                    >
                        <b-dropdown-item href="/lateness/proeco_list/AM/">
                            Matin
                        </b-dropdown-item>
                        <b-dropdown-item href="/lateness/proeco_list/PM/">
                            Après-midi
                        </b-dropdown-item>
                        <b-dropdown-item href="/lateness/proeco_list/DAY/">
                            Journée
                        </b-dropdown-item>
                    </b-dropdown>
                    <b-btn
                        @click="$refs['topLateness'].show();getTopList()"
                        variant="outline-secondary"
                        class="mt-1"
                    >
                        <b-icon icon="list-ol" />
                        Top retards
                    </b-btn>
                    <b-btn
                        variant="outline-warning"
                        @click="promptChangeCount"
                        class="mt-1"
                    >
                        <b-icon icon="gear" />
                        Début du comptage
                    </b-btn>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-pagination
                        class="mt-1"
                        :total-rows="entriesCount"
                        v-model="currentPage"
                        @change="changePage"
                        :per-page="20"
                    />
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <lateness-entry
                        v-for="(lateness, index) in latenesses"
                        :key="lateness.id"
                        :lateness="lateness"
                        ref="entries"
                        @update="latenesses.splice(index, 1, $event)"
                        @delete="askDelete(lateness)"
                        @filterStudent="filterStudent($event)"
                    />
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
                Êtes-vous sûr de vouloir supprimer ce passage ?
            </b-modal>
            <b-modal
                ref="scanModal"
                hide-footer
                centered
                no-fade
                size="xl"
                @hidden="closeQuagga"
            >
                <div
                    id="interactive"
                    class="viewport"
                />
            </b-modal>
            <b-modal
                ref="changeCountModal"
                title="Changer la date du début de comptage"
                hide-header-close
                centered
                cancel-title="Annuler"
                :no-close-on-backdrop="true"
                :no-close-on-esc="true"
                @ok="changeCountDate"
                @cancel="countDate = $store.state.settings.date_count_start"
            >
                <b-input
                    type="date"
                    v-model="countDate"
                />
            </b-modal>
            <b-modal
                ref="topLateness"
                ok-only
            >
                <b-list-group>
                    <b-list-group-item
                        v-for="item in topLateness"
                        :key="item.student.matricule"
                        class="d-flex justify-content-between align-items-center"
                    >
                        {{ item.student.display }}
                        <b-badge variant="primary">
                            {{ item.count }}
                        </b-badge>
                    </b-list-group-item>
                </b-list-group>
            </b-modal>
        </b-container>
    </div>
</template>

<script>
import Quagga from "@ericblade/quagga2";

import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

import axios from "axios";

import Menu from "assets/common/menu.vue";
import Filters from "assets/common/filters.vue";
import {getFilters} from "assets/common/filters.js";
import LatenessEntry from "./lateness_entry.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            menuInfo: {},
            loaded: false,
            search: null,
            searchId: -1,
            searchOptions: [],
            searchLoading: false,
            showFilters: false,
            filter: "",
            latenesses: [],
            entriesCount: 0,
            currentPage: 1,
            currentEntry: null,
            addingStudent: false,
            printing: true,
            justified: false,
            countDate: this.$store.state.settings.date_count_start,
            topLateness: [],
        };
    },
    methods: {
        promptChangeCount: function () {
            this.$refs["changeCountModal"].show();
        },
        changeCountDate: function () {
            axios.patch(
                `/lateness/api/settings/${this.$store.state.settings.id}/`,
                { date_count_start: this.countDate },
                token,
            ).then(() => {
                document.location.reload();
            });
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {filterType: "student__matricule", tag: matricule, value: matricule}
            );
            this.currentPage = 1;
            this.applyFilter();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            axios.delete("/lateness/api/lateness/" + this.currentEntry.id, token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const data = {
                query: query,
                teachings: this.$store.state.teachings,
                people: "student",
                check_access: false,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                
                    this.searchOptions = response.data;
                });
        },
        selectStudent: function (matricule) {
            axios.get("/annuaire/api/student/" + matricule + "/")
                .then(resp => {
                    if (resp.data) {
                        this.search = resp.data;
                        this.addStudent();
                    }
                })
                .catch(() => {
                    console.log("Aucun étudiant trouvé");
                    this.addingStudent = false;
                });
        },
        overloadInput: function () {
            setTimeout(() => {
                // Check if input is loaded.
                let refInput = this.$refs.input;
                if (refInput) {
                    let input = refInput.$refs.search;
                    input.focus();
                    input.addEventListener("keypress", (e) => {
                        if (e.key == "Enter") {
                            if (refInput.search && refInput.search.length > 1 && !isNaN(refInput.search)) {
                                this.selectStudent(refInput.search);
                                refInput.search = "";
                            }
                        }
                    });
                    return input;
                } else {
                    this.overloadInput();
                }
            }, 300);
            
        },
        addStudent: function () {
            const data = {
                student_id: this.search.matricule,
                justified: this.justified
            };
            let url = "/lateness/api/lateness/";
            if (this.printing) url += "?print=1";
            this.addingStudent = true;
            axios.post(url, data, token)
                .then(response => {
                    if (response.data.has_sanction) this.$bvToast.toast(
                        `Une sanction ${response.data.sanction_id ? "a été" : "doit être"} ajoutée !`,
                        {title: "Sanction !"}
                    );
                    this.addingStudent = false;
                    // Reload entries.
                    this.search = null;
                    this.loadEntries();
                    setTimeout(() => {
                        if (this.$refs.entries.length > 0) {
                            this.$refs.entries[this.$refs.entries.length - 1].displayPhoto();
                        }
                    }, 300);
                })
                .catch(err => {
                    alert(err);
                    this.addingStudent = false;
                });
        },
        applyFilter: function () {
            this.filter = getFilters(this.$store.state.filters);
            this.loadEntries();
        },
        loadEntries: function () {
            axios.get(`/lateness/api/lateness/?ordering=-datetime_creation${this.filter}&page=${this.currentPage}`, token)
                .then(response => {
                    this.latenesses = response.data.results;
                    this.entriesCount = response.data.count;
                    this.loaded = true;
                
                })
                .catch(err => {
                    alert(err);
                    this.loaded = true;
                });
        },
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        closeQuagga: function () {
            Quagga.stop();
        },
        scanCode: function () {
            let vueApp = this;
            vueApp.$refs.scanModal.show();
            setTimeout(() => {
                var App = {
                    init: function() {
                        var self = this;

                        Quagga.init(this.state, function(err) {
                            if (err) {
                                return self.handleError(err);
                            }
                            Quagga.start();
                        });
                    },
                    handleError: function(err) {
                        console.log(err);
                    },
                    state: {
                        inputStream: {
                            type : "LiveStream",
                            constraints: {
                                width: {min: 640},
                                height: {min: 480},
                                facingMode: "environment",
                                aspectRatio: {min: 1, max: 2}
                            }
                        },
                        numOfWorkers: 2,
                        frequency: 10,
                        decoder: {
                            readers : [{
                                format: "code_128_reader",
                                config: {}
                            }]
                        },
                    },
                };

                App.init();

                Quagga.onDetected(function(result) {
                    if (vueApp.addingStudent) return;
                    vueApp.addingStudent = true;
                    const code = result.codeResult.code;
                    Quagga.stop();
                    vueApp.$refs.scanModal.hide();
                    vueApp.selectStudent(code);
                });
            }, 300);
        },
        getTopList: function () {
            axios.get("/lateness/api/top_lateness")
                .then(resp => {
                    this.topLateness = resp.data;
                });
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
        this.applyFilter();
        this.overloadInput();        
        this.getTopList();
    },
    components: {
        "multiselect": Multiselect,
        "app-menu": Menu,
        "lateness-entry": LatenessEntry,
        "filters": Filters,
    }
};
</script>

<style>
.viewport {
    max-height: 640px;
}
</style>
