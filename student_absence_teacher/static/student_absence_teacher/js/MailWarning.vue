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
        <BCol>
            <h2>Avertir les parents de l'absence</h2>
        </BCol>
    </BRow>
    <BRow class="mb-1 text-right">
        <BCol>
            <BButton
                @click="getPDF"
                variant="outline-primary"
            >
                <IBiFileText />
                Télécharger PDF
            </BButton>
        </BCol>
    </BRow>

    <BRow v-if="student">
        <BCol>
            Éleve concerné : <strong>{{ displayStudent(student) }}</strong>
        </BCol>
    </BRow>

    <BRow>
        <BCol>
            <BFormGroup
                label="Destinataires"
                description="Si deux destinataires sont les mêmes, un seul courriel sera envoyé."
            >
                <BFormCheckboxGroup
                    v-model="recipient"
                    :options="recipientOptions"
                />
            </BFormGroup>
            <BFormGroup label="Autres personnes de l'école">
                <multiselect
                    id="responsible-0"
                    :internal-search="false"
                    :options="responsibleOptions"
                    @search-change="getResponsible"
                    placeholder="Ajouter une autre personne de l'école"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label="Cliquer dessus pour enlever"
                    v-model="otherRecipients"
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
            </BFormGroup>
        </BCol>
        <BCol>
            <BCard
                no-body
                class="scrollable"
            >
                <template
                    #header
                >
                    <div class="d-flex justify-content-between align-items-center">
                        <strong>Absences concernées (du {{ dateStart }} au {{ dateEnd }})</strong>
                        <BBadge variant="primary">
                            {{ absenceWarned.filter(a => a).length }}
                        </BBadge>
                    </div>
                </template>
                <BListGroup>
                    <BListGroupItem
                        v-for="absence, idx in lastAbsences"
                        :key="absence.id"
                        class="d-flex justify-content-between align-items-center"
                        :variant="absence.mail_warning ? '' : 'warning'"
                    >
                        <span>
                            <BFormCheckbox v-model="absenceWarned[idx]">
                                {{ absence.date_absence }}
                                ({{ store.periodEduc.find(p => p.id === absence.period).name }})
                            </BFormCheckbox>
                        </span>
                        <IBiCheck v-if="absence.mail_warning" />
                        <IBiX v-else />
                    </BListGroupItem>
                </BListGroup>
            </BCard>
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BCol>
            <text-editor v-model="text" />
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BCol>
            <BOverlay :show="sending">
                <BButton
                    variant="primary"
                    @click="send"
                >
                    Envoyer
                </BButton>
            </BOverlay>
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";
import Moment from "moment";
import "moment/dist/locale/fr";

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import TextEditor from "@s:core/js/common/text_editor.vue";

import { getPeopleByName } from "@s:core/js/common/search.js";
import { displayStudent } from "@s:core/js/common/utilities";

import { studentAbsenceTeacherStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        studentId: {
            type: String,
            default: "-1"
        }
    },
    data: function () {
        return {
            recipient: [],
            recipientOptions: [
                { "text": "Père", "value": "father" },
                { "text": "Mère", "value": "mother" },
                { "text": "Responsable légal", "value": "resp" },
                { "text": "Responsable à l'école", "value": "resp_school" },
            ],
            responsibleOptions: [],
            otherRecipients: [],
            lastAbsences: [],
            absenceWarned: [],
            text: "",
            searchId: -1,
            sending: false,
            student: null,
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        dateStart: function () {
            const absences = this.lastAbsences.filter((lA, i) => this.absenceWarned[i]);
            if (absences.length === 0) return "";

            return absences[absences.length - 1].date_absence;
        },
        dateEnd: function () {
            const absences = this.lastAbsences.filter((lA, i) => this.absenceWarned[i]);
            if (absences.length === 0) return "";

            return absences[0].date_absence;
        },
    },
    methods: {
        displayStudent,
        getResponsible: function (searchQuery) {
            this.searchId += 1;
            let currentSearch = this.searchId;

            const teachings = this.store.settings.teachings.filter(
                // eslint-disable-next-line no-undef
                value => user_properties.teaching.includes(value));
            getPeopleByName(searchQuery, teachings, "responsible")
                .then((resp) => {
                    // Avoid that a previous search overwrites a faster following search results.
                    if (this.searchId !== currentSearch)
                        return;
                    this.responsibleOptions = resp.data;
                    // this.searching = false;
                })
                .catch((err) => {
                    alert(err);
                    // this.searching = false;
                });
        },
        send: function () {
            const relatedAbsences = this.lastAbsences.filter((lA, i) => this.absenceWarned[i]).map(a => a.id);
            const data = {
                msg: this.text,
                student_id: this.studentId,
                recipients: this.recipient,
                other_recipients: this.otherRecipients.map(r => r.pk),
                absences: relatedAbsences,
            };
            this.sending = true;
            axios.post("/student_absence_teacher/api/mail_warning/", data, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/justification/").then(() => {
                        this.show({props: {
                            body: "Le message a bien été envoyé.",
                            variant: "success",
                            noCloseButton: true,
                        }});
                    });
                })
                .catch(err => {
                    console.log(err);
                    this.sending = false;
                });
        },
        getPDF: function () {
            const data = {
                student_id: this.studentId,
                text: this.text,
            };
            axios.post("/student_absence_teacher/get_pdf_warning/", data, {
                responseType: "blob",
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken"
            })
                .then(resp => {
                    const blob = new Blob([resp.data], { type: "application/pdf" });
                    var link = document.createElement("a");
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "absences_non_motivees.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });

        },
    },
    mounted: function () {
        this.store.getOptions();
        axios.get(`/student_absence_teacher/api/absence_educ/?student__matricule=${this.studentId}&status=A&ordering=-date_absence&activate_no_justification=true`)
            .then((resp) => {
                this.absenceWarned = resp.data.results.map(() => false);
                this.lastAbsences = resp.data.results;

                if (this.lastAbsences.length === 0) {
                    return;
                }

                this.student = this.lastAbsences[0].student;

                // Prefill related absences.
                let lastDate = Moment(this.lastAbsences[0].date_absence);
                for (let i in this.lastAbsences) {
                    let dateBefore = Moment(this.lastAbsences[i].date_absence);
                    if (dateBefore.day() === 5) {
                        // It is friday, add 3 days.
                        dateBefore.add(3, "days");
                    } else {
                        dateBefore.add(1, "days");
                    }

                    if (dateBefore.isSameOrAfter(lastDate)) {
                        this.absenceWarned[i] = true;
                    } else {
                        break;
                    }
                    lastDate = Moment(this.lastAbsences[i].date_absence);
                }

                axios.get(`/student_absence_teacher/api/mail_warning_template/${this.studentId}/${this.dateStart}/${this.dateEnd}/`)
                    .then((templateResp) => {
                        this.text = templateResp.data;
                    });
            });
    },
    components: {
        Multiselect,
        TextEditor
    }
};
</script>

<style>
.scrollable {
    height:400px;
    overflow-y: scroll;
}
</style>
