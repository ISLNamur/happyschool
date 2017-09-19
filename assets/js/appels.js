import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

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
