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
    <BRow>
        <BCol
            v-for="(a, index) in absences"
            :key="index"
        >
            <span v-if="a === null">-</span>
            <span v-else>
                <span :class="status(a.status) !== 'P' ? 'font-weight-bold' : ''">{{ status(a.status) }}</span>
                <IBiChatText
                    v-if="a.comment"
                    :id="`comment-${a.id}`"
                    v-b-tooltip.hover="a.comment"
                />
            </span>
        </BCol>
    </BRow>
</template>

<script>
export default {
    props: {
        absences: {
            type: Array,
            default: () => new Array()
        },
    },
    methods: {
        status: function (state) {
            const translation = {
                "presence": "P",
                "lateness": "R",
                "absence": "A",
                "exempted": "D",
                "excluded": "Exclus",
                "internship": "Stage",
            };
            return translation[state];
        },
    }
};
</script>

<style>
</style>
