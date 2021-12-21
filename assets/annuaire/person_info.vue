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
    <div id="info-student">
        <b-container>
            <b-btn
                class="mb-2"
                v-if="!noNews"
                @click="$router.go(-1)"
            >
                Retour
            </b-btn>
            <b-card
                :title="lastName + ' ' + firstName"
                no-body
            >
                <b-tabs card>
                    <b-tab
                        :title="tabTitle"
                        active
                    >
                        <b-row>
                            <b-col
                                md="5"
                                sm="12"
                            >
                                <div>
                                    <b-img
                                        rounded
                                        fluid
                                        :src="photoPath"
                                        alt="Photo"
                                    />
                                </div>
                            </b-col>
                            <b-col>
                                <dl class="row">
                                    <dt class="col-5 text-right">
                                        Nom
                                    </dt>
                                    <dd class="col-7">
                                        {{ lastName }}
                                    </dd>
                                    <dt class="col-5 text-right">
                                        Prénom
                                    </dt>
                                    <dd class="col-7">
                                        {{ firstName }}
                                    </dd>
                                    <dt
                                        v-if="type === 'student'"
                                        class="col-5 text-right"
                                    >
                                        Matricule
                                    </dt>
                                    <dd
                                        v-if="type === 'student'"
                                        class="col-7"
                                    >
                                        {{ matricule }}
                                    </dd>
                                    <dt
                                        v-if="tenure"
                                        class="col-5 text-right"
                                    >
                                        Titulariat
                                    </dt>
                                    <dd
                                        v-for="(t, index) in tenure"
                                        :key="t.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                                    >
                                        {{ t.year }}{{ t.letter.toUpperCase() }}
                                    </dd>
                                    <dd
                                        v-if="tenure && tenure.length == 0"
                                        class="col-7"
                                    />

                                    <dt class="col-5  text-right">
                                        Enseignement(s)
                                    </dt>
                                    <dd
                                        v-for="(t, index) in teachings"
                                        :key="t.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                                    >
                                        {{ t.display_name }}
                                    </dd>
                                    <dt
                                        v-if="classe.length > 0"
                                        class="col-5  text-right"
                                    >
                                        Classe(s)
                                    </dt>
                                    <dd
                                        v-for="(c, index) in classe"
                                        :key="c.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                                    >
                                        {{ c.year }}{{ c.letter.toUpperCase() }}
                                    </dd>
                                    <dt
                                        v-if="courses.length > 0"
                                        class="col-5  text-right"
                                    >
                                        Cours
                                    </dt>
                                    <dd
                                        v-for="(c, index) in courses"
                                        :key="c.id"
                                        :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                                    >
                                        <span v-if="c.course.long_name">
                                            {{ c.course.long_name }}
                                        </span>
                                        <span v-else>
                                            {{ c.course.short_name }}
                                        </span>
                                        <span v-if="c.group !== ''">
                                            ({{ c.group.toUpperCase() }})
                                        </span>
                                    </dd>
                                    <dt
                                        v-if="student_info.orientation"
                                        class="col-5 text-right"
                                    >
                                        Orientation
                                    </dt>
                                    <dd
                                        class="col-7"
                                        v-if="student_info.orientation"
                                    >
                                        {{ student_info.orientation }}
                                    </dd>
                                    <dt
                                        v-if="student_info.previous_classe"
                                        class="col-5 text-right"
                                    >
                                        Classe précédente
                                    </dt>
                                    <dd
                                        class="col-7"
                                        v-if="student_info.previous_classe"
                                    >
                                        {{ student_info.previous_classe }}
                                    </dd>
                                    <dt
                                        class="col-5 text-right"
                                        v-if="emailSchool"
                                    >
                                        Courriel de l'école
                                    </dt>
                                    <dd
                                        class="col-7"
                                        v-if="emailSchool"
                                    >
                                        {{ emailSchool }}
                                    </dd>
                                </dl>
                                <dl
                                    class="row"
                                    v-if="$store.state.settings.show_credentials"
                                >
                                    <dt
                                        v-if="username"
                                        class="col-5 text-right"
                                    >
                                        Nom d'utilisateur
                                    </dt>
                                    <dd
                                        v-if="username"
                                        class="col-7"
                                    >
                                        {{ username }}
                                    </dd>
                                    <dt
                                        v-if="password"
                                        class="col-5 text-right"
                                    >
                                        Mot de passe
                                    </dt>
                                    <dd
                                        v-if="password && showPassword"
                                        class="col-7"
                                    >
                                        {{ password }}
                                    </dd>
                                    <dd
                                        v-else-if="password"
                                        class="col-7"
                                    >
                                        <b-btn
                                            size="sm"
                                            variant="light"
                                            @click="showPassword = true"
                                        >
                                            Montrer le mot de passe
                                        </b-btn>
                                    </dd>
                                </dl>
                            </b-col>
                        </b-row>
                        <b-row v-if="important.length > 0">
                            <b-col>
                                <b-card
                                    no-body
                                    class="mb-1"
                                >
                                    <b-card-header
                                        header-tag="header"
                                        class="p-1"
                                    >
                                        <b-btn
                                            block
                                            href="#"
                                            v-b-toggle.infos-importantes
                                            variant="danger"
                                        >
                                            Infos importantes
                                        </b-btn>
                                    </b-card-header>
                                    <b-collapse id="infos-importantes">
                                        <b-card-body>
                                            <b-row>
                                                <b-col cols="2">
                                                    <strong>Date</strong>
                                                </b-col>
                                                <b-col cols="3">
                                                    <strong>Objet/Motif</strong>
                                                </b-col>
                                                <b-col><strong>Message</strong></b-col>
                                            </b-row>
                                            <b-row
                                                v-for="cas in important"
                                                :key="cas.id"
                                                class="mb-2"
                                            >
                                                <b-col cols="2">
                                                    {{ niceDate(cas.datetime_encodage) }}
                                                </b-col>
                                                <b-col cols="3">
                                                    {{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}
                                                </b-col>
                                                <b-col><div v-html="cas.explication_commentaire" /></b-col>
                                            </b-row>
                                        </b-card-body>
                                    </b-collapse>
                                </b-card>
                            </b-col>
                        </b-row>
                    </b-tab>
                    <person-schedule
                        v-if="$store.state.settings.show_schedule"
                        :courses="courses"
                    />
                    <sensitive-info
                        v-if="sensitive"
                        :info="sensitive"
                        :type="type"
                    />
                    <contact-info
                        v-if="contact"
                        :contact="contact"
                    />
                    <medical-info
                        v-if="medical"
                        :medical="medical"
                    />
                    <b-tab
                        v-if="!noNews && this.type != 'responsible'"
                        :key="infoCount"
                    >
                        <template slot="title">
                            Info générales
                            <b-badge variant="info">
                                {{ infoCount }}
                            </b-badge>
                        </template>
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
                                    <b-btn :href="'/dossier_eleve/?matricule=' + matricule ">
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
                                    <b-btn :href="`/lateness/?student__matricule=${this.matricule}`">
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
                        <p v-if="infoCount > 0">
                            <em>Aucune donnée concernant l'élève n'est présente.</em>
                        </p>
                    </b-tab>
                    <template #tabs-end>
                        <b-nav-item
                            role="presentation"
                            v-if="pia"
                            :href="`/pia/#/edit/${pia.id}/`"
                        >
                            <strong>PIA</strong>
                        </b-nav-item>
                    </template>
                </b-tabs>
            </b-card>
        </b-container>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import ContactInfo from "./contact_info.vue";
import MedicalInfo from "./medical_info.vue";
import SensitiveInfo from "./sensitive_info.vue";
import PersonSchedule from "./person_schedule.vue";

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
            lastName: "",
            firstName: "",
            showPassword: false,
            username: "",
            password: "",
            emailSchool: "",
            classe: [],
            courses: [],
            tenure: null,
            teachings: [],
            student_info: {},
            sensitive: null,
            contact: null,
            medical: null,
            important: [],
            dossier_eleve: null,
            appels: null,
            infirmerie: null,
            lateness: null,
            infoCount: 0,
            moreInfo: false,
            pia: null,
        };
    },
    computed: {
        photoPath: function () {
            let path = "/static/photos";
            if (this.type == "responsible") path += "_prof";
            return path + "/" + this.matricule + ".jpg";
        },
        tabTitle: function () {
            const start = "Fiche ";
            return this.type === "student" ? start + "de l'élève" : start + "du responsable";
        },
    },
    watch: {
        matricule: function () {
            this.loadInfo();
        },
    },
    methods: {
        reset: function () {
            this.username = "";
            this.password = "";
            this.emailSchool = "";
            this.student_info = {};
            this.sensitive = null;
            this.contact = null;
            this.medical = null;
            this.showPassword = false;
            this.tenure = null;
            this.important = [];
            this.dossier_eleve = null;
            this.appels = null;
            this.infirmerie = null;
            this.infoCount = 0;
            this.pia = null;
            this.classe = [];
            this.courses = [];
            this.lateness = null;
        },
        niceDate: function (date) {
            if (!date) return "";

            return Moment(date).calendar();
        },
        niceTime: function (date) {
            if (!date) return "";

            return Moment(date).format("HH:mm");
        },
        loadInfo: function () {
            this.reset();

            if (this.type == "student") {
                axios.get("/annuaire/api/student/" + this.matricule + "/")
                    .then(response => {
                        this.lastName = response.data.last_name;
                        this.firstName = response.data.first_name;
                        this.classe = [response.data.classe];
                        this.teachings = [response.data.teaching];
                        this.courses = response.data.courses.sort((a, b) => a.course.name >= b.course.name);
                    });

                axios.get("/annuaire/api/student_sensitive/" + this.matricule + "/")
                    .then(response => {
                        this.sensitive = response.data;
                    })
                    .catch(err => {
                        console.log(err);
                    });

                axios.get("/annuaire/api/info_general/" + this.matricule + "/")
                    .then(response => {
                        this.student_info = response.data;
                        this.username = this.student_info.username;
                        this.password = this.student_info.password.length > 15 ? "Indisponible" : this.student_info.password;
                    });

                axios.get("/annuaire/api/info_contact/" + this.matricule + "/")
                    .then(response => {
                        this.contact = response.data;
                    });

                axios.get("/annuaire/api/info_medical/" + this.matricule + "/")
                    .then(response => {
                        this.medical = response.data;
                    });

                axios.get("/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&activate_important=true&matricule_id=" + this.matricule)
                    .then(response => {
                        this.important = response.data.results;
                    });
                
                if (!this.noNews) {
                    let promises = [];
                    let apps = [];
                    // eslint-disable-next-line no-undef
                    const userMenu = menu;
                    if (userMenu.apps.find(a => a.app == "dossier_eleve")) {
                        promises.push(axios.get("/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&matricule_id=" + this.matricule));
                        apps.push("dossier_eleve");
                    }
                    if (userMenu.apps.find(a => a.app == "appels")) {
                        promises.push(axios.get("/appels/api/appel/?ordering=-datetime_appel&matricule_id=" + this.matricule));
                        apps.push("appels");
                    }
                    if (userMenu.apps.find(a => a.app == "infirmerie")) {
                        promises.push(axios.get("/infirmerie/api/passage/?ordering=-datetime_passage&matricule_id=" + this.matricule));
                        apps.push("infirmerie");
                    }
                    if (userMenu.apps.find(a => a.app == "lateness")) {
                        promises.push(axios.get(`/lateness/api/lateness/?student__matricule=${this.matricule}&scholar_year=${getCurrentScholarYear()}`));
                        apps.push("lateness");
                    }
                    Promise.all(promises)
                        .then((response) => {
                            response.forEach((resp, index) => {
                                this[apps[index]] = resp.data;
                                this.infoCount += resp.data.count;
                            });
                        });

                    // Add a PIA link.
                    if (userMenu.apps.find(a => a.app == "pia")) {
                        axios.get("/pia/api/pia/?student__matricule=" + this.matricule)
                            .then(resp => {
                                this.pia = resp.data.count > 0 ? resp.data.results[0] : null;
                            });
                    }
                }
            } else if (this.type == "responsible") {
                axios.get("/annuaire/api/responsible/" + this.matricule + "/")
                    .then(response => {
                        this.lastName = response.data.last_name;
                        this.firstName = response.data.first_name;
                        this.classe = response.data.classe.sort((a, b) => a.year + a.letter >= b.year + b.letter);
                        this.courses = response.data.courses.sort((a, b) => a.course.name >= b.course.name);
                        this.teachings = response.data.teaching;
                        this.tenure = response.data.tenure;
                        this.emailSchool = response.data.email_school;
                    });

                axios.get("/annuaire/api/responsible_sensitive/" + this.matricule + "/")
                    .then(response => {
                        this.username = response.data.user.username;
                        this.password = response.data.password.length > 15 ? "Indisponible" : response.data.password;
                        this.sensitive = {email: response.data.email};
                    });
            }
        }
    },
    mounted: function () {
        this.loadInfo();
    },
    components: {
        ContactInfo,
        MedicalInfo,
        SensitiveInfo,
        PersonSchedule,
    }
};
</script>

<style>
.important {
    background-color: rgba(255, 0, 0, 0.3);
}
</style>
