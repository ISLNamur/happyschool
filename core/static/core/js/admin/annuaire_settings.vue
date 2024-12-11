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
        <BRow>
            <BCol>
                <h5>Gestion des accès aux données</h5>
            </BCol>
        </BRow>
        <div
            v-for="permission in permissions"
            :key="permission.title"
        >
            <BRow>
                <BCol>
                    <BCard
                        no-body
                        class="mb-2"
                    >
                        <BCardHeader>
                            {{ permission.title }}
                        </BCardHeader>
                        <BListGroup flush>
                            <BListGroupItem
                                v-for="group in permission.canSee"
                                :key="group.id"
                            >
                                {{ group.name }}
                                <BButton
                                    variant="light"
                                    class="float-right"
                                    size="sm"
                                    @click="deleteGroup(permission.permissionName, group)" 
                                >
                                    <IBiTrashFill
                                        color="red"
                                    />
                                </BButton>
                            </BListGroupItem>
                        </BListGroup>
                        <BcardBody body-bg-variant="light">
                            <BFormGroup label="Sélectionner un groupe dans la liste et cliquer sur 'Ajouter'">
                                <BInputGroup>
                                    <BFormSelect
                                        v-model="permission.selected"
                                        :options="permission.availableGroups"
                                        value-field="id"
                                        text-field="name"
                                    />
                                    <template #append>
                                        <BButton
                                            size="sm"
                                            text="Button"
                                            variant="success"
                                            @click="sendPermission(permission.permissionName)"
                                        >
                                            Ajouter
                                        </BButton>
                                    </template>
                                </BInputGroup>
                            </BFormGroup>
                        </BcardBody>
                    </BCard>
                </BCol>
            </BRow>
        </div>
        <BRow>
            <BCol>
                <h5>Afficher les identifiants</h5>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup 
                    description=" Afficher les champs utilisateur/mot de passe dans la fiche info et ainsi que la liste des mots de passe des élèves par classe"
                >
                    <BFormCheckbox 
                        v-model="credentials"
                        @update:model-value="sendCredentials"
                    >
                        Afficher les champs utilisateur/mot de passe
                    </BFormCheckbox>
                </BFormGroup>
            </BCol>
        </BRow>
    </div>
</template>

<script>
import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function() {
        return {
            /** A list of permissions which includes:
             * - Current groups (canSee),
             * - Groups that can be added (availableGroups),
             * - Group selected in the adding form (selected),
             * - Name of the permission (permissionName),
             * - A description of the permission (title).
             * */
            permissions: [
                {
                    title: "Groupes pouvants voir les responsables (professeurs, éducateurs,… )",
                    permissionName: "responsibles",
                    canSee: [],
                    selected: null,
                    availableGroups: [],
                },
                {
                    title: "Groupes pouvants voir les données sensibles des responsables (professeurs, éducateurs,… )",
                    permissionName: "responsibles_sensitive",
                    canSee: [],
                    selected: null,
                    availableGroups: [],
                },
                {
                    title: "Groupes pouvants voir les données sensibles des élèves (adresses, professions des parents,… )",
                    permissionName: "student_sensitive",
                    canSee: [],
                    selected: null,
                    availableGroups: [],
                },
                {
                    title: "Groupes pouvants voir les données de contact des élèves",
                    permissionName: "student_contact",
                    canSee: [],
                    selected: null,
                    availableGroups: [],
                },
                {
                    title: "Groupes pouvants voir les données médiacles des élèves",
                    permissionName: "student_medical",
                    canSee: [],
                    selected: null,
                    availableGroups: [],
                },
            ],
            /** State of the credentials setting. */
            credentials: null,
            /** List of all groups avalaible. */
            groups: [],
        };
    },
    methods: {
        /** Update credential setting. */
        sendCredentials: function() {
            this.credentials = !this.credentials;
            axios.put("/annuaire/api/settings/1/",{ show_credentials: this.credentials },token)
                .then(() => {
                    this.show({props: {
                        body: "Sauvegardé.",
                        variant: "success",
                        noCloseButton: true
                    }});
                });
        },
        /** Add a group in a permission.
         * 
         * @param {String} permName The name of the permission.
         */
        sendPermission: function(permName) {
            let permission = this.permissions.find(p => p.permissionName == permName);
            // Create a new list so we can ensure that canSee is updated after sending it.
            const canSeeData = permission.canSee.map(g => g.id).concat([permission.selected]);
            axios.put(
                "/annuaire/api/settings/1/",
                {["can_see_" + permName]: canSeeData},
                token
            )
                .then(() => {
                    permission.canSee = canSeeData.map(id => this.groups.find(g => g.id == id));
                    permission.availableGroups = permission.availableGroups.filter(aG => aG.id != permission.selected);
                    permission.selected = null;
                    this.show({props: {
                        body: "Sauvegardé.",
                        variant: "success",
                        noCloseButton: true
                    }});
                })
                .catch(err => {
                    alert(err);
                });
        },
        /** Remove group from a permission.
         * 
         * @param {String} permName The name of the permission.
         * @param {Object} group The group that has to be removed.
         */
        deleteGroup: function(permName, group) {
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer " + group.name +" ?")
                .then(remove => {
                    if (!remove) return;

                    let permission = this.permissions.find(p => p.permissionName == permName);
                    // Create a new list so we can ensure that canSee is updated after sending it.
                    const canSeeData = permission.canSee.map(g => g.id).filter(id => id != group.id);
                    axios.put(
                        "/annuaire/api/settings/1/",
                        { ["can_see_" + permName]: canSeeData},
                        token
                    )
                        .then(() => {
                            permission.canSee = canSeeData.map(id => this.groups.find(g => g.id == id));
                            permission.availableGroups = permission.availableGroups.concat([group]);
                        })
                        .catch(err => {
                            alert(err);
                        });
                }); 
        },
        /* Get the list of groups that can be chosen. **/
        getGroups: function() {
            axios.get("/core/api/group/")
                .then(response => {
                    this.groups = response.data.results.filter(text => {
                        if (isNaN(text.name[text.name.length - 1])) {
                            return true;
                        }
                    });
                });
        },
    },
    mounted: function() {
        this.getGroups();
        axios
            .get("/annuaire/api/settings/1/") //allready selected
            .then(response => {
                this.credentials = response.data.show_credentials;
                this.permissions.forEach(perm => {
                    perm.canSee = response.data["can_see_" + perm.permissionName].map(groupId => this.groups.find(g => g.id == groupId));
                    perm.availableGroups = this.groups.filter(g => {
                        return !perm.canSee.find(usedGroup => usedGroup.name == g.name);
                    });
                });
            })
            .catch(function(error) {
                alert(error);
            });
    },
};
</script>
