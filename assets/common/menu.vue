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
        <b-navbar
            toggleable="lg"
            type="light"
            variant="light"
        >
            <b-nav-toggle target="nav_text_collapse" />
            <b-navbar-brand href="/">
                <img
                    id="logo-school"
                    src="/static/img/logo_school.png"
                    class="d-inline-block align-top"
                >
                HappySchool
            </b-navbar-brand>
            <b-collapse
                is-nav
                id="nav_text_collapse"
            >
                <b-navbar-nav
                    is-nav-bar
                    v-for="(app) in menuInfo.apps"
                    :key="app.app"
                >
                    <b-nav-item
                        :active="app.active"
                        :href="app.url"
                    >
                        {{ app.display }}
                    </b-nav-item>
                </b-navbar-nav>
                <b-navbar-nav class="ml-auto">
                    <b-nav-text><strong>{{ menuInfo.full_name }}</strong></b-nav-text>
                    <b-nav-item-dropdown
                        text="Options"
                        right
                    >
                        <b-dropdown-item href="/core/profil/">
                            Profil
                        </b-dropdown-item>
                        <b-dropdown-item
                            v-if="menuInfo.admin_settings"
                            href="/core/admin/"
                        >
                            Administration
                        </b-dropdown-item>
                        <b-dropdown-divider />
                        <b-dropdown-item href="/logout/">
                            Se déconnecter
                        </b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
export default {
    props: {
        "menu-info":{
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
        };
    },
};
</script>

<style>
#logo-school {
    max-height: 35px;
}
</style>
