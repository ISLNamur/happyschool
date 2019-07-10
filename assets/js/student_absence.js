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

import Vue from 'vue'

import store from '../student_absence/store.js';
import router from '../student_absence/router.js';

import axios from 'axios';

import Moment from 'moment';
Moment.locale('fr');

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/bundles/student_absence_sw.js', { scope: '/student_absence/' }).then(function(reg) {
      // registration worked.
      console.log('Registration succeeded. Scope is ' + reg.scope);
    }).catch(function(error) {
      // registration failed.
      console.log('Registration failed with ' + error);
    });
  };

import Menu from '../common/menu.vue';

var studentAbsenceApp = new Vue({
    el: '#vue-app',
    data: {menuInfo: {}},
    store,
    router,
    template: '<div><app-menu :menu-info="menuInfo" v-if="$store.state.onLine"></app-menu><router-view></router-view></div>',
    methods: {
        checkOnlineStatus() {
            axios.get("/core/ping/", {timeout: 2000})
            .then(resp => {
                this.$store.commit('changeOnLineStatus', true);
                setTimeout(() => {
                    this.checkOnlineStatus();
                }, 10000)
            })
            .catch(errors => {
                this.$store.commit('changeOnLineStatus', false);
                setTimeout(() => {
                    this.checkOnlineStatus();
                }, 10000)
            })
        },
    },
    components: {
        'app-menu': Menu,
    },
    mounted: function () {
        this.menuInfo = menu;
        this.checkOnlineStatus();
        // Update students and classes.
        if (this.$store.state.lastUpdate < Moment().format("YYYY-MM-DD")) {
            const sleep = this.$store.state.lastUpdate == "" ? 3000 : 2500;
            setTimeout(() => {
                this.$store.commit("updateStudentsClasses");
            }, sleep);
        }
    },
});
