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
        <b-modal
            size="lg"
            title="Exporter des données dans un fichier"
            ref="askExportModal"
            @hidden="resetModal"
        >
            <template #modal-footer>
                <div class="w-100 text-right">
                    <b-button
                        variant="primary"
                        @click="getPdf"
                        :disabled="!date_from && !date_to"
                    >
                        Créer PDF
                    </b-button>
                    <b-button
                        v-if="$store.state.hasProEco"
                        variant="primary"
                        class="ml-1"
                        @click="exportProEco"
                        :disabled="!date_from && !date_to"
                    >
                        Exporter vers ProEco
                    </b-button>
                </div>
            </template>
            <b-tabs v-model="tabIndex">
                <b-tab
                    v-if="$store.state.settings.enable_disciplinary_council"
                    title="Conseil de discipline"
                    active
                >
                    <b-row class="mt-4">
                        <b-col>
                            <b-form-row>
                                <b-form-group label="À partir du">
                                    <input
                                        type="date"
                                        v-model="date_from"
                                        :max="date_to"
                                    >
                                </b-form-group>
                            </b-form-row>
                        </b-col>
                        <b-col>
                            <b-form-row>
                                <b-form-group label="Jusqu'au">
                                    <input
                                        type="date"
                                        v-model="date_to"
                                        :min="date_from"
                                    >
                                </b-form-group>
                            </b-form-row>
                        </b-col>
                    </b-row>
                </b-tab>
                <b-tab title="Retenues">
                    <b-row class="mt-4">
                        <b-col>
                            <b-form-row>
                                <b-form-group label="À partir du">
                                    <input
                                        type="date"
                                        v-model="date_from"
                                        :max="date_to"
                                    >
                                </b-form-group>
                            </b-form-row>
                        </b-col>
                        <b-col>
                            <b-form-row>
                                <b-form-group label="Jusqu'au">
                                    <input
                                        type="date"
                                        v-model="date_to"
                                        :min="date_from"
                                    >
                                </b-form-group>
                            </b-form-row>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group>
                                <b-checkbox
                                    v-model="sortByClasse"
                                >
                                    Trier par classe
                                </b-checkbox>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group>
                                <b-checkbox
                                    v-model="sortBySanction"
                                >
                                    Trier par sanction
                                </b-checkbox>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group
                                label="Types de sanctions"
                            >
                                <b-form-select
                                    v-model="selectedSanctions"
                                    :options="optionsSanction"
                                    multiple
                                    :select-size="5"
                                />
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group>
                                <b-checkbox
                                    v-model="sanction_not_done"
                                >
                                    Sanctions non faites uniquement
                                </b-checkbox>
                            </b-form-group>
                        </b-col>
                    </b-row>
                </b-tab>
            </b-tabs>
        </b-modal>
    </div>
</template>

<script>
import Moment from "moment";
Moment.locale("fr");

import axios from "axios";

export default {
    props: {
        "entriesCount": {
            type: Number,
            default: 0
        },
    },
    data: function () {
        return {
            tabIndex: 0,
            date_from: null,
            date_to: null,
            sanction_not_done: false,
            sortByClasse: this.$store.state.settings.export_retenues_by_classe_default,
            sortBySanction: this.$store.state.settings.export_retenues_by_sanction_default,
            selectedSanctions: [],
            optionsSanction: [],
        };
    },
    watch: {
        date_from: function (date) {
            if (this.date_to === null) this.date_to = date;
        },
    },
    methods: {
        show: function () {
            this.$refs.askExportModal.show();
        },
        hide: function () {
            this.$refs.askExportModal.hide();
        },
        resetModal: function () {
            this.tabIndex = 0;
            this.date_from = null;
            this.date_to = null;
        },
        getPdf: function (evt) {
            evt.preventDefault();

            let path = "/dossier_eleve/get_pdf_";
            if (this.tabIndex == 0 && this.$store.state.settings.enable_disciplinary_council) {
                path += `council/?datetime_conseil__gte=${this.date_from} 00:00&datetime_conseil__lte=${this.date_to} 23:59`;
            } else {
                path += "retenues/?activate_all_retenues=true";
                path += "&date_sanction__gte=" + this.date_from;
                path += "&date_sanction__lte=" + this.date_to;
                path += `&sanction_decision=${this.selectedSanctions.join()}`;
                if (this.sanction_not_done) {
                    path += "&activate_not_done=true";
                }
            }
            let orderingFields = [];
            const isSanctionTab = this.$store.state.settings.enable_disciplinary_council ? this.tabIndex == 1 : true;
            if (this.sortBySanction && isSanctionTab) orderingFields.push("sanction_decision__sanction_decision");
            if (this.sortByClasse && isSanctionTab) orderingFields.push("student__classe__year,student__classe__letter");
            orderingFields.push("student__last_name");
            path += `&ordering=${orderingFields.toString()}`;
            path += "&page_size=500";
            window.open(path);
        },
        exportProEco: function () {
            const export_type = this.tabIndex == 0 && this.$store.state.settings.enable_disciplinary_council ? "council" : "retenue";
            window.open(
                `/dossier_eleve/get_proeco_sanction/${export_type}/${this.date_from}/${this.date_to}/`
            );
        }
    },
    mounted: function () {
        axios.get("/dossier_eleve/api/sanction_decision/?only_sanction=1")
            .then(resp => {
                this.optionsSanction = resp.data.results.filter(sanct => sanct.can_ask).map(sanct => {
                    return {
                        value: sanct.id,
                        text: sanct.sanction_decision,
                    };
                });
                this.selectedSanctions = this.optionsSanction.map(s => s.value);
            });
        this.show();
    },
};
</script>

<style>
</style>
