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
    <div>
        <BCard @click="displayPhoto">
            <BRow>
                <BCol
                    cols="2"
                    v-if="showPhoto"
                >
                    <BImg
                        :src="`/static/photos/${lateness.student_id}.jpg`"
                        fluid
                        alt="Photo de l'élève"
                    />
                </BCol>
                <BCol>
                    <IBiExclamationCircle v-if="lateness.sanction_id" />
                    <strong>{{ niceDate }}</strong>:
                    <a :href="`/annuaire/#/person/student/${lateness.student.matricule}/`">
                        {{ displayStudent(lateness.student) }}
                    </a>
                    <BBadge
                        v-if="!lateness.justified"
                        class="ms-1"
                        id="lateness-count"
                    >
                        {{ lateness.lateness_count }}
                    </BBadge>
                    <BTooltip target="lateness-count">
                        Nombre de retards
                    </BTooltip>
                    <BButton
                        variant="link"
                        size="sm"
                        @click="filterStudent"
                    >
                        <IBiFunnel />
                    </BButton>
                </BCol>
                <BCol
                    sm="12"
                    md="5"
                    lg="4"
                >
                    <div class="d-flex justify-content-between">
                        <BFormCheckbox
                            v-model="justified"
                            switch
                            class="me-2"
                            @update:model-value="updateJustified"
                        >
                            {{ lateness.justified ? "Justifié" : "Injustifié" }}
                        </BFormCheckbox>
                        <BFormCheckbox
                            v-if="store.settings.enable_missing_card"
                            v-model="missingCard"
                            class="me-2 ms-2"
                            @update:model-value="updateMissingCard"
                            :value="false"
                            :unchecked-value="true"
                        >
                            <IBiPersonVcardFill
                                :id="`missing-${lateness.id}`"
                                class="align-middle"
                                v-if="missingCard"
                                color="red"
                                v-b-tooltip="'Carte étudiante manquante'"
                            />
                            <IBiPersonVcard
                                v-else
                                color="green"
                            />
                        </BFormCheckbox>
                        <BButton
                            :to="`/warning/${lateness.student.matricule}/`"
                            variant="light"
                            class="card-link ms-3"
                        >
                            <IBiCard-text variant="secondary" />
                        </BButton>
                        <BButton
                            variant="light"
                            size="sm"
                            @click="$emit('delete')"
                            class="card-link ms-2"
                        >
                            <IBiTrashFill
                                variant="danger"
                            />
                        </BButton>
                    </div>
                </BCol>
            </BRow>
            <BRow v-if="sanction">
                <BCol>
                    Date de la sanction : {{ sanction.date_sanction }}
                    <span v-if="!sanction.to_be_done">
                        <IBiCheck
                            v-if="sanction.sanction_faite"
                            variant="success"
                            :id="`sanction-done-${lateness.id}`"
                        />
                        <IBiX
                            v-else
                            variant="danger"
                            :id="`sanction-not-done-${lateness.id}`"
                        />
                        <BTooltip :target="`sanction-done-${lateness.id}`">
                            Sanction faite
                        </BTooltip>
                        <BTooltip :target="`sanction-not-done-${lateness.id}`">
                            Sanction non-faite
                        </BTooltip>
                    </span>
                </BCol>
            </BRow>
        </BCard>
    </div>
</template>

<script>
import axios from "axios";
import { DateTime } from "luxon";

import { latenessStore } from "./stores/index.js";
import { displayStudent } from "@s:core/js/common/utilities.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    emits: ["delete", "filterStudent", "update"],
    props: {
        lateness: {
            type: Object,
            default: () => {},
        },
    },
    data: function () {
        return {
            justified: false,
            missingCard: false,
            showPhoto: false,
            sanction: null,
            store: latenessStore(),
        };
    },
    computed: {
        niceDate: function () {
            return DateTime.fromISO(this.lateness.datetime_creation).toFormat("HH:mm dd/MM");
        },
    },
    methods: {
        displayStudent,
        displayPhoto: function () {
            this.showPhoto = true;
            setTimeout(() => {
                this.showPhoto = false;
            }, 5000);
        },
        updateJustified: function (event) {
            const data = { justified: event };
            if (event && this.lateness.has_sanction) {
                data.has_sanction = false;
                this.sanction = null;
            }
            axios.put(`/lateness/api/lateness/${this.lateness.id}/`, data, token)
                .then((resp) => {
                    this.justified = resp.data.justified;
                    this.$emit("update", resp.data);
                });
        },
        updateMissingCard: function (event) {
            axios.put(
                `/lateness/api/lateness/${this.lateness.id}/`,
                { missing_card: this.missingCard },
                token,
            ).then((resp) => {
                this.missingCard = resp.data.missing_card;
                this.$emit("update", resp.data);
            });
        },
        filterStudent: function () {
            this.$emit("filterStudent", this.lateness.student_id);
        },
    },
    mounted: function () {
        this.justified = this.lateness.justified;
        this.missingCard = this.lateness.missing_card;

        if (!this.lateness.sanction_id) return;

        axios.get("/dossier_eleve/api/cas_eleve/" + this.lateness.sanction_id + "/")
            .then((resp) => {
                this.sanction = {
                    date_sanction: DateTime.fromISO(resp.data.date_sanction).toFormat("dd/MM/yy"),
                    sanction_faite: true,
                    to_be_done: false,
                };
            },
            )
            .catch(() => {
                axios.get("/dossier_eleve/api/ask_sanctions/" + this.lateness.sanction_id + "/")
                    .then((resp) => {
                        this.sanction = {
                            date_sanction: DateTime.fromISO(resp.data.date_sanction).toFormat("dd/MM/yy"),
                            sanction_faite: false,
                            to_be_done: DateTime.fromISO(resp.data.date_sanction) > DateTime.now(),
                        };
                    });
            });
    },
};
</script>
