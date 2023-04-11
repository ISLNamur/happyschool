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
        <b-card>
            <multiselect
                :internal-search="false"
                :options="classeOptions"
                @search-change="getClasseOptions"
                @select="getNote"
                :loading="classeLoading"
                placeholder="Rechercher une classe…"
                select-label=""
                selected-label="Sélectionné"
                deselect-label=""
                label="display"
                track-by="id"
                v-model="classe"
            >
                <template #noResult>
                    Aucune personne trouvée.
                </template>
                <template #noOptions />
                >
            </multiselect>
            <b-form-group>
                <quill-editor
                    v-model="currentNote"
                    :options="editorOptions"
                />
            </b-form-group>
            <b-btn
                :disabled="disabledSubmit"
                @click="sendData()"
            >
                Envoyer
            </b-btn>
        </b-card>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import axios from "axios";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

export default {
    data: function () {
        return {
            /**
             * The classe of the note.
             */
            classe: null,
            /**
             * The available options for class selection.
             */
            classeOptions: [],
            /**
             * State if it is searching for classes.
             */
            classeLoading: false,
            searchId: 0,
            /**
             * The current `id` of the note, -1 is for new notes.
             */
            noteId: -1,
            /**
             * Current text in the note.
             */
            currentNote: "",
            /**
             * Last update of the note.
             */
            datetime_update: null,
            /**
             * State if the is currently submitted.
             */
            sending: false,
            /**
             * Options for the rich text editor.
             */
            editorOptions: {
                modules: {
                    toolbar: [
                        ["bold", "italic", "underline", "strike"],
                        ["blockquote"],
                        [{ "list": "ordered"}, { "list": "bullet" }],
                        [{ "indent": "-1"}, { "indent": "+1" }],
                        [{ "align": [] }],
                        ["clean"]
                    ]
                },
                placeholder: ""
            },
        };
    },
    computed: {
        /**
         * State if the submit button should be disabled.
         */
        disabledSubmit: function () {
            return this.classe == null || this.sending;
        }
    },
    methods: {
        /**
         * Load a note from the server.
         */
        getNote: function (option) {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.get("/student_absence/api/classenote/?classe=" + option.id, token)
                .then(resp => {
                    if (resp.data.results.length > 0) {
                        this.noteId = resp.data.results[0].id;
                        this.currentNote = resp.data.results[0].note;
                        this.datetime_update = resp.data.results[0].datetime_update;
                    } else {
                        this.noteId = -1;
                        this.currentNote = "";
                        this.datetime_update = null;
                    }
                }) 
                .catch(err => {
                    alert(err);
                });

        },
        /**
         * Look for classes from user query.
         */
        getClasseOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                check_access: false,
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(resp => {
                    if (this.searchId !== currentSearch)
                        return;
                    this.classeOptions = resp.data;
                });
        },
        /**
         * Submit the note to the server.
         */
        sendData: function () {
            this.sending = true;
            const isNew = this.noteId < 0;
            let send = isNew ? axios.post : axios.put;
            let url = "/student_absence/api/classenote/";
            if (!isNew) url += this.noteId + "/";
            const data = {
                note: this.currentNote,
                classe: this.classe.id,
            };
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            send(url, data, token)
                .then(resp => {
                    this.noteId = resp.data.id;
                    this.$store.commit("addNote", data);
                    this.sending = false;
                    this.$bvToast.toast(`La note concernant la classe ${this.classe.display} a été enregistrée.`, {
                        variant: "success",
                        noCloseButton: true,
                    });
                })
                .catch(err => {
                    alert(err);
                    this.sending = false;
                });
        }
    },
    components: {Multiselect, quillEditor},
};
</script>
