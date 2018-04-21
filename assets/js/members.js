import Vue from 'vue';

import Members from '../core/members.vue';

var membersApp = new Vue({
    el: '#vue-app',
    template: '<members/>',
    components: { Members }
})
