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
        <BRow class="mb-1">
            <BCol
                cols="12"
                md="8"
            >
                <BForm
                    inline
                    class="d-flex flex-row align-items-center flex-wrap"
                >
                    <BFormGroup
                        label="Date"
                        class="me-2"
                    >
                        <BOverlay
                            :show="loading"
                            rounded="sm"
                        >
                            <BInputGroup>
                                <BButton
                                    size="sm"
                                    variant="info"
                                    @click="moveDateBefore"
                                >
                                    <IBiChevronLeft />
                                </BButton>
                                <BFormInput
                                    type="date"
                                    :model-value="date"
                                    @update:model-value="changeDate"
                                />
                                <BButton
                                    size="sm"
                                    variant="info"
                                    @click="moveDateAfter"
                                >
                                    <IBiChevronRight />
                                </BButton>
                            </BInputGroup>
                        </BOverlay>
                    </BFormGroup>
                    <BFormGroup
                        label="Rechercher"
                    >
                        <multiselect
                            ref="input"
                            :show-no-options="false"
                            :internal-search="false"
                            :options="searchOptions"
                            @search-change="getSearchOptions"
                            placeholder="Une classe, un élève,…"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="id"
                            v-model="search"
                            @select="selected"
                        >
                            <template #noResult>
                                Aucune personne trouvée.
                            </template>
                            <template #noOptions />
                        </multiselect>
                    </BFormGroup>
                </BForm>
            </BCol>
        </BRow>
        <router-view
            :date="date"
            @clear-search="search = null"
        />
    </div>
</template>

<script>
import axios from "axios";

import { DateTime } from "luxon";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { studentAbsenceTeacherStore } from "./stores/index.js";

export default {
    props: {
        date: {
            type: String,
            default: () => DateTime.now().toISODate(),
        },
    },
    data: function () {
        return {
            pointOfView: "teacher",
            optionsPointOfView: [
                { text: "Prof.", value: "teacher" },
                { text: "Éduc.", value: "educator" },
            ],
            classListType: "ownclass",
            optionsClassListType: [
                { text: "Ses classes", value: "ownclass" },
                { text: "Toutes", value: "allclass" },
            ],
            absence_count: [],
            fields: [
            ],
            educatorPeriods: [],
            filter: "",
            loading: false,
            searchOptions: [],
            search: "",
            searchId: -1,
            store: studentAbsenceTeacherStore(),
        };
    },
    computed: {
        isProecoActivated: function () {
            // eslint-disable-next-line no-undef
            return proeco;
        },
    },
    methods: {
        changeDate: function (date) {
            let newPath = `/overview/${date}/`;

            if ("classId" in this.$route.params) {
                this.$router.push(`${newPath}class_view/${this.$route.params.classId}/`);
            } else if ("studentId" in this.$route.params) {
                this.$router.push(`${newPath}student_view/${this.$route.params.studentId}/`);
            } else {
                this.$router.push(newPath);
            }
        },
        selected: function (option) {
            if (option.type == "classe") {
                // reroute to classe
                this.$router.push(`/overview/${this.date}/class_view/${option.id}/`);
                return;
            } else {
                this.$router.push(`/overview/${this.date}/student_view/${option.id}/`);
            }
        },
        moveDateBefore: function () {
            const currentDate = DateTime.fromISO(this.date);
            this.changeDate(currentDate.minus({ days: 1 }).toISODate());
        },
        moveDateAfter: function () {
            const currentDate = DateTime.fromISO(this.date);
            this.changeDate(currentDate.plus({ days: 1 }).toISODate());
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: "student",
                check_access: this.classListType === "ownclass",
            };
            axios.post("/annuaire/api/people_or_classes/", data, token)
                .then((response) => {
                    if (this.searchId !== currentSearch)
                        return;

                    const options = response.data.map((p) => {
                        if (Number.isNaN(Number.parseInt(query[0]))) {
                            return {
                                display: p.display,
                                id: p.matricule,
                                type: "student",
                            };
                        } else {
                            // It is a classe.
                            let classe = p;
                            classe.type = "classe";
                            return classe;
                        }
                    });

                    this.searchOptions = options;
                });
        },
    },
    components: {
        Multiselect,
    },
};
</script>
