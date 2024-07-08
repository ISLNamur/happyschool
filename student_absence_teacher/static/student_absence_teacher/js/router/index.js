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

import AddAbsence from "../add_absence.vue";
import StudentAbsenceOverview from "../student_absence_overview.vue";
import ListView from "../ListView.vue";
import ClassView from "../class_view.vue";
import StudentView from "../student_view.vue";
import ExportStatus from "../export_status.vue";
import JustificationList from "../JustificationList.vue";
import JustificationEdit from "../JustificationEdit.vue";
import MailWarning from "../MailWarning.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    routes: [
        {
            path: "/",
            component: AddAbsence,
        },
        {
            path: "/add_absence",
            component: AddAbsence,
        },
        {
            path: "/overview/:date/",
            component: StudentAbsenceOverview,
            props: true,
            children: [
                {
                    path: "",
                    component: ListView,
                    props: true,
                },
                {
                    path: "class_view/:classId/",
                    component: ClassView,
                    props: true,
                },
                {
                    path: "student_view/:studentId/",
                    component: StudentView,
                    props: true,
                },
            ]
        },
        {
            path: "/justification/",
            component: JustificationList
        },
        {
            path: "/justification/:justId/",
            component: JustificationEdit,
            props: true,
        },
        {
            path: "/justification/:justId/:studentId/",
            component: JustificationEdit,
            props: true,
        },
        {
            path: "/mail_warning/:studentId/",
            component: MailWarning,
            props: true,
        },
        {
            path: "/export",
            component: ExportStatus,
        },
    ],
    history: createWebHashHistory(),
});

export default router;
