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
    <BRow>
        <BCol
            cols="12"
            md="4"
        >
            <BButton-group>
                <BButton
                    variant="success"
                    :to="`/justification/-1/`"
                >
                    <IBiPlus />
                    Ajouter un justificatif
                </BButton>
                <BButton
                    :href="`/student_absence_teacher/get_pdf_just/?${urlData}&page_size=1000`"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <IBiFileEarmarkPdf />
                    Export
                </BButton>
            </BButton-group>
        </BCol>
        <BCol>
            <BFormCheckbox
                v-model="allClasses"
                @update:model-value="loadEntries"
                switch
            >
                Toutes les classes
            </BFormCheckbox>
        </BCol>
        <BCol>
            <BFormCheckbox
                v-model="noProcessedEntries"
                @update:model-value="loadEntries"
                switch
            >
                Non Traitées
            </BFormCheckbox>
        </BCol>
        <BCol
            cols="12"
            md="4"
        >
            <BFormGroup>
                <multiselect
                    ref="input"
                    :show-no-options="false"
                    :internal-search="false"
                    :options="searchOptions"
                    @search-change="getSearchOptions"
                    placeholder="Rechercher classe, élève"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="search"
                    @select="loadEntries"
                >
                    <template #noResult>
                        Aucune personne trouvée.
                    </template>
                    <template #noOptions />
                    <template #clear>
                        <div
                            v-if="search"
                            class="multiselect__clear"
                            @click="search = null; loadEntries()"
                        />
                    </template>
                </multiselect>
            </BFormGroup>
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BOverlay :show="loading">
            <BCol>
                <BTable
                    :items="absencesWithoutJust"
                    :fields="fields"
                    stacked="md"
                    striped
                    hover
                >
                    <template #cell(studentLabel)="data">
                        <BLink :to="`/overview/${data.item.date_absence.slice(0, 10)}/student_view/${data.item.student.matricule}/`">
                            {{ data.value }}
                        </BLink>
                        <BButton
                            variant="link"
                            size="sm"
                            @click="filterStudent(data.item.student)"
                        >
                            <IBiFunnel />
                        </BButton>
                    </template>
                    <template #cell(addJust)="data">
                        <BButton
                            size="sm"
                            variant="outline-success"
                            :to="`/justification/-1/${data.item.student.matricule}/${data.item.endDate}/${data.item.countNoJustification}/`"
                        >
                            <IBiPlus />
                            Justifier
                        </BButton>
                    </template>
                    <template #cell(mail_warning)="data">
                        <BButton
                            v-if="!data.value"
                            size="sm"
                            variant="outline-primary"
                            :to="`/mail_warning/${data.item.student.matricule}/`"
                        >
                            <IBiCardText />
                        </BButton>
                        <BButton
                            v-else
                            size="sm"
                            variant="outline-succes"
                            :to="`/mail_warning/${data.item.student.matricule}/`"
                        >
                            <IBiCheck variant="success" />
                        </BButton>
                    </template>
                </BTable>
            </BCol>
        </BOverlay>
    </BRow>
    <BRow>
        <BCol>
            <BPagination
                :total-rows="entriesCount"
                v-model="currentPage"
                @update:model-value="changePage"
            />
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";
import Moment from "moment";
import "moment/dist/locale/fr";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import { displayStudent } from "@s:core/js/common/utilities";

import { studentAbsenceTeacherStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    data: function () {
        return {
            loading: true,
            absencesWithoutJust: [],
            entriesCount: 20,
            currentPage: 1,
            allClasses: false,
            noProcessedEntries: true,
            searchOptions: [],
            search: null,
            searchId: -1,
            fields: [
                {
                    key: "studentLabel",
                    label: "Étudiant",
                },
                {
                    key: "date_absence",
                    label: "Date de l'absence",
                },
                {
                    key: "countNoJustification",
                    label: "Total non justifiées",
                },
                {
                    key: "addJust",
                    label: ""
                },
                {
                    key: "mail_warning",
                    label: "Mail"
                },
            ],
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        urlData: function () {
            const daysBefore = 1;
            const dateBefore = Moment().subtract(daysBefore, "days").toISOString().slice(0, 10);

            // Check current search.
            let searchFilter = "";
            if (this.search) {
                if (this.search.type === "student") {
                    searchFilter = `&student__matricule=${this.search.id}`;
                } else {
                    searchFilter = `&student__classe=${this.search.id}`;
                }
            }
            let url = "status=A" +
                `&activate_own_classes=${!this.allClasses}` +
                "&activate_no_justification=true" +
                `&date_absence__lte=${dateBefore}` +
                `&mail_warning=${!this.noProcessedEntries}` +
                searchFilter +
                "&ordering=-date_absence,datetime_creation" +
                // eslint-disable-next-line no-undef
                `&scholar_year=${current_scholar_year}-${current_scholar_year + 1}`;
            return url;
        }
    },
    methods: {
        displayStudent,
        sortAbsences: function (a, b) {
            if (a.date_absence < b.date_absence) {
                return true;
            }
            if (a.date_absence === b.date_absence) {
                if (`${a.student.classe.year}${a.student.classe.letter}` > `${b.student.classe.year}${b.student.classe.letter}`) {
                    return true;
                } else {
                    return false;
                }
            }
            return false;
        },
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        loadEntries: function () {
            this.loading = true;

            axios.get(`/student_absence_teacher/api/absence_educ/?${this.urlData}&page=${this.currentPage}`)
                .then((resp) => {
                    this.entriesCount = resp.data.count;
                    const groupByStudent = Object.groupBy(resp.data.results, ({ student }) => student.matricule);
                    this.absencesWithoutJust = Object.values(groupByStudent).map(student => {
                        const date_absence = student.map(s => `${s.date_absence} (${this.store.periodEduc.find(p => p.id === s.period).name})`).join(", ");
                        return {
                            student: student[0].student,
                            studentLabel: this.displayStudent(student[0].student),
                            date_absence: date_absence,
                            endDate: student.map(s => s.date_absence).toSorted().toReversed()[0],
                            mail_warning: student.some(s => s.mail_warning),
                            countNoJustification: this.countNoJustification,
                        };
                    }).sort(this.sortAbsences);

                    this.loading = false;

                    Promise.all(this.absencesWithoutJust.map(a => {
                        return axios.get(`/student_absence_teacher/api/count_no_justification/${a.student.matricule}/`);
                    }))
                        .then((resps) => {
                            resps.forEach((r, i) => {
                                this.absencesWithoutJust[i].countNoJustification = r.data.count;
                            });
                        });
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                });
        },
        filterStudent: function (student) {
            this.search = {
                display: displayStudent(student, this),
                id: student.matricule,
                type: "student",
            };
            this.loadEntries();
        },
        getSearchOptions: function (query) {
            let app = this;
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const data = {
                query: query,
                teachings: this.store.settings.teachings,
                people: "student",
                check_access: !this.allClasses,
            };
            axios.post("/annuaire/api/people_or_classes/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;

                    const options = response.data.map(p => {
                        if (Number.isNaN(Number.parseInt(query[0]))) {
                            return {
                                display: displayStudent(p, app),
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
    mounted: function () {
        this.store.getOptions();

        this.loadEntries();
    },
    components: {
        Multiselect
    }
};

</script>

<style>
.multiselect__clear {
    position: absolute;
    right: 41px;
    height: 40px;
    width: 40px;
    display: block;
    cursor: pointer;
    z-index: 2;
}
.multiselect__clear::before {
    transform: rotate(45deg);
}
.multiselect__clear::after {
    transform: rotate(-45deg);
}
.multiselect__clear::after, .multiselect__clear::before {
    content: "";
    display: block;
    position: absolute;
    width: 3px;
    height: 16px;
    background: #aaa;
    top: 12px;
    right: 4px;
}
</style>
