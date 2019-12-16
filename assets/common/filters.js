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

function addFilter (state, filter) {
    // If filter is a matricule, remove name filter to avoid conflict.
    if (filter.filterType === "matricule_id") {
        this.commit("removeFilter", "name");
    }

    // Overwrite same filter type.
    this.commit("removeFilter", filter.filterType);

    state.filters.push(filter);
}

function removeFilter (state, key) {
    for (let f in state.filters) {
        if (state.filters[f].filterType === key) {
            state.filters.splice(f, 1);
            break;
        }
    }
}

function getFilters (filters) {
    let filter = "";
    let storeFilters = filters;
    for (let f in storeFilters) {
        if (storeFilters[f].filterType.startsWith("date")
            || storeFilters[f].filterType.startsWith("time")) {
            let ranges = storeFilters[f].value.split("_");
            filter += "&" + storeFilters[f].filterType + "__gte=" + ranges[0];
            filter += "&" + storeFilters[f].filterType + "__lte=" + ranges[1];
        } else {
            filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
        }
    }
    return filter;
}

export {addFilter, removeFilter, getFilters};
