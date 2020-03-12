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
    <b-container>
        <b-row>
            <h3>PIA : {{ id ? "Modifier" : "Nouveau" }}</h3>
        </b-row>
        <b-row class="sticky-top p-2 first-line">
            <b-col>
                <b-btn to="/">
                    Retour à la liste des PIA
                </b-btn>
            </b-col>
            <b-col
                cols="2"
                align-self="end"
            >
                <b-btn
                    @click="submit"
                    variant="primary"
                    :disabled="!form.student"
                >
                    Sauver
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <h4>Référents PIA</h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-row>
                    <b-col md="4">
                        <b-form-group label="Élève">
                            <multiselect
                                id="student-0"
                                :internal-search="false"
                                :options="studentOptions"
                                @search-change="getPeople"
                                placeholder="Référent"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="form.student"
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                                :disabled="parseInt(id) >= 0"
                            >
                                <span slot="noResult">Aucun responsable trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                        </b-form-group>
                    </b-col>
                </b-form-row>
                <b-form-row>
                    <b-col md="6">
                        <b-form-group
                            label="Référent(s)"
                            :state="inputStates.referent"
                        >
                            <multiselect
                                id="responsible-0"
                                :internal-search="false"
                                :options="responsibleOptions"
                                @search-change="getPeople"
                                placeholder="Référent"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="form.referent"
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                                multiple
                            >
                                <span slot="noResult">Aucun responsable trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('referent') }}</span>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Parrain/Marraine"
                            :state="inputStates.referent"
                        >
                            <multiselect
                                id="responsible-1"
                                :internal-search="false"
                                :options="responsibleOptions"
                                @search-change="getPeople"
                                placeholder="Parrain/Marraine"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="form.sponsor"
                                label="display"
                                track-by="matricule"
                                :show-no-options="false"
                                multiple
                            >
                                <span slot="noResult">Aucun responsable trouvé.</span>
                                <span slot="noOptions" />
                            </multiselect>
                            <span slot="invalid-feedback">{{ errorMsg('sponsor') }}</span>
                        </b-form-group>
                    </b-col>
                </b-form-row>
            </b-col>
        </b-row>
        <b-row>
            <h4>Aménagements</h4>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group
                    label="Trouble d'apprentissage"
                    label-cols="3"
                    :state="inputStates.disorder"
                >
                    <multiselect
                        :options="disorderOptions"
                        placeholder="Sélectionner le ou les différents troubles"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.disorder"
                        :show-no-options="false"
                        track-by="id"
                        label="disorder"
                        @input="updateDisorderResponse"
                        multiple
                    >
                        <span slot="noResult">Aucun trouble trouvé.</span>
                        <span slot="noOptions" />
                    </multiselect>
                    <span slot="invalid-feedback">{{ errorMsg('disorder') }}</span>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group
                    label="Aménagements raisonnables liés au trouble"
                    label-cols="3"
                    :state="inputStates.disorder_response"
                >
                    <multiselect
                        :options="disorderResponseOptions"
                        placeholder="Sélectionner le ou les différents aménagements"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.disorder_response"
                        :show-no-options="false"
                        track-by="id"
                        label="response"
                        multiple
                    >
                        <span slot="noResult">Aucun aménagements trouvé.</span>
                        <span slot="noOptions" />
                    </multiselect>
                    <span slot="invalid-feedback">{{ errorMsg('disorder_response') }}</span>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group
                    label="Aménagements d'horaire"
                    label-cols="3"
                    :state="inputStates.schedule_adjustment"
                >
                    <multiselect
                        :options="scheduleAdjustmentOptions"
                        placeholder="Sélectionner le ou les différents adaptations"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        v-model="form.schedule_adjustment"
                        track-by="id"
                        label="schedule_adjustment"
                        :show-no-options="false"
                        multiple
                    >
                        <span slot="noResult">Aucun aménagements trouvé.</span>
                        <span slot="noOptions" />
                    </multiselect>
                    <span slot="invalid-feedback">{{ errorMsg('schedule_adjustment') }}</span>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <h4>Conseil de classe</h4>
        </b-row>
        <b-row>
            <b-col>
                <b-btn @click="classCouncil.unshift({id: -1})">
                    Ajouter un conseil de classe
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <class-council
                    v-for="(council, index) in classCouncil"
                    :key="council.id"
                    :class_council="council"
                    ref="councils"
                    class="mt-2"
                    @remove="removeClassCouncil(index)"
                />
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <h4>Objectifs transversaux</h4>
        </b-row>
        <b-row>
            <b-col>
                <b-btn @click="cross_goal.unshift({id: -1})">
                    Ajouter
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <goal
                    class="mt-2"
                    v-for="(goal, index) in cross_goal"
                    :key="'cg-' + goal.id"
                    :goal-object="goal"
                    ref="crossgoals"
                    @remove="removeGoal('cross_goal', index)"
                    goal-label="Objectifs transversaux"
                    item-model="cross_goal_item"
                />
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <h4>Objectifs de branche</h4>
        </b-row>
        <b-row>
            <b-col>
                <b-btn @click="branch_goal.unshift({id: -1})">
                    Ajouter
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <goal
                    class="mt-2"
                    v-for="(goal, index) in branch_goal"
                    :key="'bg-' + goal.id"
                    :goal-object="goal"
                    ref="branchgoals"
                    @remove="removeGoal('branch_goal', index)"
                    goal-label="Objectifs de branche"
                    item-model="branch_goal_item"
                    use-branch
                />
            </b-col>
        </b-row>
        <b-row />
    </b-container>
