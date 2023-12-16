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
        <div v-if="medical">
            <dl class="row">
                <dt class="col-5 text-right">
                    Médecin
                </dt>
                <dd class="col-7">
                    {{ medical.doctor }}
                </dd>
                <dt class="col-5 text-right">
                    Téléphone médecin
                </dt>
                <dd class="col-7">
                    {{ medical.doctor_phone }}
                </dd>
                <dt class="col-5 text-right">
                    Mutuelle
                </dt>
                <dd class="col-7">
                    {{ medical.mutual }}
                </dd>
                <dt class="col-5 text-right">
                    Numéro mutuelle
                </dt>
                <dd class="col-7">
                    {{ medical.mutual_number }}
                </dd>
                <dt class="col-5 text-right">
                    Infos complémentaires
                </dt>
                <dd class="col-7">
                    {{ medical.medical_information }}
                </dd>
            </dl>
        </div>
        <b-card v-if="other_medical_info.length > 0">
            <b-row
                v-for="cas in other_medical_info"
                :key="cas.id"
                class="mb-2"
            >
                <b-col
                    cols="2"
                >
                    {{ niceDate(cas.datetime_encodage) }}
                </b-col>
                <b-col>
                    <div v-html="cas.explication_commentaire" />
                </b-col>
            </b-row>
        </b-card>
    </b-overlay>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

export default {
    data: function () {
        return {
            medical: null,
            other_medical_info: [],
            loading: true,
        };
    },
    methods: {
        niceDate: function (date) {
            if (!date) return "";

            return Moment(date).calendar();
        },
    },
    mounted: function () {
        axios.get(`/annuaire/api/info_medical/${this.$route.params.matricule}/`)
            .then(response => {
                this.medical = response.data;
                this.loading = false;
            })
            .catch(err => {
                console.log(err);
                this.loading = false;
            });
        axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&student__matricule=${this.$route.params.matricule}&no_sanctions=true`)
            .then((resp) => {
                this.other_medical_info = resp.data.results.filter(cas => cas.info.info.toLowerCase().includes("médical"));
            });
    }
};
</script>
