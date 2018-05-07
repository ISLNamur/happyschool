<template>
    <div>
    <b-container>
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
            v-on:delete="askDelete(entry.id)"
            v-on:edit="editEntry(index)"
            >
        </appel-entry>
    </b-container>
    <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered @ok="deleteEntry">
        Êtes-vous sûr de vouloir supprimer cet appel ?
    </b-modal>
    <component v-bind:is="currentModal" ref="dynamicModal" @update="loadEntries"></component>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import Filters from '../common/filters.vue'
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
            currentEntry: -1,
            currentModal: 'add-modal',
            filter: "",
        }
    },
    methods: {
        changePage: function (page) {
            return;
        },
        applyFilter: function(filters) {
            console.log(filters);
            this.filter = "";
            for (var key in filters) {
                if (filters.hasOwnProperty(key)) {
                    if (key.startsWith("date") || key.startsWith("time")) {
                        let ranges = filters[key][0].split("_");
                        this.filter += "&" + key + "__gt=" + ranges[0] + "&" + key + "__lt=" + ranges[1];
                    } else {
                        this.filter += "&" + key + "=" + filters[key][0];
                    }
                }
            }
            this.loadEntries();
        },
        askDelete: function (id) {
            this.currentEntry = id;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            axios.delete('/appels/api/appel/' + this.currentEntry,
            { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'})
            .then(response => {
                this.loadEntries();
            });
        },
        editEntry: function (id) {

        },
        loadEntries: function () {
            axios.get('/appels/api/appel/?page=' + this.currentPage + this.filter)
            .then(response => {
                this.entries = response.data.results;
            });
        },
        openDynamicModal: function (modal) {
            this.currentModal = modal;
            this.$refs.dynamicModal.show();
        }
    },
    mounted: function() {
        // const params = ({params: {page: this.currentPage}});
        this.loadEntries();
    },
    components: {
        'add-modal': AddModal,
        'filters': Filters,
        // 'export-form': ExportForm,
    },
};
</script>

<style>

</style>
