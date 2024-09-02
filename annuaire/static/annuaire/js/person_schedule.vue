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
        <div>
            <full-calendar
                v-if="showCalendar"
                ref="calendar"
                :options="calendarOptions"
            />
        </div>
        <div v-if="showCalendar">
            <b-popover
                v-for="course in calendarOptions.events"
                :key="course.id"
                tabindex="0"
                :target="`popover-${course.id}`"
                triggers="hover focus"
                :title="`${course.description} (${course.title})`"
            >
                {{ course.related_classes }}
                <br>
                {{ course.place ? `${course.place} : ` : "" }}
                {{ course.related_responsibles }}
            </b-popover>
        </div>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import FullCalendar from "@fullcalendar/vue3";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import frLocale from "@fullcalendar/core/locales/fr";

export default {
    data: function () {
        return {
            periods: [],
            showCalendar: false,
            calendarOptions: {
                plugins: [timeGridPlugin, interactionPlugin],
                locale: frLocale,
                initialView: "timeGridWeek",
                weekends: false,
                events: [],
                allDaySlot: false,
                slotMinTime: "08:00:00",
                slotMaxTime: "18:00:00",
                slotLabelInterval: "08:00:00",
                slotDuration: "00:30:00",
                headerToolbar: false,
                expandRows: true,
                eventContent: (arg) => {
                    return {
                        html: `
                        <div id=popover-${arg.event.id}>
                        <small>${arg.timeText}</small><br />
                        ${arg.event.title} (${arg.event.extendedProps.related_classes})<br />
                        ${arg.event.extendedProps.place ? arg.event.extendedProps.place + " : " : "" }
                        ${this.truncateString(arg.event.extendedProps.related_responsibles, 15)}
                        </div>`
                    };
                }
            }
        };
    },
    methods: {
        truncateString: function(str, maxLength) {
            if (str.length <= maxLength) {
                return str;
            }

            return str.slice(0, maxLength) + "…";
        },
        getCourseSchedule: function () {
            this.calendarOptions.events = [];
            const courseInfoProm = [
                axios.get(`/core/api/course_schedule/?${this.$route.params.type}=${this.$route.params.matricule}`),
                axios.get(`/annuaire/api/${this.$route.params.type}/${this.$route.params.matricule}/`)
            ];

            Promise.all(courseInfoProm)
                .then(resps => {
                    this.calendarOptions.events = resps[0].data.results.map(cS => {
                        const eventDay = Moment().startOf("week").add(cS.day_of_week, "d").format("").slice(0, 11);
                        const start = `${eventDay}${this.periods[cS.period - 1].start}`;
                        const end = `${eventDay}${this.periods[cS.period - 1].end}`;
                        const course = resps[1].data.courses.find(c => cS.given_course.find(gc => gc === c.id));
                        return {
                            id: cS.id,
                            title: course.course.short_name,
                            related_classes: cS.related_classes,
                            related_responsibles: cS.related_responsibles,
                            place: cS.place,
                            description: course.course.long_name,
                            start: start,
                            end: end
                        }; 
                    });
                });
        },
    },
    mounted: function () {
        axios.get("/core/api/period/")
            .then(resp => {
                this.periods = resp.data.results;
                this.getCourseSchedule();

                setTimeout(() => {
                    this.showCalendar = true;
                }, 100);
            });
    },
    components: {
        FullCalendar,
    }
};
</script>
