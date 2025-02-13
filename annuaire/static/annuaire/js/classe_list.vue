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
    <BRow align-h="end">
        <BCol>
            <div
                v-if="students.length > 0"
                class="mb-2 text-end"
            >
                <BButtonGroup>
                    <BButton
                        variant="outline-primary"
                        target="_blank"
                        rel="noopener noreferrer"
                        :href="getClassePhoto"
                    >
                        <IBiImage />
                        Photos
                    </BButton>
                    <BButton
                        v-if="canSeeSummary"
                        variant="outline-secondary"
                        @click="summaryClassModal = !summaryClassModal"
                    >
                        <IBiFilePdf />
                        Récapitulatifs
                    </BButton>
                    <BDropdown
                        v-if="store.settings.show_credentials"
                        text="Liste identifiants"
                        variant="outline-secondary"
                    >
                        <BDropdownItem
                            target="_blank"
                            rel="noopener noreferrer"
                            :href="getClasseListExcel"
                        >
                            Fichier Excel
                        </BDropdownItem>
                        <BDropdownItem
                            target="_blank"
                            rel="noopener noreferrer"
                            :href="getClasseListPDF"
                        >
                            Fichier PDF
                        </BDropdownItem>
                    </BDropdown>
                </BButtonGroup>
            </div>
            <p v-else>
                Il n'y a pas d'élèves dans cette classe.
            </p>
            <BListGroup class="text-center">
                <BListGroupItem
                    v-for="s in students"
                    :key="s.matricule"
                    button
                    @click="selectStudent(s.matricule)"
                >
                    {{ s.display }}
                </BListGroupItem>
            </BListGroup>
        </BCol>
        <BModal
            id="summaryclass"
            v-model="summaryClassModal"
            ok-only
        >
            <BRow>
                <BCol>
                    <BFormGroup label="À partir de ">
                        <BFormInput
                            type="date"
                            v-model="date_from"
                        />
                    </BFormGroup>
                    <BFormGroup label="Jusqu'à ">
                        <BFormInput
                            type="date"
                            v-model="date_to"
                        />
                    </BFormGroup>
                </BCol>
            </BRow>
            <BRow>
                <BCol class="text-center">
                    <BButton
                        :href="`/annuaire/summary/class/${classe}/${date_from}/${date_to}/`"
                        target="_blank"
                        variant="primary"
                        :disabled="!date_from || !date_to"
                    >
                        <IBiFilePdf />
                        Télécharger
                    </BButton>
                </BCol>
            </BRow>
        </BModal>
    </BRow>
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
            summaryClassModal: false,
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

            return `/annuaire/get_class_photo_pdf/?classe_id=${this.classe}`;
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
        canSeeSummary: function () {
            const canSeeGroups = new Set(this.store.settings.can_see_summary);
            // eslint-disable-next-line no-undef
            const userGroups = new Set(user_groups.map(g => g.id));
            return canSeeGroups.intersection(userGroups).size > 0;
        }
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
