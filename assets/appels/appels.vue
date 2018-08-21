<template>
    <div>
        <div class="loading" v-if="!loaded"></div>
        <app-menu :menu-info="menuInfo"></app-menu>
        <b-container v-if="loaded">
            <b-row>
                <h2>Appels</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <b-button variant="outline-success" @click="openDynamicModal('add-modal')">
                                <icon name="plus" scale="1" color="green"></icon>
                                Ajouter un appel
                            </b-button>
                            <b-button variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-button>
                            <b-button :pressed.sync="active" variant="primary">
                                <span v-if="active">Afficher tous les appels</span>
                                <span v-else>Afficher les appels courant</span>
                            </b-button>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                        <b-collapse id="filters">
                            <b-card>
                                <filters app="appels" model="appel" ref="filters" @update="applyFilter"></filters>
                            </b-card>
                        </b-collapse>
                    </b-col>
            </b-row>
            <b-pagination :total-rows="entriesCount" v-model="currentPage" v-on:change="changePage">
            </b-pagination>
            <b-card no-body class="current-card d-none d-md-block d-lg-block d-xl-block">
                <b-row class="text-center">
                    <b-col cols="2"><strong>Objet</strong></b-col>
                    <b-col cols="2"><strong>Motif</strong></b-col>
                    <b-col cols="1"><strong>De</strong></b-col>
                    <b-col cols="1"><strong>À</strong></b-col>
                    <b-col cols="1"><strong>Appel</strong></b-col>
                    <b-col><strong>Commentaire(s)</strong></b-col>
                </b-row>
            </b-card>
            <appel-entry
                v-for="(entry, index) in entries"
                v-bind:key="entry.id"
                v-bind:row-data="entry"
                v-on:delete="askDelete(entry)"
                v-on:edit="editEntry(index)"
                >
            </appel-entry>
        </b-container>
        <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered @ok="deleteEntry">
            Êtes-vous sûr de vouloir supprimer cet appel ?
        </b-modal>
        <component v-bind:is="currentModal" ref="dynamicModal" :entry="currentEntry"
            @update="loadEntries" @reset="currentEntry = null">
        </component>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import Info from '../annuaire/info.vue'

import Filters from '../common/filters.vue'
import Menu from '../common/menu.vue'

import AddModal from './addModal.vue'

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
import AppelEntry from './appelEntry.vue'

Vue.component('icon', Icon);
Vue.component('appel-entry', AppelEntry);

Vue.use(BootstrapVue);
export default {
    data: function () {
        return {
            active: true,
            entriesCount: 20,
            currentPage: 1,
            entries: [],
            currentEntry: null,
            currentModal: 'add-modal',
            filter: "",
            menuInfo: {},
            loaded: false,
        }
    },
    watch: {
        active: function (isActive) {
            if (isActive) {
                this.$store.commit('addFilter',
                    {filterType: 'activate_ongoing', tag: "Activer", value: true}
                );
            } else {
                this.$store.commit('removeFilter', 'activate_ongoing');
            }
            this.applyFilter();
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
            this.currentEntry = entry.id;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/appels/api/appel/' + this.currentEntry.id, token)
            .then(response => {
                this.loadEntries();
            });
        },
        editEntry: function(index) {
            this.currentEntry = this.entries[index];
            this.openDynamicModal('add-modal');
        },
        loadEntries: function () {
            axios.get('/appels/api/appel/?page=' + this.currentPage + this.filter)
            .then(response => {
                this.entries = response.data.results;
                this.entriesCount = response.data.count;
                this.loaded = true;
            });
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            this.$refs.dynamicModal.show();
        }
    },
    mounted: function() {
        this.menuInfo = menu;

        this.applyFilter();
        this.loadEntries();
    },
    components: {
        'add-modal': AddModal,
        'filters': Filters,
        'app-menu': Menu,
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
