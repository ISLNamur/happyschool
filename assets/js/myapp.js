import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

var ws = new WebSocket("ws://" + window.location.host + "/?session_key=" + session);
var myappApp = new Vue({
    el: '#my-app'
});