// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.


import axios from "axios";

import { defineStore } from "pinia";

import { addFilter, removeFilter } from "@s:core/js/common/filters.js";


export const piaStore = defineStore("pia", {
    state: () => ({
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [],
        branches: [],
        disorders: [],
        // eslint-disable-next-line no-undef
        disorderResponses: disorderResponses,
        scheduleAdjustments: [],
        branchGoalItems: [],
        crossGoalItems: [],
        assessments: [],
        studentCourses: [],
        resourceDifficulty: [],
    }),
    actions: {
        addFilter,
        removeFilter,
        setCourses: function (data) {
            this.studentCourses = data;
        },
        loadOptions: function () {
            return new Promise(resolve => {
                if (this.disorders.length == 0) {
                    const promises = [
                        axios.get("/pia/api/disorder/"),
                        axios.get("/pia/api/schedule_adjustment/"),
                        axios.get("/pia/api/branch_goal_item/"),
                        axios.get("/pia/api/cross_goal_item/"),
                        axios.get("/pia/api/assessment/"),
                        axios.get("/pia/api/branch/"),
                        axios.get("/pia/api/resource_difficulty/")
                    ];
                    Promise.all(promises)
                        .then(resps => {
                            this.disorders = resps[0].data.results;
                            this.scheduleAdjustments = resps[1].data.results;
                            this.branchGoalItems = resps[2].data.results;
                            this.crossGoalItems = resps[3].data.results;
                            this.assessments = resps[4].data.results;
                            this.branches = resps[5].data.results;
                            this.resourceDifficulty = resps[6].data.results;
                            resolve();
                        });
                } else {
                    resolve();
                }
            });
        }
    }
});
