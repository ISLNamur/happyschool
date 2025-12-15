// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.

import PersonCard from "../person_card.vue";
import PersonInfo from "../person_info.vue";
import PersonSchedule from "../person_schedule.vue";
import SensitiveInfo from "../sensitive_info.vue";
import ContactInfo from "../contact_info.vue";
import MedicalInfo from "../medical_info.vue";
import OtherInfo from "../other_info.vue";
import ClassList from "../classe_list.vue";
import CourseInfo from "../course_info.vue";

export default [
    {
        path: "/person/:type/:matricule/",
        component: PersonCard,
        props: (route) => {
            const props = { ...route.params };
            props.matricule = Number(props.matricule);
            return props;
        },
        children: [
            {
                path: "",
                component: PersonInfo,
            },
            {
                path: "schedule",
                component: PersonSchedule,
            },
            {
                path: "sensitive",
                component: SensitiveInfo,
            },
            {
                path: "contact",
                component: ContactInfo,
            },
            {
                path: "medical",
                component: MedicalInfo,
            },
            {
                path: "other",
                component: OtherInfo,
            },
        ],
    },
    {
        path: "/classe/:classe/",
        component: ClassList,
        props: true,
    },
    {
        path: "/course/:course/:givenCourse/",
        component: CourseInfo,
        props: (route) => {
            const props = { ...route.params };
            props.course = Number(props.course);
            props.givenCourse = Number(props.givenCourse);
            return props;
        },
    },
    {
        path: "/course/:course/",
        component: CourseInfo,
        props: (route) => {
            const props = { ...route.params };
            props.course = Number(props.course);
            return props;
        },
    },
    // ]
];
