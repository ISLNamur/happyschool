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
    <BListGroupItem class="d-flex align-items-center mt-2">
        <span>
            <BSpinner
                v-if="loading"
                small
            />
            <BButton
                v-else
                @click="deleteEntry"
                size="sm"
                variant="danger"
                class="me-2"
            >
                Enlever
            </BButton>
            <span v-if="file">{{ file.name }}</span>
            <span v-else>
                Voir <a
                    target="_blank"
                    rel="noopener noreferrer"
                    :href="link"
                >{{ filename.substring(removestr, 40) }}</a>
            </span>
        </span>
        <BFormGroup
            v-if="groupAccess"
            label="Visible par :"
            label-cols-sm="5"
            label-align="end"
            class="flex-grow-1 ms-2"
        >
            <BFormSelect
                multiple
                :select-size="3"
                v-model="selectedGroups"
                :options="groupOptions"
                value-field="id"
                @update:model-value="updateGroup"
            />
        </BFormGroup>
    </BListGroupItem>
</template>

<script>
import axios from "axios";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    emits: ["setdata", "delete", "unavailable"],
    props: {
        id: {
            type: Number,
            default: -1,
        },
        file: {
            type: File,
            default: null,
        },
        path: {
            type: String,
            default: "",
        },
        removestr: {
            type: String,
            default: "",
        },
        groupAccess: {
            type: Boolean,
            default: false,
        },
        /** If true, replace /media from the path with another string. */
        removeMedia: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            loading: true,
            link: "",
            filename: "",
            groupOptions: [],
            selectedGroups: [],
        };
    },
    methods: {
        deleteEntry: function () {
            axios.delete(`${this.path}${this.id}/`,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                },
            ).then(() => {
                this.$emit("delete");
            });
        },
        updateGroup: function () {
            let data = new FormData();
            data.append("visible_by", this.selectedGroups);
            axios.patch(`${this.path}${this.id}/`, data, token);
        },
    },
    mounted: function () {
        if (this.id < 0) {
            var data = new FormData();
            data.append("file", this.file);
            // eslint-disable-next-line no-undef
            data.append("visible_by", user_groups.map(uG => uG.id));
            axios.put(this.path, data,
                {
                    xsrfCookieName: "csrftoken",
                    xsrfHeaderName: "X-CSRFToken",
                    headers: { "Content-Disposition": "form-data; name=\"file\"; filename=\"" + this.file.name.normalize() + "\"" },
                })
                .then((response) => {
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
                .then((response) => {
                    this.link = response.data.attachment;
                    if (this.removeMedia && this.link.startsWith("/media")) {
                        this.link = this.link.slice(6, this.link.length);
                    }
                    this.filename = this.link.split("/")[this.link.split("/").length - 1];

                    if (this.groupAccess) {
                        this.selectedGroups = response.data.visible_by;
                    }
                    this.loading = false;
                })
                .catch(() => {
                    this.$emit("unavailable");
                });
        }

        if (this.groupAccess && typeof groups !== "undefined") {
            // eslint-disable-next-line no-undef
            this.groupOptions = Object.values(groups);
            if (this.id < 0) {
                // Default group is user groups.
                // eslint-disable-next-line no-undef
                this.selectedGroups = user_groups.map(uG => uG.id);
            }
        }
    },
};
</script>

<style>
</style>
