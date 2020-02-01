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
    <!-- eslint-disable vue/no-unused-vars -->
    <div>
        <h4>Importer des étudiants</h4>
        <b-row>
            <h5>Format des champs</h5>
            <ul>
                <li>
                    <strong>Année : </strong> L'année d'étude doit être un chiffre, seuls les deux premiers caractères sont considérés.
                    Par exemple, 2C ou P2 seront considérés comme la deuxième année.
                </li>
                <li>
                    <strong>Classe : </strong> La classe peut être un ou plusieurs caractères. La classe sera automatiquement mis en minuscule dans la base de donnée,
                    mais sera affichée en majustcule dans HappySchool.
                </li>
                <li><strong>Date de naissance :</strong> La date de naissance doit être sous la forme yyyymmdd. Par exemple, 20020322 donnera le 22 mars 2002.</li>
            </ul>
            <b-alert
                show
                variant="warning"
            >
                Le fichier csv soumit doit contenir l'entièreté des étudiants de l'établissement. Ceux qui ne sont pas présent (identifié
                par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.
            </b-alert>
        </b-row>
        <b-row>
            <b-form>
                <b-form-row>
                    <!-- eslint-disable-next-line no-irregular-whitespace -->
                    <b-form-group label="Établissement où importer les étudiants :">
                        <b-select
                            v-model="teaching"
                            :options="teachingOptions"
                            value-field="id"
                            text-field="display_name"
                        />
                    </b-form-group>
                </b-form-row>
                <b-form-row>
                    <b-form-checkbox v-model="ignoreFirstLine">
                        Ignorer la première ligne
                    </b-form-checkbox>
                </b-form-row>
                <b-form-row>
                    <b-form-group description="Le fichier doit être encodé en UTF-8.">
                        <b-form-file
                            v-model="file"
                            accept=".csv"
                            @input="testFile"
                            placeholder="Importer un fichier csv..."
                        />
                    </b-form-group>
                </b-form-row>
            </b-form>
        </b-row>
        <b-row>
            <b-table
                :items="content"
                :fields="columnRawNames.slice(0, fields_number)"
            >
                <template
                    v-for="(c, i) in columnHeads.slice(0, fields_number)"
                    v-slot:[c]="data"
                    :keys="i"
                >
                    <b-select
                        v-model="columns[i]"
                        :options="column_names"
                        :key="i"
                    >
                        <template slot="first">
                            <option
                                :value="null"
                                disabled
                            >
                                Choississez le type de colonne
                            </option>
                        </template>
                    </b-select>
                </template>
            </b-table>
        </b-row>
        <div v-if="file">
            <b-row>
                <b-btn @click="importStudents">
                    Importer
                </b-btn>
            </b-row>
            <b-row class="mt-2">
                <b-col>
                    <b-card
                        bg-variant="dark"
                        text-variant="white"
                    >
                        <p class="card-text console">
                            {{ importState }}
                        </p>
                    </b-card>
                </b-col>
            </b-row>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);

import axios from "axios";

import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon.vue";

Vue.component("icon", Icon);

const column_names = [
    {value: "matricule", text: "Matricule"},
    {value: "last_name", text: "Nom"},
    {value: "first_name", text: "Prénom"},
    {value: "year", text: "Année"},
    {value: "classe_letter", text: "Classe"},
    {value: "gender", text: "Genre"},
    {value: "scholar_year", text: "Année scolaire"},
    {value: "previous_class", text: "Classe précédente"},
    {value: "orientation", text: "Orientation"},
    {value: "street", text: "Rue"},
    {value: "postal_code", text: "Code postal"},
    {value: "locality", text: "Ville"},
    {value: "birth_date", text: "Date de naissance"},
    {value: "student_phone", text: "Tél. étudiant"},
    {value: "student_mobile", text: "GSM étudiant"},
    {value: "student_email", text: "Courriel étudiant"},
    {value: "resp_last_name", text: "Nom responsable"},
    {value: "resp_first_name", text: "Prénom responsable"},
    {value: "resp_phone", text: "Tél. responsable"},
    {value: "resp_mobile", text: "GSM responsable"},
    {value: "resp_email", text: "Courriel responsable"},
    {value: "father_last_name", text: "Nom pére"},
    {value: "father_first_name", text: "Prénom pére"},
    {value: "father_job", text: "Job pére"},
    {value: "father_phone", text: "Tél. pére"},
    {value: "father_mobile", text: "GSM pére"},
    {value: "father_email", text: "Courriel pére"},
    {value: "mother_last_name", text: "Nom mère"},
    {value: "mother_first_name", text: "Prénom mère"},
    {value: "mother_job", text: "Job mère"},
    {value: "mother_phone", text: "Tél. mère"},
    {value: "mother_mobile", text: "GSM mère"},
    {value: "mother_email", text: "Courriel mère"},
    {value: "doctor", text: "Médecin"},
    {value: "doctor_phone", text: "Tél. médecin"},
    {value: "mutual", text: "Mutuelle"},
    {value: "mutual_number", text: "Numéro mutuelle"},
    {value: "medical_information", text: "Info médicale"},
    {value: "username", text: "Nom d'utilisateur"},
    {value: "password", text: "Mot de passe"}
];

export default {
    data: function () {
        return {
            ignoreFirstLine: false,
            teaching: null,
            teachingOptions: [],
            file: null,
            fields_number: 0,
            content: [],
            "columns": new Array(column_names.length),
            "column_names": column_names,
            columnRawNames: column_names.map((o, i) => i.toString()),
            columnHeads: column_names.map((o, i) => "head(" + i + ")"),
            progressSocket: null,
            importState: "",
        };
    },
    methods: {
        testFile: function () {
            if (this.progressSocket) {
                this.progressSocket.close();
                this.importState = "";
            }

            let data = new FormData();
            data.append("file", this.file);
            data.append("ignore_first_line", this.ignoreFirstLine);
            axios.post("/core/api/testfile/", data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\""},
                })
                .then(response => {
                    this.content = JSON.parse(response.data);
                    if (this.content.length > 0) {
                        this.fields_number = Object.keys(this.content[0]).length;
                    }
                })
                .catch(function (error) {
                    alert("Une erreur est survenue lors de l'analyse du fichier.\n" + error);
                });
        },
        importStudents: function () {
            let data = new FormData();
            let app = this;
            data.append("file", this.file);
            data.append("ignore_first_line", JSON.stringify(this.ignoreFirstLine));
            data.append("teaching", this.teaching);
            data.append("columns", JSON.stringify(this.columns.slice(0, this.fields_number)));
            axios.post("/core/api/import_students/", data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\""},
                })
                .then(response => {
                    app.importState = "Connecting to server…\n";
                    const protocol = window.location.protocol === "http:" ? "ws" : "wss";
                    app.progressSocket = new WebSocket(protocol + "://" + window.location.host + "/ws/core/import_student_state/" + JSON.parse(response.data) + "/");
                    app.progressSocket.onmessage = function (event) {
                        app.importState += JSON.parse(event.data)["status"] + "\n";
                    };
                });
        },
    },
    mounted: function () {
        axios.get("/core/api/teaching/")
            .then(response => {
                this.teachingOptions = response.data.results;
            })
            .catch(function (error) {
                alert(error);
            });
    },
    components: {
    }
};
</script>

<style>
.console {
    font-family:monospace;
    white-space: pre-wrap;
}
</style>
