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
        <b-card-group class="mt-2">
            <b-card title="Dernières absences">
                <b-table striped hover :items="lastAbsences" :fields="lastAbsencesFields">
                    <template slot="morning" slot-scope="data">
                        {{ data.value ? 'M' : '' }}
                    </template>
                    <template slot="afternoon" slot-scope="data">
                        {{ data.value ? 'A' : '' }}
                    </template>
                </b-table>
            </b-card>
            <b-card title="Élèves absents (en ½ jours)">
                <b-table striped hover :items="absenceCount" :fields="absenceCountFields"></b-table>
            </b-card>
        </b-card-group>
    </div>
</template>

<script>
import axios from 'axios';

import Moment from 'moment';
Moment.locale('fr');

export default {
    data: function () {
        return {
            lastAbsences: [],
            lastAbsencesFields: {
                'student.display': {
                    label: 'Élèves',
                },
                'date_absence': {
                    label: 'Date',
                    formatter: value => {
                        return Moment(value).calendar();
                    }
                },
                'morning': {
                    label: '',
                },
                'afternoon': {
                    label: ''
                }
            },
            absenceCount: [],
            absenceCountFields: {
                'student': {
                    label: 'Élèves',
                },
                'half_day_diff': {
                    label: 'Non just.',
                },
                'half_day_just': {
                    label: 'Just.'
                },
                'half_day_miss': {
                    label: 'Total',
                }
            }
        }
    },
    mounted: function () {
        axios.get('/student_absence/api/student_absence/?ordering=-datetime_creation&page_size=15')
        .then(response => {
            this.lastAbsences = response.data.results;
        });

        axios.get('/student_absence/api/absence_count/')
        .then(response => {
            this.absenceCount = response.data;
        });

    }
}
</script>