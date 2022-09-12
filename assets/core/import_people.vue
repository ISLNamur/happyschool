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
        <b-tabs content-class="mt-3">
            <b-tab title="Étudiants">
                <b-row>
                    <b-col>
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
                            <li><strong>Date de naissance :</strong> La date de naissance peut être sous les formes suivantes yyyymmdd, yyyy-mm-dd ou encore dd/mm/yyyy. Par exemple, 20020322 donnera le 22 mars 2002.</li>
                            <li><strong>Cours :</strong> Seul le nom du cours court est nécessaire. Pour prendre entre compte plusieurs cours, il suffit que la ligne de l'étudiant soit répétée (seul le matricule est nécessaire).</li>
                        </ul>
                        <b-alert
                            show
                            variant="warning"
                        >
                            Le fichier csv soumit doit contenir l'entièreté des étudiants de l'établissement. Ceux qui ne sont pas présent (identifié
                            par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.
                        </b-alert>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
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
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-table
                            :items="content"
                            :fields="studentColumnRawNames.slice(0, fields_number)"
                        >
                            <template
                                v-for="(c, i) in studentColumnHeads.slice(0, fields_number)"
                                #[c]="data"
                            >
                                <b-select
                                    v-model="student_columns[i]"
                                    :options="student_column_names"
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
                    </b-col>
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
            </b-tab>
            <b-tab title="Enseignants">
                <b-row>
                    <b-col>
                        <h5>Format des champs</h5>
                        <ul>
                            <li>
                                <strong>Classe : </strong> Le premier caractères définit l'année de la classe tandis que le reste la ou les lettres de la classe.
                            </li>
                            <li><strong>Cours :</strong> Seul le nom du cours court est nécessaire. Pour prendre entre compte plusieurs cours, il suffit que la ligne de l'étudiant soit répétée (seul le matricule est nécessaire).</li>
                        </ul>
                        <b-alert
                            show
                            variant="warning"
                        >
                            Le fichier csv soumit doit contenir l'entièreté des enseignants de l'établissement. Ceux qui ne sont pas présent (identifié
                            par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.
                        </b-alert>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
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
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-table
                            :items="content"
                            :fields="teacherColumnRawNames.slice(0, fields_number)"
                        >
                            <template
                                v-for="(c, i) in teacherColumnHeads.slice(0, fields_number)"
                                #[c]="data"
                            >
                                <b-select
                                    v-model="teacher_columns[i]"
                                    :options="teacher_column_names"
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
                    </b-col>
                </b-row>
                <div v-if="file">
                    <b-row>
                        <b-btn @click="importTeachers">
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
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue, { BootstrapVueIcons } from "bootstrap-vue";
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import axios from "axios";


const student_column_names = [
    {value: "matricule", text: "Matricule"},
    {value: "last_name", text: "Nom"},
    {value: "first_name", text: "Prénom"},
    {value: "year", text: "Année"},
    {value: "classe_letter", text: "Classe"},
    {value: "course_name_short", text: "Cours (court)"},
    {value: "course_name_long", text: "Cours (long)"},
    {value: "group", text: "Groupe"},
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

const teacher_column_names = [
    {value: "matricule", text: "Matricule"},
    {value: "last_name", text: "Nom"},
    {value: "first_name", text: "Prénom"},
    {value: "email", text: "Courriel"},
    {value: "email_school", text: "Courriel de l'école"},
    {value: "tenure", text: "Titulariat"},
    {value: "classe", text: "Classe"},
    {value: "birth_date", text: "Date de naissance"},
    {value: "course_name_short", text: "Cours (court)"},
    {value: "course_name_long", text: "Cours (long)"},
    {value: "group", text: "Groupe"},
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
            "student_columns": new Array(student_column_names.length),
            "student_column_names": student_column_names,
            "teacher_columns": new Array(teacher_column_names.length),
            "teacher_column_names": teacher_column_names,
            studentColumnRawNames: student_column_names.map((o, i) => i.toString()),
            studentColumnHeads: student_column_names.map((o, i) => "head(" + i + ")"),
            teacherColumnRawNames: teacher_column_names.map((o, i) => i.toString()),
            teacherColumnHeads: teacher_column_names.map((o, i) => "head(" + i + ")"),
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
            data.append("columns", JSON.stringify(this.student_columns.slice(0, this.fields_number)));
            axios.post("/core/api/import_students/", data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\""},
                })
                .then(response => {
                    app.importState = "Connecting to server…\n";
                    const protocol = window.location.protocol === "http:" ? "ws" : "wss";
                    app.progressSocket = new WebSocket(`${protocol}://${window.location.host}/ws/core/import_state/student/${JSON.parse(response.data)}/`);
                    app.progressSocket.onmessage = function (event) {
                        app.importState += JSON.parse(event.data)["status"] + "\n";
                    };
                });
        },
        importTeachers: function () {
            let data = new FormData();
            let app = this;
            data.append("file", this.file);
            data.append("ignore_first_line", JSON.stringify(this.ignoreFirstLine));
            data.append("teaching", this.teaching);
            data.append("columns", JSON.stringify(this.teacher_columns.slice(0, this.fields_number)));
            axios.post("/core/api/import_teachers/", data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\""},
                })
                .then(response => {
                    app.importState = "Connecting to server…\n";
                    const protocol = window.location.protocol === "http:" ? "ws" : "wss";
                    app.progressSocket = new WebSocket(`${protocol}://${window.location.host}/ws/core/import_state/teacher/${JSON.parse(response.data)}/`);
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
