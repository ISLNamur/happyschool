import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import moment from 'moment';
moment.locale('fr');
import Push from 'push.js';

import {AppeSocket} from '../common/websocket.js';

import Menu from '../menu.vue'
import scheduleChangeEntry from '../schedule_change/scheduleChangeEntry.vue'
import AddModal from '../schedule_change/addModal.vue'
import Filters from '../common/filters.vue'

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'
import Multiselect from 'vue-multiselect'

Vue.component('header-menu', Menu);
Vue.component('schedule-change-entry', scheduleChangeEntry);
Vue.component('icon', Icon);
Vue.component('multiselect', Multiselect);


Vue.use(BootstrapVue);

let actionResponse = {
    schedule_change: {
        list: function(payload) {
            // Add items to the list, clean up if necessary.
            scheduleChangeApp.scheduleChangeEntries.splice(0)
            setTimeout(function() {
                // Ensure the list is empty.
                for (let newElement in payload.data.content) {
                    scheduleChangeApp.scheduleChangeEntries.push(payload.data.content[newElement]);
                }
                scheduleChangeApp.numberOfPages = payload.data.num_pages;
                scheduleChangeApp.currentPage = payload.data.page;
                scheduleChangeApp.entriesCount = payload.data.total_count;
                scheduleChangeApp.isRefreshing = false;
            }, 300);
        },
        create: function(payload) {
            if ("pk" in payload) {
                console.log('creating…');
                scheduleChangeApp.refresh();
                scheduleChangeApp.hideModal();
            } else {
                if ("errors" in payload && payload.errors.length > 0) {
                    console.log('error while creating');
                    for (var err in payload.errors) {
                        let input = Object.keys(payload.errors[err])[0];
                        scheduleChangeApp.modalErrors[input] = false;
                    }
                } else {
                    Push.create("Un changement d'horaire a été créé.");
                }
            }
        },
        update: function(payload) {
            if ("errors" in payload && payload.errors.length > 0) {
                // Handle errors.
                console.log("error while updating");
                console.log(payload.errors);
            } else {
                console.log("updating…");
                scheduleChangeApp.refresh();
                scheduleChangeApp.hideModal();
                Push.create('Le changement a été mis à jour.');
            }
        },
        delete: function(payload) {
            if ("pk" in payload) {
                let pk = payload.pk;
                for (var e = 0; e < scheduleChangeApp.scheduleChangeEntries.length; e++) {
                    if (scheduleChangeApp.scheduleChangeEntries[e].id === pk) {
                        scheduleChangeApp.scheduleChangeEntries.splice(e, 1);
                        Push.create('Le changement a bien été supprimé.');
                        break;
                    }
                }
            }
        },
        get_filters: function(payload) {
            scheduleChangeApp.filterTypeOptions = payload.data;
            scheduleChangeApp.active = true;
        },
        get_filters_options: function(payload) {
            scheduleChangeApp.filterSearchOptions = payload.data;
        }
    },
    get_teachers: {
        search_teachers: function(payload) {
            scheduleChangeApp.modalOptions.teachersOptions = payload.result;
            scheduleChangeApp.$refs.modal.teachersIsLoading = false;
        },
    },
    get_students_classes_years: {
        search_students_classes_years: function(payload) {
            scheduleChangeApp.modalOptions.classesOptions = payload.result;
            scheduleChangeApp.$refs.modal.classesIsLoading = false;
        }
    },
    get_menu: {
        get_menu: function(payload) {
            scheduleChangeApp.menu = payload.menu;
        }
    }
}

var scheduleChangeApp = new Vue({
    el: '#vue-app',
    data: {
        appeSocket: null,
        scheduleChangeEntries: [],
        currentModal: 'add-modal',
        modalTitle: "Ajouter une date d'absence",
        modalOk: "Ajouter une date",
        isRefreshing: false,
        currentPage: 1,
        per_page: 5,
        numberOfPages: 1,
        entriesCount: 0,
        order_by: 'date_start',
        active: false,
        filters: {},
        filterTypeOptions: [],
        filterSearchOptions: [],
        modalOptions: {
            teachersOptions: [],
            classesOptions: [],
        },
        modalErrors: {
            date_start: true
        },
        'settings': settings,
        menu: {},
    },
    watch: {
        active: function() {
            if (this.active) {
                this.$refs.filters.addDateTimeTag('date_start', moment().format('Y-MM-DD'),
                                                  moment().add(1, 'years').format('Y-MM-DD'));
            } else {
                let val = 'date_start-' + moment().format('Y-MM-DD') + '_' + moment().add(1, 'years').format('Y-MM-DD')
                this.$refs.filters.removeTag(val);
            }
        }
    },
    methods: {
        setFilters: function (filters) {
            this.filters = filters;
            scheduleChangeApp.refresh();
        },
        editEntry: function (index) {
            this.showModal("add-modal");
            var scheduleChange = this.scheduleChangeEntries[index];
            let fields = ["date_start", "date_end", "time_start", "time_end",
                          "activity", "place", "comment", "id"];
            for (var f in fields) {
                this.$refs.modal[fields[f]] = scheduleChange[fields[f]];
            }

            if (scheduleChange.classes) {
                this.$refs.modal["classes"] = scheduleChange["classes"].split(", ");
            }
            if (scheduleChange.teachers) {
                this.$refs.modal["teachers"] = scheduleChange["teachers"].split(", ");
            }
        },
        deleteEntry: function (key, index) {
            if (!confirm("Êtes-vous sûr de vouloir supprimer cet élément ?")) {
                return;
            }
            this.appeSocket.delete("schedule_change", key);
            this.refresh();
        },
        showModal: function (modal) {
            this.currentModal = modal;
            for (var key in this.modalErrors) {
                this.modalErrors[key] = true;
            }
            this.$refs.modal.show();
        },
        hideModal: function() {
            this.$refs.modal.hide();
        },
        refresh: function () {
            this.isRefreshing = true;
            this.appeSocket.getList("schedule_change",
                                    this.filters,
                                    this.order_by,
                                    this.per_page,
                                    this.currentPage);
        },
        changePage(page) {
            this.currentPage = page;
            this.refresh();
        }
    },
    mounted: function() {
        // Ensure vuejs app is ready.
        let onOpen = () => {
            // this.appeSocket.getList("schedule_change",
            //                         this.filters,
            //                         this.order_by,
            //                         this.per_page,
            //                         this.currentPage);
            this.appeSocket.send("schedule_change", {action: 'get_filters'});
            this.appeSocket.send("get_menu", {action: 'get_menu', active: 'schedule_change'});
            this.appeSocket.subscribe("schedule_change", "create");
            this.appeSocket.subscribe("schedule_change", "delete");
        }
        this.appeSocket = new AppeSocket(actionResponse, onOpen);
    },
    components: {
        'add-modal': AddModal,
        'filters': Filters,
        // 'export-form': ExportForm,
    }
});
