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
    <b-modal size="lg" title="Exporter des données dans un fichier"
        ok-title="Créer pdf" :ok-only="true"
        ref="askExportModal"
        @ok="getPdf" @hidden="resetModal"
        >
        <b-tabs v-model="tabIndex">
            <b-tab title="Conseil de discipline" active>
                <b-row class="mt-4">
                    <b-col>
                        <b-form-row>
                            <b-form-group label="À partir du">
                                <input type="date" v-model="date_council_from" :max="date_council_to" />
                            </b-form-group>
                        </b-form-row>
                    </b-col>
                    <b-col>
                        <b-form-row>
                            <b-form-group label="Jusqu'au">
                                <input type="date" v-model="date_council_to" :min="date_council_from" />
                            </b-form-group>
                        </b-form-row>
                    </b-col>
                </b-row>
            </b-tab>
            <b-tab title="Retenues">
                <b-row>
                    <b-col>
                        <b-form-row>
                            <b-form-group label="À partir du">
                                <input type="date" v-model="date_retenues_from" :max="date_retenues_to" />
                            </b-form-group>
                        </b-form-row>
                    </b-col>
                    <b-col>
                        <b-form-row>
                            <b-form-group label="Jusqu'au">
                                <input type="date" v-model="date_retenues_to" :min="date_retenues_from" />
                            </b-form-group>
                        </b-form-row>
                    </b-col>
                </b-row>
            </b-tab>
        </b-tabs>
    </b-modal>
</div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import Moment from 'moment';
Moment.locale('fr');

import axios from 'axios';

export default {
    props: ['entriesCount'],
    data: function () {
        return {
            tabIndex: 0,
            date_council_from: null,
            date_council_to: null,
            date_retenues_from: null,
            date_retenues_to: null,
        }
    },
    watch: {
        date_council_from: function (date) {
            if (this.date_council_to === null) this.date_council_to = date;
        },
        date_retenues_from: function (date) {
            if (this.date_retenues_to === null) this.date_retenues_to = date;
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
            this.date_council_from = null;
            this.date_council_to = null;
            this.date_retenues_from = null;
            this.date_retenues_to = null;
        },
        getPdf: function (evt) {
            evt.preventDefault();

            let path = '/dossier_eleve/get_pdf_'
            if (this.tabIndex == 0) {
                path += 'council/' + Moment(this.date_council_from).format("DD-MM-YYYY") + '/' + Moment(this.date_council_to).format("DD-MM-YYYY") + '/';

            } else if (this.tabIndex == 1) {
                path += 'retenues/' + Moment(this.date_retenues_from).format("DD-MM-YYYY") + '/' + Moment(this.date_retenues_to).format("DD-MM-YYYY") + '/';
            }
            window.open(path);
        },
    },
    mounted: function () {
        this.show();
    },
    components: {Multiselect},
}
</script>

<style>
</style>
