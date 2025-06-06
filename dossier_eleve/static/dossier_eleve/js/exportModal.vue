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
        <b-modal
            size="lg"
            title="Exporter des données dans un fichier"
            ok-title="Créer pdf"
            :ok-only="true"
            :ok-disabled="!isOk"
            ref="exportModal"
            @ok="getPdf"
            @hidden="resetModal"
        >
            <BTabs v-model:index="tabIndex">
                <BTab
                    title="Sommaire"
                    active
                >
                    <BRow>
                        <BCol>
                            <BFormGroup
                                label="Nom, prénom ou classe"
                                label-for="input-name-classe"
                            >
                                <multiselect
                                    id="input-name-classe"
                                    :internal-search="false"
                                    :options="nameClasseOptions"
                                    @search-change="getNameClasseOptions"
                                    :loading="nameClasseLoading"
                                    placeholder="Rechercher un étudiant ou une classe…"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label=""
                                    label="display"
                                    track-by="id"
                                    v-model="nameClasse"
                                >
                                    <template #noResult>
                                        Aucune personne trouvée.
                                    </template>
                                    <template #noOptions />
                                </multiselect>
                            </BFormGroup>
                            <BFormGroup label="Type de données">
                                <BFormCheckbox v-model="info">
                                    Informations
                                </BFormCheckbox>
                                <BFormCheckbox v-model="sanction">
                                    Sanctions
                                </BFormCheckbox>
                                <BFormCheckbox v-model="allYears">
                                    Toutes années scolaires confondues
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BRow>
                </BTab>
                <BTab
                    title="Filtre courant"
                >
                    <p>
                        Vous pouvez exporter l'affichage courant (toutes pages confondues).
                    </p>
                    <p>
                        Le nombre de cas filtré est de : {{ entriesCount }}
                    </p>
                    <BAlert
                        variant="warning"
                        :model-value="entriesCount > 100 && entriesCount < 1000"
                    >
                        Le nombre de cas est relativement grand. La génération du pdf peut prendre un certain temps.
                    </BAlert>
                    <BAlert
                        variant="danger"
                        :model-value="entriesCount >= 1000"
                    >
                        Le nombre de cas est très grand ! Êtes-vous sûr de vouloir exporter autant de cas ?
                    </BAlert>
                </BTab>
            </BTabs>
        </b-modal>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import {getFilters} from "@s:core/js/common/filters.js";
import {displayStudent} from "@s:core/js/common/utilities.js";

import { dossierEleveStore } from "./stores/dossier_eleve.js";

import axios from "axios";

export default {
    props: {
        "entriesCount": {
            type: Number,
            default: 0,
        },
    },
    data: function () {
        return {
            searchId: 0,
            tabIndex: 0,
            nameClasse: null,
            nameClasseOptions: [],
            nameClasseLoading: false,
            info: true,
            sanction: true,
            allYears: false,
            store: dossierEleveStore(),
        };
    },
    computed: {
        isOk: function () {
            if (this.tabIndex == 0) {
                return this.nameClasse;
            } else if (this.tabIndex == 1) {
                return true;
            }
            return false;
        },
    },
    methods: {
        show: function () {
            this.$refs.exportModal.show();
        },
        hide: function () {
            this.$refs.exportModal.hide();
        },
        resetModal: function () {
            this.nameClasse = null;
            this.info = true;
            this.sanction = true;
            this.allYears = false;
        },
        getNameClasseOptions: function (query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: "student",
                check_access: true,
                active: false,
            };

            const app = this;
            axios.post("/annuaire/api/people_or_classes/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;

                    const options = response.data.map(p => {
                        if (Number.isNaN(Number.parseInt(query[0]))) {
                        // It is a student.
                            return {display: displayStudent(p, app), id: p.matricule};
                        } else {
                        // It is a classe.
                            return p;
                        }
                    });
                    this.nameClasseOptions = options;
                });
        },
        getPdf: function (evt) {
            evt.preventDefault();

            if (this.tabIndex == 0) {
                let path = "/dossier_eleve/get_pdf/?page_size=500&";

                path += "letter" in this.nameClasse ? "classe=" : "student__matricule=";
                path += this.nameClasse.id;

                path += this.info ? "" : "&no_infos=true";
                path += this.sanction ? "" : "&no_sanctions=true";
                // eslint-disable-next-line no-undef
                path += this.allYears ? "" : "&scholar_year=" + currentYear ;
                path += "&ordering=student__last_name,-datetime_modified";

                window.open(path);
            } else if (this.tabIndex == 1) {
                const path = `/dossier_eleve/get_pdf_list/?page_size=2000${getFilters(this.store.filters)}`;
                window.open(path);
            }
        },
    },
    mounted: function () {
        this.show();
    },
    components: {Multiselect},
};
</script>

<style>
</style>
