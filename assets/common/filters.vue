<template>
    <b-form>
        <b-form-group label="Ajouter un filtre">
            <b-input-group>
                    <b-col sm="12" md="4">
                            <b-form-select :options="filterTypeOptions" v-model="filterType" @input="cleanDate">
                            </b-form-select>
                    </b-col>
                    <b-col sm="12" md="8">
                        <multiselect v-model="filterSearch" tag-placeholder="Ajouter cette recherche"
                            select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            placeholder="Filtrer par…" :options="filterSearchOptions" track-by="value"
                            :multiple="true" :taggable="true" @tag="addNewTag" @remove="removeFilter"
                            :customLabel="niceLabel" :disabled="selectDisabled"
                            @search-change="getOptions" @input="updateFilters"
                            >
                        </multiselect>
                    </b-col>
            </b-input-group>
        </b-form-group>
        <b-form-group v-if="inputType != 'text'">
            <b-form-row>
                <b-col sm="2">
                    <p class="text-right">À partir de </p>
                </b-col>
                <b-col sm="3">
                    <b-form-input :type="inputType" v-model="dateTime1" :max="dateTime2" />
                </b-col>
                <b-col sm="2">
                    <p class="text-right">jusqu'à </p>
                </b-col>
                <b-col sm="3">
                    <b-form-input :type="inputType" v-model="dateTime2" :min="dateTime1" />
                </b-col>
                <b-col sm="2">
                    <b-button variant="success" style="display:inline"
                        @click="addDateTimeRange"
                        :disabled="dateTime1 === null || dateTime2 === null"
                        >
                        Ajouter le filtre
                    </b-button>
                </b-col>
            </b-form-row>
        </b-form-group>
    </b-form>
</template>

<script>
import Multiselect from 'vue-multiselect'
import axios from 'axios';

export default {
    props: ['app', 'model'],
    data: function () {
        return {
            filterType: null,
            filterTypeOptions: [],
            filterSearch: [],
            filterSearchOptions: [],
            filters: {},
            dateTime1: null,
            dateTime2: null,
        };
    },
    computed: {
        selectDisabled: function() {
            // When filter is a date or a time (thus a range), disable the
            // multiselect input.
            if (!this.filterType || this.filterType.startsWith("date_")
                || this.filterType.startsWith("datetime_")
                || this.filterType.startsWith("time_")) {
                return true;
            } else {
                return false;
            }
        },
        inputType: function() {
            if (!this.filterType) return "text";
            if (this.filterType.startsWith("date_")) return "date";
            if (this.filterType.startsWith("datetime_")) return "date";
            if (this.filterType.startsWith("time_")) return "time";

            return "text";
        }
    },
    watch: {
        filterTypeOptions: function (options) {
            if (options.length > 0) this.filterType = options[0].value;
        },
        dateTime1: function (dateTime) {
            if (this.dateTime2 === null) this.dateTime2 = dateTime;
        }
    },
    methods: {
        getOptions: function(search) {
            // Don't search on empty string.
            if (!search) return [];

            let param = { 'name': search, 'page':1 };
            axios.get("/" + this.app + "/api/" + this.model + "/", {params: param})
            .then(response => {
                let results = response.data.results.map(i => i[this.filterType]);
                this.filterSearchOptions = Array.from(new Set(results)).map(i => ({
                    'tag': i,
                    'filterType': this.filterType,
                }));
            });

        },
        cleanDate: function() {
            this.dateTime1 = null;
            this.dateTime2 = null;
        },
        addNewTag(newTag) {
            const tag = {
                filterType: this.filterType,
                value: newTag,
                tag: newTag
            };
            this.addTag(tag);
            console.log(tag);
        },
        addTag(tag) {
                this.filterSearch.push(tag);
                this.filterSearchOptions.push(tag);
                this.updateFilters();
        },
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
        addDateTimeRange() {
            this.addDateTimeTag(this.filterType, this.dateTime1, this.dateTime2);
        },
        addDateTimeTag(filterType, dateTime1, dateTime2) {
            let blankTime1 = filterType.startsWith("datetime") ? " 00:00" : "";
            let blankTime2 = filterType.startsWith("datetime") ? " 23:59" : "";
            const tag = {
                'filterType': filterType,
                value: dateTime1 + blankTime1 + "_" + dateTime2 + blankTime2,
                tag: dateTime1 + " " + dateTime2
            }
            this.addTag(tag);
        },
        removeFilter(removedObject, id) {
            this.updateFilters();
        },
        removeTag(value) {
            for (let s in this.filterSearch) {
                if (this.filterSearch[s].value === value) {
                    this.filterSearch.splice(s, 1);
                    break;
                }
            }
            for (let o in this.filterSearchOptions) {
                if (this.filterSearchOptions[o].value === value) {
                    this.filterSearchOptions.splice(o, 1);
                    break;
                }
            }
            this.updateFilters();
        },
        updateFilters() {
            this.filters = {};
            for (let fil in this.filterSearch) {
                let filter = this.filterSearch[fil]
                if (!this.filters.hasOwnProperty(filter.filterType)) {
                    this.filters[filter.filterType] = [filter.value];
                } else {
                    this.filters[filter.filterType].push(filter.value);
                }
            }
            this.$emit('update', this.filters);
        }
    },
    components: {Multiselect},
    mounted: function() {
        this.filterTypeOptions = filters;
    }
}

</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
</style>
