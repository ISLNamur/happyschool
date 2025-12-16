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
        <div v-if="info">
            <dl
                v-if="$route.params.type !== 'student'"
                class="row"
            >
                <dt
                    class="col-5 text-end"
                >
                    Courriel
                </dt>
                <dd
                    class="col-7"
                >
                    {{ info.email }}
                    <IBiCopy
                        class="ms-2"
                        @click="copyToClipboard(info.email)"
                    />
                </dd>
            </dl>
            <dl
                v-else
                class="row"
            >
                <dt class="col-5 text-end">
                    Date de naissance
                </dt>
                <dd class="col-7">
                    {{ niceDate(info.birth_date) }}
                </dd>
                <dt class="col-5 text-end">
                    Adresse
                </dt>
                <dd
                    v-if="info.street"
                    class="col-7"
                >
                    {{ info.street }}
                </dd>
                <dd
                    v-if="info.postal_code && info.locality"
                    class="col-7 offset-5"
                >
                    {{ info.postal_code }} – {{ info.locality }}
                </dd>
                <dt
                    v-if="info.father_job"
                    class="col-5 text-end"
                >
                    Profession du père
                </dt>
                <dd class="col-7">
                    {{ info.father_job }}
                </dd>
                <dt
                    v-if="info.mother_job"
                    class="col-5 text-end"
                >
                    Profession de la mère
                </dt>
                <dd class="col-7">
                    {{ info.mother_job }}
                </dd>
            </dl>
        </div>
    </BOverlay>
</template>

<script>
import axios from "axios";
import { DateTime } from "luxon";

import { useToastController } from "bootstrap-vue-next";

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            info: null,
            loading: true,
        };
    },
    methods: {
        copyToClipboard: function (text) {
            navigator.clipboard.writeText(text);
            this.show({
                body: "Copié !",
                variant: "success",
                noCloseButton: true,
            });
        },
        niceDate: function (date) {
            if (!date) return "";

            return DateTime.fromISO(date).toLocaleString();
        },
    },
    mounted: function () {
        if (this.$route.params.type === "student") {
            axios.get(`/annuaire/api/student_sensitive/${this.$route.params.matricule}/`)
                .then((response) => {
                    this.info = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    console.log(err);
                    this.loading = false;
                });
        } else if (this.$route.params.type === "responsible") {
            axios.get(`/annuaire/api/responsible_sensitive/${this.$route.params.matricule}/`)
                .then((response) => {
                    this.info = { email: response.data.email };
                    this.loading = false;
                })
                .catch((err) => {
                    console.log(err);
                    this.loading = false;
                });
        }
    },
};
</script>
