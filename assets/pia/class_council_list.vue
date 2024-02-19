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
        <b-row>
            <b-col>
                <h4 v-if="advanced">
                    Conseil de classe
                </h4>
                <h4 v-else>
                    Auto-évaluation
                </h4>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-btn
                    @click="councils.unshift({id: -1})"
                    variant="outline-secondary"
                >
                    <b-icon icon="plus" />
                    Ajouter
                </b-btn>
                <b-btn v-b-toggle.previous-councils>
                    Voir les anciens
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <class-council
                    v-for="(council, index) in nextCouncils"
                    :key="council.id"
                    :class_council="council"
                    :advanced="advanced"
                    ref="nextcouncils"
                    class="mt-2"
                    @remove="removeClassCouncil(index, 'nextCouncils')"
                    @save="save"
                />
            </b-col>
        </b-row>
        <b-collapse id="previous-councils">
            <b-row class="mt-2">
                <b-col>
                    <h5 v-if="advanced">
                        Anciens conseils de classe
                    </h5>
                    <h5 v-else>
                        Anciennes auto-évaluations
                    </h5>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <class-council
                        v-for="(council, index) in previousCouncils"
                        :key="council.id"
                        :class_council="council"
                        :advanced="advanced"
                        ref="precouncils"
                        class="mt-2"
                        @remove="removeClassCouncil(index, 'previousCouncils')"
                        @save="save"
                    />
                </b-col>
            </b-row>
        </b-collapse>
    </div>
</template>

<script>
import axios from "axios";

import ClassCouncil from "./class_council.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        pia: {
            type: Number,
            default: -1
        },
        advanced: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            councils: [],
        };
    },
    computed: {
        nextCouncils: function () {
            return this.councils.filter(council => council.date_council >= new Date().toISOString() || !council.date_council);
        },
        previousCouncils: function () {
            return this.councils.filter(council => council.date_council < new Date().toISOString());
        },
    },
    methods: {
        /**
         * Remove a class council.
         * 
         * @param: {String} index The index of the list.
         * @param: {String} list The list where the class council is in.
         */
        removeClassCouncil: function (index, list) {
            let app = this;
            this.$bvModal.msgBoxConfirm("Êtes-vous sûr de vouloir supprimer ce conseil de classe ?", {
                okTitle: "Oui",
                cancelTitle: "Non",
                centered: true,
            }).then(resp => {
                if (resp) {
                    const councilIndex = list === "nextCouncils" ? index : index + this.nextCouncils.length;
                    if (app.councils[councilIndex].id >= 0) {
                        axios.delete(`/pia/api/class_council/${app.councils[councilIndex].id}/`, token)
                            .then(() => app.councils.splice(councilIndex, 1))
                            .catch(err => alert(err));
                    } else {
                        app.councils.splice(councilIndex, 1);
                    }
                }
            });
        },
        save: function (piaId) {
            if (!piaId && !this.pia) {
                this.$emit("save");
                return;
            } else if (!piaId) {
                piaId = this.pia;
            }
            let app = this;
            return new Promise((resolve, reject )=> {
                const nextCouncilsComp = "nextcouncils" in app.$refs ? app.$refs.nextcouncils : [];
                const preCouncilComp = "precouncils" in app.$refs ? app.$refs.precouncils : [];
                Promise.all(
                    nextCouncilsComp.map(c => c.submit(piaId)).concat(
                        preCouncilComp.map(c => c.submit(piaId))
                    )
                ).then((resps) => {
                    app.councils = resps.map(r => r.data);
                    const nextCouncilProm = nextCouncilsComp.map((c, i) => c.submitCouncilStatement(app.nextCouncils[i].id));
                    const previousCouncilProm = preCouncilComp.map((c, i) => c.submitCouncilStatement(app.previousCouncils[i].id));
                    Promise.all(nextCouncilProm.concat(previousCouncilProm))
                        .then(() => {
                            resolve();
                        });
                }).catch((err) => {
                    console.log(err);
                    reject();
                });
            });
        }
    },
    components: {
        ClassCouncil
    },
    mounted: function () {
        axios.get(`/pia/api/class_council/?ordering=-date_council&pia_model=${this.pia}`)
            .then((resp) => {
                this.councils = resp.data.results;
                this.$emit("count", this.councils.length);
            });
    }
};
</script>
