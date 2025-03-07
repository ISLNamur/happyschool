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

import ScheduleChange from "../schedule_change.vue";
import ScheduleForm from "../scheduleForm.vue";
import MassScheduleChange from "../massScheduleChange.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    routes: [
        {
            path: "/",
            component: ScheduleChange,
        },
        {
            path: "/page/:currentPage/",
            component: ScheduleChange,
            props: (route) => {
                const props = {...route.params };
                props.currentPage = Number(props.currentPage);
                return props;
            }
        },
        {
            path: "/schedule_form/:id/",
            component: ScheduleForm,
            props: (route) => {
                const props = {...route.params };
                props.id = Number(props.id);
                return props;
            }
        },
        {
            path: "/mass_schedule_change/",
            component: MassScheduleChange,
        }
    ],
    history: createWebHashHistory(),
});

export default router;
