import Vue from "vue";

import Members from "../core/members_management.vue";

new Vue({
    el: "#vue-app",
    template: "<members/>",
    components: { Members }
});
