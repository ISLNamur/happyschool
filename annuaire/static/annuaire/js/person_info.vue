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
        <BOverlay :show="loading">
            <BRow v-if="person">
                <BCol
                    md="5"
                    sm="12"
                >
                    <div>
                        <BImg
                            rounded
                            fluid
                            :src="photoPath"
                            alt="Photo"
                        />
                    </div>
                </BCol>
                <BCol>
                    <dl class="row">
                        <dt class="col-5 text-end">
                            Nom
                        </dt>
                        <dd class="col-7">
                            {{ person.last_name }}
                        </dd>
                        <dt class="col-5 text-end">
                            Prénom
                        </dt>
                        <dd class="col-7 d-flex justify-content-between align-items-center">
                            <span>
                                {{ person.first_name }}
                            </span>
                            <IBiCopy
                                @click="copyToClipboardFullname()"
                            />
                        </dd>
                        <dt
                            v-if="personType === 'student'"
                            class="col-5 text-end"
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
                            v-if="personType === 'responsible' && person.tenure.length > 0"
                            class="col-5 text-end"
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

                        <dt class="col-5  text-end">
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
                            class="col-5  text-end"
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
                            class="col-5  text-end"
                        >
                            Cours
                        </dt>
                        <dd
                            v-for="(c, index) in person.courses"
                            :key="c.id"
                            :class="{'col-7': index == 0, 'col-7 offset-5': index > 0}"
                        >
                            <BLink :to="`/course/${c.course.id}/${c.id}/`">
                                <span
                                    v-if="c.course.long_name" 
                                    v-b-tooltip="`${c.course.short_name} (${c.group.toUpperCase()})`"
                                >
                                    {{ c.course.long_name }}
                                </span>
                                <span v-else>
                                    {{ c.course.short_name }}
                                </span>
                                <span v-if="c.group !== ''">
                                    ({{ c.classes }})
                                </span>
                            </BLink>
                        </dd>
                        <dt
                            v-if="personType === 'student' && person.orientation"
                            class="col-5 text-end"
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
                            class="col-5 text-end"
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
                            class="col-5 text-end"
                            v-if="personType === 'responsible' && person.email_school"
                        >
                            Courriel de l'école
                        </dt>
                        <dd
                            class="col-7"
                            v-if="personType === 'responsible' && person.email_school"
                        >
                            {{ person.email_school }}
                            <IBiCopy
                                class="ms-2"
                                @click="copyToClipboard(person.email_school)"
                            />
                        </dd>
                    </dl>
                    <dl
                        class="row"
                        v-if="store.settings.show_credentials"
                    >
                        <dt
                            v-if="username"
                            class="col-5 text-end"
                        >
                            Nom d'utilisateur
                        </dt>
                        <dd
                            v-if="username"
                            class="col-7"
                        >
                            {{ username }}
                            <IBiCopy
                                class="ms-2"
                                @click="copyToClipboard(username)"
                            />
                        </dd>
                        <dt
                            v-if="password"
                            class="col-5 text-end"
                        >
                            Mot de passe
                        </dt>
                        <dd
                            v-if="password && showPassword"
                            class="col-7"
                        >
                            {{ password }}
                            <IBiCopy
                                class="ms-2"
                                @click="copyToClipboard(password)"
                            />
                        </dd>
                        <dd
                            v-else-if="password"
                            class="col-7"
                        >
                            <BButton
                                size="sm"
                                variant="light"
                                @click="showPassword = true"
                            >
                                Montrer le mot de passe
                            </BButton>
                        </dd>
                    </dl>
                </BCol>
            </BRow>
            <BRow v-if="important.length > 0">
                <BCol>
                    <BCard
                        no-body
                        class="mb-1"
                    >
                        <BCard-header
                            header-tag="header"
                            class="p-1 text-center"
                        >
                            <BButton
                                block
                                v-b-toggle.infos-importantes
                                variant="danger"
                            >
                                Infos importantes
                            </BButton>
                        </BCard-header>
                        <BCollapse id="infos-importantes">
                            <BCardBody>
                                <BRow>
                                    <BCol cols="2">
                                        <strong>Date</strong>
                                    </BCol>
                                    <BCol cols="3">
                                        <strong>Objet/Motif</strong>
                                    </BCol>
                                    <BCol><strong>Message</strong></BCol>
                                </BRow>
                                <BRow
                                    v-for="cas in important"
                                    :key="cas.id"
                                    class="mb-2"
                                >
                                    <BCol cols="2">
                                        {{ niceDate(cas.datetime_encodage) }}
                                    </BCol>
                                    <BCol cols="3">
                                        {{ cas.sanction_decision ? cas.sanction_decision.sanction_decision : cas.info.info }}
                                    </BCol>
                                    <BCol><div v-html="cas.explication_commentaire" /></BCol>
                                </BRow>
                            </BCardBody>
                        </BCollapse>
                    </BCard>
                </BCol>
            </BRow>
        </BOverlay>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import { useToastController } from "bootstrap-vue-next";
