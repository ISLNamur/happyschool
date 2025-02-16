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
            <BCard
                v-if="courseObject"
                :title="`${courseObject.long_name} (${courseObject.short_name})`"
            >
                <BRow>
                    <BCol>
                        <dl>
                            <dt>Enseignement</dt>
                            <dd>{{ currentTeaching }}</dd>
                        </dl>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <h3>Liste des cours donnés</h3>
                        <BListGroup>
                            <BListGroupItem
                                v-for="gC in givenCourses"
                                :key="gC.id"
                                class="d-flex justify-content-between align-items-center"
                                :variant="gC.id === givenCourse ? 'primary': ''"
                            >
                                <span>
                                    {{ gC.classes }}
                                    <br>(<span
                                        v-for="teacher in gC.teachers"
                                        :key="teacher.id"
                                    >
                                        <a :href="`/annuaire/#/person/responsible/${teacher.matricule}/`">{{ teacher.fullname }}</a>
                                    </span>)
                                </span>
                                <span>
                                    <BButtonGroup>
                                        <BButton
                                            size="sm"
                                            variant="outline-primary"
                                            :href="`/annuaire/get_class_photo_pdf/?course_id=${gC.id}`"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <IBiImage />
                                        </BButton>
                                        <BButton
                                            size="sm"
                                            variant="outline-secondary"
                                            :href="`/annuaire/get_class_list_excel/?course_id=${gC.id}&list_type=info`"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            <IBiFileEarmarkSpreadsheet />
                                        </BButton>
                                        <BButton
                                            size="sm"
                                            variant="outline-primary"
                                            :to="`/course/${course}/${gC.id}/`"
                                        >
                                            <IBiCaretRight />
                                        </BButton>
                                    
                                    </BButtonGroup>
                                </span>
                            </BListGroupItem>
                        </BListGroup>
                    </BCol>
                    <BCol>
                        <h3>Liste des élèves du cours</h3>
                        <ul>
                            <li
                                v-for="student in studentList"
                                :key="`${givenCourse.id}-${student.matricule}`"
                            >
                                <a :href="`#/person/student/${student.matricule}/`">
                                    {{ displayStudent(student) }}
                                </a>
                            </li>
                        </ul>
                    </BCol>
                </BRow>
            </BCard>
        </BCol>
    </BRow>
</template>

<script>
import axios from "axios";

import { displayStudent } from "@s:core/js/common/utilities.js";

export default {
    props: {
        course: {
            type: Number,
            default: -1,
        },
        givenCourse: {
            type: Number,
            default: -1,
        }
    },
    data: function () {
        return {
            courseObject: null,
            currentTeaching: "",
            givenCourses: [],
        };
    },
    computed: {
        studentList: function () {
            if (this.givenCourse < 0) {
                return [];
            }

            const givenCourse = this.givenCourses.find(gC => gC.id === this.givenCourse);
            if (!givenCourse) {
                return [];
            }

            return givenCourse.students;
        }
    },
    methods: {
        displayStudent,
    },
    mounted: function () {
        Promise.all([
            axios.get(`/core/api/course/${this.course}/`),
            axios.get("/core/api/teaching/"),
            axios.get(`/core/api/given_course_info/?course=${this.course}`),
        ]).then(resps => {
            this.courseObject = resps[0].data;
            this.currentTeaching = resps[1].data.results.find(
                r => r.id === this.courseObject.teaching
            ).display_name;

            this.givenCourses = resps[2].data.results;
            Promise.all(
                this.givenCourses.map(gC => {
                    return axios.get(`/annuaire/api/student_given_course/${gC.id}/`);
                })
            ).then(gCResps => {
                this.givenCourses = this.givenCourses.map((gC, index) => {
                    gC.students = gCResps[index].data;
                    return gC;
                });
            });
        });
    }
};
</script>
