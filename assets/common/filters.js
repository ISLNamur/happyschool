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

import "core-js/stable";
import "regenerator-runtime/runtime";

function addFilter(state, filter) {
    // If filter is a matricule, remove name filter to avoid conflict.
    if (filter.filterType === "matricule_id") {
        this.commit("removeFilter", "name");
    }

    // Overwrite same filter type except for specific cases.
    switch (filter.filterType) {
    case "classe":
        break;
    default:
        this.commit("removeFilter", filter.filterType);
    }

    state.filters.push(filter);
}

function addFilterPinia (filter) {
    // If filter is a matricule, remove name filter to avoid conflict.
    if (filter.filterType === "matricule_id") {
        this.removeFilter("name");
    }

    // Overwrite same filter type except for specific cases.
    switch (filter.filterType) {
    case "classe":
        break;
    default:
        this.removeFilter(filter.filterType);
    }

    this.filters.push(filter);
}

function removeFilter (state, key) {
    for (let f in state.filters) {
        if (state.filters[f].filterType === key) {
            state.filters.splice(f, 1);
            break;
        }
    }
}

function removeFilterPinia (key) {
    for (let f in this.filters) {
        if (this.filters[f].filterType === key) {
            this.filters.splice(f, 1);
            break;
        }
    }
}

function _groupBy (list, keyGetter) {
    const map = new Map();
    list.forEach((item) => {
        const key = keyGetter(item);
        const collection = map.get(key);
        if (!collection) {
            map.set(key, [item]);
        } else {
            collection.push(item);
        }
    });
    return map;
}

function getFilters (filters) {
    let filter = "";
    let storeFilters = filters;
    filters = _groupBy(storeFilters, f => f.filterType);
    filters.forEach((f, fT) => {
        if (fT.startsWith("date") || fT.startsWith("time")) {
            // Handle only one range.
            const range = f[0].value.split("_");
            const gte = range[0];
            const lte = range[1];
            filter += "&" + fT + "__gte=" + gte;
            filter += "&" + fT + "__lte=" + lte;
        } else if (fT.startsWith("activate_")) {
            filter += `&${fT}=true`;
        } else {
            const value = f.map(o => o.value).reduce((a, cV) => a + "," + cV);
            filter += "&" + fT + "=" + value;
        }
    });
    return filter;
}

export {addFilter, addFilterPinia, removeFilter, removeFilterPinia, getFilters};
