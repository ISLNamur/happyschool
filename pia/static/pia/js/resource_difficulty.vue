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
    <BListGroupItem :variant="value === null ? 'info' : ''">
        <div class="d-flex w-100 justify-content-between">
            <span :class="value ? 'text-success' : ''">
                <IBiCheck v-if="value" />
                <IBiX v-if="value == false" />
                {{ !value && value !== null ? resourceDifficulty.difficulty : resourceDifficulty.resource }}
            </span>
            <span>
                <BButton
                    v-if="editMode && !value"
                    variant="success"
                    @click="$emit('input', true)"
                    size="sm"
                >
                    <IBiCheck />
                    Acquis
                </BButton>
                <BButton
                    v-if="editMode && (value === true || value === null)"
                    variant="danger"
                    @click="$emit('input', false)"
                    size="sm"
                >
                    <IBiX />
                    Non acquis
                </BButton>
                <BButton
                    v-if="editMode && value !== null"
                    variant="outline-info"
                    @click="$emit('input', null)"
                    size="sm"
                >
                    <IBiArrowCounterclockwise />
                    Non considéré
                </BButton>
            </span>
        </div>
    </BListGroupItem>
</template>

<script>
export default {
    props: {
        editMode: {
            type: Boolean,
            default: false,
        },
        resourceDifficulty: {
            type: Object,
            default: () => {}
        },
        value: {
            type: Boolean,
            default: null,
        }
    },

};
</script>
