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
        <h4>Annuaire</h4>
        <br>
        <!-- groups who can see responsibles -->
        <b-row>
            <h5>Groupes pouvants voir les responsables (professeurs, éducateurs,...)</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <b-list-group-item
                        v-for="item in options_responsibles"
                        :key="item.pk"
                    >
                        {{ item }}
                        <b-btn
                            variant="light"
                            class="float-right"
                            @click="deleteGroup('responsibles',item)" 
                        >
                            <icon
                                name="remove"
                                scale="1"
                                color="red"
                            />
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
                <br>
                <b-form-group label="Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'">
                    <b-input-group>
                        <b-form-select
                            v-model="selected_responsibles.name"
                            :options="groups_name_responsibles"
                            value-field="name"
                            text-field="name"
                        />
                        <b-input-group-append>
                            <b-button
                                size="sm"
                                text="Button"
                                variant="success"
                                @click="send('responsibles')"
                            >
                                Ajouter
                            </b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
        </b-row>
        <br>
        <!-- groups who can see responsibles sensitive -->
        <b-row>
            <h5>Groupes pouvants voir les données sensibles des responsables (professeurs, éducateurs,...)</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <b-list-group-item
                        v-for="item in options_responsibles_sensitive"
                        :key="item.pk"
                    >
                        {{ item }}
                        <b-btn
                            variant="light"
                            class="float-right"
                            @click="deleteGroup('responsibles_sensitive',item)" 
                        >
                            <icon
                                name="remove"
                                scale="1"
                                color="red"
                            />
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
                <br>
                <b-form-group label="Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'">
                    <b-input-group>
                        <b-form-select
                            v-model="selected_responsibles_sensitive.name"
                            :options="groups_name_responsibles_sensitive"
                            value-field="name"
                            text-field="name"
                        />
                        <b-input-group-append>
                            <b-button
                                size="sm"
                                text="Button"
                                variant="success"
                                @click="send('responsibles_sensitive')"
                            >
                                Ajouter
                            </b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
        </b-row>
        <!-- groups who can see student contact -->
        <b-row>
            <h5>Groupes pouvants voir les données de contact des élèves</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <b-list-group-item
                        v-for="item in options_student_contact"
                        :key="item.pk"
                    >
                        {{ item }}
                        <b-btn
                            variant="light"
                            class="float-right"
                            @click="deleteGroup('student_contact',item)" 
                        >
                            <icon
                                name="remove"
                                scale="1"
                                color="red"
                            />
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
                <br>
                <b-form-group label="Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'">
                    <b-input-group>
                        <b-form-select
                            v-model="selected_student_contact.name"
                            :options="groups_name_student_contact"
                            value-field="name"
                            text-field="name"
                        />
                        <b-input-group-append>
                            <b-button
                                size="sm"
                                text="Button"
                                variant="success"
                                @click="send('student_contact')"
                            >
                                Ajouter
                            </b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
        </b-row>
        <!-- groups who can see student medical -->
        <b-row>
            <h5>Groupes pouvants voir les données médiacles des élèves</h5>
        </b-row>
        <b-row>
            <b-col>
                <b-list-group>
                    <b-list-group-item
                        v-for="item in options_student_medical"
                        :key="item.pk"
                    >
                        {{ item }}
                        <b-btn
                            variant="light"
                            class="float-right"
                            @click="deleteGroup('student_medical',item)" 
                        >
                            <icon
                                name="remove"
                                scale="1"
                                color="red"
                            />
                        </b-btn>
                    </b-list-group-item>
                </b-list-group>
                <br>
                <b-form-group label="Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'">
                    <b-input-group>
                        <b-form-select
                            v-model="selected_student_medical.name"
                            :options="groups_name_student_medical"
                            value-field="name"
                            text-field="name"
                        />
                        <b-input-group-append>
                            <b-button
                                size="sm"
                                text="Button"
                                variant="success"
                                @click="send('student_medical')"
                            >
                                Ajouter
                            </b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
        </b-row>
        <br>
        <b-row>
            <h5>Afficher les identifiants</h5>
        </b-row>
        <br>
        <b-row>
            <b-col>
                <b-form-group 
                    description=" Afficher les champs utilisateur/mot de passe dans la fiche info et ainsi que la liste des mots de passe des élèves par classe"
                >
                    <b-form-checkbox 
                        v-model="credentials"
                        @change="send_credentials"
                    >
                        Afficher les champs utilisateur/mot de passe
                    </b-form-checkbox>
                </b-form-group>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

