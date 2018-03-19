<template>
    <b-form>
        <b-form-group label="Ajouter un filtre">
            <b-input-group>
                    <b-col>
                        <!-- <b-input-group-button slot="left"> -->
                            <b-form-select :options="filterTypeOptions" v-model="filterType" @input="cleanDate">
                            </b-form-select>
                        <!-- </b-input-group-button> -->
                    </b-col>
                    <b-col cols="8">
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
            <b-input-group>
                <b-input-group-addon>À partir de </b-input-group-addon>
                <b-form-input :type="inputType" v-model="dateTime1" :max="dateTime2" />
                <b-input-group-addon>jusqu'à </b-input-group-addon>
                <b-form-input :type="inputType" v-model="dateTime2" :min="dateTime1" />
                <b-input-group-button>
                    <b-button variant="success"
                        @click="addDateTimeRange"
                        :disabled="dateTime1 === '' || dateTime2 === ''"
                        >
                        Ajouter le filtre
                    </b-button>
                </b-input-group-button>
            </b-input-group>
        </b-form-group>
    </b-form>
</template>

<script>
import Multiselect from 'vue-multiselect'
import axios from 'axios';

export default {
    props: ['app'],
    data: function () {
        return {
            filterType: null,
            filterTypeOptions: [],
            filterSearch: [],
            filterSearchOptions: [],
            filters: {},
            dateTime1: '',
            dateTime2: '',
        };
    },
    computed: {
        selectDisabled: function() {
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
            if (this.filterType.startsWith("datetime-local_")) return "datetime-local";
            if (this.filterType.startsWith("time_")) return "time";

            return "text";
        }
    },
    watch: {
        filterTypeOptions: function(options) {
            if (options.length > 0) this.filterType = options[0].value;
        }
    },
    methods: {
        getOptions: function(search) {
            // Don't search on empty string.
            if (!search) return [];

            let param = { 'name': search, 'page':1 };
            axios.get("/" + this.app + "/api/", {params: param})
            .then(response => {
                let results = response.data.results.map(i => i[this.filterType]);
                this.filterSearchOptions = Array.from(new Set(results)).map(i => ({
                    'tag': i,
                    'filterType': this.filterType,
                }));
            });

        },
        cleanDate: function() {
            this.dateTime1 = '';
            this.dateTime2 = '';
        },
        addNewTag(newTag) {
            const tag = {
                filterType: this.filterType,
                value: this.filterType + "-" + newTag,
                tag: newTag
            };
            this.addTag(tag);
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
            const tag = {
                'filterType': filterType,
                value: filterType + '-' + dateTime1 + "_" + dateTime2,
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
                    this.filters[filter.filterType] = [filter.tag];
                } else {
                    this.filters[filter.filterType].push(filter.tag);
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
