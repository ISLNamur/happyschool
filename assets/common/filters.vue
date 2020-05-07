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
    <b-form>
        <b-form-group label="Ajouter un filtre">
            <b-input-group>
                <b-col
                    sm="12"
                    md="4"
                >
                    <b-form-select
                        :options="filterTypeOptions"
                        v-model="filterType"
                        @input="cleanDate"
                        ref="selectType"
                    />
                </b-col>
                <b-col
                    sm="12"
                    md="8"
                >
                    <multiselect
                        tag-placeholder="Ajouter cette recherche"
                        ref="filters"
                        :show-no-options="false"
                        select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                        selected-label="Sélectionné"
                        deselect-label="Cliquer dessus pour enlever"
                        placeholder="Filtrer par…"
                        :value="filtersValue"
                        :options="filterSearchOptions"
                        track-by="value"
                        :multiple="true"
                        :taggable="true"
                        @remove="removeFilter"
                        @select="addFilter"
                        @tag="addCustomTag"
                        :custom-label="niceLabel"
                        @search-change="getOptions"
                        :internal-search="false"
                        @open="handleSpecificInput"
                    >
                        <span slot="noOptions" />
                    </multiselect>
                </b-col>
            </b-input-group>
        </b-form-group>
        <b-modal
            id="prompt-period-modal"
            title="Choisir une période"
            ok-title="Ajouter"
            cancel-title="Annuler"
            ok-variant="success"
            @ok="addDateTimeTag"
        >
            <b-form-row>
                <b-col>
                    <b-form-group
                        label="À partir de"
                    >
                        <b-form-input
                            :type="inputType"
                            v-model="dateTime1"
                            :max="dateTime2"
                        />
                    </b-form-group>
                </b-col>
            </b-form-row>
            <b-form-row>
                <b-col>
                    <b-form-group
                        label="Jusqu'à"
                    >
                        <b-form-input
                            :type="inputType"
                            v-model="dateTime2"
                            :min="dateTime1"
                        />
                    </b-form-group>
                </b-col>
            </b-form-row>
        </b-modal>
    </b-form>
</template>

<script>
import Multiselect from "vue-multiselect";
import axios from "axios";

