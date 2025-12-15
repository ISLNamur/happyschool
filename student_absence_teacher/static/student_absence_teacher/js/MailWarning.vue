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
    <BOverlay :show="sending">
        <MailTemplate
            :student-id="studentId"
            :teachings="store.settings.teachings"
            title="Avertir les parents de l'absence"
            get-pdf-url="/student_absence_teacher/get_pdf_warning/"
            get-pdf-filename="absences_non_motivees.pdf"
            template-url="/student_absence_teacher/api/mail_warning_template/"
            :template-context="context"

            @sending="send"
        >
            <template #side>
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
            </template>
        </mailtemplate>
    </BOverlay>
</template>

<script>
import axios from "axios";

import MailTemplate from "@s:core/js/common/MailTemplate.vue";

import { studentAbsenceTeacherStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        studentId: {
            type: String,
            default: "-1",
        },
    },
    data: function () {
        return {
            lastAbsences: [],
            absenceWarned: [],
            sending: false,
            student: null,
            store: studentAbsenceTeacherStore(),
        };
    },
    computed: {
        context: function () {
            return {
                dates: this.lastAbsences.map((lA) => {
                    const periodName = this.store.periodEduc.find(p => p.id === lA.period).name;
                    return `${lA.date_absence} ${periodName}`;
                }).join(","),
            };
        },
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
        send: function (data) {
            const relatedAbsences = this.lastAbsences.filter((lA, i) => this.absenceWarned[i]).map(a => a.id);
            const context = Object.assign(data, { absences: relatedAbsences });
            this.sending = true;
            axios.post("/student_absence_teacher/api/mail_warning/", context, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/justification/").then(() => {
                        this.show({
                            body: "Le message a bien été envoyé.",
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch((err) => {
                    console.log(err);
                    this.sending = false;
                });
        },
    },
    mounted: function () {
        this.store.getOptions();
        // eslint-disable-next-line no-undef
        axios.get(`/student_absence_teacher/api/absence_educ/?student__matricule=${this.studentId}&status=A&ordering=-date_absence&activate_no_justification=true&scholar_year=${current_scholar_year}`)
            .then((resp) => {
                this.absenceWarned = resp.data.results.map(() => true);
                this.lastAbsences = resp.data.results;

                if (this.lastAbsences.length === 0) {
                    return;
                }
            });
    },
    components: {
        MailTemplate,
    },
};
</script>

<style>
.scrollable {
    height:400px;
    overflow-y: scroll;
}
</style>
