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

import PiaRecord from "../pia_record.vue";
import PiaList from "../PiaList.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    routes: [
        {
            path: "/",
            component: PiaList,
        },
        {
            path: "/page/:currentPage/",
            component: PiaList,
            props: (route) => {
                const props = { ...route.params };
                props.currentPage = Number(props.currentPage);
                return props;
            },
        },
        {
            path: "/edit/:id/:advanced/",
            component: PiaRecord,
            props: (route) => {
                const props = { ...route.params };
                props.advanced = props.advanced === "true";
                return props;
            }
        },
        {
            path: "/new/:advanced/",
            component: PiaRecord,
            props: (route) => {
                const props = { ...route.params };
                props.advanced = props.advanced === "true";
                return props;
            }
        },
    ],
    history: createWebHashHistory(),
});

export default router;
