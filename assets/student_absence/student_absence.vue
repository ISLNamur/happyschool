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

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

export default {
    data: function () {
        return {
        };
    }
};
</script>