</template>

<script>
import axios from "axios";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {getPeopleByName} from "../common/search.js";
import Goal from "./goal.vue";
import ClassCouncil from "./class_council.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        id: {
            type: String,
            default: null,
        }
    },
    data: function () {
        return {
            responsibleOptions: [],
            studentOptions: [],
            disorderOptions: [],
            disorderResponseOptions: [],
            scheduleOptions: [],
            disorderResponseAll: [],
            /** Available options for schedule adjustment select.  */
            scheduleAdjustmentOptions: [],
            searchId: -1,
            sending: false,
            form: {
                id: null,
                student: null,
                referent: [],
                sponsor: [],
                disorder: [],
                disorder_response: [],
                schedule_adjustment: [],
            },
            cross_goal: [],
            branch_goal: [],
            /** List of class council related to this PIA. */
            classCouncil: [],
            errors: {},
            /** List of input error states. */
            inputStates: {
                "student": null,
                "referent": null,
                "sponsor": null,
                "disorder": null,
                "disorder_response": null,
                "schedule_adjustment": null
            },
        };
    },
    watch: {
        id: function (newVal) {
            if (newVal) {
                // Reset data.
                Object.assign(this.$data, this.$options.data());
                this.initApp();
            } else {
                this.reset();
            }
        },
        /**
         * Handle returned errors states.
         * 
         * @param {Object} newErrors Errors states with error message.
         */
        errors: function (newErrors) {
            Object.keys(this.inputStates).forEach(key => {
                if (key in newErrors) {
                    this.inputStates[key] = newErrors[key].length == 0;
                } else {
                    this.inputStates[key] = null;
                }
            });
        },
    },
    methods: {
        /** 
         * Assign text error if any.
         * 
         * @param {String} err Field name.
         */
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        /**
         * Remove a goal from the list.
         * 
         * @param {String} goalType The type of the goal (cross_goal or branch_goal).
         * @param {Number} goalIndex The index of the goal in the associated goal list.
         */
        removeGoal: function (goalType, goalIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer l'objectif ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app[goalType][goalIndex].id >= 0) {
                        axios.delete(`/pia/api/${goalType}/` + app[goalType][goalIndex].id + "/", token)
                            .then(() => app[goalType].splice(goalIndex, 1))
                            .catch(err => alert(err));
                    } else {
                        app[goalType].splice(goalIndex, 1);
                    }
                }
            });
        },
        /**
         * Remove a class council.
         * 
         * @param: {String} councilIndex The index of the class council.
         */
        removeClassCouncil: function (councilIndex) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer ce conseil de classe ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    if (app.classCouncil[councilIndex].id >= 0) {
                        axios.delete("/pia/api/class_council/" + app.classCouncil[councilIndex].id + "/", token)
                            .then(() => app.classCouncil.splice(councilIndex, 1))
                            .catch(err => alert(err));
                    } else {
                        app.classCouncil.splice(councilIndex, 1);
                    }
                }
            });
        },
        getPeople: function (searchQuery, person) {
            person = person.split("-")[0];
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.$store.state.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, person)
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this[person + "Options"] = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
        updateDisorderResponse: function (selected) {
            this.disorderResponseOptions = this.disorderResponseAll.filter(d => {
                return this.form.disorder.map(x => x.id).includes(d.disorder);
            });

            if (selected.length == 0) return;

            // Append corresponding disorder response.
            const lastDisorder = selected[selected.length -1];
            const newDisorderResponse = this.disorderResponseAll.filter(d => {
                const matchDisorder = d.disorder == lastDisorder.id;
                const alreadySelected = this.form.disorder_response.map(dr => dr.id).includes(d.id);
                return matchDisorder && !alreadySelected;
            });
            this.form.disorder_response = this.form.disorder_response.concat(newDisorderResponse);
        },
        showSuccess: function (recordId) {
            let app = this;
            app.sending = false;
            if (app.id) {
                app.$root.$bvToast.toast("Les données ont bien été sauvegardée", {
                    variant: "success",
                    noCloseButton: true,
                });
            } else {
                app.$router.push("/edit/" + recordId + "/",() => {
                    app.$root.$bvToast.toast("Les données ont bien été sauvegardée", {
                        variant: "success",
                        noCloseButton: true,
                    });
                });
            }
        },
        submit: function (evt) {
            evt.preventDefault();

            let app = this;
            this.sending = true;
            const data = Object.assign({}, this.form);
            data.student_id = data.student.matricule;
            data.disorder = data.disorder.map(d => d.id);
            data.disorder_response = data.disorder_response.map(dr => dr.id);
            data.referent = data.referent.map(r => r.matricule);
            data.sponsor = data.sponsor.map(s => s.matricule);
            data.schedule_adjustment = data.schedule_adjustment.map(sa => sa.id);

            let send = this.id ? axios.put : axios.post;
            let url = "/pia/api/pia/";
            if (this.id) url += this.id + "/";
            send(url, data, token)
                .then(resp => {
                    const recordId = resp.data.id;
                    // No goals, no promises.
                    if (this.cross_goal.length == 0 && this.branch_goal.length == 0 && this.classCouncil.length == 0) {
                        this.showSuccess(recordId);
                        return;
                    }

                    const crossGoalPromises = this.cross_goal.length != 0 ? this.$refs.crossgoals.map(g => g.submit(recordId)) : [];
                    const branchGoalPromises = this.branch_goal.length != 0 ? this.$refs.branchgoals.map(g => g.submit(recordId)) : [];
                    const classCouncilPromises = this.classCouncil.length != 0 ? this.$refs.councils.map(c => c.submit(recordId)) : [];
                    Promise.all(crossGoalPromises.concat(branchGoalPromises, classCouncilPromises))
                        .then(resps => {
                            // Update goals component with response.
                            const subPromises = [];
                            const councilResponses = resps.filter(r => r.config.url.includes("/pia/api/class_council/"));

                            if (councilResponses.length == 0) {
                                this.showSuccess(recordId);
                                return;
                            }
                            // Get branch statement promises.
                            councilResponses.forEach((r, i) => {
                                if (!("id" in app.$refs.councils[i])) {
                                    app.classCouncil.splice(i, 1, r.data);
                                    subPromises.concat(app.$refs.councils[i].submitBranchStatement(app.classCouncil[i].id));
                                }
                            });

                            Promise.all(subPromises)
                                .then(() => {
                                    this.showSuccess(recordId);
                                })
                                .catch(err => {
                                    app.sending = false;
                                    alert(err);
                                });
                        })
                        .catch(err => {
                            app.sending = false;
                            alert(err);
                        });

                }).catch(function (error) {
                    app.sending = false;
                    alert(error);
                    if ("response" in error) app.errors = error.response.data;
                });
        },
        /**
        * Assign record data from a request.
        * 
        * @param {Number} newId The id of the record.
        */
        loadPIA: function (newId) {
            axios.get("/pia/api/pia/" + newId + "/")
                .then(resp => {
                    this.form.student = resp.data.student;
                    resp.data.referent.map(r => {
                        axios.get("/annuaire/api/responsible/" + r + "/")
                            .then(resp => this.form.referent.push(resp.data));
                    });
                    resp.data.sponsor.map(s => {
                        axios.get("/annuaire/api/responsible/" + s + "/")
                            .then(resp => this.form.sponsor.push(resp.data));
                    });
                    this.form.disorder = this.disorderOptions.filter(d => resp.data.disorder.includes(d.id));
                    this.form.disorder_response = this.disorderResponseAll.filter(dr => resp.data.disorder_response.includes(dr.id));
                    this.form.schedule_adjustment = this.scheduleAdjustmentOptions.filter(sa => resp.data.schedule_adjustment.includes(sa.id));
                });
        },
        /**
         * Initialize the component.
         * 
         * It will request options for the select inputs and if editing, call
         * the retrieval of the current data record (goals and council included).
         */
        initApp: function () {
            const promises = [
                axios.get("/pia/api/disorder/"),
                axios.get("/pia/api/disorder_response/"),
                axios.get("/pia/api/schedule_adjustment/")
            ];
            Promise.all(promises)
                .then(resps => {
                    this.disorderOptions = resps[0].data.results;
                    this.disorderResponseAll = resps[1].data.results;
                    this.scheduleAdjustmentOptions = resps[2].data.results;
                    if (this.id) this.loadPIA(this.id);
                });

            // Load goals and class council.
            if (this.id) {
                axios.get("/pia/api/cross_goal/?pia_model=" + this.id)
                    .then(resp => {
                        this.cross_goal = resp.data.results;
                    });
                axios.get("/pia/api/branch_goal/?pia_model=" + this.id)
                    .then(resp => {
                        this.branch_goal = resp.data.results;
                    });
                axios.get("/pia/api/class_council/?pia_model=" + this.id)
                    .then(resp => {
                        this.classCouncil = resp.data.results;
                    });
            }
        }
    },
    mounted: function () {
        this.initApp();
    },
    components: {
        Multiselect,
        Goal,
        ClassCouncil,
    }
};
</script>

<style>
.first-line {
    background-color: rgba(236, 236, 236, 0.8);
}
</style>
