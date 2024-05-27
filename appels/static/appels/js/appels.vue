<template>
    <div>
        <div
            class="loading"
            v-if="!loaded"
        />
        <b-container v-if="loaded">
            <b-row>
                <h2>Appels</h2>
            </b-row>
            <b-row>
                <b-col
                    cols="12"
                    md="4"
                    lg="3"
                >
                    <b-button
                        variant="outline-success"
                        to="/add/"
                        class="w-100"
                    >
                        <b-icon
                            icon="plus"
                            scale="1.5"
                        />
                        Ajouter un appel
                    </b-button>
                </b-col>
                <b-col
                    cols="12"
                    lg="9"
                >
                    <filters
                        app="appels"
                        model="appel"
                        ref="filters"
                        :store="store"
                        @update="applyFilter"
                        :show-search="showFilters"
                        @toggleSearch="showFilters = !showFilters"
                        class="mt-1 mt-lg-0"
                    />
                </b-col>
            </b-row>
            <b-pagination
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
            />
            <b-card
                no-body
                class="current-card d-none d-md-block d-lg-block d-xl-block"
            >
                <b-row class="text-center">
                    <b-col cols="2">
                        <strong>Objet</strong>
                    </b-col>
                    <b-col cols="2">
                        <strong>Motif</strong>
                    </b-col>
                    <b-col cols="1">
                        <strong>De</strong>
                    </b-col>
                    <b-col cols="1">
                        <strong>À</strong>
                    </b-col>
                    <b-col cols="1">
                        <strong>Appel</strong>
                    </b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <appel-entry
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index)"
                @processing="processEntry(index)"
                @filterStudent="filterStudent($event)"
                @showInfo="showInfo(entry)"
            />
        </b-container>
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
            Êtes-vous sûr de vouloir supprimer cet appel ?
        </b-modal>
        <b-modal
            :title="currentName"
            size="xl"
            ref="infoModal"
            centered
            ok-only
            @hidden="currentEntry = null"
        >
            <b-tabs>
                <b-tab title="Info">
                    <person-info
                        v-if="currentEntry"
                        :custom-matricule="currentEntry.matricule_id"
                        custom-person-type="student"
                    />
                </b-tab>
                <b-tab title="Moyens de contacts">
                    <person-contact
                        v-if="currentEntry"
                        :custom-matricule="currentEntry.matricule_id"
                        custom-person-type="student"
                    />
                </b-tab>
            </b-tabs>
        </b-modal>
    </div>
</template>

<script>
import Vue from "vue";
import {BootstrapVue, BootstrapVueIcons} from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

import PersonInfo from "@s:annuaire/js/person_info.vue";
import PersonContact from "@s:annuaire/js/contact_info.vue";

import Filters from "@s:core/js/common/filters_form.vue";
import { appelsStore } from "./stores/index.js";

import axios from "axios";

import AppelEntry from "./appelEntry.vue";

Vue.component("AppelEntry", AppelEntry);

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

export default {
    data: function () {
        return {
            entriesCount: 20,
            currentPage: 1,
            entries: [],
            currentEntry: null,
            filter: "",
            ordering: "&ordering=-datetime_appel",
            menuInfo: {},
            loaded: false,
            processing: false,
            showFilters: false,
            store: appelsStore(),
        };
    },
    computed: {
        currentName: function () {
            if (this.currentEntry) {
                return this.currentEntry.name;
            }
            return "";
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
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.store.addFilter(
                {filterType: "matricule_id", tag: matricule, value: matricule}
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
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.currentPage = 1;
            this.loadEntries();
        },
        showInfo: function (entry) {
            this.currentEntry = entry;
            this.$refs.infoModal.show();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.delete("/appels/api/appel/" + this.currentEntry.id, token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
        },
        processEntry: function(index) {
            this.processing = true;
            this.editEntry(index);
        },
        loadEntries: function () {
            axios.get("/appels/api/appel/?page=" + this.currentPage + this.filter + this.ordering)
                .then(response => {
                    this.entries = response.data.results;
                    this.entriesCount = response.data.count;
                    this.loaded = true;
                });
        },
    },
    mounted: function() {
        this.store.loadEmails();
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
        this.applyFilter();
        this.loadEntries();
    },
    components: {
        "filters": Filters,
        "person-info": PersonInfo,
        "person-contact": PersonContact,
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
