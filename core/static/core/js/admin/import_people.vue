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
        <BTabs content-class="mt-3">
            <BTab title="Étudiants">
                <BRow>
                    <BCol>
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
                        <BAlert
                            show
                            variant="warning"
                        >
                            Le fichier csv soumit doit contenir l'entièreté des étudiants de l'établissement. Ceux qui ne sont pas présent (identifié
                            par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.
                        </BAlert>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BForm>
                            <BFormRow>
                                <!-- eslint-disable-next-line no-irregular-whitespace -->
                                <BFormGroup label="Établissement où importer les étudiants :">
                                    <BFormSelect
                                        v-model="teaching"
                                        :options="teachingOptions"
                                        value-field="id"
                                        text-field="display_name"
                                    />
                                </BFormGroup>
                            </BFormRow>
                            <BFormRow>
                                <BFormGroup>
                                    <BFormCheckbox v-model="ignoreFirstLine">
                                        Ignorer la première ligne
                                    </BFormCheckbox>
                                </BFormGroup>
                            </BFormRow>
                            <BFormRow>
                                <BFormGroup description="Le fichier doit être encodé en UTF-8.">
                                    <BFormFile
                                        v-model="file"
                                        accept=".csv"
                                        @update:model-value="testFile"
                                        placeholder="Importer un fichier csv..."
                                    />
                                </BFormGroup>
                            </BFormRow>
                        </BForm>
                    </BCol>
                </BRow>
                <BRow
                    v-if="file"
                    class="mt-3 mb-3"
                >
                    <BCol>
                        <BFormGroup label="Association des columns">
                            <BFormSelect
                                :options="fieldAssociationOptions"
                                value-field="id"
                                text-field="name"
                                v-model="fieldAssociation"
                                @update:model-value="setFieldAssociation"
                            />
                        </BFormGroup>
                    </BCol>
                    <BCol>
                        <BFormGroup label="Enregistrer l'association actuelle">
                            <BInputGroup>
                                <BFormInput v-model="newAssociationName" />
                                <BButton
                                    variant="outline-primary"
                                    @click="saveAssociation('ST')"
                                >
                                    <IBiSave />
                                    Enregistrer
                                </BButton>
                            </BInputGroup>
                        </BFormGroup>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BTableSimple
                            striped-columns
                            responsive
                        >
                            <BTbody>
                                <BTr
                                    v-for="(field, i) in testData"
                                    :key="i"
                                >
                                    <BTd
                                        sticky-column
                                        class="first-column"
                                    >
                                        <BFormSelect
                                            :options="student_column_names"
                                            v-model="fieldToColumn[i]"
                                        >
                                            <template #first>
                                                <BFormSelectOption
                                                    :value="undefined"
                                                />
                                            </template>
                                        </BFormSelect>
                                    </BTd>
                                    <BTd
                                        v-for="(test, j) in field"
                                        :key="j"
                                    >
                                        {{ test }}
                                    </BTd>
                                </BTr>
                            </BTbody>
                        </BTableSimple>
                    </BCol>
                </BRow>
                <div v-if="file">
                    <BRow>
                        <BButton @click="importStudents">
                            Importer
                        </BButton>
                    </BRow>
                    <BRow class="mt-2">
                        <BCol>
                            <BCard
                                bg-variant="dark"
                                text-variant="white"
                            >
                                <p class="card-text console">
                                    {{ importState }}
                                </p>
                            </BCard>
                        </BCol>
                    </BRow>
                </div>
            </BTab>
            <BTab title="Enseignants">
                <BRow>
                    <BCol>
                        <h5>Format des champs</h5>
                        <ul>
                            <li>
                                <strong>Classe : </strong> Le premier caractères définit l'année de la classe tandis que le reste la ou les lettres de la classe.
                            </li>
                            <li><strong>Cours :</strong> Seul le nom du cours court est nécessaire. Pour prendre entre compte plusieurs cours, il suffit que la ligne de l'étudiant soit répétée (seul le matricule est nécessaire).</li>
                        </ul>
                        <BAlert
                            show
                            variant="warning"
                        >
                            Le fichier csv soumit doit contenir l'entièreté des enseignants de l'établissement. Ceux qui ne sont pas présent (identifié
                            par le matricule) seront considérés comme inactifs (anciens) et pourront donc par la suite être réintégrés, par exemple dans un autre établissement.
                        </BAlert>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BForm>
                            <BFormRow>
                                <!-- eslint-disable-next-line no-irregular-whitespace -->
                                <BFormGroup label="Établissement où importer les étudiants :">
                                    <BFormSelect
                                        v-model="teaching"
                                        :options="teachingOptions"
                                        value-field="id"
                                        text-field="display_name"
                                    />
                                </BFormGroup>
                            </BFormRow>
                            <BFormRow>
                                <BFormCheckbox v-model="ignoreFirstLine">
                                    Ignorer la première ligne
                                </BFormCheckbox>
                            </BFormRow>
                            <BFormRow>
                                <BFormGroup description="Le fichier doit être encodé en UTF-8.">
                                    <BFormFile
                                        v-model="file"
                                        accept=".csv"
                                        @update:model-value="testFile"
                                        placeholder="Importer un fichier csv..."
                                    />
                                </BFormGroup>
                            </BFormRow>
                        </BForm>
                    </BCol>
                </BRow>
                <BRow>
                    <BCol>
                        <BTableSimple
                            striped-columns
                            responsive
                        >
                            <BTbody>
                                <BTr
                                    v-for="(field, i) in testData"
                                    :key="i"
                                >
                                    <BTd
                                        sticky-column
                                        class="first-column"
                                    >
                                        <BFormSelect
                                            :options="teacher_column_names"
                                            v-model="fieldToColumn[i]"
                                        >
                                            <template #first>
                                                <BFormSelectOption
                                                    :value="undefined"
                                                />
                                            </template>
                                        </BFormSelect>
                                    </BTd>
                                    <BTd
                                        v-for="(test, j) in field"
                                        :key="j"
                                    >
                                        {{ test }}
                                    </BTd>
                                </BTr>
                            </BTbody>
                        </BTableSimple>
                    </BCol>
                </BRow>
                <div v-if="file">
                    <BRow>
                        <BButton @click="importTeachers">
                            Importer
                        </BButton>
                    </BRow>
                    <BRow class="mt-2">
                        <BCol>
                            <BCard
                                bg-variant="dark"
                                text-variant="white"
                            >
                                <p class="card-text console">
                                    {{ importState }}
                                </p>
                            </BCard>
                        </BCol>
                    </BRow>
                </div>
            </BTab>
        </BTabs>
    </div>
</template>

<script>
import axios from "axios";

import { useToastController } from "bootstrap-vue-next";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

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
    setup: function () {
        const { show } = useToastController();
        return { show };
    },
    data: function () {
        return {
            ignoreFirstLine: false,
            teaching: null,
            teachingOptions: [],
            file: null,
            fields_number: 0,
            content: [],
            testData: [],
            fieldToColumn: [],
            student_column_names: student_column_names,
            teacher_column_names: teacher_column_names,
            progressSocket: null,
            importState: "",
            fieldAssociation: null,
            fieldAssociationOptions: [],
            newAssociationName: "",
        };
    },
    methods: {
        testFile: function (file) {
            if (this.progressSocket) {
                this.progressSocket.close();
                this.importState = "";
            }

            let data = new FormData();
            data.append("file", file);
            data.append("ignore_first_line", this.ignoreFirstLine);
            axios.post("/core/api/testfile/", data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + file.name.normalize() + "\""},
                })
                .then(response => {
                    this.content = response.data;
                    this.fieldToColumn = new Array(response.data[0].length);
                    this.testData = response.data[0].map((_, colIndex) => response.data.map(row => row[colIndex]));
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
            data.append(
                "columns",
                JSON.stringify(
                    Object.fromEntries(this.fieldToColumn.map((f, i) => [f, i]).filter(f => f[1] !== undefined))
                )
            );

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
            data.append(
                "columns",
                JSON.stringify(
                    Object.fromEntries(this.fieldToColumn.map((f, i) => [f, i]).filter(f => f[1] !== undefined))
                )
            );

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
        setFieldAssociation: function () {
            const fieldAssociation = this.fieldAssociationOptions.find(cTF => cTF.id === this.fieldAssociation);

            if (!fieldAssociation) {
                return;
            }

            this.fieldToColumn = fieldAssociation.column_to_field;
        },
        saveAssociation: function (modelType) {
            const data = {
                name: this.newAssociationName,
                model: modelType,
                column_to_field: this.fieldToColumn,
            };
            axios.post("/core/api/column_to_field_import/", data, token)
                .then((resp) => {
                    this.fieldAssociationOptions.push(resp.data);
                    this.show({
                        body: "L'association entre les colonnes et les champs a été sauvée.",
                        variant: "success"
                    });
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

        axios.get("/core/api/column_to_field_import/")
            .then((resp) => {
                this.fieldAssociationOptions = resp.data.results;
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

.first-column {
    min-width: 10rem;
}
</style>