export default {
    props: {
        /**
         * The name of the application used for API calls.
         */
        "app": {
            type: String,
            default: ""
        },
        /**
         * The name of the model used for API calls.
         */
        "model": {
            type: String,
            default: ""
        }
    },
    data: function () {
        return {
            /** The type of the filter. */
            filterType: null,
            /** Available options for filterType. */
            filterTypeOptions: [],
            /** Current search. */
            filterSearch: [],
            /** Options available for the current search. */
            filterSearchOptions: [],
            /** The filters. */
            filters: {},
            searchId: 0,
            /** First input for date/time/month period filters. */
            dateTime1: null,
            /** Second input for date/time/month period filters. */
            dateTime2: null,
        };
    },
    computed: {
        /**
         * Compute the type of the html input type.
         */
        inputType: function() {
            if (!this.filterType) return "text";
            if (this.filterType.startsWith("date_month")) return "month";
            if (this.filterType.startsWith("date_")) return "date";
            if (this.filterType.startsWith("datetime_")) return "date";
            if (this.filterType.startsWith("time_")) return "time";

            return "text";
        },
        /**
         * Return the filters in use.
         */
        filtersValue: function () {
            return this.$store.state.filters;
        }
    },
    watch: {
        /**
         * Update filterType if there is a result (?).
         */
        filterTypeOptions: function (options) {
            if (options.length > 0) this.filterType = options[0].value;
        },
        /**
         * Update the second input for date/time/month input from first input.
         */
        dateTime1: function (dateTime) {
            if (this.dateTime2 === null) this.dateTime2 = dateTime;
        }
    },
    methods: {
        /** 
         * Prompt a modal if type is date, month or time.
         */
        handleSpecificInput: function () {
            if (this.inputType == "date"
                || this.inputType == "month"
                || this.inputType == "time") {
                this.$refs.selectType.focus();
                this.$bvModal.show("prompt-period-modal");
            }
        },
        /** 
         * Get options by calling the API of the application.
         * 
         * A filter type starting with "activate" won't call the API
         * but will return an only option to activate the filter.
         * 
         * @param {String} search The search to filter the options.
         */
        getOptions: function(search) {
            // Don't search on empty string.
            if (!search) {
                this.filterSearchOptions = [];
                return;
            }
            
            let param = {};
            if (!this.filterType.endsWith("display")) param["unique"] = this.filterType;
            param[this.filterType] = search;
            this.searchId += 1;
            let currentSearch = this.searchId;
            if (this.filterType == "classe") {
                const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
                let data = {
                    query: search,
                    teachings: this.$store.state.settings.teachings,
                    check_access: 1
                };
                axios.post("/annuaire/api/classes/", data, token)
                    .then(response => {
                        if (this.searchId !== currentSearch)
                            return;
                        this.filterSearchOptions = Array.from(response.data.map(i => ({
                            "tag": i.display,
                            "filterType": "classe",
                            "value": i.year + i.letter,
                        })));
                    });
                return;
            } else if (this.filterType == "scholar_year") {
                axios.get("/core/api/scholar_year/?scholar_year=" + search)
                    .then(response => {
                        if (this.searchId !== currentSearch)
                            return;
                        this.filterSearchOptions = Array.from(response.data.map(i => ({
                            "tag": i,
                            "filterType": "scholar_year",
                            "value": i,
                        })));
                    });
                return;
            } else if (this.filterType.startsWith("activate_")) {
                this.filterSearchOptions = [{
                    "tag": "Activer",
                    "filterType": this.filterType,
                    "value": true,
                }];
                return;
            }

            axios.get("/" + this.app + "/api/" + this.model + "/", {params: param})
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                    let results = [];
                    if (this.filterType.includes("__")) {
                        const subTypes = this.filterType.split("__");
                        results = response.data.results.map(i => i[subTypes[0]][subTypes[1]]);
                    } else {
                        results = response.data.results.map(i => i[this.filterType]);
                    }
                    this.filterSearchOptions = Array.from(new Set(results)).map(i => ({
                        "tag": i,
                        "filterType": this.filterType,
                        "value": i
                    }));
                });

        },
        /** 
         * Clear dates values
         */
        cleanDate: function() {
            this.dateTime1 = null;
            this.dateTime2 = null;
        },
        /**
         * Return a nice formatted string for option results.
         * 
         * @param {String} search The search string.
         */
        niceLabel(search) {
            let displayType = search.filterType;
            for (let opt in this.filterTypeOptions) {
                if (this.filterTypeOptions[opt].value === search.filterType) {
                    displayType = this.filterTypeOptions[opt].text;
                    break;
                }
            }
            return displayType + " : " + search.tag ;
        },
        /**
         * Add a datetime tag to filters.
         * 
         * It will automatically includes the complete day.
         */
        addDateTimeTag() {
            let blankTime1 = this.filterType.startsWith("datetime") ? " 00:00" : "";
            let blankTime2 = this.filterType.startsWith("datetime") ? " 23:59" : "";
            const tag = {
                "filterType": this.filterType,
                value: this.dateTime1 + blankTime1 + "_" + this.dateTime2 + blankTime2,
                tag: this.dateTime1 + " " + this.dateTime2
            };
            this.addFilter(tag);
        },
        /** 
         * Add a tag to the filters.
         * 
         * @param {String} tag The tag.
         */
        addCustomTag: function (tag) {
            const newTag = {
                filterType: this.filterType,
                tag: tag,
                value: tag,
            };
            this.addFilter(newTag);
        },
        /**
         * Add a filter to the store.
         * 
         * @param {object} addedObject An object with the filter type, the tag and the value.
         */
        addFilter(addedObject) {
            this.$store.commit("addFilter", addedObject);
            this.updateFilters();
        },
        /**
         * Remove a filter from the store.
         * 
         * @param {object} removedObject The filter to removed.
         */
        removeFilter(removedObject) {
            if (removedObject == "current") {
                this.$store.commit("removeFilter", this.filterType);
            } else {
                this.$store.commit("removeFilter", removedObject.filterType);
            }
            this.updateFilters();
        },
        /**
         * Emit an update event.
         */
        updateFilters() {
            this.$emit("update");
        }
    },
    components: {Multiselect},
    mounted: function() {
        // eslint-disable-next-line no-undef
        this.filterTypeOptions = filters;
        setTimeout(() => {
            // Check if filters is loaded.
            let refInput = this.$refs.filters;
            if (refInput) {
                refInput.$refs.search.focus();
            }
        }, 500);
    }
};

</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
</style>
