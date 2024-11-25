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
        <b-card @click="displayPhoto">
            <b-row>
                <b-col
                    cols="2"
                    v-if="showPhoto"
                >
                    <b-img
                        :src="`/static/photos/${lateness.student_id}.jpg`"
                        fluid
                        alt="Photo de l'élève"
                    />
                </b-col>
                <b-col>
                    <b-icon
                        v-if="lateness.sanction_id"
                        icon="exclamation-circle"
                    />
                    <strong>{{ niceDate }}</strong>:
                    <a :href="`/annuaire/#/person/student/${lateness.student.matricule}/`">
                        {{ lateness.student.display }}
                    </a>
                    <b-badge
                        v-if="!lateness.justified"
                        v-b-tooltip.hover
                        title="Nombre de retards"
                    >
                        {{ lateness.lateness_count }}
                    </b-badge>
                    <b-btn
                        variant="link"
                        size="sm"
                        @click="filterStudent"
                    >
                        <b-icon icon="funnel" />
                    </b-btn>
                </b-col>
                <b-col
                    sm="12"
                    md="4"
                    lg="3"
                >
                    <div class="text-right d-flex">
                        <b-form-checkbox
                            v-model="justified"
                            switch
                            class="pr-2"
                            @input="updateJustified"
                        >
                            {{ lateness.justified ? "Justifié" : "Injustifié" }}
                        </b-form-checkbox>
                        <b-btn
                            :to="`/warning/${lateness.student.matricule}/`"
                            variant="light"
                            class="card-link"
                        >
                            <b-icon
                                icon="card-text"
                                variant="secondary"
                            />
                        </b-btn>
                        <b-btn
                            variant="light"
                            size="sm"
                            @click="$emit('delete')"
                            class="card-link ml-2"
                        >
                            <b-icon
                                icon="trash-fill"
                                variant="danger"
                            />
                        </b-btn>
                    </div>
                </b-col>
            </b-row>
            <b-row v-if="sanction">
                <b-col>
                    Date de la sanction : {{ sanction.date_sanction }}
                    <span v-if="!sanction.to_be_done">
                        <b-icon
                            v-if="sanction.sanction_faite"
                            icon="check"
                            variant="success"
                            v-b-tooltip.hover
                            title="Sanction faite"
                        />
                        <b-icon
                            v-else
                            icon="x"
                            variant="danger"
                            v-b-tooltip.hover
                            title="Sanction non-faite"
                        />
                    </span>
                </b-col>
            </b-row>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        lateness: {
            type: Object,
            default: () => {}
        }
    },
    data: function () {
        return {
            justified: false,
            showPhoto: false,
            sanction: null,
        };
    },
    computed: {
        niceDate: function () {
            return Moment(this.lateness.datetime_creation).format("HH:mm DD/MM");
        }
    },
    methods: {
        displayPhoto: function () {
            this.showPhoto = true;
            setTimeout(() => {
                this.showPhoto = false;
            }, 5000);
        },
        updateJustified: function (event) {
            const data = {justified: event};
            if (event && this.lateness.has_sanction) {
                data.has_sanction = false;
                this.sanction = null;
            }
            axios.put(`/lateness/api/lateness/${this.lateness.id}/`, data, token)
                .then(resp => {
                    this.justified = resp.data.justified;
                    this.$emit("update", resp.data);
                });
        },
        filterStudent: function () {
            this.$emit("filterStudent", this.lateness.student_id);
        },
    },
    mounted: function () {
        this.justified = this.lateness.justified;

        if (!this.lateness.sanction_id) return;

        axios.get("/dossier_eleve/api/cas_eleve/" + this.lateness.sanction_id + "/")
            .then(resp => {
                this.sanction = {
                    date_sanction: Moment(resp.data.date_sanction).format("DD/MM/YY"),
                    sanction_faite: true,
                    to_be_done: false
                };
            }
            )
            .catch(() => {
                axios.get("/dossier_eleve/api/ask_sanctions/" + this.lateness.sanction_id + "/")
                    .then(resp => {
                        this.sanction = {
                            date_sanction: Moment(resp.data.date_sanction).format("DD/MM/YY"),
                            sanction_faite: false,
                            to_be_done: Moment(resp.data.date_sanction) > Moment()
                        };
                    });
            });
    }
};
</script>
