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
        <BToastOrchestrator />
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
                            class="mb-2"
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
                            :placeholder="advancedSearchSelected.desc"
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
                <BCol md="2">
                    <BButton
                        v-b-toggle.collapseAdvancedSearch
                        variant="outline-primary"
                    >
                        Recherche avancée
                    </BButton>
                    <BCollapse
                        id="collapseAdvancedSearch"
                        class="mt-2"
                    >
                        <BFormGroup 
                            label="Type de recherche :"
                        >
                            <BFormSelect
                                v-model="advancedSearchSelected"
                                :options="advancedSearchOptions"
                                :select-size="1"
                            />
                        </BFormGroup>
                    </BCollapse>
                </BCol>
            </BRow>
            <BRow>
                <BFormGroup>
                    <BCol>
                        <div>
                            <BTable
                                responsive
                                hover 
                                :items="phoneNumberResults"
                            >
                                <template #cell(student)="data">
                                    <!-- `data.value` is the value after formatted by the Formatter -->
                                    <!-- <RouterLink to="/person/student/{{data.item.student}}">
                                    {{ data.item.student }}
                                </RouterLink> -->
                                    <a :href="`/annuaire/#/person/student/${data.item.student}`">
                                        {{ data.item.student }}
                                    </a>
                                </template>
                            </BTable>
                        </div>
                    </BCol>
                </BFormGroup>
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
import { BCol, BFormGroup, BRow,BCollapse } from "bootstrap-vue-next";
import { RouterLink } from "vue-router";
import { options } from "@fullcalendar/core/preact.js";

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
            phoneNumber: "",
            phoneNumberResults:[],
            advancedSearchSelected: {value:"default",desc:"Rechercher un étudiant, une classe, un professeur, …"},
            advancedSearchOptions:[
                {text:"Normale",value:{value:"default",desc:"Rechercher un étudiant, une classe, un professeur, …"}},
                {text:"Par téléphone",value:{value:"phone",desc:"Rechercher par numéro de téléphone fix ou GSM ex: 0470.00.00.00 …"}},
                {text:"Par e-mail",value:{value:"email",desc:"Rechercher par e-mail ex: adresse@email.be"}},
            ],
        };
    },
    methods: {
        selected: function (option) {
            if (option.type == "classe") {
                this.$router.push(`/classe/${option.id}/`);
                return;
            }else if(option.type == "phone"){
                this.$router.push(`/person/student/${option.id}/contact`);
            }
            else {
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
            console.log(query);
            if (this.advancedSearchSelected.value == "phone")
            {
                query = this.numberPhoneConvertor(query);
                console.log("convert and query: "+query);
                axios.get(`api/yellowpage/${query}/`)
                    .then(response => {
                        console.log(response.data);
                        const options = response.data.map(p => {
                            return {
                                display: p.display,
                                id: p.matricule,
                                type: "phone",
                            };
                        });
                        this.searchOptions = options;
                    })
                    .catch(err => {
                        console.log(err);
                    });
            }
            else if(this.advancedSearchSelected.value == "email"){
                axios.get(`api/emailsearcher/${query}/`)
                    .then(response => {
                        console.log(response.data);
                        const options = response.data.map(p => {
                            return {
                                display: p.display,
                                id: p.matricule,
                                type: "phone",
                            };
                        });
                        this.searchOptions = options;
                    })
                    .catch(err => {
                        console.log(err);
                    });
            }
            else{
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
            }

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
        numberPhoneConvertor(numberPhone){
            var numberPhoneConverted;
            if(numberPhone.length == 10){
                console.log("is Mobile");
                numberPhoneConverted = `${numberPhone.substring(0,4)}.${numberPhone.substring(4,6)}.${numberPhone.substring(6,8)}.${numberPhone.substring(8,10)}`; 
            }else if (numberPhone.length == 9){
                console.log("is Fix");
                numberPhoneConverted = `${numberPhone.substring(0,3)}.${numberPhone.substring(3,5)}.${numberPhone.substring(5,7)}.${numberPhone.substring(7,9)}`; 
            }
            else{
                numberPhoneConverted = numberPhone;
            }
            console.log(numberPhoneConverted);
            return numberPhoneConverted;
        } 
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
