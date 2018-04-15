import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon.vue'

Vue.use(BootstrapVue);
Vue.component('icon', Icon);

var mailNotificationListApp = new Vue({
    el: '#vue-app',
    data: function () {
    },
});
