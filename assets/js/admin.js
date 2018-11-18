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

import Vue from 'vue';

import Vuex from 'vuex';
Vue.use(Vuex);

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Admin from '../core/admin.vue';
import Import from '../core/import.vue';
import GeneralSettings from '../core/general_settings.vue';
import Menu from '../common/menu.vue';

const router = new VueRouter({
    routes: [
    {
        path: '',
        component: Admin,
        children: [
            {
                path: '',
                component: GeneralSettings,
            },
            {
                path: 'general',
                component: GeneralSettings,
            },
            {
                path: 'import',
                component: Import,
            },
        ]
    },
    ]
});

// const store = new Vuex.Store({
//   state: {
//     settings: settings
//   },
// });

var adminApp = new Vue({
    el: '#vue-app',
    data: {menuInfo: {}},
    // store,
    router,
    template: '<div><app-menu :menu-info="menuInfo"></app-menu><router-view></router-view></div>',
    mounted: function () {
        this.menuInfo = menu;
    },
    components: {
        'app-menu': Menu,
    }
});
