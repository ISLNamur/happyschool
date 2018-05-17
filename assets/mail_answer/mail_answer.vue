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
            <h1>Réponse d'email</h1>
                <component v-bind:is="currentComponent"
                    :id="templateId"
                    @changeComponent="changeComponent($event)"
                    @changeId="templateId = $event">
                </component>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

import MailTemplateList from './mail_template_list.vue';
import MailTemplate from './mail_template.vue';
import MailAnswerList from './mail_answer_list.vue';

export default {
    data: function () {
        return {
            currentComponent: 'mail-template-list',
            templateId: null,
        }
    },
    methods: {
        changeComponent: function (component) {
            this.currentComponent = component;
        }
    },
    components: {
        'mail-template-list': MailTemplateList,
        'mail-template': MailTemplate,
        'mail-answer-list': MailAnswerList,
    }
}
</script>

<style>
</style>
