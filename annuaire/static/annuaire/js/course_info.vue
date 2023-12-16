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
    <b-row>
        <b-col>
            <b-card
                v-if="courseObject"
                :title="`${courseObject.long_name} (${courseObject.short_name})`"
            >
                <b-row>
                    <b-col>
                        <dl>
                            <dt>Enseignement</dt>
                            <dd>{{ currentTeaching }}</dd>
                        </dl>
                        <dl>
                            <dt>Liste des cours donnés</dt>
                            <dd>
                                <ul>
                                    <li
                                        v-for="givenCourse in givenCourses"
                                        :key="givenCourse.id"
                                    >
                                        <dt>
                                            <a
                                                v-for="teacher in givenCourse.teachers"
                                                :key="teacher.id"
                                                :href="`/annuaire/#/person/responsible/${teacher.matricule}/`"
                                            >
                                                {{ teacher.fullname }}
                                            </a>
                                        </dt>
                                        <dd>
                                            Classes concernées : {{ givenCourse.classes }}
                                            (<a
                                                v-b-toggle="`students-${givenCourse.id}`"
                                            >
                                                Voir les étudiants
                                            </a>)
                                            <b-collapse :id="`students-${givenCourse.id}`">
                                                <ul>
                                                    <li
                                                        v-for="student in givenCourse.students"
                                                        :key="`${givenCourse.id}-${student.matricule}`"
                                                    >
                                                        <a :href="`#/person/student/${student.matricule}/`">
                                                            {{ student.display }}
                                                        </a>
                                                    </li>
                                                </ul>
                                            </b-collapse>
                                        </dd>
                                    </li>
                                </ul>
                            </dd>
                        </dl>
                    </b-col>
                </b-row>
            </b-card>
        </b-col>
    </b-row>
</template>

<script>
import axios from "axios";

export default {
    props: {
        course: {
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
