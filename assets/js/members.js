import Vue from "vue";

import Members from "../core/members.vue";

new Vue({
    el: "#vue-app",
    template: "<members/>",
    components: { Members }
});
