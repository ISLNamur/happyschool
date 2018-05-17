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
                <b-form-checkbox-group stacked>
                        <b-form-checkbox v-for="(option, index) in options" :key="option.id" :value="option.id">
                            <b-form inline>
                            {{ option.text }}
                            <b-form-input class="ml-1" v-if="option.input" type="text"></b-form-input>
                            <b-btn v-b-modal.addOptionModal variant="light" class="ml-1"
                                @click="editOption(index)">
                                <icon name="edit" color="green"></icon>
                            </b-btn>
                            <b-btn variant="light" :disabled="disabled" @click="removeOption(index)" class="ml-1">
                                <icon name="remove" color="red"></icon>
                            </b-btn>
                            </b-form>
                        </b-form-checkbox>
                </b-form-checkbox-group>
            </b-form-group>
        </b-row>
        <b-row>
            <b-btn v-b-modal.addOptionModal variant="success"><icon name="plus"></icon>Ajouter une option</b-btn>
        </b-row>
        <b-modal ref="addOptionModal" id="addOptionModal"
            :disabled="disabled"
            cancel-title="Annuler"
            title="Ajouter une option"
            centered
            @ok="addOption"
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
    props: ['options', 'disabled'],
    data: function () {
        return {
            selected: [],
            textInput: "",
            checkInclude: false,
            itemIndex: -1,
        }
    },
    methods: {
        addOption: function () {
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            if (this.itemIndex < 0) {
                // Create new option.
                let data = {text: this.textInput, input: this.checkInclude};
                axios.post('/mail_answer/api/options/', data, token)
                .then(response => {
                    data.id = response.data.id;
                    this.options.push(data);
                })
                .catch(function (error) {
                    console.log(error);
                });
            } else {
                // Update option.
                let data = this.options[this.itemIndex];
                data.text = this.textInput;
                data.input = this.checkInclude;
                axios.put('/mail_answer/api/options/' + this.options[this.itemIndex].id + '/', data, token)
                .then(response => {
                    this.options[this.itemIndex] = data;
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
        },
        editOption: function(index) {
            this.textInput = this.options[index].text;
            this.checkInclude = this.options[index].input;
            this.itemIndex = index;
        },
        removeOption: function(index) {
            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.delete('/mail_answer/api/options/' + this.options[index].id + '/', token)
            .then(response => {
                this.options.splice(index, 1);
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
