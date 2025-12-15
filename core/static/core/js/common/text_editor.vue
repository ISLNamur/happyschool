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
        <ckeditor
            :config="editorOptions"
            :editor="editor"
            :model-value="modelValue"
            @update:model-value="$emit('update:modelValue', $event)"
        />
    </div>
</template>

<script>
import { Ckeditor } from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

export default {
    props: {
        modelValue: {
            type: String,
            default: "",
            required: true,
        },
        placeholder: {
            type: String,
            default: "Ajouter un texte.",
        },
        advanced: {
            type: Boolean,
            default: false,
        },
        divBlock: {
            type: Boolean,
            default: false,
        },
    },
    emits: ["update:modelValue"],
    data: function () {
        return {
            editor: ClassicEditor,
        };
    },
    computed: {
        editorOptions: function () {
            if (this.advanced) {
                return {
                    toolbar: [
                        "undo", "redo",
                        "|",
                        "heading",
                        "|",
                        "bold", "italic", "blockQuote", "link",
                        "|",
                        "bulletedList", "numberedList",
                        "|",
                        "outdent", "indent",
                    ],
                    placeholder: this.placeholder,
                    licenseKey: "GPL",
                };
            } else {
                return {
                    toolbar: [
                        "undo", "redo",
                        "|",
                        "bold", "italic", "blockQuote",
                        "|",
                        "bulletedList", "numberedList",
                    ],
                    placeholder: this.placeholder,
                    licenseKey: "GPL",
                };
            }
        },
    },
    mounted: function () {
        if (this.divBlock) {
            // const Block = Quill.import("blots/block");
            // Block.tagName = "DIV";
            // Quill.register(Block, true);
        }
    },
    components: {
        ckeditor: Ckeditor,
    },
};
</script>

<style></style>
