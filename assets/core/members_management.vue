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
        <app-menu :menu-info="menuInfo" />
        <b-container v-cloak>
            <h1>Gestion du personnels</h1>
            <b-row>
                <p class="card-text mb-2 ml-3">
                    <b-btn
                        v-b-modal.addGroupModal
                        variant="primary"
                    >
                        <b-icon
                            icon="plus"
                            scale="1.5"
                        />
                        Ajouter un groupe
                    </b-btn>
                </p>
            </b-row>
            <b-row>
                <b-col>
                    <b-card-group columns>
                        <b-card header="<b>Secrétaires</b>">
                            <b-list-group>
                                <b-list-group-item
                                    v-for="item in secretary"
                                    :key="item.pk"
                                >
                                    {{ item.last_name }} {{ item.first_name }}
                                </b-list-group-item>
                            </b-list-group>
                        </b-card>
                        <b-card>
                            <div slot="header">
                                <b>Autres personnels</b>
                                <b-icon
                                    id="others-info"
                                    icon="info-circle"
                                    variant="primary"
                                />
                                <b-tooltip
                                    target="others-info"
                                    title="Personnes responsables"
                                />
                            </div>
                            <b-list-group>
                                <b-list-group-item
                                    v-for="item in others"
                                    :key="item.pk"
                                    class="d-flex justify-content-between align-items-center"
                                    v-b-popover.hover="item.email"
                                >
                                    {{ item.last_name }} {{ item.first_name }}
                                    <div>
                                        <b-btn
                                            v-b-modal.addModal
                                            variant="light"
                                            @click="fillModal(item)"
                                        >
                                            <b-icon
                                                icon="square-pencil"
                                                scale="1"
                                                variant="success"
                                            />
                                        </b-btn>
                                        <b-btn
                                            v-b-modal.deleteModal
                                            variant="light"
                                            class="card-link"
                                            @click="currentItem = item"
                                        >
                                            <b-icon
                                                icon="trash-fill"
                                                variant="danger"
                                            />
                                        </b-btn>
                                    </div>
                                </b-list-group-item>
                            </b-list-group>
                            <p class="card-text mt-2">
                                <b-btn
                                    v-b-modal.addModal
                                    variant="light"
                                >
                                    <b-icon
                                        icon="plus"
                                        variant="success"
                                    />
                                    Ajouter
                                </b-btn>
                            </p>
                        </b-card>
                        <b-card
                            v-for="g in groups"
                            :key="g.id"
                        >
                            <div slot="header">
                                <b>{{ g.name }}</b>
                                <b-btn
                                    v-b-modal.deleteGroupModal
                                    variant="light"
                                    class="card-link"
                                    @click="currentGroup = g"
                                >
                                    <b-icon
                                        icon="dash"
                                        scale="1.5"
                                        variant="danger"
                                    />
                                </b-btn>
                            </div>
                            <b-list-group>
                                <b-list-group-item
                                    v-for="p in otherEmails[g.id]"
                                    :key="p.id"
                                    v-b-popover.hover="p.email"
                                    class="d-flex justify-content-between align-items-center"
                                >
                                    {{ p.last_name }} {{ p.first_name }}
                                    <div>
                                        <b-btn
                                            v-b-modal.addModal
                                            variant="light"
                                            @click="fillModal(p)"
                                        >
                                            <b-icon
                                                icon="pencil-square"
                                                variant="success"
                                            />
                                        </b-btn>
                                        <b-btn
                                            v-b-modal.deleteModal
                                            variant="light"
                                            class="card-link"
                                            @click="currentItem = p"
                                        >
                                            <b-icon
                                                icon="trash-fill"
                                                variant="danger"
                                            />
                                        </b-btn>
                                    </div>
                                </b-list-group-item>
                            </b-list-group>
                            <p class="card-text mt-2">
                                <b-btn
                                    v-b-modal.addModal
                                    variant="light"
                                    @click="group = g.id"
                                >
                                    <b-icon
                                        icon="plus"
                                        scale="1.5"
                                        variant="success"
                                    />
                                    Ajouter
                                </b-btn>
                            </p>
                        </b-card>
                    </b-card-group>
                </b-col>
            </b-row>
        </b-container>
        <b-modal
            id="deleteModal"
            cancel-title="Annuler"
            hide-header
            centered
            @ok="deleteCoreEntry"
        >
            Êtes-vous sûr de vouloir supprimer {{ currentItem.last_name }} {{ currentItem.first_name }} ?
        </b-modal>
        <b-modal
            id="deleteGroupModal"
            cancel-title="Annuler"
            hide-header
            centered
            @ok="deleteGroup"
        >
            Êtes-vous sûr de vouloir supprimer {{ currentGroup.name }} ?
        </b-modal>
        <b-modal
            id="addGroupModal"
            ref="addGroupModal"
            cancel-title="Annuler"
            title="Ajouter un groupe"
            centered
            @ok="addGroup"
            @hidden="resetGroupModal"
        >
            <b-form>
                <b-form-input
                    type="text"
                    v-model="groupName"
                    placeholder="Nom du groupe"
                />
            </b-form>
        </b-modal>
        <b-modal
            id="addModal"
            ref="addModal"
            cancel-title="Annuler"
            title="Ajouter une personne"
            ok-title="Ajouter"
            centered
            @ok="addEntry"
            @hidden="resetModal"
        >
            <form>
                <b-form-input
                    type="text"
                    v-model="last_name"
                    placeholder="Nom"
                    id="last_name"
                    aria-describedby="lastNameFeedback"
                    :state="inputStates.last_name"
                />
                <b-form-invalid-feedback id="lastNameFeedback">
                    {{ errorMsg('last_name') }}
                </b-form-invalid-feedback>
                <b-form-input
                    type="text"
                    v-model="first_name"
                    placeholder="Prénom"
                    id="first_name"
                    aria-describedby="firstNameFeedback"
                    :state="inputStates.first_name"
                />
                <b-form-invalid-feedback id="firstNameFeedback">
                    {{ errorMsg('first_name') }}
                </b-form-invalid-feedback>
                <b-form-input
                    type="email"
                    v-model="email"
                    placeholder="Email"
                    id="email"
                    aria-describedby="emailFeedback"
                    :state="inputStates.email"
                />
                <b-form-invalid-feedback id="emailFeedback">
                    {{ errorMsg('email') }}
                </b-form-invalid-feedback>
            </form>
        </b-modal>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue, { BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import axios from "axios";

import Menu from "../common/menu_bar.vue";

export default {
    data: function () {
        return {
            menuInfo: {},
            secretary: [],
            others: [],
            groups: [],
            otherEmails: {},
            currentItem: {},
            currentGroup: {},
            last_name: "",
            first_name: "",
            groupName: "",
            email: "",
            pk: null,
            group: null,
            errors: {},
            inputStates: {
                email: null,
                last_name: null,
                first_name: null,
            },
            mail_notification: true,
        };
    },
    watch: {
        errors: function (newErrors) {
            let inputs = ["email", "last_name", "first_name"];
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
            this.pk = "group" in item ? item.id : item.pk;
            if ("group" in item) {
                this.group = item.group;
            }
        },
        resetModal() {
            this.last_name = "";
            this.first_name = "";
            this.email = "";
            this.pk = null;
            this.group = null;
        },
        resetGroupModal() {
            this.groupName = "";
        },
        loadCorePeople(personType) {
            // Load person type.
            let param = { "person_type": personType };
            axios.get("/core/api/members", {params: param})
                .then(response => {
                    this[personType] = response.data.results;
                });
        },
        loadOtherPeople() {
            axios.get("/mail_notification/api/other_email/")
                .then(response => {
                    for (let g in this.groups) {
                        let id = this.groups[g].id;
                        let results = response.data.results.filter(e => e.group === id);
                        // So we are sure vue knows that the list changed.
                        Vue.set(this.otherEmails, id, results);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        loadGroups() {
            axios.get("/mail_notification/api/other_email_group/")
                .then(response => {
                    this.groups = response.data.results;
                    this.loadOtherPeople();
                });
        },
        deleteCoreEntry() {
            let token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let isCore = !("group" in this.currentItem);
            let path = isCore ? "/core/api/members/" : "/mail_notification/api/other_email/";
            let id = isCore ? this.currentItem.pk : this.currentItem.id;
            axios.delete(path + id, token)
                .then(() => {
                    if (isCore) {
                        this.loadCorePeople("others");
                    } else {
                        this.loadOtherPeople();
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        deleteGroup() {
            let token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let path = "/mail_notification/api/other_email_group/" + this.currentGroup.id + "/";
            axios.delete(path, token)
                .then(() => {
                    this.loadGroups();
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        addGroup(evt) {
            evt.preventDefault();

            let token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let data = {name: this.groupName};
            axios.post("/mail_notification/api/other_email_group/", data, token)
                .then(response => {
                    let id = response.data.id;
                    this.groups.push({"id": id, "name": this.groupName});
                    this.resetGroupModal();

                    this.$refs.addGroupModal.hide();
                })
                .catch(function (error) {
                    console.log(error);
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

            if (this.group) data.group = this.group;

            var path = this.group ? "/mail_notification/api/other_email/" : "/core/api/members/";
            // Check if this is a modification.
            if (this.pk) path += this.pk.toString() + "/";

            let token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let send = this.pk ? axios.put(path, data, token) : axios.post(path, data, token);
            send.then(() => {
                // Reload custom groups.
                if ("group" in data) {
                    this.loadOtherPeople();
                } else {
                    // Reload people list.
                    this.loadCorePeople("others");
                }
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
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
        // Load people.
        this.loadCorePeople("secretary");
        this.loadCorePeople("others");

        // Load other people (non core) if mail notification is enabled.
        if (!this.mail_notification) return;

        this.loadGroups();
    },
    components: {
        "app-menu": Menu,
    }
};
</script>

<style>
</style>
