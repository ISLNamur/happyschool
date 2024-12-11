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
    <BListGroupItem :variant="modelValue === null ? 'info' : ''">
        <div class="d-flex w-100 justify-content-between">
            <span :class="modelValue ? 'text-success' : ''">
                <IBiCheck v-if="modelValue" />
                <IBiX v-if="modelValue == false" />
                {{ !modelValue && modelValue !== null ? resourceDifficulty.difficulty : resourceDifficulty.resource }}
            </span>
            <BButtonGroup>
                <BButton
                    v-if="editMode && !modelValue"
                    variant="success"
                    @click="$emit('update:modelValue', true)"
                    size="sm"
                >
                    <IBiCheck />
                    Acquis
                </BButton>
                <BButton
                    v-if="editMode && (modelValue === true || modelValue === null)"
                    variant="danger"
                    @click="$emit('update:modelValue', false)"
                    size="sm"
                >
                    <IBiX />
                    Non acquis
                </BButton>
                <BButton
                    v-if="editMode && modelValue !== null"
                    variant="outline-info"
                    @click="$emit('update:modelValue', null)"
                    size="sm"
                >
                    <IBiArrowCounterclockwise />
                    Non considéré
                </BButton>
            </BButtonGroup>
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
        modelValue: {
            type: Boolean,
            default: null,
        }
    },

};
</script>
