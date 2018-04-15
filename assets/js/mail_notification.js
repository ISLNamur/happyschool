import Vue from 'vue';

import MailNotification from '../mail_notification/mail_notification.vue';

var mailNotificationApp = new Vue({
    el: '#vue-app',
    template: '<mail-notification/>',
    components: { MailNotification }
})
