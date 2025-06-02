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
        <BTabs v-model:index="tabIndex">
            <BTab title="Reporter">
                <p><strong>Reporter les sanctions sélectionnées</strong></p>
                <p>Les sanctions sélectionnées seront reportées d'une semaine</p>
            </BTab>
            <BTab
                title="Changer de sanction"
                disabled
            >
                <strong>Changer de type de sanctions</strong>
                <BFormGroup label="Choississez vers quelle sanction changer">
                    En cours de construction…
                </BFormGroup>
            </BTab>
        </BTabs>
        <div>
            <BListGroup>
                Nombre de sanctions sélectionnées : {{ selected.length }}
                <BFormCheckboxGroup v-model="selected">
                    <BListGroupItem
                        class="d-flex justify-content-between align-items-center"
                        v-for="sanction in sanctions"
                        :key="sanction.id"
                    >
                        <span>
                            <em>
                                {{ sanction.date_sanction }}
                                →
                                {{ nextWeek(sanction.date_sanction) }}
                            </em>
                            <strong>{{ displayStudent(sanction.student) }}</strong>
                        </span>
                        <span>
                            {{ sanction.sanction_decision.sanction_decision }}
                            <BFormCheckbox
                                class=""
                                :value="sanction.id"
                            />
                        </span>
                    </BListGroupItem>
                </BFormCheckboxGroup>
                <BButton
                    variant="success"
                    @click="reportSanctions"
                >
                    {{ tabIndex ? "Changer" : "Reporter" }}
                </BButton>
            </BListGroup>
        </div>
    </div>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
import axios from "axios";

import { displayStudent } from "@s:core/js/common/utilities.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        sanctions: {
            type: Array,
            default: () => [],
        }
    },
    data: function () {
        return {
            selected: [],
            tabIndex: 0
        };
    },
    methods: {
        displayStudent,
        nextWeek: function (date) {
            return Moment(date).add(7, "days").format("YYYY-MM-DD");
        },
        reportSanctions: function () {
            this.$emit("loading", 0);
            const chunk = 10;
            let i, j;
            const chunkOfSanctions = [];
            for (i = 0, j = this.selected.length; i < j; i += chunk) {
                chunkOfSanctions.push(this.selected.slice(i, i + chunk));
            }
            chunkOfSanctions.forEach((c, i) => {
                setTimeout(() => {
                    const isLastChunk = i === chunkOfSanctions.length - 1;
                    const promiseSanctions = c.map(sId => {
                        const sanction = this.sanctions.find(s => s.id == sId);
                        const newDate = this.nextWeek(sanction.date_sanction);
                        const comment = sanction.explication_commentaire
                            + `<p>Report de la sanction du ${sanction.date_sanction} au ${newDate}</p>`;
                        return axios.patch(
                            `/dossier_eleve/api/ask_sanctions/${sanction.id}/`,
                            { date_sanction: newDate, explication_commentaire: comment },
                            token
                        );
                    });
                    Promise.all(promiseSanctions)
                        .then(() => {
                            if (!isLastChunk) {
                                this.$emit("loading", (i + 1) / chunkOfSanctions.length);
                                return;
                            }

                            this.loading = false;
                            this.$emit("loading", 1);
                        })
                        .catch(err => {
                            console.log(err);
                            this.$emit("loading", 1);
                        });
                }, 500 * i);
            });


        }
    },
    mounted: function () {
        this.selected = this.sanctions.map(s => s.id);
    }
};
</script>
