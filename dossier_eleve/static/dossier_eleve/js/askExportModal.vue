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
                    <BButton
                        variant="primary"
                        @click="getPdf"
                        :disabled="!date_from && !date_to"
                    >
                        Créer PDF
                    </BButton>
                    <BButton
                        v-if="store.hasProEco"
                        variant="primary"
                        class="ml-1"
                        @click="exportProEco"
                        :disabled="!date_from && !date_to"
                    >
                        Exporter vers ProEco
                    </BButton>
                </div>
            </template>
            <BTabs v-model="tabIndex">
                <BTab
                    v-if="store.settings.enable_disciplinary_council"
                    title="Conseil de discipline"
                    active
                >
                    <BRow class="mt-4">
                        <BCol>
                            <BFormRow>
                                <BFormGroup label="À partir du">
                                    <input
                                        type="date"
                                        v-model="date_from"
                                        :max="date_to"
                                    >
                                </BFormGroup>
                            </BFormRow>
                        </BCol>
                        <BCol>
                            <BFormRow>
                                <BFormGroup label="Jusqu'au">
                                    <input
                                        type="date"
                                        v-model="date_to"
                                        :min="date_from"
                                    >
                                </BFormGroup>
                            </BFormRow>
                        </BCol>
                    </BRow>
                </BTab>
                <BTab title="Retenues">
                    <BFormRow class="mt-4">
                        <BCol>
                            <BFormRow>
                                <BFormGroup label="À partir du">
                                    <input
                                        type="date"
                                        v-model="date_from"
                                        :max="date_to"
                                    >
                                </BFormGroup>
                            </BFormRow>
                        </BCol>
                        <BCol>
                            <BFormRow>
                                <BFormGroup label="Jusqu'au">
                                    <input
                                        type="date"
                                        v-model="date_to"
                                        :min="date_from"
                                    >
                                </BFormGroup>
                            </BFormRow>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup>
                                <BFormCheckbox
                                    v-model="sortByClasse"
                                >
                                    Trier par classe
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup>
                                <BFormCheckbox
                                    v-model="sortBySanction"
                                >
                                    Trier par sanction
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup
                                label="Types de sanctions"
                            >
                                <BFormSelect
                                    v-model="selectedSanctions"
                                    :options="optionsSanction"
                                    multiple
                                    :select-size="5"
                                />
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup>
                                <BFormCheckbox
                                    v-model="sanction_not_done"
                                >
                                    Sanctions non faites uniquement
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                    <BFormRow>
                        <BCol>
                            <BFormGroup>
                                <BFormCheckbox
                                    v-model="ownClass"
                                >
                                    Uniquement ses classes
                                </BFormCheckbox>
                            </BFormGroup>
                        </BCol>
                    </BFormRow>
                </BTab>
            </BTabs>
        </b-modal>
    </div>
</template>

<script>
import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import axios from "axios";

import { askSanctionsStore } from "./stores/ask_sanctions.js";

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
            ownClass: false,
            sortByClasse: false,
            sortBySanction: false,
            selectedSanctions: [],
            optionsSanction: [],
            store: askSanctionsStore(),
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
            if (this.tabIndex == 0 && this.store.settings.enable_disciplinary_council) {
                path += `council/?datetime_conseil__gte=${this.date_from} 00:00&datetime_conseil__lte=${this.date_to} 23:59`;
            } else {
                path += `retenues/?${this.ownClass ? "activate_own_classes=true" : ""}`;
                path += "&date_sanction__gte=" + this.date_from;
                path += "&date_sanction__lte=" + this.date_to;
                if (this.sanction_not_done) {
                    path += "&activate_not_done=true";
                }
            }
            let orderingFields = [];
            const isSanctionTab = this.store.settings.enable_disciplinary_council ? this.tabIndex == 1 : true;
            if (this.sortBySanction && isSanctionTab) orderingFields.push("sanction_decision__sanction_decision");
            if (this.sortByClasse && isSanctionTab) orderingFields.push("student__classe__year,student__classe__letter");
            orderingFields.push("student__last_name");
            path += `&ordering=${orderingFields.toString()}`;
            path += "&page_size=500";
            path += `&sanction_decision=${this.selectedSanctions.join()}`;
            window.open(path);
        },
        exportProEco: function () {
            const export_type = this.tabIndex == 0 && this.store.settings.enable_disciplinary_council ? "council" : "retenue";
            let url = `/dossier_eleve/get_proeco_sanction/${export_type}/${this.date_from}/${this.date_to}/${this.selectedSanctions.join()}/`;
            if (export_type === "retenue") {
                url += `${this.ownClass}/`;
            }
            window.open(url);
        }
    },
    mounted: function () {
        this.ownClass = this.store.settings.export_retenues_own_classes_default;
        this.sortByClasse = this.store.settings.export_retenues_by_classe_default;
        this.sortBySanction = this.store.settings.export_retenues_by_sanction_default;
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
