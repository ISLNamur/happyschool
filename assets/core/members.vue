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
        <b-container v-cloak>
            <h1>Gestion du personnels</h1>
            <b-row>
                <b-col>
                <b-card-group deck>
                    <b-card header="<b>Secrétaires</b>">
                        <b-list-group>
                            <b-list-group-item  v-for="item in secretary" :key="item.pk">
                                {{ item.last_name }} {{ item.first_name }}
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                    <b-card header="<b>Autres personnels</b>">
                        <b-list-group>
                            <b-list-group-item v-for="item in others" :key="item.pk"
                                class="d-flex justify-content-between align-items-center"
                                v-b-popover.hover="item.email">
                                {{ item.last_name }} {{ item.first_name }}
                                <div>
                                    <b-btn v-b-modal.addModal variant="light"
                                        @click="fillModal(item)">
                                        <icon name="edit" scale="1" color="green"></icon>
                                    </b-btn>
                                    <b-btn v-b-modal.deleteModal variant="light"
                                        class="card-link" @click="currentItem = item">
                                        <icon name="remove" scale="1" color="red"></icon>
                                    </b-btn>
                                </div>

                            </b-list-group-item>
                        </b-list-group>
                        <p class="card-text mt-2">
                            <b-btn v-b-modal.addModal variant="light">
                                <icon name="plus" scale="1" color="green"></icon>
                                Ajouter
                            </b-btn>
                        </p>
                    </b-card>
                </b-card-group>
            </b-col>
            </b-row>
        </b-container>
        <b-modal id="deleteModal" cancel-title="Annuler" hide-header centered v-on:ok="deleteEntry">
            Êtes-vous sûr de vouloir supprimer {{ currentItem.last_name }} {{ currentItem.first_name }} ?
        </b-modal>
        <b-modal id="addModal" ref="addModal"
                cancel-title="Annuler"
                title="Ajouter une personne"
                ok-title="Ajouter"
                centered
                @ok="addEntry" @hidden="resetModal">
            <form>
                <b-form-input type="text" v-model="last_name" placeholder="Nom"
                    id="last_name" aria-describedby="lastNameFeedback"
                    :state="inputStates.last_name"></b-form-input>
                <b-form-invalid-feedback id="lastNameFeedback">
                    {{ errorMsg('last_name') }}
                </b-form-invalid-feedback>
                <b-form-input type="text" v-model="first_name" placeholder="Prénom"
                    id="first_name" aria-describedby="firstNameFeedback"
                    :state="inputStates.first_name"></b-form-input>
                <b-form-invalid-feedback id="firstNameFeedback">
                    {{ errorMsg('first_name') }}
                </b-form-invalid-feedback>
                <b-form-input type="email" v-model="email" placeholder="Email"
                    id="email" aria-describedby="emailFeedback"
                    :state="inputStates.email"></b-form-input>
                <b-form-invalid-feedback id="emailFeedback">
                    {{ errorMsg('email') }}
                </b-form-invalid-feedback>
            </form>
        </b-modal>
    </div>
</template>

<script>
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios';

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'

Vue.component('icon', Icon);

Vue.use(BootstrapVue);

export default {
    data: function () {
        return {
            secretary: [],
            others: [],
            currentItem: {},
            last_name: "",
            first_name: "",
            email: "",
            pk: null,
            errors: {},
            inputStates: {
                email: null,
                last_name: null,
                first_name: null,
            }
        }
    },
    watch: {
        errors: function (newErrors, oldErrors) {
            let inputs = ['email', 'last_name', 'first_name'];
            for (let u in inputs) {
                if (inputs[u] in newErrors) {
                    this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                } else {
                    this.inputStates[inputs[u]] = null;
                }
            }
        }
    },
    methods: {
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        fillModal(item) {
            this.last_name = item.last_name;
            this.first_name = item.first_name;
            this.email = item.email;
            this.pk = item.pk;
        },
        resetModal() {
            this.last_name = "";
            this.first_name = "";
            this.email = "";
            this.pk = null;
        },
        loadPeople(personType) {
            // Load person type.
            let param = { 'person_type': personType };
            axios.get("/core/api/members", {params: param})
            .then(response => {
                this[personType] = response.data.results;
            });
        },
        deleteEntry() {
            axios.delete("/core/api/members/" + this.currentItem.pk,
            {
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
            }
            )
            .then(response => {
                this.loadPeople('others');
            });
        },
        addEntry(evt) {
            evt.preventDefault();

            let app = this;
            let data = {
                last_name: this.last_name,
                first_name: this.first_name,
                email: this.email,
            };

            var path = "/core/api/members/";
            // Check if this is a modification.
            if (this.pk) path += this.pk.toString() + "/";

            let token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            let send = this.pk ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(response => {
                // Reload people list.
                this.loadPeople('others');
                // Reset errors if any.
                this.errors = {};
                this.$refs.addModal.hide();
            })
            .catch(function (error) {
                app.errors = error.response.data;
            });
        }
    },
    mounted: function () {
        // Load people.
        this.loadPeople('secretary');
        this.loadPeople('others');
    },
}
</script>

<style>
</style>
