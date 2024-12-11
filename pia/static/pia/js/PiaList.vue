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
            <BRow>
                <h2>Plan Individuel d'Apprentissage</h2>
            </BRow>
            <BRow>
                <BCol
                    v-if="canAddPia"
                    cols="12"
                    sm="3"
                >
                    <BDropdown variant="success">
                        <template #button-content>
                            <IBiPlus
                                scale="1.5"
                            />
                            Ajouter
                        </template>
                        <BDropdownItem to="/new/true/">
                            PIA
                        </BDropdownItem>
                        <BDropdownItem to="/new/false/">
                            Aide élève
                        </BDropdownItem>
                    </BDropdown>
                </BCol>
                <BCol>
                    <BFormGroup
                        label="Filtrer PIA/Aide"
                        label-cols="12"
                        label-cols-md="5"
                    >
                        <BFormSelect
                            v-model="filterAdvanced"
                            :options="filterOptions"
                            @update:model-value="loadEntries"
                        />
                    </BFormGroup>
                </BCol>
                <BCol>
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
                </BCol>
            </BRow>
            <BRow class="mt-2">
                <BCol>
                    <BAlert
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
                    </BAlert>
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BPagination
                        :value="currentPage"
                        :total-rows="entriesCount"
                        :per-page="entriesPerPage"
                        @update:model-value="changePage"
                        class="mt-1"
                    />
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <pia-entry
                        v-for="(entry, index) in entries"
                        :key="entry.id"
                        :row-data="entry"
                        @delete="deleteRecord(index)"
                    />
                </BCol>
            </BRow>
        </BContainer>
    </div>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";
import { displayStudent } from "@s:core/js/common/utilities.js";

import Multiselect from "vue-multiselect";

import PiaEntry from "./pia_entry.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

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

            return Math.ceil(this.entriesCount / 20);
        }
    },
    methods: {
        displayStudent: displayStudent,
        /**
         * Move to another page.
         * 
         * @param {Number} pageNum The page number
         */
        changePage: function (pageNum) {
            this.$router.push(`/page/${pageNum}/`);
            scroll(0, 0);
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
