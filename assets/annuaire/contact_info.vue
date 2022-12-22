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
        <div v-if="contact">
            <dl class="row">
                <dt class="col-5 text-right">
                    Téléphone de l'élève
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.student_phone.replaceAll('.', '')}`">
                        {{ contact.student_phone }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    GSM de l'élève
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.student_mobile.replaceAll('.', '')}`">
                        {{ contact.student_mobile }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    Email de l'élève
                </dt>
                <dd class="col-7">
                    <a :href="'mailto:' + contact.student_email">{{ contact.student_email }}</a>
                </dd>
                <dt class="col-5 text-right">
                    Nom du responsable
                </dt>
                <dd class="col-7">
                    {{ contact.resp_last_name }} {{ contact.resp_first_name }}
                </dd>
                <dt class="col-5 text-right">
                    Téléphone responsable
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.resp_phone.replaceAll('.', '')}`">
                        {{ contact.resp_phone }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    GSM responsable
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.resp_mobile.replaceAll('.', '')}`">
                        {{ contact.resp_mobile }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    Email responsable
                </dt>
                <dd class="col-7">
                    <a :href="'mailto:' + contact.resp_email">{{ contact.resp_email }}</a>
                </dd>
                <dt class="col-5 text-right">
                    Nom de la mère
                </dt>
                <dd class="col-7">
                    {{ contact.mother_last_name }} {{ contact.mother_first_name }}
                </dd>
                <dt class="col-5 text-right">
                    Téléphone de la mère
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.mother_phone.replaceAll('.', '')}`">
                        {{ contact.mother_phone }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    GSM de la mère
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.mother_mobile.replaceAll('.', '')}`">
                        {{ contact.mother_mobile }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    Email de la mère
                </dt>
                <dd class="col-7">
                    <a :href="'mailto:' + contact.mother_email">{{ contact.mother_email }}</a>
                </dd>
                <dt class="col-5 text-right">
                    Nom du père
                </dt>
                <dd class="col-7">
                    {{ contact.father_last_name }} {{ contact.father_first_name }}
                </dd>
                <dt class="col-5 text-right">
                    Téléphone du père
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.father_phone.replaceAll('.', '')}`">
                        {{ contact.father_phone }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    GSM du père
                </dt>
                <dd class="col-7">
                    <a :href="`tel:${contact.father_mobile.replaceAll('.', '')}`">
                        {{ contact.father_mobile }}
                    </a>
                </dd>
                <dt class="col-5 text-right">
                    Email du père
                </dt>
                <dd class="col-7">
                    <a :href="'mailto:' + contact.father_email">{{ contact.father_email }}</a>
                </dd>
            </dl>
        </div>
    </b-overlay>
</template>

<script>
import axios from "axios";

export default {
    data: function () {
        return {
            contact: null,
            loading: true,
        };
    },
    mounted: function () {
        axios.get(`/annuaire/api/info_contact/${this.$route.params.matricule}/`)
            .then(response => {
                this.contact = response.data;
                this.loading = false;
            })
            .catch(err => {
                console.log(err);
                this.loading = false;
            });
    }
};
</script>
