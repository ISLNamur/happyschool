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

import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

import StudentAbsence from "../student_absence/student_absence.vue";
import AbsenceOverview from "../student_absence/absence_overview.vue";
import AddAbsence from "../student_absence/add_absence.vue";
import ClasseNotes from "../student_absence/classe_notes.vue";
import AbsenceList from "../student_absence/absence_list.vue";

export default new VueRouter({
    routes: [
        {
            path: "",
            component: StudentAbsence,
            children: [
                {
                    path: "",
                    component: AbsenceOverview,
                },
                {
                    path: "overview",
                    component: AbsenceOverview,
                },
                {
                    path: "add_absence",
                    component: AddAbsence,
                },
                {
                    path: "notes",
                    component: ClasseNotes,
                },
                {
                    path: "list",
                    component: AbsenceList,
                }
            ]
        },
    ]
});
