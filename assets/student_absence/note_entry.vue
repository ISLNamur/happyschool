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
            <span slot="noResult">Aucune personne trouvée.</span>
            <span slot="noOptions"></span>
            >
            </multiselect>
            <b-form-group>
                <quill-editor v-model="currentNote" :options="editorOptions">
                </quill-editor>
            </b-form-group>
            <b-btn :disabled="disabledSubmit" @click="sendData()" >Envoyer</b-btn>
        </b-card>
    </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.min.css'

import axios from 'axios';

import {quillEditor} from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'

export default {
    data: function () {
        return {
            classe: null,
            classeOptions: [],
            classeLoading: false,
            searchId: 0,
            noteId: -1,
            currentNote: "",
            datetime_update: null,
            sending: false,
            editorOptions: {
                modules: {
                    toolbar: [
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote'],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'indent': '-1'}, { 'indent': '+1' }],
                        [{ 'align': [] }],
                        ['clean']
                    ]
                },
                placeholder: ""
            },
        }
    },
    computed: {
        disabledSubmit: function () {
            return this.classe == null || this.sending;
        }
    },
    methods: {
        getNote(option) {
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            axios.get("/student_absence/api/classenote/?classe=" + option.id, token)
            .then(resp => {
                if (resp.data.results.length > 0) {
                    this.noteId = resp.data.results[0].id;
                    this.currentNote = resp.data.results[0].note;
                    this.datetime_update = resp.data.results[0].datetime_update;
                }

            }) 
            .catch(err => {
                alert(err);
            })

        },
        getClasseOptions(query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                check_access: false,
            };
            axios.post('/annuaire/api/classes/', data, token)
            .then(resp => {
                if (this.searchId !== currentSearch)
                    return;
                this.classeOptions = resp.data;
            })
        },
        sendData() {
            this.sending = true;
            const isNew = this.noteId < 0;
            let send = isNew ? axios.post : axios.put;
            let url = "/student_absence/api/classenote/";
            if (!isNew) url += this.noteId + "/";
            const data = {
                note: this.currentNote,
                classe: this.classe.id,
            }
            const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
            send(url, data, token)
            .then(resp => {
                this.noteId = resp.data.id;
                this.$store.commit('addNote', data);
                this.sending = false;
            })
            .catch(err => {
                alert(err);
                this.sending = false;
            })
        }
    },
    components: {Multiselect, quillEditor},
}
</script>