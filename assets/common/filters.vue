<template>
    <b-form>
        <b-form-group label="Ajouter un filtre">
            <b-input-group>
                    <b-col sm="12" md="4">
                            <b-form-select :options="filterTypeOptions" v-model="filterType" @input="cleanDate">
                            </b-form-select>
                    </b-col>
                    <b-col sm="12" md="8">
                        <multiselect tag-placeholder="Ajouter cette recherche"
                            select-label="Appuyer sur entrée pour sélectionner ou cliquer dessus"
                            selected-label="Sélectionné"
                            deselect-label="Cliquer dessus pour enlever"
                            placeholder="Filtrer par…"
                            :value="filtersValue"
                            :options="filterSearchOptions" track-by="value"
                            :multiple="true" :taggable="true" @remove="removeFilter"
                            @select="addFilter" @tag="addCustomTag"
                            :customLabel="niceLabel" :disabled="selectDisabled"
                            @search-change="getOptions"
                            :internalSearch="false"
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
                        @click="addDateTimeTag"
                        :disabled="dateTime1 === null || dateTime2 === null"
                        >
                        Ajouter le filtre
                    </b-button>
                    <b-button variant="danger" @click="removeFilter('current')">
                        Retirer
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
            searchId: 0,
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
        },
        filtersValue: function () {
            return this.$store.state.filters;
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
            if (!search) {
                this.filterSearchOptions = [];
                return;
            }

            let param = {'unique': this.filterType};
            param[this.filterType] = search;
            this.searchId += 1;
            let currentSearch = this.searchId;
            if (this.filterType == 'classe') {
                const token = {xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
                let data = {
                    query: search,
                    teachings: this.$store.state.settings.teachings,
                    check_access: 1
                }
                axios.post('/annuaire/api/classes/', data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                    this.filterSearchOptions = Array.from(response.data.map(i => ({
                        'tag': i.display,
                        'filterType': 'classe',
                        'value': i.year + i.letter,
                    })))
                })
                return;
            } else if (this.filterType == 'scholar_year') {
                axios.get('/core/api/scholar_year/?scholar_year=' + search)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                    this.filterSearchOptions = Array.from(response.data.map(i => ({
                        'tag': i,
                        'filterType': 'scholar_year',
                        'value': i,
                    })))
                })
                return;
            } else if (this.filterType.startsWith('activate_')) {
                this.filterSearchOptions = [{
                    'tag': 'Activer',
                    'filterType': this.filterType,
                    'value': true,
                }]
                return;
            }

            axios.get("/" + this.app + "/api/" + this.model + "/", {params: param})
            .then(response => {
                if (this.searchId !== currentSearch)
                    return;
                let results = [];
                if (this.filterType.includes('__')) {
                    const subTypes = this.filterType.split('__');
                    results = response.data.results.map(i => i[subTypes[0]][subTypes[1]]);
                } else {
                    results = response.data.results.map(i => i[this.filterType]);
                }
                this.filterSearchOptions = Array.from(new Set(results)).map(i => ({
                    'tag': i,
                    'filterType': this.filterType,
                    'value': i
                }));
            });

        },
        cleanDate: function() {
            this.dateTime1 = null;
            this.dateTime2 = null;
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
        addDateTimeTag() {
            let blankTime1 = this.filterType.startsWith("datetime") ? " 00:00" : "";
            let blankTime2 = this.filterType.startsWith("datetime") ? " 23:59" : "";
            const tag = {
                'filterType': this.filterType,
                value: this.dateTime1 + blankTime1 + "_" + this.dateTime2 + blankTime2,
                tag: this.dateTime1 + " " + this.dateTime2
            }
            this.addFilter(tag);
        },
        addCustomTag: function (tag) {
            const newTag = {
                filterType: this.filterType,
                tag: tag,
                value: tag,
            }
            this.addFilter(newTag);
        },
        addFilter(addedObject, id) {
            this.$store.commit('addFilter', addedObject);
            this.updateFilters();
        },
        removeFilter(removedObject, id) {
            if (removedObject == 'current') {
                this.$store.commit('removeFilter', this.filterType);
            } else {
                this.$store.commit('removeFilter', removedObject.filterType);
            }
            this.updateFilters();
        },
        updateFilters() {
            this.$emit('update');
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