import axios from "axios";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    data: function() {
        return {
            credentials: null,
            selected_responsibles: { id: null, name: null },
            selected_responsibles_sensitive: { id: null, name: null },
            selected_student_contact: { id: null, name: null },
            selected_student_medical: { id: null, name: null },
            options_responsibles: [],
            options_responsibles_sensitive: [],
            options_student_contact: [],
            options_student_medical: [],
            groupOptions: [],
            responsibles: [],
            groups_name_responsibles: [],
            groups_name_responsibles_sensitive: [],
            groups_name_student_contact: [],
            groups_name_student_medical: [],
            groups: [],
            inputStates: { display_name: null, name: null },
            errors: {},
            logo: null
        };
    },
    watch: {
        errors: function(newErrors) {
            const inputs = Object.keys(this.inputStates);
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
        send_credentials:function(){
            this.credentials = !this.credentials;
            axios.put("/annuaire/api/settings/1/",{ show_credentials: this.credentials },token)
                .then(() => {
                    this.$bvToast.toast("Sauvegardé.", {
                        variant: "success",
                        noCloseButton: true
                    });
                });
        },
        send: function(grp) {
            const selected = this["selected_" + grp];
            const groups_name = this["groups_name_" + grp];
            const options = this["options_" + grp];
            const groupOptions = this["groupOptions_" + grp];
            for (let i in this.groups) {
                if (this.groups[i].name == selected.name) {
                    selected.id = this.groups[i].id;
                    break;
                }
            }
            for (let i in this.groups_name_responsibles) {
                if (groups_name[i] == selected.name) {
                    groups_name.splice(i, 1);
                    break;
                }
            }
            options.push(selected.name);
            groupOptions.push(selected.id);
            axios
                .put(
                    "/annuaire/api/settings/1/",
                    { ["can_see_" + grp]: groupOptions },
                    token
                ) //  /core/api/group/
                .then(() => {
                    selected.name = null;
                    selected.id = null;
                    this.$bvToast.toast("Sauvegardé.", {
                        variant: "success",
                        noCloseButton: true
                    });
                })
                .catch(err => {
                    alert(err);
                });
        },
        deleteGroup: function(grp,item) {
            var currentGroup = { id: null, name: null };
            const groupOptions = this["groupOptions_" + grp];
            const options = this["options_" + grp];
            const grp_name = this["groups_name_" + grp];
            this.$bvModal.msgBoxOk("Êtes-vous sûr de vouloir supprimer " + item +" ?")
                .then(() => {
                    for (let i in this.groups) {
                        if (this.groups[i].name == item) {
                            currentGroup.id = this.groups[i].id;
                            break;
                        }
                    }
                    for (let i in groupOptions) {
                        if (currentGroup.id == groupOptions[i]) {
                            groupOptions.splice(i, 1);
                            options.splice(i, 1);
                            break;
                        }
                    }
                    grp_name.push(item);
                    this["options_" + grp]=options;
                    this["group_name" + grp]=grp_name;
                    axios.put(
                        "/annuaire/api/settings/1/",
                        { ["can_see_" + grp]: this["groupOptions_" +grp]},
                        token
                    );
                }); 
        },
        resetGroups: function() {
            axios
                .get("/core/api/group/") //all can be selected
                .then(response => {
                    this.groups = response.data.results.filter(text => {
                        if (isNaN(text.name[text.name.length - 1])) {
                            return true;
                        }
                    });
                });
        },
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        }
    },
    mounted: function() {
        var names_groups = ["responsibles","responsibles_sensitive","student_contact","student_medical"];
        this.resetGroups();
        axios
            .get("/annuaire/api/settings/1/") //allready selected
            .then(response => {
                this.credentials = response.data.show_credentials;
                this.groupOptions_responsibles = response.data.can_see_responsibles;
                this.groupOptions_responsibles_sensitive = response.data.can_see_responsibles_sensitive;
                this.groupOptions_student_contact = response.data.can_see_student_contact;
                this.groupOptions_student_medical = response.data.can_see_student_medical;
                for (let i in names_groups){
                    var groupOptions = this["groupOptions_" + names_groups[i]];
                    var options = this["options_" + names_groups[i]];
                    var groups_names = this["groups_name_" + names_groups[i]];
                    for (let item in groupOptions) {
                        for (let temp in this.groups) {
                            if (groupOptions[item] == this.groups[temp].id) {
                                options.push(this.groups[temp].name);
                            }
                        }
                    }
                    for (let temp in this.groups) {
                        if (!options.includes(this.groups[temp].name)) {
                            groups_names.push(this.groups[temp].name);
                        }
                    }
                    options = options.filter(text => {
                        if (isNaN(text[text.length - 1])) {
                            return true;
                        }
                    });
                    this["groupOptions" + names_groups[i]] = groupOptions;
                    this["options" + names_groups[i]] = options;
                    this["groups_names" + names_groups[i]] = groups_names;
                }
            })
            .catch(function(error) {
                alert(error);
            });
    },
    components: {}
};
</script>

    
