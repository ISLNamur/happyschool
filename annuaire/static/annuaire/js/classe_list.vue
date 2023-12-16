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
                class="mb-2"
            >
                Téléchargements :
                <b-button
                    target="_blank"
                    rel="noopener noreferrer"
                    :href="getClassePhoto"
                >
                    Photos de classe
                </b-button>
                <span v-if="store.settings.show_credentials">
                    <b-button
                        target="_blank"
                        rel="noopener noreferrer"
                        :href="getClasseListExcel"
                    >
                        Liste des étudiants avec identifiants (excel)
                    </b-button>
                    <b-button
                        target="_blank"
                        rel="noopener noreferrer"
                        :href="getClasseListPDF"
                    >
                        Liste des étudiants avec identifiants (PDF)
                    </b-button>
                </span>
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
