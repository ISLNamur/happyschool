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
        <BNavbar
            toggleable="lg"
            type="light"
            variant="light"
        >
            <BNavbarToggle target="nav_text_collapse" />
            <BNavbarBrand href="/">
                <img
                    id="logo-school"
                    :src="'/media/core/logo.png'"
                    class="d-inline-block align-top"
                >
                HappySchool
            </BNavbarBrand>
            <BCollapse
                is-nav
                id="nav_text_collapse"
            >
                <BNavbarNav
                    is-nav-bar
                    v-for="(app) in menuInfo.apps"
                    :key="app.app"
                >
                    <BNavItem
                        :active="app.active"
                        :href="app.url"
                        :target="app.new_tab ? '_blank' : ''"
                        :rel="app.new_tab ? 'noreferrer noopener' : ''"
                    >
                        {{ app.display }}
                        <BBadge
                            v-if="app.new_items && (app.new_items > 0 || app.new_items.length > 1)"
                            variant="primary"
                        >
                            {{ app.new_items }}
                        </BBadge>
                    </BNavItem>
                </BNavbarNav>
                <BNavbarNav class="ml-auto">
                    <BNavText><strong>{{ menuInfo.full_name }}</strong></BNavText>
                    <BNavItem-dropdown
                        text="Options"
                        right
                    >
                        <BDropdownItem
                            v-if="userMatricule"
                            :href="`/annuaire/#/person/responsible/${userMatricule}/`"
                        >
                            Profil
                        </BDropdownItem>
                        <BDropdownItem
                            v-if="menuInfo.admin_settings"
                            href="/core/admin/"
                        >
                            Administration
                        </BDropdownItem>
                        <BDropdownDivider />
                        <BDropdownItem href="/logout/">
                            Se déconnecter
                        </BDropdownItem>
                    </BNavItem-dropdown>
                </BNavbarNav>
            </BCollapse>
        </BNavbar>
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
            userMatricule: null,
        };
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        if (user_properties && user_properties.matricule) this.userMatricule = user_properties.matricule;
    }
};
</script>

<style>
#logo-school {
    max-height: 35px;
}
</style>
