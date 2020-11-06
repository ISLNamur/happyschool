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
        <b-container>
            <b-row>
                <h1>Absences Élèves</h1>
            </b-row>
            <b-row>
                <b-nav tabs>
                    <b-nav-item to="overview">
                        Vue d'ensemble
                    </b-nav-item>
                    <b-nav-item to="add_absence">
                        <icon
                            name="plus"
                            scale="1"
                            color="green"
                            class="align-middle"
                        />
                        Ajouter absences
                    </b-nav-item>
                    <b-nav-item to="list">
                        Liste d'absences
                    </b-nav-item>
                    <b-nav-item to="notes">
                        Notes
                    </b-nav-item>
                    <b-nav-item-dropdown right>
                        <b-dropdown-item @click="$store.commit('updateStudentsClasses')">
                            Mettre à jour des étudiants
                        </b-dropdown-item>
                        <b-dropdown-item @click="$store.commit('toggleForceAllAccess')">
                            {{ $store.state.forceAllAccess ? "Activer" : "Désactiver" }} la restriction par classe
                        </b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-nav>
            </b-row>
            <router-view />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import Moment from "moment";
Moment.locale("fr");

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

export default {
    data: function () {
        return {
        };
    },
    mounted: function () {
        // Check if students and classes need to be updated.
        setTimeout(() => {
            if (this.$store.state.onLine) {
                let modalText = "";
                if (this.$store.state.lastUpdate === "") {
                    modalText = "Afin de pouvoir prendre les présences, il est nécessaire de copier la liste des étudiants et des classes dans le navigateur. Ceci permet à HappySchool de fonctionner sans connexion.";
                } else if (Moment(this.$store.state.lastUpdate).add(1, "months").isBefore(Moment())) {
                    modalText = "Il semblerait que la liste des étudiants et des classes ne soit plus récente. Il est conseillé de mettre à jour celle-ci.";
                }
                if (modalText !== "") {
                    this.$bvModal.msgBoxConfirm(modalText, {
                        title: "Mise à jour des étudiants et des classes",
                        headerBgVariant: "info",
                        headerTextVariant: "light",
                        okTitle: "Mettre à jour",
                        cancelTitle: "Annuler",
                        hideHeaderClose: false,
                        centered: true
                    })
                        .then(value => {
                            if (value) {
                                this.$router.push("add_absence");
                                this.$store.commit("updateStudentsClasses");
                            }
                        })
                        .catch(err => {
                            // An error occurred
                            console.log(err);
                        });
                }
            }
        }, 4000);
    }
};
</script>
