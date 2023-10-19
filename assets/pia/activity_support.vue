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
    <b-table-simple v-if="!loading">
        <b-thead>
            <b-tr>
                <b-th>Jour</b-th>
                <b-th>Cours</b-th>
                <b-th>Prof</b-th>
            </b-tr>
        </b-thead>
        <b-tbody>
            <b-tr
                v-for="day in supportDays"
                :key="day"
            >
                <b-td>{{ dayOfWeek[day] }}</b-td>
                <b-td>
                    <multiselect
                        :internal-search="false"
                        :options="store.branches"
                        placeholder="Choisir une matière"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        :value="value[day].branch"
                        @input="emitChangedData($event, 'branch', day)"
                        :show-no-options="false"
                        label="branch"
                        track-by="id"
                        multiple
                    >
                        <template #noResult>
                            Aucune branche trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-td>
                <b-td>
                    <multiselect
                        :id="`responsible-support-${day}`"
                        :internal-search="false"
                        :options="responsibleOptions"
                        @search-change="getPeople"
                        placeholder="Choisir un ou plusieurs profs"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        :value="value[day].teachers"
                        @input="emitChangedData($event, 'teachers', day)"
                        label="display"
                        track-by="matricule"
                        :show-no-options="false"
                        multiple
                    >
                        <template #noResult>
                            Aucun responsable trouvé.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-td>
            </b-tr>
        </b-tbody>
    </b-table-simple>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import {getPeopleByName} from "../common/search.js";

import { piaStore } from "./stores/index.js";

export default {
    props: {
        value: {
            type: Object,
            default: () => {},
        },
        loading: {
            type: Boolean,
            default: true,
        }
    },
    data: function () {
        return {
            responsibleOptions: [],
            branch: [],
            teachers: [],
            store: piaStore(),
            // support_activities: {},
            dayOfWeek: {1: "Lundi", 2: "Mardi", 3: "Mercredi", 4: "Jeudi", 5: "Vendredi", 6: "Samedi", 7: "Dimanche"},
            searchId: 0,
        };
    },
    computed: {
        supportDays: function () {
            const seqDays = this.store.settings.weekday_support_activity.split(",");
            const days = seqDays.filter(d => d.length === 1).map(d => Number(d.trim()));
            const ranges = seqDays.filter(d => d.length === 3).map(d => d.trim()).filter(d => d[1] === "-");
            ranges.forEach(r => {
                const start = Number(r[0]);
                const end = Number(r[2]);
                if (start <= end) {
                    Array(end - start + 1).fill().map((_, i) => i + start).forEach(d => days.push(d));
                }
            });

            return days.sort();
        }
    },
    methods: {
        emitChangedData: function (payload, key, day) {
            let valueCopy = Object.assign({}, this.value);
            valueCopy[day][key] = payload;
            this.$emit("input", valueCopy);
        },
        getPeople: function (searchQuery, person) {
            person = person.split("-")[0];
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, person)
                .then( (resp) => {
                // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this[person + "Options"] = resp.data;
                // this.searching = false;
                })
                .catch( (err) => {
                    alert(err);
                // this.searching = false;
                });
        },
    },
    components: {
        Multiselect
    },
    mounted: function () {
    }
};
</script>
