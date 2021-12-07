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
        <b-container>
            <b-row>
                <h2>Plan Individuel d'Apprentissage</h2>
            </b-row>
            <b-row>
                <b-col v-if="canAddPia">
                    <b-btn
                        variant="success"
                        to="/new"
                    >
                        <b-icon
                            icon="plus"
                            scale="1.5"
                        />
                        Ajouter un PIA
                    </b-btn>
                </b-col>
                <b-col>
                    <multiselect
                        id="search"
                        :internal-search="false"
                        :options="studentOptions"
                        placeholder="Rechercher un étudiant"
                        @search-change="searchStudent"
                        @select="goToRecord"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        label="display"
                        track-by="matricule"
                        :show-no-options="false"
                        v-model="currentStudent"
                        preserve-search
                        :clear-on-select="false"
                    >
                        <span slot="noResult">Aucun responsable trouvé.</span>
                    </multiselect>
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
                    <pia-entry
                        v-for="(entry, index) in entries"
                        :key="entry.id"
                        :row-data="entry"
                        @delete="deleteRecord(index)"
                    />
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import Vue from "vue";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import Multiselect from "vue-multiselect";

import PiaEntry from "./pia_entry.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

/**
 * The main PIA component. It lists all of the PIA records.
 */
export default {
    data: function () {
        return {
            entries: [],
            currentPage: 1,
            entriesCount: 0,
            studentOptions: [],
            canAddPia: false,
            currentStudent: null,
            searchId: -1,
        };
    },
    methods: {
        /**
         * Move to the PIA record page.
         * 
         * @param {object} student A student object with the matricule.
         */
        goToRecord: function (student) {
            this.$router.push(`/edit/${student.pia}/`);
        },
        /**
         * Search for a student.
         * 
         * @param {String} search The current search.
         */
        searchStudent: function (search) {
            this.searchId += 1;
            const currentSearch = this.searchId;
            axios.get(`/pia/api/pia/?student__last_name=${search}`)
                .then(resp => {
                    if (currentSearch < this.searchId) return;
                    this.studentOptions = resp.data.results.map(p => {
                        return {
                            "display": p.student.display,
                            "matricule": p.student.matricule,
                            "pia": p.id,
                        };
                    });
                });
        },
        /**
         * Delete a PIA record.
         * 
         * @param {Number} index Index of the pia entry.
         */
        deleteRecord: function (index) {
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer ce PIA ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    axios.delete("/pia/api/pia/" + this.entries[index].id + "/", token)
                        .then(() => this.entries.splice(index, 1))
                        .catch(err => alert(err));
                }
            });
        },
        /**
         * Change the currently displayed page.
         * 
         * @param {Number} page The page number to display.
         */
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
        },
        /** Load or reload PIA entries. */
        loadEntries: function () {
            const ordering = "ordering=student__classe__year,student__classe__letter";
            axios.get("/pia/api/pia/?" + ordering + "&page=" + this.currentPage)
                .then(resp => {
                    this.entries = resp.data.results;
                    this.entriesCount = resp.data.count;
                });
        },
    },
    mounted: function () {
        this.loadEntries();
        // eslint-disable-next-line no-undef
        this.canAddPia = canAddPIA;

        this.$store.dispatch("loadOptions");
    },
    components: {
        PiaEntry,
        Multiselect
    }
};
</script>
