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
    <quill-editor
        :value="value"
        :options="editorOptions"
        @input="$emit('input', $event)"
    />
</template>

<script>
import {quillEditor} from "vue-quill-editor";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";

import Quill from "quill";

export default {
    props: {
        value: {
            type: String,
            default: ""
        },
        placeholder: {
            type: String,
            default: "Ajouter un texte.",
        },
        advanced: {
            type: Boolean,
            default: false
        },
        divBlock: {
            type: Boolean,
            default: false,
        }
    },
    computed: {
        editorOptions: function () {
            if (this.advanced) {
                return {
                    modules: {
                        toolbar: [
                            ["bold", "italic", "underline", "strike"],        // toggled buttons
                            ["blockquote"],
                            ["link", "image"],

                            [{ "header": 1 }, { "header": 2 }],               // custom button values
                            [{ "list": "ordered"}, { "list": "bullet" }],
                            [{ "script": "sub"}, { "script": "super" }],      // superscript/subscript
                            [{ "indent": "-1"}, { "indent": "+1" }],          // outdent/indent
                            [{ "direction": "rtl" }],                         // text direction

                            [{ "size": ["small", false, "large", "huge"] }],  // custom dropdown

                            [{ "color": [] }, { "background": [] }],          // dropdown with defaults from theme
                            [{ "font": [] }],
                            [{ "align": [] }],

                            ["clean"]
                        ]
                    },
                    placeholder: this.placeholder
                };
            } else {
                return {
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
                    placeholder: this.placeholder
                };
            }
        },
    },
    beforeMount: function () {
        if (this.divBlock) {
            var Block = Quill.import("blots/block");
            Block.tagName = "DIV";
            Quill.register(Block, true);
        }
    },
    components: {
        quillEditor
    }
};
</script>

<style>

</style>
