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
        <BOverlay :show="sending">
            <MailTemplate
                title="Avertir les parents du retard"
                :student-id="studentId"
                get-pdf-url="/lateness/get_pdf_warning/"
                get-pdf-filename="retards.pdf"
                template-url="/lateness/api/mail_template/"
                :template-context="{}"
                :teaching="store.settings.teachings"
                @sending="send"
            >
                <template #side>
                    <BAlert :model-value="hasParentNotification">
                        Au moins un des parents reçoit des notifications.
                    </BAlert>
                    <BCard
                        no-body
                        class="scrollable"
                        header="Derniers retards"
                    >
                        <BListGroup>
                            <BListGroupItem
                                v-for="lateness in lastLatenesses"
                                :key="lateness.id"
                                class="d-flex justify-content-between align-items-center"
                            >
                                <span>
                                    {{ niceDate(lateness.datetime_creation) }}
                                </span>
                                <span v-if="lateness.justified">
                                    <strong>Justifié</strong>
                                </span>
                            </BListGroupItem>
                        </BListGroup>
                    </BCard>
                </template>
            </MailTemplate>
        </BOverlay>
    </BContainer>
</template>

<script>
import axios from "axios";
import Moment from "moment";
import "moment/dist/locale/fr";

import { useToastController } from "bootstrap-vue-next";
import MailTemplate from "@s:core/js/common/MailTemplate.vue";

import { latenessStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    props: {
        studentId: {
            type: String,
            default: "-1",
        },
    },
    data: function () {
        return {
            sending: false,
            lastLatenesses: [],
            hasParentNotification: false,
            store: latenessStore(),
        };
    },
    methods: {
        niceDate: function (dateStr) {
            return Moment(dateStr).format("HH:mm DD/MM");
        },
        send: function (data) {
            this.sending = true;
            axios.post("/lateness/api/mail_warning/", data, token)
                .then(() => {
                    this.sending = false;
                    this.$router.push("/").then(() => {
                        this.show({
                            body: "Le message a bien été envoyé.",
                            variant: "success",
                            noCloseButton: true,
                        });
                    });
                })
                .catch((err) => {
                    console.log(err);
                    this.sending = false;
                });
        },
    },
    mounted: function () {
        axios.get(`/lateness/api/lateness/?student__matricule=${this.studentId}&activate_after_count=true&ordering=-datetime_creation`)
            .then((resp) => {
                this.lastLatenesses = resp.data.results;

                // Check if there is parent notification.
                axios.get(`/core/api/parent_settings/${this.lastLatenesses[0].student.uuid}/`)
                    .then((resp) => {
                        this.hasParentNotification = resp.data.length > 0;
                    });
            });
    },
    components: {
        MailTemplate,
    },
};
</script>
