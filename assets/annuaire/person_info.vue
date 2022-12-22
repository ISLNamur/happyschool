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
        <b-overlay :show="loading">
            <b-row v-if="person">
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
                            {{ person.last_name }}
                        </dd>
                        <dt class="col-5 text-right">
                            Prénom
                        </dt>
                        <dd class="col-7">
                            {{ person.first_name }}
                        </dd>
                        <dt
                            v-if="personType === 'student'"
                            class="col-5 text-right"
                        >
                            Matricule
                        </dt>
                        <dd
                            v-if="personType === 'student'"
                            class="col-7"
                        >
                            {{ person.matricule }}
                        </dd>
                        <dt
                            v-if="personType === 'responsible'"
                            class="col-5 text-right"
                        >
                            Titulariat
                        </dt>
                        <dd
                            v-for="(t, index) in person.tenure"
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
                            v-for="(t, index) in person.teaching"
                            :key="t.id"
                            :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                        >
                            {{ t.display_name }}
                        </dd>
                        <dt
                            v-if="person.classe.length > 0"
                            class="col-5  text-right"
                        >
                            Classe(s)
                        </dt>
                        <dd
                            v-for="(c, index) in person.classe"
                            :key="c.id"
                            :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                        >
                            {{ c.year }}{{ c.letter.toUpperCase() }}
                        </dd>
                        <dt
                            v-if="person.courses.length > 0"
                            class="col-5  text-right"
                        >
                            Cours
                        </dt>
                        <dd
                            v-for="(c, index) in person.courses"
                            :key="c.id"
                            :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                        >
                            <a :href="`/annuaire/#/course/${c.course.id}/`">
                                <span
                                    v-if="c.course.long_name" 
                                    v-b-tooltip
                                    :title="`${c.course.short_name} (${c.group.toUpperCase()})`"
                                >
                                    {{ c.course.long_name }}
                                </span>
                                <span v-else>
                                    {{ c.course.short_name }}
                                </span>
                                <span v-if="c.group !== ''">
                                    ({{ c.classes }})
                                </span>
                            </a>
                        </dd>
                        <dt
                            v-if="personType === 'student' && person.orientation"
                            class="col-5 text-right"
                        >
                            Orientation
                        </dt>
                        <dd
                            class="col-7"
                            v-if="personType === 'student' && person.orientation"
                        >
                            {{ person.orientation }}
                        </dd>
                        <dt
                            v-if="personType === 'student' && person.previous_classe"
                            class="col-5 text-right"
                        >
                            Classe précédente
                        </dt>
                        <dd
                            class="col-7"
                            v-if="personType === 'student' && person.previous_classe"
                        >
                            {{ person.previous_classe }}
                        </dd>
                        <dt
                            class="col-5 text-right"
                            v-if="personType === 'responsible' && person.email_school"
                        >
                            Courriel de l'école
                        </dt>
                        <dd
                            class="col-7"
                            v-if="personType === 'responsible' && person.email_school"
                        >
                            {{ person.email_school }}
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
        </b-overlay>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

export default {
    data: function () {
        return {
            person: null,
            loading: true,
            username: "",
            password: "",
            important: [],
            lastName: "",
            firstName: "",
            showPassword: false,
            emailSchool: "",
            classe: [],
            courses: [],
            tenure: null,
            teachings: [],
        };
    },
    computed: {
        personType: function () {
            return this.$route.params.type;
        },
        photoPath: function () {
            const matricule = Number(this.$route.params.matricule);

            return `/static/photos${this.personType === "responsible" ? "_prof" : ""}/${matricule}.jpg`;
        },
    },
    watch: {
        "$route.params.matricule": function (to, from) {
            if (from) {
                this.loading = true;
                this.person = null;

                this.loadInfo();
            }
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
        loadInfo: function () {
            const personType = this.$router.currentRoute.params.type;
            const matricule = Number(this.$router.currentRoute.params.matricule);
            
            switch (personType) {
            case "student":
                axios.get(`/annuaire/api/student/${matricule}/`)
                    .then(response => {
                        this.person = response.data;
                        this.person.courses = this.person.courses.sort((a, b) => a.course.name >= b.course.name);
                        this.person.teaching = [this.person.teaching];
                        this.person.classe = this.person.classe ? [this.person.classe] : [];
                        this.loading = false;
                    });

                axios.get(`/annuaire/api/info_general/${matricule}/`)
                    .then(response => {
                        this.username = response.data.username;
                        this.password = response.data.password;
                    });

                axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&activate_important=true&student__matricule=${matricule}`)
                    .then(response => {
                        this.important = response.data.results;
                    });
                break;
            case "responsible":
                axios.get(`/annuaire/api/responsible/${matricule}/`)
                    .then(response => {
                        this.person = response.data;
                        this.person.courses = this.person.courses.sort((a, b) => a.course.name >= b.course.name);
                        this.person.classe = this.person.classe.sort((a, b) => a.year + a.letter >= b.year + b.letter);
                        this.loading = false;
                    });
                axios.get(`/annuaire/api/responsible_sensitive/${matricule}/`)
                    .then(response => {
                        this.username = response.data.user.username;
                        this.password = response.data.password.length > 15 ? "Indisponible" : response.data.password;
                    });
                break;
        
            default:
                break;
            }
        },
    },
    mounted: function () {
        this.loadInfo();
    },
};
</script>

<style>
.important {
    background-color: rgba(255, 0, 0, 0.3);
}
</style>
