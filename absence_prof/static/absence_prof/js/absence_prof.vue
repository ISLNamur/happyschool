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
                <h2>Absence Prof</h2>
            </BRow>
            <BRow>
                <BCol
                    cols="12"
                    lg="3"
                >
                    <BFormGroup>
                        <div>
                            <BButton
                                variant="outline-success"
                                to="/new/"
                                class="w-100"
                            >
                                <IBiPlus
                                    scale="1.5"
                                />
                                Ajouter une absence
                            </BButton>
                            <BButton
                                :href="'/absence_prof/list/?ordering=name&page_size=200' + filter"
                                target="_blank"
                                class="w-100 mt-1"
                            >
                                <IBiFileEarmark />
                                Exporter en PDF
                            </BButton>
                        </div>
                    </BFormGroup>
                </BCol>
                <BCol>
                    <filters
                        app="absence_prof"
                        model="absence"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggle-search="showFilters = !showFilters"
                    />
                </BCol>
            </BRow>
            <BPagination
                class="mt-2"
                :total-rows="entriesCount"
                v-model="currentPage"
                @page-click="changePage"
                :per-page="20"
            />
            <absence-prof-entry
                v-for="entry in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(entry)"
            />
        </BContainer>
    </div>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import axios from "axios";
import { useModalController } from "bootstrap-vue-next";

import Filters from "@s:core/js/common/filters_form.vue";

import { absenceProfStore } from "./stores/index.js";

import AbsenceProfEntry from "./absenceProfEntry.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
// const { show } = useModalController();

export default {
    setup: function () {
        const { confirm } = useModalController();
        return { confirm };
    },
    data: function () {
        return {
            menu: {},
            loaded: false,
            showFilters: false,
            active: true,
            currentPage: 1,
            currentEntry: null,
            entriesCount: 0,
            filter: "",
            ordering: "&ordering=date_absence_start,date_absence_end,name",
            entries: [],
            store: absenceProfStore(),
        };
    },
    computed: {
        name: function () {
            if (this.currentEntry) return this.currentEntry.name;

            return "";
        }
    },
    methods: {
        changePage: function (_, page) {
            this.currentPage = page;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.confirm(
                {props: {
                    body: `Êtes-vous sûr de vouloir supprimer cette absence : ${this.name} ?`,
                    noHeader: true,
                    okVariant: "danger",
                    okTitle: "Oui",
                    cancelTitle: "Annuler",
                }}
            ).then((resp) => {
                if (resp) {
                    this.deleteEntry();
                }
            });
            // this.$refs.deleteModal;
        },
        deleteEntry: function () {
            axios.delete("/absence_prof/api/absence/" + this.currentEntry.id + "/", token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        editEntry: function(entry) {
            this.currentEntry = entry;
        },
        loadEntries: function () {
            axios.get("/absence_prof/api/absence/?page_size=20&page=" + this.currentPage + this.filter + this.ordering)
                .then(response => {
                    this.entries = response.data.results;
                    this.entriesCount = response.data.count;
                    this.loaded = true;
                });
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
        }
    },
    mounted: function () {
        this.applyFilter();
    },
    components: {
        "filters": Filters,
        "absence-prof-entry": AbsenceProfEntry,
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
