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
    <b-modal size="lg" title="Exporter des données dans un fichier"
        ok-title="Créer pdf" :ok-only="true"
        :ok-disabled="!isOk"
        ref="exportModal"
        @ok="getPdf" @hidden="resetModal"
        >
        <b-tabs v-model="tabIndex">
            <b-tab title="Sommaire" active>
                <b-row>
                    <b-col>
                        <b-form-group label="Nom, prénom ou classe" label-for="input-name-classe">
                            <multiselect id="input-name-classe"
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
                                <span slot="noResult">Aucune personne trouvée.</span>

                            </multiselect>
                        </b-form-group>
                        <b-form-group label="Type de données">
                            <b-form-checkbox v-model="info">Informations</b-form-checkbox>
                            <b-form-checkbox v-model="sanction">Sanctions</b-form-checkbox>
                            <b-form-checkbox v-model="allYears">Toutes années scolaires confondues</b-form-checkbox>
                        </b-form-group>
                    </b-col>
                </b-row>
            </b-tab>
            <b-tab title="Filtre courant" disabled>
                <p>
                    Vous pouvez exporter l'affichage courant (toutes pages confondues).
                </p>
                <p>
                    Le nombre de cas filtré est de : {{ entriesCount }}
                </p>
                <b-alert variant="warning" :show="entriesCount > 100 && entriesCount < 1000">
                    Le nombre de cas est relativement grand. La génération du pdf peut prendre un certain temps.
                </b-alert>
                <b-alert variant="danger" :show="entriesCount >= 1000">
                    Le nombre de cas est très grand ! Êtes-vous sûr de vouloir exporter autant de cas ?
                </b-alert>
            </b-tab>
        </b-tabs>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Moment from 'moment';
Moment.locale('fr');

import axios from 'axios';

export default {
    props: ['entriesCount'],
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
        }
    },
    computed: {
        isOk: function () {
            if (this.tabIndex == 0) {
                return this.nameClasse;
            } else if (this.tabIndex == 1) {
                return true;
            }
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
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: 'student',
                check_access: true,
            };
            axios.post('/annuaire/api/people_or_classes/', data, token)
            .then(response => {
                if (this.searchId !== currentSearch)
                    return;

                const options = response.data.map(p => {
                    if (Number.isNaN(Number.parseInt(query[0]))) {
                        // It is a student.
                        return {display: p.last_name + ' ' + p.first_name + ' – ' + p.teaching.display_name, id: p.matricule}
                    } else {
                        // It is a classe.
                        return p;
                    }
                })
                this.nameClasseOptions = options;
            });
        },
        getPdf: function (evt) {
            evt.preventDefault();

            let path = '/dossier_eleve/get_pdf/';
            path += this.allYears ? '1/' : '0/' ;

            if ('letter' in this.nameClasse) {
                // It is a classe.
                path += this.nameClasse.year + this.nameClasse.letter + '/';
            } else {
                // It is a student.
                path += this.nameClasse.id + '/';
            }
            path += this.info ? '1/' : '0/';
            path += this.sanction ? '1/' : '0/';

            window.open(path);
        },
    },
    mounted: function () {
        this.show();
    },
    components: {Multiselect},
}
</script>

<style>
</style>
