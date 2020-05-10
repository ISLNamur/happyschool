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
            <b-form-row>
                <b-col>
                    <strong>
                        <b-form inline>
                            Date<b-form-input
                                type="date"
                                v-model="date_comment"
                                class="mr-sm-2 ml-2"
                                :state="inputStates.date_comment"
                            />
                            <b-form-invalid-feedback :state="inputStates.date_comment">
                                {{ errorMsg('date_student_project') }}{{ errorMsg('date_parents_opinion') }}
                            </b-form-invalid-feedback>
                        </b-form>
                    </strong>
                </b-col>
                <b-col
                    cols="1"
                    align-self="end"
                    class="text-right"
                >
                    <b-btn
                        @click="$emit('remove')"
                        variant="danger"
                        size="sm"
                        v-b-tooltip.hover
                        title="Supprimer"
                    >
                        <b-icon icon="trash" />
                    </b-btn>
                </b-col>
            </b-form-row>
            <b-form-row class="mt-2">
                <b-col>
                    <quill-editor
                        v-model="comment"
                        :options="editorOptions"
                    />
                </b-col>
            </b-form-row>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    props: {
        /** The data from an existing comment. */
        commentObject: {
            type: Object,
            default: () => {},
        },
        /**
         * The type of the comment (student_project or parents_opinion).
         * It will also use for api url construction.
         */
        commentType: {
            type: String,
            default: ""
        }
    },
    data: function () {
        return {
            /** Date of the comment. */
            date_comment: null,
            /** The comment. */
            comment: "",
            /** States of the input. */
            inputStates: {
                date_comment: null
            },
            /** Options for the text editor. */
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
            errors: {}
        };
    },
    watch: {
        errors: function (newErrors) {
            this.inputStates.date_comment = `date_${this.commentType}` in newErrors ? false : null;
        },
    },
    methods: {
        /** 
         * Assign text error if any.
         * 
         * @param {String} err Field name.
         */
        errorMsg(err) {
            if (err in this.errors) {
                return this.errors[err][0];
            } else {
                return "";
            }
        },
        /**
         * Submit the comment to the server.
         * 
         * Return a promise and handle any error.
         * 
         * @param {Strinrg} piaId The id of parent pia model.
         */
        submit: function (piaId) {
            // Reset errors.
            this.errors = {};

            const dateField = "date_" + this.commentType;
            const commentField = this.commentType;
            let data = {
                pia_model: piaId,
                [dateField]: this.date_comment,
                [commentField]: this.comment,
            };

            const isNew = this.commentObject.id < 0;
            const url =  !isNew ? `/pia/api/${this.commentType}/${this.commentObject.id}/` : `/pia/api/${this.commentType}/`;
            const putOrPost = !isNew ? axios.put : axios.post;
            return putOrPost(url, data, token)
                .catch(error => {
                    this.errors = error.response.data;
                    throw "Erreur lors de l'envoi des données.";
                });
        },
        /**
         * If the comment already exists load the data to the form.
         */
        assignComment: function () {
            if (this.commentObject.id >= 0) {
                const dateField = "date_" + this.commentType;
                this.date_comment = this.commentObject[dateField];
                this.comment = this.commentObject[this.commentType];
            }
        }
    },
    components: {
        quillEditor,
    },
    mounted: function () {
        this.assignComment();
    }
};
</script>
