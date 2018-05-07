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
            <b-btn v-b-modal.changeAckModal variant="light" class="mr-1"
                @click="changedText = text">
                <icon name="edit" scale="1" color="green"></icon>
            </b-btn>
            <b-form-checkbox id="acknowledgement">
                {{ text }}
            </b-form-checkbox>
        </b-row>
        <b-modal ref="changeAckModal" id="changeAckModal"
            cancel-title="Annuler"
            title="Changer le  texte"
            centered
            @ok="changeAck">
            <b-form>
                <b-form-textarea v-model="changedText" placeholder="Texte de confirmation" :rows="3"></b-form-textarea>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

export default {
    props: ['text'],
    data: function () {
        return {
            changedText: "",
        }
    },
    methods: {
        changeAck: function() {
            this.$emit('update', this.changedText);
        },
    }
}
</script>

<style>
</style>
