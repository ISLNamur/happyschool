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
        <BRow>
            <BCol>
                <BPagination
                    class="mt-1"
                    :total-rows="entriesCount"
                    v-model="currentPage"
                    @update:model-value="changePage"
                    :per-page="20"
                />
            </BCol>
        </BRow>
        <BOverlay :show="loading">
            <BRow
                v-for="email in emails"
                :key="email.id"
            >
                <BCol>
                    <BCard
                        :title="email.subject"
                        class="mb-2"
                    >
                        <p class="card-text">
                            Expéditeur : {{ email.email_from }} <br>
                            Date : {{ email.datetime_created }} <br>
                            État : {{ email.errors }}
                        </p>
                        <p>
                            Message <IBiPaperclip v-if="email.attachments.length > 0" /> :
                        </p>
                        <BCardBody>
                            <div v-html="email.body" />
                        </BCardBody>
                    </BCard>
                </BCol>
            </BRow>
        </BOverlay>
        <BRow>
            <BCol>
                <BPagination
                    class="mt-1"
                    :total-rows="entriesCount"
                    v-model="currentPage"
                    @update:model-value="changePage"
                    :per-page="20"
                />
            </BCol>
        </BRow>
    </BContainer>
</template>

<script>

import axios from "axios";

export default {
    data: function () {
        return {
            emails: [],
            currentPage: 1,
            entriesCount: 0,
            loading: false,
        };
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        loadEntries: function () {
            this.loading = true;
            axios.get(`/mail_notification/api/notif/?page=${this.currentPage}`)
                .then((resp) => {
                    this.emails = resp.data.results;
                    this.entriesCount = resp.data.count;
                    this.loading = false;
                });
        },
    },
    mounted: function () {
        this.loadEntries();
    },
};

</script>
