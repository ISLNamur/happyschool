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
    <b-list-group-item>
        <icon
            v-if="loading"
            name="spinner"
            scale="1"
            :pulse="loading"
        />
        <b-btn
            v-else
            @click="deleteEntry"
            size="sm"
            variant="danger"
        >
            Enlever
        </b-btn>
        <span v-if="file">{{ file.name }}</span>
        <span v-else>
            Voir <a
                target="_blank"
                rel="noopener noreferrer"
                :href="link"
            >{{ filename.substring(removestr, 40) }}</a>
        </span>
    </b-list-group-item>
</template>

<script>
import axios from "axios";
import Icon from "vue-awesome/components/Icon.vue";

export default {
    props: {
        "id": {
            type: Number,
            default: -1,
        },
        "file": {
            type: File,
            default: null,
        },
        "path": {
            type: String,
            default: ""
        },
        "removestr": {
            type: String,
            default: "",
        },
        /** If true, replace /media from the path with another string. */
        removeMedia: {
            type: Boolean,
            default: false,
        }
    },
    data: function () {
        return {
            loading: true,
            link: "",
            filename: "",
        };
    },
    methods: {
        deleteEntry: function() {
            axios.delete(this.path + this.id,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                }
            ).then(() => {
                this.$emit("delete");
            });
        },
    },
    mounted: function() {
        if (this.id < 0) {
            var data = new FormData();
            data.append("file", this.file);
            axios.put(this.path, data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: {"Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\""},
                })
                .then(response => {
                    this.link = response.data.attachment;
                    this.$emit("setdata", response.data);
                    this.loading = false;
                })
                .catch(function (error) {
                    alert("Une erreur est survenue lors de l'ajout du fichier, merci de réessayer.\n" + error);
                    this.$emit("delete");
                });
        } else {
            axios.get(this.path + this.id + "/")
                .then(response => {
                    this.link = response.data.attachment;
                    if (this.removeMedia && this.link.startsWith("/media")) {
                        this.link = this.link.slice(6, this.link.length);
                    }
                    this.filename = this.link.split("/")[this.link.split("/").length - 1];
                    this.loading = false;
                });
        }
    },
    components: {Icon},
};
</script>

<style>
</style>
