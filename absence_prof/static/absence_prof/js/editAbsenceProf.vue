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
    <BContainer>
        <BRow>
            <h3>Absence Prof : {{ this.id ? "Modification" : "Ajout" }}</h3>
        </BRow>
        <BRow>
            <BCol>
                <BButton to="/">
                    Retour à la liste des absences
                </BButton>
            </BCol>
        </BRow>
        <BRow>
            <BCol sm="4">
                <BImg
                    rounded
                    :src="`/static/photos_prof/${form.id_person}.jpg`"
                    fluid
                    alt="Photo de la personne"
                />
            </BCol>
            <BCol>
                <BForm
                    @submit="submit"
                    @reset="reset"
                >
                    <BFormGroup class="mb-1">
                        <multiselect
                            :internal-search="false"
                            :options="responsibleOptions"
                            @search-change="getResponsibles"
                            placeholder="Personne absente"
                            :loading="searching"
                            select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            v-model="person"
                            label="display"
                            track-by="matricule"
                            :show-no-options="false"
                            :multiple="!id"
                        >
                            <template #noResult>
                                Aucun responsable trouvé.
                            </template>
                            <template #noOptions />
                        </multiselect>
                    </BFormGroup>
                    <BFormGroup
                        label="Motif"
                        class="mb-1"
                    >
                        <BFormSelect
                            v-model="form.motif"
                            :options="motifOptions"
                            required
                        />
                    </BFormGroup>
                    <BFormGroup
                        label="Date de début"
                        :state="inputStates.non_field_errors"
                        class="mb-1"
                    >
                        <BFormInput
                            v-model="form.date_absence_start"
                            type="date"
                            required
                            @update:model-value="updateEnd"
                        />
                        <template #invalid-feedback>
                            {{ errorMsg('non_field_errors') }}
                        </template>
                    </BFormGroup>
                    <BFormGroup
                        label="Date de fin"
                        :state="inputStates.non_field_errors"
                        class="mb-1"
                    >
                        <BFormInput
                            v-model="form.date_absence_end"
                            type="date"
                            required
                        />
                        <template #invalid-feedback>
                            {{ errorMsg('non_field_errors') }}
                        </template>
                    </BFormGroup>
                    <BFormGroup
                        label="Commentaire"
                        class="mb-1"
                    >
                        <BFormTextarea v-model="form.comment" />
                    </BFormGroup>
                    <BButton
                        type="submit"
                        variant="primary"
                        :disabled="sending"
                    >
                        Soumettre
                    </BButton>
                </BForm>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import {getPeopleByName} from "@s:core/js/common/search.js";
import { absenceProfStore } from "./stores/index.js";

import { useToastController } from "bootstrap-vue-next";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        id: {
            type: String,
            default: null,
        }
    },
    watch: {
        id: function (newVal) {
            if (newVal) {
                this.loadAbsence(newVal);
            } else {
                this.reset();
            }
        },
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
    data: function () {
        return {
            responsibleOptions: [],
            motifOptions: [],
            searching: false,
            form: {
                id_person: null,
                name: null,
                motif: null,
                date_absence_start: null,
                date_absence_end: null,
                comment: "",
            },
            person: [],
            searchId: -1,
            sending: false,
            errors: {},
            inputStates: {
                non_field_errors: null
            },
            store: absenceProfStore(),
        };
    },
    methods: {
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        updateEnd: function (value) {
            if (!this.form.date_absence_end) this.form.date_absence_end = value;
        },
        loadAbsence: function () {
            axios.get(`/absence_prof/api/absence/${this.id}/`, token)
                .then(resp => {
                    if (resp.data) {
                        axios.get(`/annuaire/api/responsible/${resp.data.id_person}/`, token)
                            .then(resp => {
                                this.person = [resp.data];
                            });
                        this.form.id_person = resp.data.id_person;
                        this.form.motif = resp.data.motif;
                        this.form.name = resp.data.name;
                        this.form.date_absence_start = resp.data.date_absence_start;
                        this.form.date_absence_end = resp.data.date_absence_end;
                        this.form.comment = resp.data.comment;
                    }
                })
                .catch(err => {
                    alert(err);
                });
        },
        reset: function () {

        },
        submit: function (evt) {
            evt.preventDefault();

            this.sending = true;
            const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

            const promises = [];
            for (let p in this.person) {
                let data = Object.assign({}, this.form);
                data.id_person = this.person[p].matricule;
                data.name = this.person[p].display;
                let send = this.id ? axios.put : axios.post;
                let url = "/absence_prof/api/absence/";
                if (this.id) url += this.id + "/";
                promises.push(send(url, data, token));
            }
            Promise.all(promises)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/").then(() => {
                        this.show({
                            body: "Les données ont bien été envoyées",
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch(err => {
                    this.errors = err.response.data;
                    this.sending = false;
                });
        },
        getResponsibles: function (query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.searching = true;

            getPeopleByName(query, this.store.settings.teachings, "responsible")
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                    this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                    this.searching = false;
                });
        }
    },
    mounted: function () {
        const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
        axios.get("/absence_prof/api/motif/", token)
            .then(resp => {
                this.motifOptions = resp.data.results.map(v => {return {value: v.motif, text: v.motif};});
            })
            .catch(() => {
                alert("Unable to get motives");
            });

        if (this.id) this.loadAbsence();
    },
    components: {
        Multiselect
    }
};
</script>
