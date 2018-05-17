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
                <b-btn variant="primary" @click="$emit('changeComponent', 'mail-template-list')">Revenir à la liste des modèles</b-btn>
            </p>
        </b-row>
        <b-row >
            <b-col>
                <b-card-group columns>
                    <b-card :header="'Année ' + key"  v-for="(classes, key) in answers" :key="key" class="mb-2">
                        <b-list-group>
                            <b-list-group-item button v-for="(classe, index) in classes" :key="index"
                                class="d-flex justify-content-between align-items-center"
                                @click="loadAnswers(classe[1][0])" v-b-modal.list-answers>
                                {{ classe[0] }}
                                <b-badge pill>{{ classe[1][0].answered_count }}/{{ classe[1][0].answers_count }}</b-badge>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </b-card-group>
            </b-col>
        </b-row>
        <b-modal id="list-answers" :title="currentClasse.classe_name" size="lg" :ok-only="true">
            <b-list-group>
                <b-list-group-item v-for="(answer, index) in currentAnswers" :key="index">
                    <span :class="answer.is_answered ? '' : 'font-italic' ">{{ answer.student_name }}</span>
                    <em v-if="!answer.is_answered">(en attente d'une réponse)</em>
                    <b-btn variant="light" v-if="answer.is_answered" v-b-toggle="'answer-' + index">Réponse</b-btn>
                    <b-collapse :id="'answer-' + index" class="mt-2">
                        <answer-result :answer="answer.answer" :template="template"></answer-result>
                    </b-collapse>
                </b-list-group-item>
            </b-list-group>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import axios from 'axios';

import AnswerResult from './answer_result.vue';

export default {
    props: ['id'],
    data: function () {
        return {
            answers: {},
            template: {},
            loading: true,
            currentClasse: {},
            currentAnswers: [],
        }
    },
    methods: {
        loadData: function () {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const url = '/mail_answer/api/answers_classes/' + this.id + '/';

            // Get answers.
            axios.get(url, token)
            .then(response => {
                let byYear = this.groupBy(response.data, ans => ans.classe_year);
                for (const [year, classes] of byYear.entries()) {
                    this.$set(this.answers, year, Array.from(this.groupBy(classes, c => c.classe_name)));
                }
                this.loading = false;
            })
            .catch(function (error) {
                alert(error);
            });

            // Get template.
            axios.get('/mail_answer/api/mail_template/' + this.id + '/', token)
            .then(response => {
                this.template = response.data;
                const choices = this.template.choices;
                this.template.choices = {};
                for (let c in choices) {
                    axios.get('/mail_answer/api/choices/' + choices[c] + '/', token)
                    .then(r => {
                        this.$set(this.template.choices, r.data.id, r.data.text);
                    })
                    .catch(function (error) {
                        alert(error);
                    });
                }
                const options = this.template.options;
                this.template.options = {};
                for (let o in options) {
                    axios.get('/mail_answer/api/options/' + options[o] + '/', token)
                    .then(r => {
                        this.$set(this.template.options, r.data.id, r.data.text);
                    })
                    .catch(function (error) {
                        alert(error);
                    });
                }
            })
            .catch(function (error) {
                alert(error);
            });
        },
        loadAnswers: function (classe) {
            this.currentClasse = classe;
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const url = '/mail_answer/api/answers/' + this.id + '/' + classe.classe_id + '/';

            // Get answers.
            axios.get(url, token)
            .then(response => {
                this.currentAnswers = response.data;
            })
            .catch(function (error) {
                alert(error);
            });
        },
        groupBy: function (list, keyGetter) {
            const map = new Map();
            list.forEach((item) => {
                const key = keyGetter(item);
                const collection = map.get(key);
                if (!collection) {
                    map.set(key, [item]);
                } else {
                    collection.push(item);
                }
            });
            return map;
        }
    },
    mounted: function () {
        this.loadData();
    },
    components: {AnswerResult}
}
</script>

<style>
</style>
