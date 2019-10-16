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
        <h4>Paramètres généraux</h4>
        <b-row>
            <p>Pour le moment, HappySchool utilise principalement les pages d'administrations fournies par django.</p>
            <p><b-button href="/admin">Accèder à l'interface d'administration de django</b-button></p>
        </b-row>
        <b-row>
            <h5>Établissement(s)</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <b-list-group-item  v-for="item in teachings" :key="item.pk">
                        {{ item.display_name }} ({{ item.name }})
                        <b-btn v-b-modal.addModal variant="light"
                            @click="currentTeaching = item" class="float-right">
                            <icon name="edit" scale="1" color="green"></icon>
                        </b-btn>
                        <b-btn v-b-modal.deleteModal variant="light"
                            class="float-right" @click="currentTeaching = item">
                            <icon name="remove" scale="1" color="red"></icon>
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
                <p class="card-text mt-2">
                    <b-btn v-b-modal.addModal variant="light">
                        <icon name="plus" scale="1" color="green"></icon>
                        Ajouter
                    </b-btn>
                </p>
            </b-col>
        </b-row>
        <b-row>
            <h5>Logo</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-form-group description="Le logo doit être au format png.">
                            <b-form-file v-model="logo" accept=".png" placeholder="Sélectionner le logo"></b-form-file>
                        </b-form-group>
                    </b-form-row>
                </b-form>
                <p class="card-text mt-2">
                    <b-btn variant="light" @click="sendLogo" :disabled="!logo">
                        <icon name="plus" scale="1" color="green"></icon>
                        Envoyer
                    </b-btn>
                </p>
            </b-col>
        </b-row>
        <b-modal id="deleteModal" cancel-title="Annuler" hide-header centered
                @ok="deleteTeaching" @hidden="resetTeachings">
            Êtes-vous sûr de vouloir supprimer {{ currentTeaching.display_name }} ({{ currentTeaching.name }})
            ainsi que toutes les classes cet établissement définitivement ?
        </b-modal>
        <b-modal id="addModal" ref="addModal"
                cancel-title="Annuler"
                title="Ajouter un établissement"
                ok-title="Ajouter"
                centered
                @ok="setTeaching" @hidden="resetTeachings">
            <form>
                <b-form-input type="text" v-model="currentTeaching.display_name" placeholder="Nom d'affichage"
                    aria-describedby="displayNameFeedback"
                    :state="inputStates.display_name"></b-form-input>
                <b-form-invalid-feedback id="displayNameFeedback">
                    {{ errorMsg('display_name') }}
                </b-form-invalid-feedback>
                <b-form-input type="text" v-model="currentTeaching.name" placeholder="Nom simple"
                    aria-describedby="nameFeedback"
                    :state="inputStates.name"></b-form-input>
                <b-form-invalid-feedback id="nameFeedback">
                    {{ errorMsg('name') }}
                </b-form-invalid-feedback>
            </form>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue);

import axios from 'axios';

const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};

export default {
    data: function () {
        return {
            teachings: [],
            currentTeaching: {display_name: null, name: null},
            inputStates: {display_name: null, name: null},
            errors: {},
            logo: null,
        }
    },
    watch: {
        errors: function (newErrors, oldErrors) {
            const inputs = Object.keys(this.inputStates);
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        },
    },
    methods: {
        sendLogo: function () {
            let data = new FormData();
            data.append('file', this.logo)
            axios.post('/core/api/logo/', data, token)
            .then(resp => {
                this.logo = null;
                this.$bvToast.toast(`Le logo a été envoyé, actualisez la page pour voir le nouveau logo.`, {
                    variant: 'success',
                    noCloseButton: true,
                });
            })
            .catch(err => {
                alert(err);
            })
        },
        deleteTeaching: function () {
            axios.delete('/core/api/teaching/' + this.currentTeaching.id + '/', token);
        },
        resetTeachings: function () {
            this.currentTeaching = {display_name: null, name: null};
            axios.get('/core/api/teaching/')
            .then(response => {
                this.teachings = response.data.results;
            });
        },
        setTeaching: function (evt) {
            // evt.preventDefault();

            let modal = this;
            let path = "/core/api/teaching/";
            const isModify = 'id' in this.currentTeaching;
            if (isModify) path += this.currentTeaching.id + '/';

            let send = isModify ? axios.put(path, this.currentTeaching, token) : axios.post(path, this.currentTeaching, token);
            send.then(response => {
            })
            .catch(function (error) {
                modal.errors = error.response.data;
            });
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
    },
    mounted: function () {
        this.resetTeachings();
    },
    components: {
    }
}
</script>

    