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
        <app-menu :menu-info="menuInfo" />
        <b-container>
            <h1>Réponse d'email</h1>
            <component
                :is="currentComponent"
                :id="templateId"
                @changeComponent="changeComponent($event)"
                @changeId="templateId = $event"
            />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue, { BootstrapVueIcons } from "bootstrap-vue";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import MailTemplateList from "./mail_template_list.vue";
import MailTemplate from "./mail_template.vue";
import MailAnswerList from "./mail_answer_list.vue";

import Menu from "../common/menu_bar.vue";

export default {
    data: function () {
        return {
            menuInfo: {},
            currentComponent: "mail-template-list",
            templateId: null,
        };
    },
    methods: {
        changeComponent: function (component) {
            this.currentComponent = component;
        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
    },
    components: {
        "mail-template-list": MailTemplateList,
        "mail-template": MailTemplate,
        "mail-answer-list": MailAnswerList,
        "app-menu": Menu,
    }
};
</script>

<style>
</style>
