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
        <div v-if="medical">
            <dl class="row">
                <dt class="col-5 text-end">
                    Médecin
                </dt>
                <dd class="col-7">
                    {{ medical.doctor }}
                </dd>
                <dt class="col-5 text-end">
                    Téléphone médecin
                </dt>
                <dd class="col-7">
                    {{ medical.doctor_phone }}
                </dd>
                <dt
                    v-if="medical.mutual"
                    class="col-5 text-end"
                >
                    Mutuelle
                </dt>
                <dd
                    v-if="medical.mutual"
                    class="col-7"
                >
                    {{ medical.mutual }}
                </dd>
                <dt
                    v-if="medical.mutual_number"
                    class="col-5 text-end"
                >
                    Numéro mutuelle
                </dt>
                <dd
                    v-if="medical.mutual_number"
                    class="col-7"
                >
                    {{ medical.mutual_number }}
                </dd>
                <dt class="col-5 text-end">
                    Infos complémentaires
                </dt>
                <dd class="col-7">
                    {{ medical.medical_information }}
                </dd>
            </dl>
        </div>
        <BCard
            v-if="other_medical_info.length > 0"
            no-body
        >
            <BListGroup flush>
                <BListGroupItem
                    v-for="cas in other_medical_info"
                    :key="cas.id"
                    :variant="cas.important ? 'danger' : ''"
                    class="mb-2"
                >
                    <em>{{ niceDate(cas.datetime_encodage) }}</em>
                    <div v-html="cas.explication_commentaire" />
                </BListGroupItem>
            </BListGroup>
        </BCard>
    </BOverlay>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

export default {
    props: {
        student: {
            type: Number,
            default: -1
        }
    },
    data: function () {
        return {
            medical: null,
            other_medical_info: [],
            loading: true,
        };
    },
    watch: {
        student: function () {
            this.loadData();
        }
    },
    methods: {
        niceDate: function (date) {
            if (!date) return "";

            return Moment(date).calendar();
        },
        loadData: function () {
            const studentId = this.$route.params.matricule ? this.$route.params.matricule : this.student;
            axios.get(`/annuaire/api/info_medical/${studentId}/`)
                .then(response => {
                    this.medical = response.data;
                    this.loading = false;
                })
                .catch(err => {
                    console.log(err);
                    this.loading = false;
                });
            axios.get(`/dossier_eleve/api/cas_eleve/?ordering=-datetime_encodage&student__matricule=${studentId}&no_sanctions=true`)
                .then((resp) => {
                    this.other_medical_info = resp.data.results.filter(cas => cas.info.info.toLowerCase().includes("médical"));
                });
        }
    },
    mounted: function () {
        this.loadData();
    }
};
</script>
