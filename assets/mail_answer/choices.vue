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
                        <b-form-radio v-for="(choice, index) in choices">
                            <b-form inline>
                            {{ choice.text }}
                            <b-form-input class="ml-1" v-if="choice.input" type="text"></b-form-input>
                            <b-btn v-b-modal.addChoiceModal variant="light" class="ml-1"
                                @click="editChoice(index)">
                                <icon name="edit" scale="1" color="green"></icon>
                            </b-btn>
                            <b-btn variant="light" @click="choices.splice(index, 1)" class="ml-1">
                                <icon name="remove" scale="1" color="red"></icon>
                            </b-btn>
                            </b-form>
                        </b-form-radio>
                </b-form-radio-group>
            </b-form-group>
        </b-row>
        <b-row>
            <b-btn v-b-modal.addChoiceModal variant="success"><icon name="plus" scale="1" color="white"></icon>Ajouter un choix</b-btn>
        </b-row>
        <b-modal ref="addChoiceModal" id="addChoiceModal"
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

export default {
    data: function () {
        return {
            choices: [
                {id: -1, text: 'Un choix parmi d\'autres.', input: true},
            ],
            textInput: "",
            checkInclude: false,
            itemIndex: -1,
        }
    },
    methods: {
        addChoice: function () {
            if (this.itemIndex < 0) {
                this.choices.push({id: this.itemId, text: this.textInput, input: this.checkInclude});
            } else {
                this.choices[this.itemIndex].text = this.textInput;
                this.choices[this.itemIndex].input = this.checkInclude;
            }
        },
        editChoice: function(index) {
            this.textInput = this.choices[index].text;
            this.checkInclude = this.choices[index].input;
            this.itemIndex = index;
        },
        resetModal: function () {
            this.textInput = "";
            this.checkInclude = false;
            this.itemIndex = -1;
        }
    }
}
</script>

<style>
</style>
