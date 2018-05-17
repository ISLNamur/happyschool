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
                <b-button variant="primary" @click="$emit('changeComponent', 'mail-template-list')">
                    Revenir à la liste des modèles
                </b-button>
            </p>
        </b-row>
        <b-row>
            <b-col>
            <b-card :header="name.length > 0 ? name : 'Choisissez un nom de modèle !'">
                <b-form-group label="Nom du modèle :">
                    <b-form-input type="text" v-model="name" required></b-form-input>
                </b-form-group>
                <p>
                En tant que responsable de {{ student.fullname }} en {{ student.classe }}, veuillez remplir le formulaire suivant. Si vous n'êtes pas responsable de {{ student.fullname }},
                merci de contacter au plus vite le service informatique de l'école.
                </p>
                <p>
                    <b-btn
                        @click="hasText = !hasText"
                        :class="hasText ? 'collapsed' : null"
                        aria-controls="intro-text"
                        :aria-expanded="hasText ? 'true' : 'false'">
                        {{ hasText ? 'Enlever': 'Ajouter' }} texte d'introduction
                    </b-btn>
                </p>
                <b-collapse class="mt-2" v-model="hasText" id="intro-text">
                    <b-form-group>
                        <b-form-textarea id="intro-textarea"
                            v-model="text"
                            :rows="3">
                        </b-form-textarea>
                    </b-form-group>
                </b-collapse>
                <p>
                    <b-btn
                        :disabled="is_used"
                        @click="hasChoices = !hasChoices"
                        :class="hasChoices ? 'collapsed' : null"
                        aria-controls="has-choices"
                        :aria-expanded="hasChoices ? 'true' : 'false'">
                        {{ hasChoices ? 'Enlever': 'Ajouter' }} choix unique
                    </b-btn>
                </p>
                <b-collapse class="mt-2" v-model="hasChoices" id="has-choices">
                    <b-card>
                        <choices :choices="choices" :disabled="is_used"></choices>
                    </b-card>
                </b-collapse>
                <p>
                    <b-btn
                        :disabled="is_used"
                        @click="hasOptions = !hasOptions"
                        :class="hasOptions ? 'collapsed' : null"
                        aria-controls="has-options"
                        :aria-expanded="hasOptions ? 'true' : 'false'">
                        {{ hasOptions ? 'Enlever': 'Ajouter' }} choix multiples
                    </b-btn>
                </p>
                <b-collapse class="mt-2" v-model="hasOptions" id="has-options">
                    <b-card>
                        <options :options="options" :disabled="is_used"></options>
                    </b-card>
                </b-collapse>
                <p>
                    <b-btn
                        @click="hasAcknowledge = !hasAcknowledge"
                        :class="hasAcknowledge ? 'collapsed' : null"
                        aria-controls="has-acknowlegde"
                        :aria-expanded="hasAcknowledge ? 'true' : 'false'">
                        {{ hasAcknowledge ? 'Enlever': 'Ajouter' }} confirmation
                    </b-btn>
                </p>
                <b-collapse v-model="hasAcknowledge" id="has-acknowlegde">
                    <b-card>
                        <acknowledgement :text="acknowledgeText" @update="acknowledgeText = $event"></acknowledgement>
                    </b-card>
                </b-collapse>
                <b-row>
                    <b-col>
                        <div class="mt-2">
                            <b-btn variant="primary" @click="sendData">Sauvegarder <icon v-if="saving" name="spinner" scale="1" :spin="saving"></icon></b-btn>
                        </div>
                    </b-col>
                </b-row>
            </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

import Choices from './choices.vue';
import Options from './options.vue';
import Acknowledgement from './acknowledge.vue';

export default {
    props: ['id'],
    data: function () {
        return {
            student: {'fullname': 'NOM ÉTUDIANT', 'classe': 'CLASSE'},
            hasText: false,
            name: 'Nouveau modèle',
            text: '',
            hasChoices: false,
            choices: [],
            hasOptions: false,
            options: [],
            hasAcknowledge: true,
            acknowledgeText: "En tant que responsable, je déclare avoir pris connaissance des présentes informations.",
            saving: false,
            is_used: false,
        }
    },
    methods: {
        sendData: function () {
            this.saving = true;
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let data = {name: this.name, text: this.text,
                acknowledge: this.hasAcknowledge, acknowledge_text: this.acknowledgeText};
            if (this.hasChoices) {
                let choices = this.choices;
                data.choices = choices.map(c => c.id);
            }
            if (this.hasOptions) {
                let options = this.options;
                data.options = options.map(o => o.id);
            }

            let url = '/mail_answer/api/mail_template/';
            if (this.id) url += this.id.toString() + '/'
            let send = this.id ? axios.put(url, data, token) : axios.post(url, data, token)

            send.then(response => {
                if (!this.id) this.id = response.data.id;
                this.saving = false;
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        resetForm: function () {
            this.hasText = false;
            this.name = 'Nouveau modèle';
            this.text = '';
            this.hasChoices = false;
            this.choices = [];
            this.hasOptions = false;
            this.options = [];
            this.hasAcknowledge = true;
            this.acknowledgeText = "En tant que responsable, je déclare avoir pris connaissance des présentes informations.";
        }
    },
    mounted: function () {
        if (this.id) {
            // Get data and fill the form.
            let app = this;
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.get('/mail_answer/api/mail_template/' + this.id + '/', token)
            .then(response => {
                this.name = response.data.name;
                this.text = response.data.text;
                this.is_used = response.data.is_used;
                if (this.text.length > 0) this.hasText = true;
                this.hasAcknowledge = response.data.acknowledge;
                this.acknowledgeText = response.data.acknowledge_text;

                // Load options and choices.
                let choices = response.data.choices;
                if (choices.length > 0) {
                    app.hasChoices = true;
                    for (let c in choices) {
                        axios.get('/mail_answer/api/choices/' + choices[c] + '/', token)
                        .then(choiceResp => {
                            app.choices.push(choiceResp.data);
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                    }
                }
                let options = response.data.options;
                if (options.length > 0) {
                    app.hasOptions = true;
                    for (let c in options) {
                        axios.get('/mail_answer/api/options/' + options[c] + '/', token)
                        .then(optionResp => {
                            app.options.push(optionResp.data);
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                    }
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    },
    components: { Choices, Options, Acknowledgement }
}
</script>

<style>
</style>