import { displayStudent } from "@s:core/js/common/utilities.js";

import { annuaireStore } from "./stores/index.js";

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        customMatricule: {
            type: Number,
            default: -1
        },
        customPersonType: {
            type: String,
            default: null
        }
    },
    data: function () {
        return {
            matricule: -1,
            personType: null,
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
            store: annuaireStore(),
        };
    },
    computed: {
        photoPath: function () {
            const matricule = Number(this.matricule);
            const personType = this.personType ? this.personType : this.$router.currentRoute.value.params.type;

            return `/static/photos${personType === "responsible" ? "_prof" : ""}/${matricule}.jpg`;
        },
    },
    watch: {
        "$route.params.matricule": function (to, from) {
            if (from) {
                this.loading = true;
                this.person = null;

                this.personType = this.$router.currentRoute.value.params.type;
                this.matricule = this.$route.params.matricule;
                this.loadInfo();
            }
        }
    },
    methods: {
        copyToClipboard: function (text) {
            navigator.clipboard.writeText(text);
            this.show({
                body: "Copié !",
                variant: "success",
                noCloseButton: true,
            });
        },
        copyToClipboardFullname: function(){
            let fullname = "";
            if (this.personType === "responsible") {
                fullname = `${this.person.first_name} ${this.person.last_name}`;
            } else if (this.personType =="student") {
                fullname = `${displayStudent(this.person, this)} (${this.person.matricule})`;
            }
            this.copyToClipboard(fullname);
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
            switch (this.personType) {
            case "student":
                axios.get(`/annuaire/api/student/${this.matricule}/`)
                    .then(response => {
                        this.person = response.data;
                        this.person.courses = this.person.courses.sort((a, b) => a.course.name >= b.course.name);
                        this.person.teaching = [this.person.teaching];
                        this.person.classe = this.person.classe ? [this.person.classe] : [];
                        this.loading = false;
                    });

                axios.get(`/annuaire/api/info_general/${this.matricule}/`)
                    .then(response => {
                        this.username = response.data.username;
                        this.password = response.data.password;
                    });

                axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&activate_important=true&student__matricule=${this.matricule}`)
                    .then(response => {
                        this.important = response.data.results;
                    });
                break;
            case "responsible":
                axios.get(`/annuaire/api/responsible/${this.matricule}/`)
                    .then(response => {
                        this.person = response.data;
                        this.person.courses = this.person.courses.sort((a, b) => a.course.name >= b.course.name);
                        this.person.classe = this.person.classe.sort((a, b) => a.year + a.letter >= b.year + b.letter);
                        this.loading = false;
                    });
                axios.get(`/annuaire/api/responsible_sensitive/${this.matricule}/`)
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
        this.personType = this.$router.currentRoute.value.params.type ? this.$router.currentRoute.value.params.type : this.customPersonType;
        this.matricule = this.$route.params.matricule ? this.$route.params.matricule : this.customMatricule;
        this.loadInfo();
    },
};
</script>

<style>
.important {
    background-color: rgba(255, 0, 0, 0.3);
}
</style>
