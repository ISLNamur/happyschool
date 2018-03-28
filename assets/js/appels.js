// This file is part of Appyschool.
//
// Appyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Appyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Appyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import Filters from '../common/filters.vue'

import axios from 'axios';
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
import AppelEntry from '../appels/appelEntry.vue'

Vue.component('icon', Icon);
Vue.component('appel-entry', AppelEntry);

Vue.use(BootstrapVue);
var AppelsApp = new Vue({
    el: '#vue-app',
    data: {
        active: true,
        entriesCount: 20,
        currentPage: 1,
        entries: [],
    },
    methods: {
        changePage: function (page) {
            return;
        },
        deleteEntry: function (id) {

        },
        editEntry: function (id) {

        }
    },
    mounted: function() {
        // const params = ({params: {page: this.currentPage}});
        axios.get('/appels/api/?page=' + this.currentPage)
        .then(response => {
            this.entries = response.data.results;
        });
    },
    components: {
        // 'add-modal': AddModal,
        'filters': Filters,
        // 'export-form': ExportForm,
    },

});
