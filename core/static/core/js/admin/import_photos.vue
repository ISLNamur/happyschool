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
        <h4>Importer des photos</h4>
        <BRow>
            <p>Les photos des étudiants doivent être sous la forme "numéro_de_matricule.jpg", par exemple 6143.<strong>jpg</strong>.</p>
        </BRow>
        <BRow>
            <BForm>
                <BFormRow>
                    <BFormGroup label="Type de personne">
                        <BFormSelect
                            v-model="people"
                            :options="peopleOptions"
                        />
                    </BFormGroup>
                </BFormRow>
                <BFormRow v-if="people">
                    <BFormGroup label="Photos">
                        <BFormFile
                            v-model="photos"
                            accept=".jpg"
                            placeholder="Choisir les photos..."
                            multiple
                            :file-name-formatter="formatNames"
                        />
                    </BFormGroup>
                </BFormRow>
                <BFormRow v-if="people && photos.length > 0">
                    <BFormGroup>
                        <BButton
                            @click="uploadPhotos"
                            :disabled="sending"
                        >
                            <BSpinner
                                small
                                label="Sending..."
                                v-if="sending"
                                variant="light"
                            />
                            {{ sendingButton }}
                        </BButton>
                    </BFormGroup>
                </BFormRow>
            </BForm>
        </BRow>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data: function () {
        return {
            people: null,
            peopleOptions: [
                { text: "Étudiants", value: "student" },
                { text: "Responsables (enseignants, éducateurs,…)", value: "responsible" }],
            photos: [],
            sending: false,
            currentPhoto: 0,
        };
    },
    computed: {
        sendingButton: function () {
            if (this.sending) {
                return `En cours d'envoi (${this.currentPhoto}/${this.photos.length})`;
            } else {
                return "Envoyer";
            }
        },
    },
    methods: {
        formatNames(files) {
            if (files.length === 1) {
                return files[0].name;
            } else {
                return `${files.length} photos sélectionnées`;
            }
        },
        uploadPhotos: function () {
            this.sending = true;
            this.uploadPhoto();
        },
        uploadPhoto: function () {
            let app = this;
            const header = {
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: { "Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.photos[this.currentPhoto].name.normalize() + "\"" },
            };
            let data = new FormData();
            data.append("file", this.photos[this.currentPhoto]);
            data.append("people", this.people);
            axios.post("/core/api/photo/", data, header)
                .then(() => {
                    this.currentPhoto += 1;
                    if (this.currentPhoto == this.photos.length) {
                        this.currentPhoto = 0;
                        this.sending = false;
                    } else {
                        this.uploadPhoto();
                    }
                })
                .catch(() => {
                // Try again.
                    data = new FormData();
                    data.append("file", app.photos[app.currentPhoto]);
                    data.append("people", app.people);
                    axios.post("/core/api/photo/", data, header)
                        .then(() => {
                            app.currentPhoto += 1;
                            if (app.currentPhoto == app.photos.length) {
                                app.currentPhoto = 0;
                                app.sending = false;
                            } else {
                                app.uploadPhoto();
                            }
                        })
                        .catch(() => {
                            alert("Unable to send photo: " + app.photos[app.currentPhoto].name);
                        });
                });
        },
    },
};
</script>
