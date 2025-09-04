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
    <BToastOrchestrator />
    <BContainer>
        <BCard class="mt-2">
        <BRow>
            <BCol>
                <h1 class="text-center">Paramètres de notification</h1>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <h2>Retards et exclusions</h2>
                <p>
                    Si vous le décidez, vous avez la possibilité de recevoir un courriel chaque semaine un récapitulatif des retards justifiés et injustifiés ainsi que des exclusions de cours.
                    S'il n'y a aucun retard ou aucune exclusion, aucun courriel ne sera envoyé.
                </p>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                Élève concerné : <strong>{{ student }}</strong>
            </BCol>
        </BRow>
        <BRow v-for="email, i in emails" :key="i">
            <BCol class="mt-4">
                <label>{{ email }}</label>
                <BFormCheckbox v-model="notif[i]">
                    Envoyer des notifications par courriel toutes les semaines.
                </BFormCheckbox>
            </BCol>
        </BRow>
        <BRow class="mt-3">
            <BCol>
                <BButton
                    variant="primary"
                    :loading="sending"
                    :disabled="sending"
                    @click="sendSettings"
                >
                    Envoyer
                </BButton>
            </BCol>
        </BRow>
        </BCard>
    </BContainer>
</template>

<script>
import axios from 'axios';

import { useToastController } from "bootstrap-vue-next";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            student: student,
            contact: null,
            emails: emails,
            notif: new Array(emails.length),
            sending: false,
        };
    },
    methods: {
        sendSettings: function () {
            this.sending = true;

            let data = [];
            this.notif.forEach((setting, i) => {
                if (setting) {
                    data.push(this.emails[i]);
                }
            });
            
            axios.post(`/core/api/parent_settings/${uuid}/`, data={ emails: data }, token)
                .then(() => {
                    this.sending = false;
                    this.show({
                        body: "Les informations ont été sauvées.",
                        variant: "success",
                    })
                }).catch(() => {
                    this.show({
                        body: "Une erreur est survenue. Merci de réessayer plus tard ou de prévenir le service informatique de l'école.",
                        variant: "danger",
                    })
                })
        }
    },
    mounted: function () {
        axios.get(`/core/api/parent_settings/${uuid}/`)
            .then(resp => {
                console.log(resp.data);
                const emailsNotif = resp.data.map(p => p.contact);
                this.emails.forEach((e,i) => {
                    if (emailsNotif.includes(e)) {
                        this.notif[i] = true;
                    }
                });
            })
    }
};
</script>
