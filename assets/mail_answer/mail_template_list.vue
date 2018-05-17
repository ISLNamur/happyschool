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
        <b-row>
            <p>
                <b-button v-if="!(remoteInUse && isRemote)"
                    variant="primary" @click="editTemplate(null)">
                    <icon name="plus"></icon>
                    Ajouter un template
                </b-button>
            </p>
        </b-row>
        <b-row v-for="template in templates" :key="template.id" class="mb-2">
            <b-col>
                <b-card :title="template.name">
                    <p class="card-text">
                        Utilisé par un envoi d'email : <icon :name="template.is_used ? 'check' : 'times'" scale="1.2"
                                                             :color="template.is_used ? 'green' : 'red'"></icon>
                    </p>
                    <b-button v-if="!(remoteInUse && !(isRemote == template.is_used))" @click="editTemplate(template.id)"><icon name="edit"></icon>Modifier</b-button>
                    <b-button v-if="template.is_used && !(remoteInUse && !isRemote)" @click="showAnswers(template.id)" variant="light">
                        <icon name="eye"></icon>
                        Voir les réponses
                    </b-button>
                </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import axios from 'axios';

export default {
    data: function () {
        return {
            templates: [],
        }
    },
    computed: {
        remoteInUse: function () {
            return this.$store.state.settings.use_remote;
        },
        isRemote: function () {
            return this.$store.state.settings.is_remote;
        }
    },
    methods: {
        loadData: function () {
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let url = '/mail_answer/api/mail_template/';
            axios.get(url, token)
            .then(response => {
                this.templates = response.data.results;
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        editTemplate: function (id) {
            this.$emit('changeId', id);
            this.$emit('changeComponent', 'mail-template');
        },
        showAnswers: function (id) {
            this.$emit('changeId', id);
            this.$emit('changeComponent', 'mail-answer-list');
        }
    },
    mounted: function () {
        this.loadData();
    },
    components: {}
}
</script>

<style>
</style>
