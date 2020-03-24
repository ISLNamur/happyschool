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

import Vue from "vue";
import Vuex from "vuex";

import axios from "axios";

Vue.use(Vuex);

import {addFilter, removeFilter} from "../common/filters.js";


export default new Vuex.Store({
    state: {
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [],
        branches: [],
        disorders: [],
        disorderResponses: [],
        scheduleAdjustments: [],
        branchGoalItems: [],
        crossGoalItems: [],
        assessments: [],
    },
    mutations: {
        addFilter: addFilter,
        removeFilter: removeFilter,
    },
    actions: {
        loadOptions: function (context) {
            return new Promise(resolve => {
                if (context.state.disorders.length == 0) {
                    const promises = [
                        axios.get("/pia/api/disorder/"),
                        axios.get("/pia/api/disorder_response/"),
                        axios.get("/pia/api/schedule_adjustment/"),
                        axios.get("/pia/api/branch_goal_item/"),
                        axios.get("/pia/api/cross_goal_item/"),
                        axios.get("/pia/api/assessment/"),
                        axios.get("/pia/api/branch/")
                    ];
                    Promise.all(promises)
                        .then(resps => {
                            context.state.disorders = resps[0].data.results;
                            context.state.disorderResponses = resps[1].data.results;
                            context.state.scheduleAdjustments = resps[2].data.results;
                            context.state.branchGoalItems = resps[3].data.results;
                            context.state.crossGoalItems = resps[4].data.results;
                            context.state.assessments = resps[5].data.results;
                            context.state.branches = resps[6].data.results;
                            resolve();
                        });
                } else {
                    resolve();
                }
            });
        }
    }
});
