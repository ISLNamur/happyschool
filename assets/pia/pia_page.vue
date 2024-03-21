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
                <b-col
                    v-if="canAddPia"
                    cols="12"
                    sm="3"
                >
                    <b-dropdown
                        variant="success"
                    >
                        <template #button-content>
                            <b-icon
                                icon="plus"
                                scale="1.5"
                            />
                            Ajouter
                        </template>
                        <b-dropdown-item to="/new/true/">
                            PIA
                        </b-dropdown-item>
                        <b-dropdown-item to="/new/false/">
                            Aide élève
                        </b-dropdown-item>
                    </b-dropdown>
                </b-col>
                <b-col>
                    <b-form-group
                        label="Filtrer PIA/Aide"
                        label-cols="12"
                        label-cols-md="5"
                    >
                        <b-form-select
                            v-model="filterAdvanced"
                            :options="filterOptions"
                            @change="loadEntries"
                        />
                    </b-form-group>
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
                        <template #noResult>
                            Aucun élève trouvé.
                        </template>
                    </multiselect>
                </b-col>
            </b-row>
            <b-row class="mt-2">
                <b-col>
                    <b-alert
                        :show="lastPias.length > 0"
                        dismissible
                    >
                        <p>Les PIA des élèves suivants ont été modifiés récemment :</p>
                        <ul>
                            <li
                                v-for="pia in lastPias"
                                :key="pia.id"
                            >
                                <a :href="`#/edit/${pia.id}/${pia.advanced}/`">
                                    {{ displayStudent(pia.student) }}
                                </a>
                            </li>
                        </ul>
                    </b-alert>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-pagination-nav
                        class="mt-1"
                        :number-of-pages="pagesCount"
                        :link-gen="pageLink"
                        use-router
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

import { piaStore } from "./stores/index.js";
import { displayStudent } from "../common/utilities.js";

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import Multiselect from "vue-multiselect";

import PiaEntry from "./pia_entry.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

/**
 * The main PIA component. It lists all of the PIA records.
 */
export default {
    props: {
        currentPage: {
            type: Number,
            default: 1
        }
    },
    data: function () {
        return {
            entries: [],
            entriesCount: 1,
            filterAdvanced: null,
            filterOptions: [
                { value: null, text: "Tous" },
                { value: false, text: "Aide élève" },
                { value: true, text: "PIA" },
            ],
            lastPias: [],
            studentOptions: [],
            canAddPia: false,
            currentStudent: null,
            searchId: -1,
        };
    },
    watch: {
        currentPage: function () {
            this.loadEntries();
        }
    },
    computed: {
        pagesCount: function () {
            if (this.entriesCount === 0) return 1;

            return Math.ceil(this.entriesCount/20);
        }
    },
    methods: {
        displayStudent: displayStudent,
        /**
         * Generate link to other pages.
         * 
         * @param {Number} pageNum The page number
         */
        pageLink: function (pageNum) {
            return {
                path: `/page/${pageNum}/`,
            };
        },
        /**
         * Move to the PIA record page.
         * 
         * @param {object} student A student object with the matricule.
         */
        goToRecord: function (student) {
            this.$router.push(`/edit/${student.pia}/${student.advanced}/`);
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
                            "advanced": p.advanced,
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
        /** Load or reload PIA entries. */
        loadEntries: function () {
            const ordering = "ordering=student__classe__year,student__classe__letter,student__last_name";
            const advanced = this.filterAdvanced === null ? "" : `&advanced=${this.filterAdvanced}`;
            axios.get("/pia/api/pia/?" + ordering + "&page=" + this.currentPage + advanced)
                .then(resp => {
                    this.entries = resp.data.results;
                    this.entriesCount = resp.data.count;
                });
        },
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        const app = menu.apps.find(a => a.app === "pia");
        if (app && "new_items" in app && app.new_items > 0) {
            // If new_items is "20+", only keep 20.
            const new_items = isNaN(app.new_items) ? app.new_items.slice(0, 1) : app.new_items;
            axios.get(`/pia/api/pia/?ordering=-datetime_updated&page_size=${new_items}`)
                .then((resp) => {
                    this.lastPias = resp.data.results;
                });
        }

        this.loadEntries();
        // eslint-disable-next-line no-undef
        this.canAddPia = canAddPIA;

        piaStore().loadOptions();
    },
    components: {
        PiaEntry,
        Multiselect
    }
};
</script>
