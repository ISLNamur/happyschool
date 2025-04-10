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
    <BOverlay :show="loading">
        <BRow>
            <BCol>
                <h4 class="mt-4">
                    Aménagements d'horaire
                </h4>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup>
                    <BFormSelect
                        :options="scheduleAdjustments"
                        value-field="id"
                        v-model="currentSchedAdjId"
                        @update:model-value="updateCurrentSchedAdj"
                    />
                </BFormGroup>
            </BCol>
            <BCol>
                <BButtonGroup>
                    <BButton
                        variant="outline-secondary"
                        @click="copy"
                        :disabled="scheduleAdjustments.length === 0"
                    >
                        <IBiFiles />
                        Copier
                    </BButton>
                    <BButton
                        variant="success"
                        @click="add"
                    >
                        <IBiPlus />
                        Ajouter
                    </BButton>
                    <BButton
                        variant="danger"
                        @click="remove"
                        :disabled="scheduleAdjustments.length === 0"
                    >
                        <IBiTrash />
                        Supprimer
                    </BButton>
                </BButtonGroup>
            </BCol>
        </BRow>
        <BRow v-if="currentSchedAdj">
            <BCol>
                <BCard>
                    <BRow class="mb-1">
                        <BCol>
                            <strong>
                                <BForm class="d-flex flex-row align-items-center flex-wrap">
                                    <label class="col-form-label me-2">Du</label>
                                    <div class="col-lg-3 me-2 my-2">
                                        <BFormInput
                                            type="date"
                                            v-model="currentSchedAdj.date_start"
                                            class="mr-sm-2 ml-2"
                                        />
                                    </div>
                                    <label class="col-form-label me-2">au</label>
                                    <div class="col-lg-3 me-2 my-2">
                                        <BFormInput
                                            type="date"
                                            v-model="currentSchedAdj.date_end"
                                            class="ml-2"
                                        />
                                    </div> 
                                </BForm>
                            
                            </strong>
                        </BCol>
                    </BRow>
                    <BRow>
                        <BCol>
                            <multiselect
                                :options="store.scheduleAdjustments"
                                placeholder="Sélectionner le ou les différents adaptations"
                                select-label=""
                                selected-label="Sélectionné"
                                deselect-label="Cliquer dessus pour enlever"
                                v-model="currentSchedAdj.schedule_adjustment"
                                track-by="id"
                                label="schedule_adjustment"
                                :show-no-options="false"
                                multiple
                            >
                                <template #noResult>
                                    Aucun aménagements trouvé.
                                </template>
                                <template #noOptions />
                            </multiselect>
                        </BCol>
                    </BRow>
                </BCard>
            </BCol>
        </BRow>
    </BOverlay>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };


import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

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
            scheduleAdjustments: [],
            currentSchedAdjId: null,
            currentSchedAdj: { schedule_adjustments: [], id: -1 },
            store: piaStore(),
        };
    },
    methods: {
        add: function () {
            const newId = Math.min(Math.min(...this.scheduleAdjustments.map(sA => sA.id)), 0) - 1;
            this.scheduleAdjustments.push(
                { schedule_adjustments: [], id: newId, date_start: null, date_end: null, text: "Nouvel aménagement" }
            );
            this.currentSchedAdj = this.scheduleAdjustments[this.scheduleAdjustments.length - 1];
            this.currentSchedAdjId = newId;
        },
        copy: function () {
            let copy = Object.assign({}, this.currentSchedAdj);
            copy.id = Math.min(Math.min(...this.scheduleAdjustments.map(sA => sA.id)), 0) - 1;
            copy.text = `Copie de ${copy.text}`;
            this.scheduleAdjustments.push(copy);
            this.currentSchedAdj = this.scheduleAdjustments[this.scheduleAdjustments.length - 1];
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
                    const sAIndex = this.scheduleAdjustments.findIndex(
                        sA => sA.id === this.currentSchedAdj.id && sA.date_start === this.currentSchedAdj.date_start
                    );
                    const removedObj = this.scheduleAdjustments.splice(sAIndex, 1)[0];
                    this.currentSchedAdj = this.scheduleAdjustments[this.scheduleAdjustments.length - 1];
                    axios.delete(`/pia/api/schedule_adjustment_plan/${removedObj.id}/`, token);
                }
            });
        },
        save: function (piaId) {
            return new Promise((resolve, reject) => {
                this.loading = true;
                Promise.all(
                    this.scheduleAdjustments.map(sA => {
                        const isNew = sA.id < 0;
                        const send = isNew ? axios.post : axios.put;
                        const url = `/pia/api/schedule_adjustment_plan/${isNew ? "" : sA.id + "/"}`;

                        // Copy schedule adjustment for sending.
                        let data = Object.assign({}, sA);
                        data.pia_model = piaId;
                        data.schedule_adjustment = data.schedule_adjustment.map(adjObj => adjObj.id);
                        return send(url, data, token);
                    })
                ).then((resps) => {
                    this.expandScheduleAdjustment(resps.map(r => r.data));
                    this.loading = false;
                    resolve();
                }).catch((err) => {
                    console.log(err);
                    this.loading = false;
                    reject(err);
                });
            });
        },
        updateCurrentSchedAdj: function (selected) {
            this.currentSchedAdj = this.scheduleAdjustments.find(sA => sA.id === selected);
        },
        expandScheduleAdjustment: function (scheduleAdjustments) {
            this.scheduleAdjustments = scheduleAdjustments.sort((a, b) => a.date_start < b.date_start).map(sA => {
                sA.text = `Du ${sA.date_start} au ${sA.date_end}`;
                sA.schedule_adjustment = sA.schedule_adjustment
                    .map(id => this.store.scheduleAdjustments.find(s => s.id === id));
                return sA;
            });

            if (this.scheduleAdjustments.length > 0) {
                this.currentSchedAdj = this.scheduleAdjustments[0];
                this.currentSchedAdjId = this.scheduleAdjustments[0].id;
            }
        }
    },
    components: {
        Multiselect
    },
    mounted: function () {
        this.store.loadOptions()
            .then(() => {
                if (this.pia) {
                    axios.get(`/pia/api/schedule_adjustment_plan/?pia_model=${this.pia}`)
                        .then((resp) => {
                            this.expandScheduleAdjustment(resp.data.results);
                        });
                }
            });
    }
};
</script>
