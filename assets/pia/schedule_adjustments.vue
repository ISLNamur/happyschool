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
    <b-overlay :show="loading">
        <b-row>
            <b-col>
                <h4 class="mt-4">
                    Aménagements d'horaire
                </h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group>
                    <b-select
                        :options="scheduleAdjustments"
                        value-field="id"
                        v-model="currentSchedAdj"
                    />
                </b-form-group>
            </b-col>
        </b-row>
        <b-row v-if="currentSchedAdj">
            <b-col>
                <b-card>
                    <b-row>
                        <b-col>
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
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>
        </b-row>
    </b-overlay>
</template>

<script>
import axios from "axios";

import { piaStore } from "./stores/index.js";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};


import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

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
            currentSchedAdj: null,
            other: {},
            store: piaStore(),
        };
    },
    components: {
        Multiselect
    },
    mounted: function () {
        // this.currentSchedAdj = {schedule_adjustments: [], id: -1};
        axios.get(`/pia/api/schedule_adjustment_plan/?pia_model=${this.pia}`)
            .then((resp) => {
                this.scheduleAdjustments = resp.data.results.map(sA => {
                    sA.text = `Du ${sA.date_start} au ${sA.date_end}`;
                    return sA;
                }); 

                if (this.scheduleAdjustments.length > 0) {
                    this.currentSchedAdj = this.scheduleAdjustments[0];
                }
            });
    }
};
</script>
