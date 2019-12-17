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
        <b-card>
            <strong>{{ absence.date_absence }}</strong>:
            <a :href="`/annuaire/#/person/student/${absence.student.matricule}/`">
                {{ absence.student.display }}
            </a>
            ({{ display_absence }})
        </b-card>
    </div>
</template>

<script>
import Vue from "vue";

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";
Vue.component("icon", Icon);

export default {
    props: {
        "absence": {
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
        };
    },
    computed: {
        display_absence: function () {
            let display = "";
            if (this.absence.morning) {
                display += "matin";
                if (this.absence.afternoon) display += ", ";
            }
            if (this.absence.afternoon) display += "après-midi";
            return display;
        }
    }
};
</script>
