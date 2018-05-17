<template>
    <div>
        <div class="loading" v-if="!loaded"></div>
        <b-container v-if="loaded">
            <h1>{{ template.name }}</h1>
            <b-row>
                <b-col>
                    <p>
                        En tant que responsable de <strong>{{ student.full_name }}</strong> en {{ student.classe }}, veuillez remplir le formulaire suivant. Si vous n'êtes pas responsable de {{ student.full_name }},
                        merci de contacter au plus vite le service informatique de l'école.
                    </p>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <p>
                        {{ template.text }}
                    </p>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-form>
                        <b-form-row v-if="template.choices.length > 0">
                            <b-form-group label="Merci de choisir une des options ci-dessous :" invalid-feedback="Choisissez au moins une option." :state="choiceState">
                                <b-form-radio-group v-model="form.choices" stacked>
                                        <b-form-radio class="mb-3"
                                            v-for="(choice, index) in template.choices" :key="choice.id" :value="choice.id">
                                            <b-form inline>
                                                {{ choice.text }}
                                                <b-form-input class="ml-2" type="text"
                                                    v-if="choice.input && form.choices == choice.id"
                                                    v-model="form.choiceText[index].text">
                                                </b-form-input>
                                            </b-form>
                                        </b-form-radio>
                                </b-form-radio-group>
                            </b-form-group>
                        </b-form-row>
                        <b-form-row v-if="template.options.length > 0">
                            <b-form-group label="Merci de choisir une ou plusieurs des options ci-dessous :">
                                <b-form-checkbox-group v-model="form.options" stacked>
                                        <b-form-checkbox class="mb-3"
                                            v-for="(option, index) in template.options" :key="option.id" :value="option.id">
                                            <b-form inline>
                                                {{ option.text }}
                                                <b-form-input class="ml-2" type="text"
                                                    v-if="option.input"
                                                    v-model="form.optionText[index].text">
                                                </b-form-input>
                                            </b-form>
                                        </b-form-checkbox>
                                </b-form-checkbox-group>
                            </b-form-group>
                        </b-form-row>
                    </b-form>
                </b-col>
            </b-row>
            <b-row v-if="template.acknowledge">
                <b-col>
                    <b-card class="mb-2">
                        <b-form-group v-if="template.acknowledge">
                            <b-form-checkbox v-model="form.acknowledge">
                                {{ template.acknowledge_text }}
                            </b-form-checkbox>
                        </b-form-group>
                    </b-card>
                </b-col>
            </b-row>
            <b-row>
                <p>
                    <b-btn @click="sendData" :disabled="saving" variant="primary">
                        {{ sent ? "Mettre à jour" : "Envoyer"}}
                        <icon v-if="saving" name="spinner" scale="1" :spin="saving"></icon>
                    </b-btn>
                </p>
            </b-row>
            <b-row>
                <p>
                    <b-alert variant="success" :show="countDownSuccess">Les données ont été envoyées !</b-alert>
                </p>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
Vue.use(BootstrapVue);

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

import axios from 'axios';

export default {
    props: ['uuid'],
    data: function () {
        return {
            loaded: false,
            student : {full_name: '', classe: ''},
            template: {},
            form: {
                acknowledge: false,
                options: [],
                optionText: [],
                choices: '',
                choiceText: [],
            },
            sent: false,
            saving: false,
            countDownSuccess: 0,
            choiceState: null,
        }
    },
    methods: {
        sendData: function () {
            // Ensure a choice has been made.
            if (this.template.choices.length > 0 && this.form.choices == 0) {
                this.choiceState = false;
                return;
            }

            if (!this.choiceState) this.choiceState = true;

            this.saving = true;
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let url = '/mail_answer/api/public/mail_answer/' + this.uuid + '/';
            axios.put(url, {answers: JSON.stringify(this.form)}, token)
            .then(response => {
                this.sent = true;
                this.saving = false;
                this.countDownSuccess = 4;
            })
            .catch(function (error) {
                alert("Un problème est survenu.\nMerci de réessayer ou de contacter le service informatique.");
                this.saving = false;
            });
        }
    },
    mounted: function () {
        let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
        let url = '/mail_answer/api/public/mail_answer/' + this.uuid + '/'
        axios.get(url, token)
        .then(resp => {
            // Get student info.
            this.student.full_name = resp.data.student.last_name + ' ' + resp.data.student.first_name;
            this.student.classe = resp.data.student.classe.year + resp.data.student.classe.letter.toUpperCase();

            this.template = resp.data.template;

            let answer = JSON.parse(resp.data.answers);

            let alreadyFilled = Object.keys(answer).length > 2
            // Prepare form data.
            if (alreadyFilled) {
                this.form.acknowledge = answer.acknowledge;
                this.form.choices = answer.choices;
                this.form.options = answer.options;
                this.sent = true;
            }

            for (let c in this.template.choices) {
                let cText = alreadyFilled ? answer.choiceText[c].text : ''
                this.form.choiceText.push({id: this.template.choices[c].id, text: cText});
            }

            for (let o in this.template.options) {
                let oText = alreadyFilled ? answer.optionText[o].text : ''
                this.form.optionText.push({id: this.template.options[o].id, text: oText});
            }
            this.loaded = true;
        })

    }
}
</script>

<style>
.loading {
  content: " ";
  display: block;
  position: absolute;
  width: 80px;
  height: 80px;
  background-image: url(/static/img/spin.svg);
  background-size: cover;
  left: 50%;
  top: 50%;
}
</style>
