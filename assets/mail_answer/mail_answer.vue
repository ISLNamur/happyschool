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
                <b-col>
                <b-card header="Nom du modèle">
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
                            @click="hasChoices = !hasChoices"
                            :class="hasChoices ? 'collapsed' : null"
                            aria-controls="has-choices"
                            :aria-expanded="hasChoices ? 'true' : 'false'">
                            {{ hasChoices ? 'Enlever': 'Ajouter' }} choix unique
                        </b-btn>
                    </p>
                    <b-collapse class="mt-2" v-model="hasChoices" id="has-choices">
                        <b-card>
                            <choices></choices>
                        </b-card>
                    </b-collapse>
                </b-card>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import Choices from './choices.vue';

export default {
    data: function () {
        return {
            student: {'fullname': 'NOM ÉTUDIANT', 'classe': 'CLASSE'},
            hasText: false,
            text: '',
            hasChoices: false,
            choices: [],
        }
    },
    components: { Choices }
}
</script>

<style>
</style>
