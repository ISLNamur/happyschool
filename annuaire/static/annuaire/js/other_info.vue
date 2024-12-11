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
    <BOverlay :show="loading">
        <BRow v-if="canSeeSummary">
            <BCol class="text-end">
                <BButton
                    variant="outline-primary"
                    @click="summaryModal = !summaryModal"
                >
                    <IBiFilePdf />
                    Récapitulatif
                </BButton>
            </BCol>
        </BRow>
        <BCard
            :header="`Derniers messages du dossier des élèves (${dossier_eleve.count} au total)`"
            class="mt-2"
            v-if="dossier_eleve && dossier_eleve.count > 0"
        >
            <BRow>
                <BCol cols="2">
                    <strong>Date</strong>
                </BCol>
                <BCol cols="2">
                    <strong>Objet/Motif</strong>
                </BCol>
                <BCol><strong>Message</strong></BCol>
            </BRow>
            <BRow
                v-for="cas in dossier_eleve.results.slice(0, 5)"
                :key="cas.id"
                class="mb-2"
            >
                <BCol
                    cols="2"
                    :class="cas.important ? ' important' : ''"
                >
                    {{ niceDate(cas.datetime_encodage) }}
                </BCol>
                <BCol
                    cols="2"
                    :class="cas.important ? ' important' : ''"
                >
                    {{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}
                </BCol>
                <BCol :class="cas.important ? ' important' : ''">
                    <div v-html="cas.explication_commentaire" />
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    <BButton :href="'/dossier_eleve/?matricule=' + $route.params.matricule ">
                        <IBiEye />
                        Voir tous les cas dans le dossier des élèves
                    </BButton>
                </BCol>
            </BRow>
        </BCard>
        <BCard
            :header="`Retards (${lateness.count} au total)`"
            v-if="lateness && lateness.count > 0"
            class="mt-2"
        >
            <BRow>
                <BCol>
                    Nombre de retards cette année : {{ lateness.count }}
                </BCol>
            </BRow>
            <BRow>
                <BCol>
                    Derniers retards:
                    <BListGroupItem
                        v-for="l in lateness.results.slice(0, 5)"
                        :key="l.id"
                    >
                        {{ niceDate(l.datetime_creation) }} à {{ niceTime(l.datetime_creation) }}
                    </BListGroupItem>
                </BCol>
            </BRow>
            <BRow class="mt-2">
                <BCol>
                    <BButton :href="`/lateness/?student__matricule=${$route.params.matricule}`">
                        <IBiEye />
                        Voir tous les retards
                    </BButton>
                </BCol>
            </BRow>
        </BCard>
        <BCard
            :header="`Derniers passages à l'infirmerie (${infirmerie.count} au total)`"
            class="mt-2"
            v-if="infirmerie && infirmerie.count > 0"
        >
            <BRow>
                <BCol cols="2">
                    <strong>Arrivé</strong>
                </BCol>
                <BCol cols="2">
                    <strong>Sortie</strong>
                </BCol>
                <BCol cols="2">
                    <strong>Motifs d'admission</strong>
                </BCol>
                <BCol><strong>Remarques de sortie</strong></BCol>
            </BRow>
            <BRow
                v-for="passage in infirmerie.results.slice(0, 5)"
                :key="passage.id"
                class="mb-2"
            >
                <BCol cols="2">
                    {{ niceDate(passage.datetime_arrive) }}
                </BCol>
                <BCol cols="2">
                    {{ passage.datetime_sortie ? niceDate(passage.datetime_sortie) : '' }}
                </BCol>
                <BCol cols="2">
                    {{ passage.motifs_admission }}
                </BCol>
                <BCol>{{ passage.remarques_sortie }}</BCol>
            </BRow>
        </BCard>
        <BCard
            :header="`Derniers appels (${appels.count} au total)`"
            class="mt-2"
            v-if="appels && appels.count > 0"
        >
            <BRow>
                <BCol cols="2">
                    <strong>Date</strong>
                </BCol>
                <BCol cols="2">
                    <strong>Objet</strong>
                </BCol>
                <BCol cols="2">
                    <strong>Motif</strong>
                </BCol>
                <BCol><strong>Message</strong></BCol>
            </BRow>
            <BRow
                v-for="appel in appels.results.slice(0, 5)"
                :key="appel.id"
                class="mb-2"
            >
                <BCol cols="2">
                    {{ niceDate(appel.datetime_appel) }}
                </BCol>
                <BCol cols="2">
                    {{ appel.object.display }}
                </BCol>
                <BCol cols="2">
                    {{ appel.motive.display }}
                </BCol>
                <BCol>{{ appel.commentaire }}</BCol>
            </BRow>
        </BCard>
        <p v-if="infoCount == 0">
            <em>Aucune donnée concernant l'élève n'est présente.</em>
        </p>
        <BModal
            id="summary"
            v-model="summaryModal"
            ok-only
        >
            <BRow>
                <BCol>
                    <BFormGroup label="À partir de ">
                        <BFormInput
                            type="date"
                            v-model="date_from"
                        />
                    </BFormGroup>
                    <BFormGroup label="Jusqu'à ">
                        <BFormInput
                            type="date"
                            v-model="date_to"
                        />
                    </BFormGroup>
                </BCol>
            </BRow>
            <BRow>
                <BCol class="text-center">
                    <BButton
                        :href="`/annuaire/summary/student/${$route.params.matricule}/${date_from}/${date_to}/`"
                        target="_blank"
                        variant="primary"
                        :disabled="!date_from || !date_to"
                    >
                        <IBiFilePdf />
                        Télécharger
                    </BButton>
                </BCol>
            </BRow>
        </BModal>
    </BOverlay>
</template>


<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import {getCurrentScholarYear} from "@s:core/js/common/utilities.js";
import { annuaireStore } from "./stores/index.js";

export default {
    data: function () {
        return {
            loading: true,
            dossier_eleve: [],
            appels: [],
            infirmerie: [],
            lateness: [],
            infoCount: 0,
            date_from: null,
            date_to: null,
            summaryModal: false,
            store: annuaireStore(),
        };
    },
    computed: {
        canSeeSummary: function () {
            const canSeeGroups = new Set(this.store.settings.can_see_summary);
            // eslint-disable-next-line no-undef
            const userGroups = new Set(user_groups.map(g => g.id));
            return canSeeGroups.intersection(userGroups).size > 0;
        }
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
