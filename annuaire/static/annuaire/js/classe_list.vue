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
    <b-row>
        <b-col>
            <div
                v-if="students.length > 0"
                class="mb-2 text-right"
            >
                <b-button-group>
                    <b-button
                        variant="outline-primary"
                        target="_blank"
                        rel="noopener noreferrer"
                        :href="getClassePhoto"
                    >
                        <b-icon icon="image" />
                        Photos
                    </b-button>
                    <b-button
                        variant="outline-secondary"
                        v-b-modal.summaryclass
                    >
                        <b-icon icon="file-pdf" />
                        Récapitulatifs
                    </b-button>
                    <b-dropdown
                        v-if="store.settings.show_credentials"
                        text="Liste identifiants"
                        variant="outline-secondary"
                    >
                        <b-dropdown-item
                            target="_blank"
                            rel="noopener noreferrer"
                            :href="getClasseListExcel"
                        >
                            Fichier Excel
                        </b-dropdown-item>
                        <b-dropdown-item
                            target="_blank"
                            rel="noopener noreferrer"
                            :href="getClasseListPDF"
                        >
                            Fichier PDF
                        </b-dropdown-item>
                    </b-dropdown>
                </b-button-group>
            </div>
            <p v-else>
                Il n'y a pas d'élèves dans cette classe.
            </p>
            <b-list-group class="text-center">
                <b-list-group-item
                    v-for="s in students"
                    :key="s.matricule"
                    button
                    @click="selectStudent(s.matricule)"
                >
                    {{ s.display }}
                </b-list-group-item>
            </b-list-group>
        </b-col>
        <b-modal
            id="summaryclass"
            ok-only
        >
            <b-row>
                <b-col>
                    <b-form-group label="À partir de ">
                        <b-input
                            type="date"
                            v-model="date_from"
                        />
                    </b-form-group>
                    <b-form-group label="Jusqu'à ">
                        <b-input
                            type="date"
                            v-model="date_to"
                        />
                    </b-form-group>
                </b-col>
            </b-row>
            <b-row>
                <b-col class="text-center">
                    <b-btn
                        :href="`/annuaire/summary/class/${classe}/${date_from}/${date_to}/`"
                        target="_blank"
                        variant="primary"
                        :disabled="!date_from || !date_to"
                    >
                        <b-icon icon="file-pdf" />
                        Télécharger
                    </b-btn>
                </b-col>
            </b-row>
        </b-modal>
    </b-row>
</template>

<script>
import { annuaireStore } from "./stores/index.js";

import axios from "axios";


export default {
    props: {
        "classe": {
            type: String,
            default: ""
        }
    },
    data: function () {
        return {
            students: [],
            date_from: null,
            date_to: null,
            store: annuaireStore(),
        };
    },
    watch: {
        "$route" () {
            this.loadClasse();
        }
    },
    computed: {
        getClassePhoto: function () {
            if (!this.classe)
                return "";

            return "/annuaire/get_class_photo_pdf/" + this.classe + "/";
        },
        getClasseListExcel: function () {
            if (!this.classe)
                return "";

            return "/annuaire/get_class_list_excel/" + this.classe + "/";
        },
        getClasseListPDF: function () {
            if (!this.classe)
                return "";

            return "/annuaire/get_class_list_pdf/" + this.classe + "/";
        },
        // canSeeSummary: function () {
        //     const canSeeGroups = new Set(this.store.settings.can_see_summary);
        //     // eslint-disable-next-line no-undef
        //     const userGroups = new Set(user_groups.map(g => g.id));
        //     return canSeeGroups.intersection(userGroups).size > 0;
        // }
    },
    methods: {
        selectStudent: function (matricule) {
            this.$router.push(`/person/student/${matricule}/`);
        },
        loadClasse: function () {
            const data = {params: {classe: this.classe}};
            axios.get("/annuaire/api/studentclasse/", data)
                .then(response => {
                    this.students = response.data;
                });
        }
    },
    mounted: function () {
        this.loadClasse();
    }
};

</script>
