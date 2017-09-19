<template>
    <b-modal size="lg" title="Ajouter un changement"
        ok-title="Soumettre" cancel-title="Annuler"
        ref="addModal"
        v-on:ok="submitForm"
        v-on:hidden="resetData"
        >
        <b-form>
            <b-form-row>
                <b-form-group
                    id="date-start-input-group"
                    description="Date de début de l'absence"
                    label="Date début :"
                    :state="errors.date_start"
                    >

                    <b-form-input type="date" v-model="date_start">
                    </b-form-input>
                    <b-form-feedback>
                        Merci de mettre une date de début correcte.
                    </b-form-feedback>
                </b-form-group>
                <b-form-group
                    id="time-start-input-group"
                    description="Heure de début de l'absence"
                    label="Heure de début :"
                    >
                    <b-form-input type="time" v-model="time_start"></b-form-input>
                </b-form-group>
            </b-form-row>
            <b-form-row>
                <b-form-group
                    id="date-end-input-group"
                    description="Date de fin de l'absence"
                    label="Date fin :"
                    >
                    <b-form-input type="date" v-model="date_end">
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    id="time-end-input-group"
                    description="Heure de fin de l'absence"
                    label="Heure de fin :"
                    >
                    <b-form-input type="time" v-model="time_end"></b-form-input>
                </b-form-group>
            </b-form-row>
            <b-form-group
                label="Classe(s) et/ou année(s)"
                >
                <multiselect
                    :internal-search="false"
                    :options="options.classesOptions"
                    @search-change="getStudentsClassesYears"
                    :multiple="true"
                    :loading="classesIsLoading"
                    placeholder="Chercher une classe ou une année…"
                    select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                    selected-label="Sélectionné"
                    deselect-label="Cliquer dessus pour enlever"
                    v-model="classes"
                    >
                    <span slot="noResult">Aucune classe trouvée.</span>
                </multiselect>
            </b-form-group>
            <b-form-group
                label="Activité"
                >
                <b-form-input type="text" v-model="activity"></b-form-input>
            </b-form-group>
            <b-form-group
                label="Professeurs"
                >
                <multiselect
                    :internal-search="false"
                    :options="options.teachersOptions"
                    @search-change="getTeachers"
                    :multiple="true"
                    placeholder="Ajouter un ou des professeurs…"
                    :loading="teachersIsLoading"
                    select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                    selected-label="Sélectionné"
                    deselect-label="Cliquer dessus pour enlever"
                    v-model="teachers"
                    >
                    <span slot="noResult">Aucun professeur trouvé.</span>
                </multiselect>
            </b-form-group>
            <b-form-group
                label="Lieu"
                >
                <b-form-input type="text" v-model="place"></b-form-input>
            </b-form-group>
            <b-form-group
                label="Commentaire"
                >
                <b-form-textarea v-model="comment" :rows="2"
                    placeholder="Un commentaire sur le changement">
                </b-form-textarea>
            </b-form-group>
        </b-form>
    </b-modal>
</template>

<script>
import Moment from 'moment';
Moment.locale('fr');

import vSelect from "vue-select"
import Multiselect from 'vue-multiselect'

import axios from 'axios';

export default {
    props: {
        appeSocket: {
            default: null
        },
        teaching: {
            default: ['all']
        },
        errors: null,
        options: null,
    },
    data: function () {
        return {
            id: -1,
            date_start: "",
            time_start: null,
            date_end: null,
            time_end: null,
            classes: [],
            classesIsLoading: false,
            activity: "",
            teachers: [],
            teachersIsLoading: false,
            place: "",
            comment: "",
        };
    },
    methods: {
        resetData: function () {
            Object.assign(this.$data, this.$options.data.call(this));
        },
        show: function () {
            this.$refs.addModal.show();
        },
        hide: function() {
            this.$refs.addModal.hide();
        },
        getStudentsClassesYears(search) {
            this.classesIsLoading = true;
            this.appeSocket.send("get_students_classes_years", {"query": search, "context": "add-modal", "teaching": this.teaching});
        },
        getTeachers(search) {
            this.teachersIsLoading = true;
            this.appeSocket.send("get_teachers", {"query": search, "context": "add-modal", "teaching": this.teaching});
        },
        submitForm: function (evt) {
            evt.preventDefault();

            let actionType = this.id < 0 ? "create" : "update"

            let data = {
                date_start: this.date_start,
                time_start: this.time_start,
                date_end: this.date_end,
                time_end: this.time_end,
                classes: this.classes,
                activity: this.activity,
                teachers: this.teachers,
                place: this.place,
                comment: this.comment,
            }
            console.log(data);

            if (this.id < 0) {
                // Create new entry.
                this.appeSocket.create("schedule_change", data);
            } else {
                // Update entry.
                this.appeSocket.update("schedule_change", this.id, data);
            }
        }
    },
    components: {Multiselect},
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
</style>
