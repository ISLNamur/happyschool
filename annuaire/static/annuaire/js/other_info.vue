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
    <b-overlay :show="loading">
        <b-card
            :header="`Derniers messages du dossier des élèves (${dossier_eleve.count} au total)`"
            class="mt-2"
            v-if="dossier_eleve && dossier_eleve.count > 0"
        >
            <b-row>
                <b-col cols="2">
                    <strong>Date</strong>
                </b-col>
                <b-col cols="2">
                    <strong>Objet/Motif</strong>
                </b-col>
                <b-col><strong>Message</strong></b-col>
            </b-row>
            <b-row
                v-for="cas in dossier_eleve.results.slice(0, 5)"
                :key="cas.id"
                class="mb-2"
            >
                <b-col
                    cols="2"
                    :class="cas.important ? ' important' : ''"
                >
                    {{ niceDate(cas.datetime_encodage) }}
                </b-col>
                <b-col
                    cols="2"
                    :class="cas.important ? ' important' : ''"
                >
                    {{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}
                </b-col>
                <b-col :class="cas.important ? ' important' : ''">
                    <div v-html="cas.explication_commentaire" />
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-btn :href="'/dossier_eleve/?matricule=' + $route.params.matricule ">
                        <b-icon
                            icon="eye"
                        />
                        Voir tous les cas dans le dossier des élèves
                    </b-btn>
                </b-col>
            </b-row>
        </b-card>
        <b-card
            :header="`Retards (${lateness.count} au total)`"
            v-if="lateness && lateness.count > 0"
            class="mt-2"
        >
            <b-row>
                <b-col>
                    Nombre de retards cette année : {{ lateness.count }}
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    Derniers retards:
                    <b-list-group-item
                        v-for="l in lateness.results.slice(0, 5)"
                        :key="l.id"
                    >
                        {{ niceDate(l.datetime_creation) }} à {{ niceTime(l.datetime_creation) }}
                    </b-list-group-item>
                </b-col>
            </b-row>
            <b-row class="mt-2">
                <b-col>
                    <b-btn :href="`/lateness/?student__matricule=${$route.params.matricule}`">
                        <b-icon
                            icon="eye"
                        />
                        Voir tous les retards
                    </b-btn>
                </b-col>
            </b-row>
        </b-card>
        <b-card
            :header="`Derniers passages à l'infirmerie (${infirmerie.count} au total)`"
            class="mt-2"
            v-if="infirmerie && infirmerie.count > 0"
        >
            <b-row>
                <b-col cols="2">
                    <strong>Arrivé</strong>
                </b-col>
                <b-col cols="2">
                    <strong>Sortie</strong>
                </b-col>
                <b-col cols="2">
                    <strong>Motifs d'admission</strong>
                </b-col>
                <b-col><strong>Remarques de sortie</strong></b-col>
            </b-row>
            <b-row
                v-for="passage in infirmerie.results.slice(0, 5)"
                :key="passage.id"
                class="mb-2"
            >
                <b-col cols="2">
                    {{ niceDate(passage.datetime_arrive) }}
                </b-col>
                <b-col cols="2">
                    {{ passage.datetime_sortie ? niceDate(passage.datetime_sortie) : '' }}
                </b-col>
                <b-col cols="2">
                    {{ passage.motifs_admission }}
                </b-col>
                <b-col>{{ passage.remarques_sortie }}</b-col>
            </b-row>
        </b-card>
        <b-card
            :header="`Derniers appels (${appels.count} au total)`"
            class="mt-2"
            v-if="appels && appels.count > 0"
        >
            <b-row>
                <b-col cols="2">
                    <strong>Date</strong>
                </b-col>
                <b-col cols="2">
                    <strong>Objet</strong>
                </b-col>
                <b-col cols="2">
                    <strong>Motif</strong>
                </b-col>
                <b-col><strong>Message</strong></b-col>
            </b-row>
            <b-row
                v-for="appel in appels.results.slice(0, 5)"
                :key="appel.id"
                class="mb-2"
            >
                <b-col cols="2">
                    {{ niceDate(appel.datetime_appel) }}
                </b-col>
                <b-col cols="2">
                    {{ appel.object.display }}
                </b-col>
                <b-col cols="2">
                    {{ appel.motive.display }}
                </b-col>
                <b-col>{{ appel.commentaire }}</b-col>
            </b-row>
        </b-card>
        <p v-if="infoCount == 0">
            <em>Aucune donnée concernant l'élève n'est présente.</em>
        </p>
    </b-overlay>
</template>


<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import {getCurrentScholarYear} from "@s:core/js/common/utilities.js";

export default {
    data: function () {
        return {
            loading: true,
            dossier_eleve: [],
            appels: [],
            infirmerie: [],
            lateness: [],
            infoCount: 0,
        };
    },
    methods: {
        niceDate: function (date) {
            if (!date) return "";

            return Moment(date).calendar();
        },
        niceTime: function (date) {
            if (!date) return "";

            return Moment(date).format("HH:mm");
        },
    },
    mounted: function () {
        let promises = [];
        let apps = [];
        // eslint-disable-next-line no-undef
        const userMenu = menu;
        if (userMenu.apps.find(a => a.app == "dossier_eleve")) {
            promises.push(axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&student__matricule=${this.$route.params.matricule}`));
            apps.push("dossier_eleve");
        }
        if (userMenu.apps.find(a => a.app == "appels")) {
            promises.push(axios.get(`/appels/api/appel/?ordering=-datetime_appel&matricule_id=${this.$route.params.matricule}`));
            apps.push("appels");
        }
        if (userMenu.apps.find(a => a.app == "infirmerie")) {
            promises.push(axios.get(`/infirmerie/api/passage/?ordering=-datetime_passage&matricule_id=${this.$route.params.matricule}`));
            apps.push("infirmerie");
        }
        if (userMenu.apps.find(a => a.app == "lateness")) {
            promises.push(axios.get(`/lateness/api/lateness/?ordering=-datetime_creation&student__matricule=${this.$route.params.matricule}&scholar_year=${getCurrentScholarYear()}`));
            apps.push("lateness");
        }
        Promise.all(promises)
            .then((response) => {
                response.forEach((resp, index) => {
                    this[apps[index]] = resp.data;
                    this.infoCount += resp.data.count;
                });
                this.loading = false;
            });
    }
};
</script>
