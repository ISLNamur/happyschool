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
    <b-tab
        title="Horaire"
        @click="showCal"
    >
        <div>
            <full-calendar
                v-if="showCalendar"
                ref="calendar"
                :options="calendarOptions"
            />
        </div>
    </b-tab>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import FullCalendar from "@fullcalendar/vue";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import frLocale from "@fullcalendar/core/locales/fr";

export default {
    props: {
        courses: {
            type: Array,
            default: () => []
        }
    },
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
                        html: `<small>${arg.timeText}</small><br />
                        ${arg.event.title} (${arg.event.extendedProps.related_classes})<br />
                        ${arg.event.extendedProps.related_responsibles}`
                    };
                }
            }
        };
    },
    watch: {
        courses: function () {
            this.getCourseSchedule();
        }
    },
    methods: {
        showCal: function () {
            this.showCalendar = false;
            setTimeout(() => {
                this.showCalendar = true;
            }, 100);
        },
        getCourseSchedule: function () {
            this.calendarOptions.events = [];
            const promises = this.courses.map(c => axios.get(`/core/api/course_schedule/?given_course=${c.id}`));
            Promise.all(promises)
                .then(resps => {
                    resps.forEach((r, i) => {
                        this.calendarOptions.events = this.calendarOptions.events.concat(r.data.results.map(e => {
                            const eventDay = Moment().startOf("week").add(e.day_of_week, "d").format("").slice(0, 11);
                            const start = `${eventDay}${this.periods[e.period - 1].start}`;
                            const end = `${eventDay}${this.periods[e.period - 1].end}`;
                            return {
                                title: this.courses[i].course.short_name,
                                related_classes: e.related_classes,
                                related_responsibles: e.related_responsibles,
                                description: this.courses[i].course.long_name,
                                start: start,
                                end: end
                            };
                        }));
                    });
                });
        },
    },
    mounted: function () {
        axios.get("/core/api/period/")
            .then(resp => {
                this.periods = resp.data.results;
            });
    },
    components: {
        FullCalendar,
    }
};
</script>
