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
        <transition
            appear
            name="fade"
        >
            <BCard
                :class="'px-4 mt-2 ' + statusClass"
                no-body
            >
                <BRow>
                    <BCol>
                        <h5>{{ date }} – {{ rowData.name }}</h5>
                    </BCol>
                    <BCol sm="2">
                        <div class="text-end">
                            <BButton
                                variant="light"
                                size="sm"
                                :to="'/edit/' + rowData.id + '/'"
                                class="card-link"
                            >
                                <IBiPencilSquare
                                    color="green"
                                />
                            </BButton>
                            <BButton
                                variant="light"
                                size="sm"
                                @click="deleteEntry"
                                class="card-link"
                            >
                                <IBiTrashFill
                                    color="red"
                                />
                            </BButton>
                        </div>
                    </BCol>
                </BRow>
                <BRow class="text-center">
                    <BCol md="2">
                        <strong>Statut :</strong> {{ rowData.status }}
                    </BCol>
                    <BCol md="3">
                        <strong>Motif :</strong> {{ rowData.motif }}
                    </BCol>
                    <BCol>{{ rowData.comment }}</BCol>
                </BRow>
            </BCard>
        </transition>
    </div>
</template>

<script>
import { DateTime } from "luxon";

export default {
    emits: ["edit", "delete"],
    props: {
        rowData: {
            type: Object,
            default: () => {},
        },
    },
    data: function () {
        return {
        };
    },
    computed: {
        date: function () {
            const dateStart = DateTime.fromISO(this.rowData.date_absence_start).toLocaleString();
            if (this.rowData.date_absence_start == this.rowData.date_absence_end)
                return dateStart;

            const dateEnd = DateTime.fromISO(this.rowData.date_absence_end).toLocaleString();
            return `${dateStart} → ${dateEnd}`;
        },
        statusClass: function () {
            if (this.rowData.status == "A venir") return "avenir";
            if (this.rowData.status == "En cours") return "encours";
            if (this.rowData.status == "Clôturé") return "cloture";
            return "";
        },
    },
    methods: {
        editEntry: function () {
            this.$emit("edit");
        },
        deleteEntry: function () {
            this.$emit("delete");
        },
    },
};
</script>

<style>
.avenir {
    background-color: lightgreen;
}
.encours {
    background-color: lightyellow;
}
.cloture {
    background-color: lightpink;
}
</style>
