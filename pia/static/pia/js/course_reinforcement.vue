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
        <b-card>
            <b-row>
                <b-col>
                    <b-form-group>
                        <b-form-radio-group
                            v-model="reinforcement"
                            :options="[{ text: 'Oui', value: true }, { text: 'Non', value: false }]"
                            name="has-reinforcement"
                            button-variant="outline-primary"
                            buttons
                        />
                        <template #label>
                            <strong>Renforcement/Méthodo cours CE1D</strong>
                        </template>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row v-if="reinforcement">
                <b-col>
                    <b-form-group>
                        <b-select
                            :options="courseReinforcements"
                            value-field="id"
                            v-model="currentCourseReinforId"
                            @change="updateCourseReinforcement"
                        />
                    </b-form-group>
                </b-col>
                <b-col>
                    <b-btn
                        variant="outline-secondary"
                        @click="copy"
                        :disabled="courseReinforcements.length === 0"
                    >
                        <b-icon icon="files" />
                        Copier
                    </b-btn>
                    <b-btn
                        variant="success"
                        @click="add"
                    >
                        <b-icon icon="plus" />
                        Ajouter
                    </b-btn>
                    <b-btn
                        variant="danger"
                        @click="remove"
                        :disabled="courseReinforcements.length === 0"
                    >
                        <b-icon icon="trash" />
                        Supprimer
                    </b-btn>
                </b-col>
            </b-row>
            <b-row v-if="currentCourseReinfor">
                <b-col>
                    <strong>
                        <b-form inline>
                            Du<b-form-input
                                type="date"
                                v-model="currentCourseReinfor.date_start"
                                class="mr-sm-2 ml-2"
                            />
                            au<b-form-input
                                type="date"
                                v-model="currentCourseReinfor.date_end"
                                class="ml-2"
                            />
                        </b-form>
                    </strong>
                </b-col>
            </b-row>
            <b-row
                v-if="currentCourseReinfor"
                class="mt-1"
            >
                <multiselect
                    :internal-search="false"
                    :options="store.branches"
                    placeholder="Choisir une matière"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label="Cliquer dessus pour enlever"
                    v-model="currentCourseReinfor.branches"
                    :show-no-options="false"
                    label="branch"
                    track-by="id"
                    multiple
                >
                    <template #noResult>
                        Aucune branche trouvé.
                    </template>
                    <template #noOptions />
                </multiselect>
            </b-row>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        pia: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
            loading: false,
            reinforcement: false,
            currentCourseReinforId: null,
            currentCourseReinfor: null,
            courseReinforcements: [],
            store: piaStore(),
        };
    },
    methods: {
        add: function () {
            const newId = Math.min(Math.min(...this.courseReinforcements.map(sA => sA.id)), 0) - 1;

            this.courseReinforcements.push({
                id: newId, date_start: null, date_end: null, text: "Nouveau renforcement/méthodo", branches: []
            });

            this.currentCourseReinfor = this.courseReinforcements[this.courseReinforcements.length - 1];
            this.currentCourseReinforId = newId;
        },
        copy: function () {
            let copy = JSON.parse(JSON.stringify(this.currentCourseReinfor));
            copy.id = Math.min(Math.min(...this.courseReinforcements.map(sA => sA.id)), 0) - 1;
            copy.text = `Copie de ${copy.text}`;
            this.courseReinforcements.push(copy);
            this.currentCourseReinfor = copy;
            this.currentCourseReinforId = copy.id;

        },
        remove: function () {
            this.$bvModal.msgBoxConfirm(
                "Êtes-vous sûr de vouloir supprimer l'élément ?",
                {
                    title: "Attention !",
                    okVariant: "danger",
                    okTitle: "Oui",
                    cancelTitle: "Non",
                },
            ).then((confirm) => {
                if (confirm) {
                    const cRIndex = this.courseReinforcements.findIndex(
                        cR => cR.id === this.currentCourseReinfor.id && cR.date_start === this.currentCourseReinfor.date_start
                    );
                    const removedObj = this.courseReinforcements.splice(cRIndex, 1)[0];
                    this.currentCourseReinfor = this.courseReinforcements[this.courseReinforcements.length - 1];
                    axios.delete(`/pia/api/course_reinforcement/${removedObj.id}/`, token);
                }
            });
        },
        save: function (piaId) {
            return new Promise((resolve, reject) => {
                this.loading = true;
                Promise.all(
                    this.courseReinforcements.map(cR => {
                        const isNew = cR.id < 0;
                        const send = isNew ? axios.post : axios.put;
                        const url = `/pia/api/course_reinforcement/${isNew ? "" : cR.id + "/"}`;

                        // Copy activity support for sending.
                        let data = Object.assign({}, cR);
                        data.pia_model = piaId;
                        data.branches = data.branches.map(b => b.id);
                        return send(url, data, token);
                    })
                ).then((resps) => {
                    this.expandCourseReinforcement(resps.map(r => r.data));
                    this.loading = false;
                    resolve();
                }).catch((err) => {
                    console.log(err);
                    this.loading = false;
                    reject(err);
                });
            });
        },
        updateCourseReinforcement: function (selected) {
            this.currentCourseReinfor = this.courseReinforcements.find(cR => cR.id === selected);
        },
        expandCourseReinforcement: function (courseReinforcements) {
            this.courseReinforcements = courseReinforcements.sort((a, b) => a.date_start < b.date_start).map(cR => {
                cR.text = `Du ${cR.date_start} au ${cR.date_end}`;
                cR.branches = cR.branches.map(bId => this.store.branches.find(bObj => bObj.id === bId));
                return cR;
            });

            if (this.courseReinforcements.length > 0) {
                this.currentCourseReinfor = this.courseReinforcements[0];
                this.currentCourseReinforId = this.courseReinforcements[0].id;
                this.reinforcement = true;
            }
        },
    },
    components: {
        Multiselect
    },
    beforeMount: function () {
        this.store.loadOptions()
            .then(() => {
                if (this.pia) {
                    axios.get(`/pia/api/course_reinforcement/?pia_model=${this.pia}`)
                        .then((resp) => {
                            this.expandCourseReinforcement(resp.data.results);
                            this.loading = false;
                        });
                } else {
                    this.loading = false;
                }
            });
    }
};
</script>
