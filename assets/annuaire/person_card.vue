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
        <b-btn
            @click="$router.back()"
            class="mb-1"
        >
            <b-icon icon="chevron-left" />
            Retour
        </b-btn>
        <b-card no-body>
            <b-card-header header-tag="nav">
                <b-nav
                    card-header
                    tabs
                >
                    <b-nav-item
                        :to="`/person/${type}/${matricule}/`"
                        exact
                        exact-active-class="active"
                    >
                        Fiche
                    </b-nav-item>
                    <b-nav-item
                        to="sensitive"
                        exact
                    >
                        Infos personnelles
                    </b-nav-item>
                    <b-nav-item
                        to="schedule"
                        exact
                    >
                        Horaire
                    </b-nav-item>
                    <b-nav-item
                        v-if="type === 'student'"
                        to="contact"
                        exact
                    >
                        Moyens de contacts
                    </b-nav-item>
                    <b-nav-item
                        v-if="type === 'student'"
                        to="medical"
                        exact
                    >
                        Infos médicales
                    </b-nav-item>
                    <b-nav-item
                        v-if="type === 'student' && !noNews"
                        to="other"
                        exact
                    >
                        Infos générales
                        <b-badge>
                            {{ infoCount }}
                        </b-badge>
                    </b-nav-item>
                    <b-nav-item
                        v-if="pia"
                        :href="`/pia/#/edit/${pia.id}/${pia.advanced}/`"
                        link-classes="font-weight-bold"
                    >
                        PIA
                    </b-nav-item>
                </b-nav>
            </b-card-header>

            <b-card-body>
                <router-view />
            </b-card-body>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import {getCurrentScholarYear} from "../common/utilities.js";
export default {
    props: {
        matricule: {
            type: Number,
            default: 0
        },
        type: {
            type: String,
            default: "student"
        },
        noNews: {
            type: Boolean,
            default: false,
        }
    },
    data: function () {
        return {
            infoCount: 0,
            pia: null,
        };
    },
    methods: {
        initInfo: function () {
            if (this.type === "student") {
                axios.get(`/pia/api/pia/?student__matricule=${this.matricule}`)
                    .then(resp => {
                        this.pia = resp.data.count > 0 ? resp.data.results[0] : null;
                    });

                let promises = [];
                let apps = [];
                // eslint-disable-next-line no-undef
                const userMenu = menu;
                if (userMenu.apps.find(a => a.app == "dossier_eleve")) {
                    promises.push(axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&student__matricule=${this.matricule}`));
                    apps.push("dossier_eleve");
                }
                if (userMenu.apps.find(a => a.app == "appels")) {
                    promises.push(axios.get(`/appels/api/appel/?ordering=-datetime_appel&matricule_id=${this.matricule}`));
                    apps.push("appels");
                }
                if (userMenu.apps.find(a => a.app == "infirmerie")) {
                    promises.push(axios.get(`/infirmerie/api/passage/?ordering=-datetime_passage&matricule_id=${this.matricule}`));
                    apps.push("infirmerie");
                }
                if (userMenu.apps.find(a => a.app == "lateness")) {
                    promises.push(axios.get(`/lateness/api/lateness/?ordering=-datetime_creation&student__matricule=${this.matricule}&scholar_year=${getCurrentScholarYear()}`));
                    apps.push("lateness");
                }
                Promise.all(promises)
                    .then((response) => {
                        response.forEach((resp) => {
                            this.infoCount += resp.data.count;
                        });
                        this.loading = false;
                    });
            }
        }
    },
    
    mounted: function () {
        this.initInfo();
    }
};
</script>
