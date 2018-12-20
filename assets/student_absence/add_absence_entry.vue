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
        <b-row>
        <b-col cols="3">{{ student.last_name }} {{ student.first_name }}</b-col>
        <b-col>
            <b-row>
                <b-col>
                    <div class="text-right">
                    <strong>Matin </strong>
                    <label class="switch">
                        <input type="checkbox" class="primary" v-model="morning_absence"
                        @click="updateAbsence('morning')">
                        <span class="slider round"></span>
                    </label>
                    </div>
                </b-col>
                <b-col>
                    <div class="text-right">
                    <strong>Après-midi </strong>
                    <label class="switch">
                        <input type="checkbox" class="primary" v-model="afternoon_absence"
                        @click="updateAbsence('afternoon')">
                        <span class="slider round"></span>
                    </label>
                    </div>
                </b-col>
            </b-row>
        </b-col>
        </b-row>
    </b-list-group-item>
</template>

<script>
export default {
    props: ['date_absence', 'student',],
    data: function () {
        return {
            morning_absence: false,
            afternoon_absence: false,
            baseAbsence: {},
        }
    },
    methods: {
        updateAbsence: function (partDay) {
            this.changeAbsence(!this[partDay + '_absence'], partDay);
        },
        changeAbsence: function (isAbsent, partDay) {
            let absence = {matricule: this.student.matricule, date_absence: this.date_absence, student: this.student};
            if (!(partDay in this.baseAbsence)) {
                if (isAbsent) {
                    absence[partDay] = isAbsent;
                    this.$store.commit('setChange', absence);
                } else {
                    const otherPartDay = partDay == 'morning' ? 'afternoon' : 'morning';
                    this.$store.commit('removeChange', absence);
                    if (otherPartDay in this.baseAbsence) {
                        if (this[otherPartDay + '_absence'] != this.baseAbsence[otherPartDay]) {
                            absence[otherPartDay] = this[otherPartDay + '_absence'];
                            this.$store.commit('setChange', absence);
                        }
                    } else if (this[otherPartDay + '_absence']) {
                        absence[otherPartDay] = this[otherPartDay + '_absence'];
                            this.$store.commit('setChange', absence);
                    }
                }
            } else {
                if (this.baseAbsence[partDay] != isAbsent) {
                    absence[partDay] = isAbsent;
                    this.$store.commit('setChange', absence);
                } else {
                    const otherPartDay = partDay == 'morning' ? 'afternoon' : 'morning';
                    this.$store.commit('removeChange', absence);
                    if (otherPartDay in this.baseAbsence) {
                        if (this[otherPartDay + '_absence'] != this.baseAbsence[otherPartDay]) {
                            absence[otherPartDay] = this[otherPartDay + '_absence'];
                            this.$store.commit('setChange', absence);
                        }
                    } else if (this[otherPartDay + '_absence']) {
                        absence[otherPartDay] = this[otherPartDay + '_absence'];
                            this.$store.commit('setChange', absence);
                    }
                }
            }
        }
    },
    mounted: function () {
        this.baseAbsence = this.$store.getters.change({matricule: this.student.matricule, date_absence: this.date_absence, student: this.student})
        console.log(this.baseAbsence);
        if (this.baseAbsence) {
            if ('morning' in this.baseAbsence && this.baseAbsence.morning) this.morning_absence = true;
            if ('afternoon' in this.baseAbsence && this.baseAbsence.afternoon) this.afternoon_absence = true;
        } else {
            if ('savedAbsence' in this.student) {
                this.baseAbsence = this.student.savedAbsence;
                if ('morning' in this.baseAbsence && this.baseAbsence.morning) this.morning_absence = true;
                if ('afternoon' in this.baseAbsence && this.baseAbsence.afternoon) this.afternoon_absence = true;
            } else {
                this.baseAbsence = {};
            }
        }
    }
}
</script>

<style>


/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  float: right;
}

/* Hide default HTML checkbox */
.switch input {display:none;}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input.default:checked + .slider {
  background-color: #444;
}
input.primary:checked + .slider {
  background-color: #2196F3;
}
input.success:checked + .slider {
  background-color: #8bc34a;
}
input.info:checked + .slider {
  background-color: #3de0f5;
}
input.warning:checked + .slider {
  background-color: #FFC107;
}
input.danger:checked + .slider {
  background-color: #f44336;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
