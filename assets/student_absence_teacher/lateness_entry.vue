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
            <strong>{{ lateness.date }}</strong>:
            <a :href='`/annuaire/#/person/student/${lateness.student.matricule}/`'>
                {{ lateness.student.display }}
            </a>
             ({{ lateness.lesson.lesson }} : {{ lateness.period.name }})
             <p>{{ lateness.comment }}</p>
        </b-card>
    </div>
</template>

<script>
import Vue from 'vue';

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
Vue.component('icon', Icon);

export default {
    props: ["lateness"],
    data: function () {
        return {
        }
    },
    computed: {
    }
}
</script>