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
        <BBreadcrumb>
            <BBreadcrumbItem
                v-if="backHistory"
                @click="$router.back()"
            >
                Retour
            </BBreadcrumbItem>
            <BBreadcrumbItem
                v-for="(item, i) in locations"
                :key="item.text"
                :to="item.to"
                :active="locations.length - 1 === i"
            >
                {{ item.text }}
            </BBreadcrumbItem>
        </BBreadcrumb>
        <BCard no-body>
            <BCard-header header-tag="nav">
                <BNav
                    card-header
                    tabs
                >
                    <BNavItem
                        :to="`/person/${type}/${matricule}/`"
                        exact
                        exact-active-class="active"
                    >
                        Fiche
                    </BNavItem>
                    <BNavItem
                        to="sensitive"
                        exact
                    >
                        Infos personnelles
                    </BNavItem>
                    <BNavItem
                        to="schedule"
                        exact
                    >
                        Horaire
                    </BNavItem>
                    <BNavItem
                        v-if="type === 'student'"
                        to="contact"
                        exact
                    >
                        Moyens de contacts
                    </BNavItem>
                    <BNavItem
                        v-if="type === 'student'"
                        to="medical"
                        exact
                    >
                        Infos médicales
                    </BNavItem>
                    <BNavItem
                        v-if="type === 'student' && !noNews"
                        to="other"
                        exact
                    >
                        Infos générales
                        <BBadge>
                            {{ infoCount }}
                        </BBadge>
                    </BNavItem>
                    <BNavItem
                        v-if="pia"
                        :href="`/pia/#/edit/${pia.id}/${pia.advanced}/`"
                        link-classes="font-weight-bold"
                    >
                        PIA
                    </BNavItem>
                </BNav>
            </BCard-header>

            <BCard-body>
                <router-view />
            </BCard-body>
        </BCard>
    </div>
</template>

<script>
import axios from "axios";

import {getCurrentScholarYear} from "@s:core/js/common/utilities.js";

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
            locations: [],
            backHistory: false,
            pia: null,
        };
    },
    methods: {
        initInfo: function () {
            if (window.history.length > 1 && !window.history.state.back) {
                this.backHistory = true;
            }
            if (this.type === "student") {
                axios.get(`/annuaire/api/student/${this.matricule}/`)
                    .then((resp) => {
                        this.locations.push({text: "Classe", to: `/classe/${resp.data.classe.id}/`});
                        this.locations.push({text: "Élève"});
                    });

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
            } else if (this.type === "responsible") {
                this.locations = [{text: "Responsable"}];
            }
        }
    },
    
    mounted: function () {
        this.initInfo();
    }
};
</script>
