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
                        <icon
                            name="plus"
                            scale="1"
                        />
                        Ajouter un PIA
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
                    <entry
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
import BootstrapVue from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";

Vue.use(BootstrapVue);
Vue.component("icon", Icon);

import Entry from "./entry.vue";

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
        };
    },
    methods: {
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
            axios.get("/pia/api/pia/?ordering=student__classe__year,student__classe__letter&page=" + this.currentPage)
                .then(resp => {
                    this.entries = resp.data.results;
                    this.entriesCount = resp.data.count;
                });
        },
    },
    mounted: function () {
        this.loadEntries();
    },
    components: {
        Entry
    }
};
</script>
