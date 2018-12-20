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

import Vuex from 'vuex';
Vue.use(Vuex);
import VuexPersistence from 'vuex-persist'

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import Moment from 'moment';
Moment.locale('fr');

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/bundles/student_absence_sw.js', { scope: '/' }).then(function(reg) {
      // registration worked.
      console.log('Registration succeeded. Scope is ' + reg.scope);
    }).catch(function(error) {
      // registration failed.
      console.log('Registration failed with ' + error);
    });
  };

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

const store = new Vuex.Store({
    state: {
      settings: settings,
      filters: [],
      todayAbsences: {},
      changes: [],
      onLine: navigator.onLine,
      lastUpdate: "",
      updating: false,
    },
    getters: {
        change(state) {
            return change => {
                for (let c in state.changes) {
                    if (state.changes[c].matricule == change.matricule && state.changes[c].date_absence == change.date_absence) {
                        state.changes[c].index = c;
                        return state.changes[c];
                    }
                }
                return null;
            }
        }
    },
    mutations: {
        addFilter: function (state, filter) {
            // If filter is a matricule, remove name filter to avoid conflict.
            if (filter.filterType === 'matricule_id') {
                this.commit('removeFilter', 'name');
            }
  
            // Overwrite same filter type.
            this.commit('removeFilter', filter.filterType);
  
            state.filters.push(filter);
        },
        removeFilter: function (state, key) {
            for (let f in state.filters) {
                if (state.filters[f].filterType === key) {
                    state.filters.splice(f, 1);
                    break;
                }
            }
        },
        removeChange: function (state, change) {
            for (let c in state.changes) {
                if (state.changes[c].matricule == change.matricule && state.changes[c].date_absence == change.date_absence) {
                    state.changes.splice(c, 1);
                    break;
                }
            }
        },
        setChange: function (state, change) {
            let oldChange = this.getters.change(change);
            if (!oldChange) {
                state.changes.push(change);
            } else {
                if ('morning' in change) state.changes[oldChange.index].morning = change.morning;
                if ('afternoon' in change) state.changes[oldChange.index].afternoon = change.afternoon;
                // Force update.
                Vue.set(state.changes, oldChange.index, state.changes[oldChange.index]);
            }
        },
        setTodayAbsences: function (state, absences) {
            state.todayAbsences = absences;
        },
        updateStudentsClasses: function (state) {
            console.log("coucou");
            state.lastUpdate = Moment().format("YYYY-MM-DD");
            this.commit('updatingStatus', true);
            const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: 'everybody',
                teachings: state.settings.teachings,
                people: 'student',
                active: true,
            };
            axios.post('/annuaire/api/people/', data, token)
            .then(response => {
                console.log('hello');
                this.commit('updatingStatus', false);
            });
        },
        updatingStatus: function (state, updating) {
            state.updating = updating;
        },
        changeOnLineStatus: function (state, onLine) {
            state.onLine = onLine;
        }
    },
    plugins: [vuexLocal.plugin],
  });

import StudentAbsence from '../student_absence/student_absence.vue';
import Overview from '../student_absence/overview.vue';
import AddAbsence from '../student_absence/add_absence.vue';

  const router = new VueRouter({
    routes: [
    {
        path: '',
        component: StudentAbsence,
        children: [
            {
                path: '',
                component: Overview,
            },
            {
                path: 'overview',
                component: Overview,
            },
            {
                path: 'add_absence',
                component: AddAbsence,
            },
        ]
    },
    ]
});

import axios from 'axios';

import Menu from '../common/menu.vue';

var studentAbsenceApp = new Vue({
    el: '#vue-app',
    data: {menuInfo: {}},
    store,
    router,
    template: '<div><app-menu :menu-info="menuInfo" v-if="$store.state.onLine"></app-menu><router-view></router-view></div>',
    methods: {
        updateOnlineStatus(e) {
            const {
                type
            } = e;
            this.$store.commit('changeOnLineStatus', type === 'online');
        },
    },
    components: {
        'app-menu': Menu,
    },
    mounted: function () {
        this.menuInfo = menu;
        // Update students and classes.
        if (this.$store.state.lastUpdate < Moment().format("YYYY-MM-DD")) this.$store.commit("updateStudentsClasses");
        
        window.addEventListener('online', this.updateOnlineStatus);
        window.addEventListener('offline', this.updateOnlineStatus);
    },
    beforeDestroy() {
        window.removeEventListener('online', this.updateOnlineStatus);
        window.removeEventListener('offline', this.updateOnlineStatus);
    }
});
