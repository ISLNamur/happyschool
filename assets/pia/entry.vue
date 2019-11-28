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
        <transition appear name="fade">
            <b-card class="px-4 mt-2" no-body>
                <b-row>
                    <b-col>
                        <h5>{{ rowData.student.display }}</h5>
                    </b-col>
                    <b-col sm="2">
                        <div class="text-right">
                            <b-btn variant="light" size="sm" :to="'/edit/' + rowData.id + '/'"
                            class="card-link"><icon scale="1.3" name="edit" color="green" class="align-text-bottom"></icon></b-btn>
                            <b-btn variant="light" size="sm" @click="deleteEntry"
                            class="card-link"><icon scale="1.3" name="trash" color="red" class="align-text-bottom"></icon></b-btn>
                        </div>
                    </b-col>
                </b-row>
            </b-card>
        </transition>
    </div>
</template>

<script>
import Moment from 'moment';
Moment.locale('fr');

export default {
    props: {
        rowData : {type: Object},
    },
    data: function () {
        return {
        }
    },
    computed: {
    },
    methods: {
        deleteEntry: function () {
            this.$emit("delete");
        }
    }
}
</script>
