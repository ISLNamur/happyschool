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
            {{ display_absence }}
        </b-card>
    </div>
</template>

<script>
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
            const absence = (this.absence.is_absent ? "Absent" : "Présent");
            const period = this.$store.state.periods.find(p => p.id == this.absence.period).name;
            return absence + " (" + period + ")";
        }
    }
};
</script>
