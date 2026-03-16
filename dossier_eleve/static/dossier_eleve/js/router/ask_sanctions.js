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

import AskSanctions from "../askSanctions.vue";
import Ask from "../AskSanctionForm.vue";
import WarnSanction from "../warnSanction.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    routes: [{
        path: "/",
        component: AskSanctions,
    },
    {
        path: "/edit/:id/",
        component: Ask,
        props: (route) => {
            const props = { ...route.params };
            props.id = Number(props.id);
            return props;
        },
    },
    {
        path: "/new/",
        component: Ask,
        props: true,
    },
    {
        path: "/warn/:id/",
        component: WarnSanction,
        props: (route) => {
            const props = { ...route.params };
            props.id = Number(props.id);
            return props;
        },
    },
    ],
    history: createWebHashHistory(),
});

export default router;
