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
        <app-menu
            v-if="loaded"
            :menu-info="menuInfo"
        />
        <BContainer v-if="loaded">
            <h1>Annuaire</h1>
            <BRow>
                <BCol
                    v-if="teachingsOptions.length > 1"
                    md="2"
                    sm="12"
                >
                    <BFormGroup label="Établissement(s) :">
                        <BFormSelect
                            multiple
                            :select-size="3"
                            v-model="teachings"
                            :options="teachingsOptions"
                            value-field="id"
                            text-field="display_name"
                        />
                    </BFormGroup>
                </BCol>
                <BCol>
                    <BFormGroup
                        label="Recherche :"
                        class="ml-4"
                    >
                        <multiselect
                            ref="input"
                            :show-no-options="false"
                            :internal-search="false"
                            :options="searchOptions"
                            @search-change="getSearchOptions"
                            :loading="searchLoading"
                            placeholder="Rechercher un étudiant, une classe, un professeur, …"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="id"
                            v-model="search"
                            @select="selected"
                        >
                            <template #noResult>
                                Aucune personne trouvée.
                            </template>
                            <template #noOptions />
                        </multiselect>
                    </BFormGroup>
                </BCol>
            </BRow>
            <router-view v-slot="{ Component }">
                <transition
                    name="slide-right"
                    mode="out-in"
                >
                    <component :is="Component" />
                </transition>
            </router-view>
        </BContainer>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import Menu from "@s:core/js/common/menu_bar.vue";

export default {
    data: function () {
        return {
            menuInfo: {},
            loaded: false,
            searchId: 0,
            teachings: [],
            teachingsOptions: [],
            search: null,
            searchOptions: [],
            searchLoading: false,

        };
    },
    methods: {
        selected: function (option) {
            if (option.type == "classe") {
                this.$router.push(`/classe/${option.id}/`);
                return;
            } else {
                this.$router.push(`/person/${option.type}/${option.id}/`);
            }
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.teachings.length > 0 ? this.teachings : this.teachingsOptions.map(t => t.id),
                people: "all",
                active: false,
                check_access: false,
            };
            axios.post("/annuaire/api/people_or_classes/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;

                    const options = response.data.map(p => {
                        if (Number.isNaN(Number.parseInt(query[0]))) {
                        // It is a student or a responsible.
                            if ("is_secretary" in p) {
                            // It is a responsible.
                                let teachings = " —";
                                for (let t in p.teaching) {
                                    teachings += " " + p.teaching[t].display_name;
                                }

                                return {
                                    display: p.last_name + " " + p.first_name + teachings,
                                    id: p.matricule,
                                    type: "responsible",
                                };
                            } else {
                            // It is a student.
                                return {
                                    display: p.display,
                                    id: p.matricule,
                                    type: "student",
                                };
                            }
                        } else {
                        // It is a classe.
                            let classe = p;
                            classe.type = "classe";
                            return classe;
                        }
                    });

                    this.searchOptions = options;
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
                                axios.get("/annuaire/api/student/" + refInput.search + "/")
                                    .then(resp => {
                                        if (resp.data) {
                                            this.$router.push(`/person/student/${refInput.search}/`);
                                            refInput.search = "";
                                        }
                                    })
                                    .catch(() => {
                                        console.log("Aucun étudiant trouvé");
                                    });
                            }
                        }
                    });
                    return input;
                } else {
                    this.overloadInput();
                }
            }, 300);
            
        },
    },
    mounted: function () {
        axios.get("/core/api/teaching/")
            .then(response => {
                this.teachingsOptions = response.data.results;
                this.loaded = true;
            });

        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
        this.overloadInput();
    },
    components: {
        "multiselect": Multiselect,
        "app-menu": Menu,
    }
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
