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
        <b-row>
            <b-col>
                <h2>Exporter les données enregistrées</h2>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group label="À partir du">
                    <input
                        type="date"
                        v-model="date_from"
                        :max="date_to"
                    >
                </b-form-group>
            </b-col>
            <b-col>
                <b-form-group label="Jusqu'au">
                    <input
                        type="date"
                        v-model="date_to"
                        :min="date_from"
                    >
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form-group label="Type de document">
                    <b-form-radio
                        v-model="document"
                        value="pdf"
                    >
                        PDF
                    </b-form-radio>
                    <b-form-radio
                        v-model="document"
                        value="csv"
                    >
                        CSV (compatible MS Excel)
                    </b-form-radio>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-btn
                    :disabled="!date_from || !date_to"
                    variant="primary"
                    :href="`/student_absence_teacher/export/${document}/${date_from}/${date_to}/`"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <b-icon icon="download" />
                    Télécharger
                </b-btn>
            </b-col>
        </b-row>
    </div>
</template>

<script>
export default {
    data: function () {
        return {
            date_from: null,
            date_to: null,
            document: "pdf"
        };
    }
};
</script>
