<template>
<div>
    <b-modal size="lg" title="Ajouter un appel"
        ok-title="Soumettre" cancel-title="Annuler"
        ref="addModal"
        >
        <b-row>
            <b-col sm="4">PHOTO</b-col>
            <b-col>
                <b-form>
                    <b-form-row>
                        <b-col sm="8">
                            <b-form-group label="Nom" label-for="input-name">
                                <!-- <b-form-input id="input-name" size="sm" type="text" placeholder="Nom et prénom"></b-form-input> -->
                                <multiselect
                                    :internal-search="false"
                                    :options="nameOptions"
                                    @search-change="getNameOptions"
                                    :loading="nameLoading"
                                    placeholder="Rechercher une personne…"
                                    select-label=""
                                    selected-label="Sélectionné"
                                    deselect-label=""
                                    label="display"
                                    track-by="matricule"
                                    v-model="name"
                                    >
                                    <span slot="noResult">Aucune personne trouvée.</span>
                                </multiselect>
                            </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Matricule" label-for="input-matricule">
                                <b-form-input id="input-matricule" type="text" v-model="name.matricule" readonly></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Objet" label-for="input-objet">
                                <b-form-select v-model="object" :options="objectOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un objet</option>
                                    </template>
                                </b-form-select>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Motif" label-for="input-motif">
                                <b-form-select v-model="motive" :options="motiveOptions">
                                    <template slot="first">
                                        <option :value="null" disabled>Choisissez un motif</option>
                                    </template>
                                </b-form-select>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col sm="4">
                            <b-form-group label="Début du motif" label-for="input-date-motif-start">
                                <b-form-input id="input-date-motif-start" type="date"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col sm="2">
                            <b-form-group label="(heure)" label-for="input-time-motif-start">
                                <b-form-input id="input-time-motif-start" type="time" step="300"></b-form-input>
                            </b-form-group>
                        </b-form-group>
                        </b-col>
                        <b-col sm="4">
                            <b-form-group label="Fin du motif" label-for="input-date-motif-end">
                                <b-form-input id="input-date-motif-end" type="date"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col sm="2">
                            <b-form-group label="(heure)" label-for="input-time-motif-end">
                                <b-form-input id="input-time-motif-end" type="time" step="300"></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Date de l'appel" label-for="input-date-appel">
                                <b-form-input id="input-date-appel" type="date"></b-form-input>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group label="Heure de l'appel" label-for="input-time-appel">
                                <b-form-input id="input-time-appel" type="time" step="60"></b-form-input>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                    <b-form-row>
                        <b-col>
                            <b-form-group label="Commentaires" label-for="input-comment">
                                <b-form-textarea id="input-comment" :rows="3"></b-form-textarea>
                            </b-form-group>
                        </b-col>
                    </b-form-row>
                </b-form>
            </b-col>
        </b-row>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Moment from 'moment';
Moment.locale('fr');

import axios from 'axios';
window.axios = axios;
window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

export default {
    data: function () {
        return {
            object: null,
            objectOptions: [],
            motive: null,
            motiveOptions: [],
            name: {matricule: null},
            nameOptions: [],
            nameLoading: false,
            searchId: 0,
        };
    },
    methods: {
        show: function () {
            this.$refs.addModal.show();
        },
        hide: function() {
            this.$refs.addModal.hide();
        },
        getNameOptions(query) {
            this.searchId += 1;
            let currentSearch = this.searchId;
            this.nameLoading = true;
            axios.get("/annuaire/api/?query=" + query)
            .then(response => {
                // Avoid that a previous search overwrites a faster following search results.
                if (this.searchId !== currentSearch)
                    return;
                this.nameOptions = response.data.map(p => {
                    // Format entries.
                    let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                    if ('classe' in p) {
                        // It's a student.
                        entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                        entry.display += " – " + p.teaching.display_name;
                    } else {
                        // It's a responsible.
                        let teachings = " —";
                        for (let t in p.teaching) {
                            teachings += " " + p.teaching[t].display_name;
                        }
                        entry.display += teachings;
                    }
                    return entry;
                });
                this.nameLoading = false;
            })
            .catch(function (error) {
                this.nameLoading = false;
            });
        },
    },
    components: {Multiselect},
    mounted: function () {
        // Set motive options.
        axios.get('/appels/api/motive/')
        .then(response => {
            this.motiveOptions = response.data.results.map(m => {
                return {value: m.id, text: m.motive}
            });
        });
        // Set object options.
        axios.get('/appels/api/object/')
        .then(response => {
            this.objectOptions = response.data.results.map(m => {
                return {value: m.id, text: m.object}
            });
        });
    }
}
</script>

<style>
</style>
