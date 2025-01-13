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
        <BContainer>
            <h1>Retards des élèves</h1>
            <BOverlay :show="loading">
                <BRow class="mb-1">
                    <BCol
                        sm="12"
                        :md="store.settings.enable_camera_scan ? '8' : '10' "
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
                            <template #noResult>
                                Aucune personne trouvée.
                            </template>
                        </multiselect>
                    </BCol>
                    <BCol
                        cols="3"
                        sm="2"
                        class="mt-1 mt-md-0"
                    >
                        <BButton
                            :disabled="!search || addingStudent"
                            @click="addStudent"
                        >
                            <BSpinner
                                v-if="addingStudent"
                                small
                            />
                            Ajouter
                        </BButton>
                    </BCol>
                    <BCol
                        v-if="store.settings.enable_camera_scan"
                        cols="3"
                        sm="2"
                        class="mt-1 mt-md-0"
                    >
                        <BButton @click="scanCode">
                            Scanner
                        </BButton>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol
                        v-if="store.settings.printer.length > 0"
                        cols="5"
                        md="4"
                    >
                        <BCard
                            bg-variant="light"
                            no-body
                            class="p-2"
                        >
                            <BFormCheckbox v-model="printing">
                                Imprimer le retard
                            </BFormCheckbox>
                        </BCard>
                    </BCol>
                    <BCol
                        cols="4"
                        md="4"
                    >
                        <BCard
                            bg-variant="light"
                            no-body
                            class="p-2"
                        >
                            <BFormCheckbox v-model="justified">
                                Retard justifié
                            </BFormCheckbox>
                        </BCard>
                    </BCol>
                    <BCol
                        cols="3"
                        md="4"
                        v-if="store.settings.printer.length > 0 && availablePrinters.length > 1"
                    >
                        <BCard
                            bg-variant="light"
                            no-body
                            class="p-1"
                        >
                            <BButton
                                v-b-modal.printer-selection
                                size="sm"
                            >
                                <IBiPrinter />
                                <span class="d-none d-md-inline">
                                    Imprimante :
                                </span>
                                {{ printer ? availablePrinters.find(p => p.value === printer).text : "" }}
                            </BButton>
                        </BCard>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <filters
                            app="lateness"
                            model="lateness"
                            ref="filters"
                            @update="applyFilter"
                            :store="store"
                            :show-search="showFilters"
                            @toggle-search="showFilters = !showFilters"
                            class="mt-2"
                        />
                    </BCol>
                    <BCol
                        cols="12"
                        md="5"
                        class="text-end"
                    >
                        <BDropdown
                            text="Export"
                            variant="outline-secondary"
                            class="mt-1"
                        >
                            <BDropdownItem href="/lateness/proeco_list/AM/">
                                Matin
                            </BDropdownItem>
                            <BDropdownItem href="/lateness/proeco_list/PM/">
                                Après-midi
                            </BDropdownItem>
                            <BDropdownItem href="/lateness/proeco_list/DAY/">
                                Journée
                            </BDropdownItem>
                        </BDropdown>
                        <BButton
                            @click="$refs['topLateness'].show();getTopList()"
                            variant="outline-secondary"
                            class="mt-1"
                        >
                            <IBiListOl />
                            Top retards
                        </BButton>
                        <BButton
                            v-if="store.hasSettingsPerm"
                            variant="outline-warning"
                            @click="promptChangeCount"
                            class="mt-1"
                        >
                            <IBiGear />
                            Début du comptage
                        </BButton>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BPagination
                            class="mt-1"
                            :total-rows="entriesCount"
                            v-model="currentPage"
                            @update:model-value="changePage"
                            :per-page="20"
                        />
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <lateness-entry
                            v-for="(lateness, index) in latenesses"
                            :key="lateness.id"
                            :lateness="lateness"
                            ref="entries"
                            @update="latenesses.splice(index, 1, $event)"
                            @delete="askDelete(lateness)"
                            @filter-student="filterStudent($event)"
                        />
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
                    Êtes-vous sûr de vouloir supprimer ce passage ?
                </BModal>
                <BModal
                    ref="changeCountModal"
                    title="Changer la date du début de comptage"
                    hide-header-close
                    centered
                    cancel-title="Annuler"
                    :no-close-on-backdrop="true"
                    :no-close-on-esc="true"
                    @ok="changeCountDate"
                    @cancel="countDate = store.settings.date_count_start"
                >
                    <BFormInput
                        type="date"
                        v-model="countDate"
                    />
                </BModal>
                <BModal
                    ref="topLateness"
                    ok-only
                >
                    <BFormGroup>
                        <BFormCheckbox
                            v-model="topOwnClasses"
                            switch
                            @input="getTopList()"
                        >
                            N'afficher que ses classes
                        </BFormCheckbox>
                    </BFormGroup>
                    <BListGroup>
                        <BListGroupItem
                            v-for="item in topLateness"
                            :key="item.student.matricule"
                            class="d-flex justify-content-between align-items-center"
                        >
                            {{ item.student.display }}
                            <BBadge variant="primary">
                                {{ item.count }}
                            </BBadge>
                        </BListGroupItem>
                    </BListGroup>
                </BModal>
                <BModal
                    id="printer-selection"
                    ok-only
                >
                    <BFormGroup
                        label="Sélectionner l'imprimante à utiliser"
                    >
                        <BFormSelect
                            v-model="printer"
                            :options="availablePrinters"
                        />
                    </BFormGroup>
                </BModal>
            </BOverlay>
        </BContainer>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

