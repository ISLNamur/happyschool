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
    <app-menu
        :menu-info="menuInfo"
    />
    <b-container>
        <h3>Page d'administration d'HappySchool</h3>
        <b-row>
            <b-col sm="3">
                <b-list-group>
                    <b-list-group-item to="general">
                        <strong>Général</strong>
                    </b-list-group-item>
                    <b-list-group-item to="import">
                        <strong>Import</strong>
                    </b-list-group-item>
                    <b-list-group-item to="photos">
                        <strong>Photos</strong>
                    </b-list-group-item>
                    <b-list-group-item to="update">
                        <strong>Mise à jour</strong>
                    </b-list-group-item>
                    <b-list-group-item to="annuaire">
                        <strong>Annuaire</strong>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
            <b-col>
                <router-view v-slot="{ Component }">
                    <transition
                        name="slide-left"
                        mode="out-in"
                    >
                        <component :is="Component" />
                    </transition>
                </router-view>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import Menu from "@s:core/js/common/menu_bar.vue";

export default {
    data: function () {
        return {
            menuInfo: {},    
        };
    },
    mounted: function() {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
    },
    components: {
        "app-menu": Menu,
    }
};
</script>
