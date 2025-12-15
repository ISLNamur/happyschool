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
        <BRow>
            <p>Pour le moment, HappySchool utilise principalement les pages d'administrations fournies par django.</p>
            <p>
                <BButton href="/admin">
                    Accèder à l'interface d'administration de django
                </BButton>
            </p>
        </BRow>
        <BRow>
            <h5>Établissement(s)</h5>
        </BRow>
        <BRow>
            <BCol>
                <BListGroup>
                    <BListGroupItem
                        v-for="item in teachings"
                        :key="item.pk"
                    >
                        {{ item.display_name }} ({{ item.name }})
                        <BButton
                            v-b-modal.addModal
                            variant="light"
                            @click="currentTeaching = item"
                            class="float-right"
                        >
                            <IBiPencilSquare
                                color="green"
                            />
                        </BButton>
                        <BButton
                            v-b-modal.deleteModal
                            variant="light"
                            class="float-right"
                            @click="currentTeaching = item"
                        >
                            <IBiTrashFill
                                color="red"
                            />
                        </BButton>
                    </BListGroupItem>
                </BListGroup>
                <p class="card-text mt-2">
                    <BButton
                        v-b-modal.addModal
                        variant="outline-success"
                    >
                        <IBiPlus
                            scale="1.5"
                            color="green"
                        />
                        Ajouter
                    </BButton>
                </p>
            </BCol>
        </BRow>
        <BRow>
            <h5>Logo</h5>
        </BRow>
        <BRow>
            <BCol>
                <BForm>
                    <BFormRow>
                        <BFormGroup description="Le logo doit être au format png.">
                            <BFormFile
                                v-model="logo"
                                accept=".png"
                                placeholder="Sélectionner le logo"
                            />
                        </BFormGroup>
                    </BFormRow>
                </BForm>
                <p class="card-text mt-2">
                    <BButton
                        variant="outline-success"
                        @click="sendLogo"
                        :disabled="!logo"
                    >
                        <IBiPlus
                            scale="1.5"
                            color="green"
                        />
                        Envoyer
                    </BButton>
                </p>
            </BCol>
        </BRow>
        <b-modal
            id="deleteModal"
            cancel-title="Annuler"
            hide-header
            centered
            @ok="deleteTeaching"
            @hidden="resetTeachings"
        >
            Êtes-vous sûr de vouloir supprimer {{ currentTeaching.display_name }} ({{ currentTeaching.name }})
            ainsi que toutes les classes cet établissement définitivement ?
        </b-modal>
        <b-modal
            id="addModal"
            ref="addModal"
            cancel-title="Annuler"
            title="Ajouter/Modifier un établissement"
            ok-title="Ajouter"
            centered
            @ok="setTeaching"
            @hidden="resetTeachings"
        >
            <form>
                <BFormInput
                    type="text"
                    v-model="currentTeaching.display_name"
                    placeholder="Nom d'affichage"
                    aria-describedby="displayNameFeedback"
                    :state="inputStates.display_name"
                />
                <BFormInvalidFeedback id="displayNameFeedback">
                    {{ errorMsg('display_name') }}
                </BFormInvalidFeedback>
                <BFormInput
                    type="text"
                    v-model="currentTeaching.name"
                    placeholder="Nom simple"
                    aria-describedby="nameFeedback"
                    :state="inputStates.name"
                />
                <BFormInvalidFeedback id="nameFeedback">
                    {{ errorMsg('name') }}
                </BFormInvalidFeedback>
            </form>
        </b-modal>
    </div>
</template>

<script>
import { useToastController } from "bootstrap-vue-next";

import axios from "axios";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            teachings: [],
            currentTeaching: { display_name: null, name: null },
            inputStates: { display_name: null, name: null },
            errors: {},
            logo: null,
        };
    },
    watch: {
        errors: function (newErrors) {
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
            data.append("file", this.logo);
            axios.post("/core/api/logo/", data, token)
                .then(() => {
                    this.logo = null;
                    this.show({
                        body: "Le logo a été envoyé, actualisez la page pour voir le nouveau logo.",
                        variant: "success",
                        noCloseButton: true,
                    });
                })
                .catch((err) => {
                    alert(err);
                });
        },
        deleteTeaching: function () {
            axios.delete("/core/api/teaching/" + this.currentTeaching.id + "/", token);
        },
        resetTeachings: function () {
            this.currentTeaching = { display_name: null, name: null };
            axios.get("/core/api/teaching/")
                .then((response) => {
                    this.teachings = response.data.results;
                });
        },
        setTeaching: function () {
            // evt.preventDefault();

            let modal = this;
            let path = "/core/api/teaching/";
            const isModify = "id" in this.currentTeaching;
            if (isModify) path += this.currentTeaching.id + "/";

            let send = isModify ? axios.put(path, this.currentTeaching, token) : axios.post(path, this.currentTeaching, token);
            send.then(() => {
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
    },
};
</script>
