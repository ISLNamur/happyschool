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
        <div class="loading" v-if="!loaded"></div>
        <b-container v-if="loaded">
            <b-row>
                <h2>Infirmerie</h2>
            </b-row>
            <b-row>
                <b-col>
                    <b-form-group>
                        <div>
                            <!--change modal to page-->
                            <b-button variant="outline-success" to="/new/">
                                <icon name="plus" scale="1" color="green"></icon>
                                Ajouter un malade
                            </b-button>
                            <b-button variant="outline-secondary" v-b-toggle.filters>
                                <icon name="search" scale="1"></icon>
                                Ajouter des filtres
                            </b-button>
                            <b-button :pressed.sync="active" variant="primary">
                                <span v-if="active">Afficher tous les malades</span>
                                <span v-else>Afficher les malades présents</span>
                            </b-button>
                        </div>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                        <b-collapse id="filters" v-model=showFilters>
                            <b-card>
                                <filters app="infirmerie" model="infirmerie" ref="filters" @update="applyFilter"></filters>
                            </b-card>
                        </b-collapse>
                    </b-col>
            </b-row>
            <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
            </b-pagination>
            <infirmerie-entry
                v-for="(entry, index) in entries"
                v-bind:key="entry.id"
                v-bind:row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index, false)"
                @sortie="editEntry(index, true)"
                @filterStudent="filterStudent($event)"
                @showInfo="showInfo(entry)"
                >
            </infirmerie-entry>
        </b-container>
        <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered
            @ok="deleteEntry" @cancel="currentEntry = null"
            :no-close-on-backdrop="true" :no-close-on-esc="true">
            Êtes-vous sûr de vouloir supprimer ce passage ?
        </b-modal>
        <b-modal :title="currentName" size="lg" ref="infoModal" centered ok-only @hidden="currentEntry = null">
            <info v-if="currentEntry" :matricule="currentEntry.matricule_id" type="student" no-news></info>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import VueRouter from 'vue-router'

Vue.use(VueRouter)

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Info from '../annuaire/info.vue'

import Filters from '../common/filters.vue'
import Menu from '../common/menu.vue'

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
import InfirmerieEntry from './infirmerieEntry.vue'

Vue.component('icon', Icon);
Vue.component('infirmerie-entry', InfirmerieEntry);

Vue.use(BootstrapVue);
export default {
    data: function () {
        return {
            menu: {},
            loaded: false,
            active: true,
            currentPage: 1,
            showFilters: false,
            filter: "",
            ordering: "&ordering=-datetime_arrive",
            currentEntry: null,
            entries: [],
            entriesCount: 0,
            inputStates: {
                "name": null,
            }
        }
    },
    computed: {
        currentName: function () {
            return "";
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
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
        },
        showInfo: function (entry) {
            this.currentEntry = entry
            this.$refs.infoModal.show();
        },
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit('addFilter',
                {filterType: 'matricule_id', tag: matricule, value: matricule}
            );
            this.applyFilter();
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
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/infirmerie/api/passage/' + this.currentEntry.id, token)
            .then(response => {
                this.loadEntries();
            });

            this.currentEntry = null;
        },
        editEntry: function(index, sortie) {
            this.currentEntry = this.entries[index];
        },
        loadEntries: function () {
            axios.get('/infirmerie/api/passage/?page=' + this.currentPage + this.filter + this.ordering)
            .then(response => {
                this.entries = response.data.results;
                this.entriesCount = response.data.count;
                this.loaded = true;
            });
        },
    },
    mounted: function() {
        this.menu = menu;
        this.applyFilter();
    },
    components: {
        'filters': Filters,
        'app-menu': Menu,
        'info': Info,
    },
}
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
