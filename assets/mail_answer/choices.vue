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
            <b-form-group>
                <b-form-radio-group stacked>
                        <b-form-radio v-for="(choice, index) in choices" :key="choice.id">
                            <b-form inline>
                            {{ choice.text }}
                            <b-form-input class="ml-1" v-if="choice.input" type="text"></b-form-input>
                            <b-btn v-b-modal.addChoiceModal variant="light" class="ml-1"
                                @click="editChoice(index)">
                                <icon name="edit" color="green"></icon>
                            </b-btn>
                            <b-btn variant="light" :disabled="disabled" @click="removeChoice(index)" class="ml-1">
                                <icon name="remove" color="red"></icon>
                            </b-btn>
                            </b-form>
                        </b-form-radio>
                </b-form-radio-group>
            </b-form-group>
        </b-row>
        <b-row>
            <b-btn v-b-modal.addChoiceModal variant="success"><icon name="plus" color="white"></icon>Ajouter un choix</b-btn>
        </b-row>
        <b-modal ref="addChoiceModal" id="addChoiceModal"
            :disabled="disabled"
            cancel-title="Annuler"
            title="Ajouter un choix"
            centered
            @ok="addChoice"
            @hidden="resetModal">
            <b-form>
                <b-form-input v-model="textInput" placeholder="Texte du choix"></b-form-input>
                <b-form-checkbox v-model="checkInclude">Inclure une entrée.</b-form-checkbox>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

import axios from 'axios';

export default {
    props: ['choices', 'disabled'],
    data: function () {
        return {
            textInput: "",
            checkInclude: false,
            itemIndex: -1,
        }
    },
    methods: {
        addChoice: function () {
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            if (this.itemIndex < 0) {
                // Create new choice.
                let data = {text: this.textInput, input: this.checkInclude};
                axios.post('/mail_answer/api/choices/', data, token)
                .then(response => {
                    data.id = response.data.id;
                    this.choices.push(data);
                })
                .catch(function (error) {
                    console.log(error);
                });
            } else {
                // Update choice.
                let data = this.choices[this.itemIndex];
                data.text = this.textInput;
                data.input = this.checkInclude;
                axios.put('/mail_answer/api/choices/' + this.choices[this.itemIndex].id + '/', data, token)
                .then(response => {
                    this.choices[this.itemIndex] = data;
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
        },
        editChoice: function(index) {
            this.textInput = this.choices[index].text;
            this.checkInclude = this.choices[index].input;
            this.itemIndex = index;
        },
        removeChoice: function(index) {
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/mail_answer/api/choices/' + this.choices[index].id + '/', token)
            .then(response => {
                this.choices.splice(index, 1);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        resetModal: function () {
            this.textInput = "";
            this.checkInclude = false;
            this.itemIndex = -1;
        },
    }
}
</script>

<style>
</style>