import Filters from "@s:core/js/common/filters_form.vue";
import {getFilters} from "@s:core/js/common/filters.js";
import LatenessEntry from "./lateness_entry.vue";

import { latenessStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            menuInfo: {},
            loading: true,
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
            countDate: null,
            topLateness: [],
            topOwnClasses: false,
            printer: null,
            availablePrinters: [],
            store: latenessStore(),
        };
    },
    methods: {
        promptChangeCount: function () {
            this.$refs["changeCountModal"].show();
        },
        changeCountDate: function () {
            axios.patch(
                `/lateness/api/settings/${this.store.settings.id}/`,
                { date_count_start: this.countDate },
                token,
            ).then(() => {
                document.location.reload();
            });
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.store.addFilter(
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
                teachings: this.store.teachings,
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
            if (this.printing) url += `?print=1&printer=${this.printer}`;
            this.addingStudent = true;
            axios.post(url, data, token)
                .then(response => {
                    if (response.data.has_sanction) this.show({props: {
                        body: `Une sanction ${response.data.sanction_id ? "a été" : "doit être"} ajoutée !`,
                        title: "Sanction !"
                    }});
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
            this.filter = getFilters(this.store.filters);
            this.loadEntries();
        },
        loadEntries: function () {
            axios.get(`/lateness/api/lateness/?ordering=-datetime_creation${this.filter}&page=${this.currentPage}`)
                .then((response) => {
                    this.latenesses = response.data.results;
                    this.entriesCount = response.data.count;
                    this.loading = false;
                }).catch(err => {
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
        getTopList: function () {
            axios.get(`/lateness/api/top_lateness?${this.topOwnClasses ? "own_classes=True" : ""}`)
                .then(resp => {
                    this.topLateness = resp.data;
                });
        },
        checkMatriculeFilter: function () {
            const matricule = (new URL(document.location)).searchParams.get("student__matricule");
            if (matricule) {
                this.store.addFilter({filterType: "student__matricule", value: matricule, tag: matricule});
                this.showFilters = true;
            }
        }
    },
    mounted: function () {
        this.countDate = this.store.settings.date_count_start;

        this.checkMatriculeFilter();
        this.applyFilter();
        this.overloadInput();        
        this.getTopList();

        this.availablePrinters = this.store.settings.printer.split(",")
            .map((p, i) => {
                return {
                    // eslint-disable-next-line no-irregular-whitespace
                    text: `Impr. ${i + 1}`,
                    value: p,
                };
            });
        this.printer = this.availablePrinters ? this.availablePrinters[0].value : null;
    },
    components: {
        "multiselect": Multiselect,
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
