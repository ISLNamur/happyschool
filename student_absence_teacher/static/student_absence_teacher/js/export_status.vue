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
        <BRow>
            <BCol>
                <h2>Exporter les données enregistrées</h2>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup label="À partir du">
                    <input
                        type="date"
                        v-model="date_from"
                        :max="date_to"
                    >
                </BFormGroup>
            </BCol>
            <BCol>
                <BFormGroup label="Jusqu'au">
                    <input
                        type="date"
                        v-model="date_to"
                        :min="date_from"
                    >
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BFormGroup label="Type de document">
                    <BFormRadio
                        v-model="document"
                        value="pdf"
                    >
                        PDF
                    </BFormRadio>
                    <BFormRadio
                        v-model="document"
                        value="csv"
                    >
                        CSV (compatible MS Excel)
                    </BFormRadio>
                </BFormGroup>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BButton
                    :disabled="!date_from || !date_to"
                    variant="primary"
                    :href="`/student_absence_teacher/export/${document}/${date_from}/${date_to}/`"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <IBiDownload />
                    Télécharger
                </BButton>
            </BCol>
        </BRow>
    </div>
</template>

<script>
export default {
    data: function () {
        return {
            date_from: null,
            date_to: null,
            document: "pdf",
        };
    },
};
</script>
