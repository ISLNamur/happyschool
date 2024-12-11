<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <BContainer>
        <BRow>
            <BNav tabs>
                <BNavItem to="/">
                    Envoyer un email
                </BNavItem>
                <BNavItem
                    active
                    href="/mail_notification/list/"
                >
                    Liste des emails envoyés
                </BNavItem>
            </BNav>
        </BRow>
        <BRow
            v-for="email in emails"
            :key="email.id"
        >
            <BCol>
                <BCard
                    :title="email.subject"
                    :sub-title="`Envoyé à : ${email.email_to} (${email.teaching}) à partir de : ${email.email_from}`"
                >
                    <p class="card-text">
                        Destination : {{ email.to_type }} <br>
                        Date : {{ email.datetime_created }} <br>
                        État : {{ email.errors }}
                    </p>
                    <p>
                        Message <IBiPaperclip v-if="email.attachments.length > 0" /> :
                    </p>
                    <BCardBody v-html="email.body" />
                </BCard>
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>

import axios from "axios";
import { BCardBody } from "bootstrap-vue-next";

export default {
    data: function () {
        return {
            emails: []
        };
    },
    mounted: function () {
        axios.get("/mail_notification/api/notif")
            .then((resp) => {
                this.emails = resp.data.results;
            });
    }
};

</script>
