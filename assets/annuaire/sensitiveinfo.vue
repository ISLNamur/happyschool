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
    <b-tab
        title="Infos personnelles"
    >
        <dl
            v-if="type !== 'student'"
            class="row"
        >
            <dt
                class="col-5 text-right"
            >
                Courriel
            </dt>
            <dd
                class="col-7"
            >
                {{ info.email }}
            </dd>
        </dl>
        <dl
            v-else
            class="row"
        >
            <dt class="col-5 text-right">
                Date de naissance
            </dt>
            <dd class="col-7">
                {{ niceDate(info.birth_date) }}
            </dd>
            <dt class="col-5 text-right">
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
                class="col-5 text-right"
            >
                Profession du père
            </dt>
            <dd class="col-7">
                {{ info.father_job }}
            </dd>
            <dt
                v-if="info.mother_job"
                class="col-5 text-right"
            >
                Profession de la mère
            </dt>
            <dd class="col-7">
                {{ info.mother_job }}
            </dd>
        </dl>
    </b-tab>
</template>

<script>
import Moment from "moment";
Moment.locale("fr");

export default {
    props: {
        info: {
            type: Object,
            default: () => {}
        },
        type: {
            type: String,
            default: "student"
        }
    },
    methods: {
        niceDate: function (date) {
            if (!date) return "";

            return Moment(date).calendar();
        },
    }
};
</script>
