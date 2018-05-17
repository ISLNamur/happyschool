<template>
    <div>
        <b-card>
            <div class="card-text">
                <p>
                    Accepte :
                    <icon :name="result.acknowledge ? 'check' : 'times'"
                        :color="result.acknowledge ? 'green' : 'red'">
                    </icon>
                </p>
            </div>
            <div v-if="result.choices" class="card-text">
                <p><strong>Choix : </strong>{{ template.choices[this.result.choices.toString()] }}</p>
                <p v-if="choiceComment" class="ml-3">
                    <em>{{ choiceComment }}</em>
                </p>
            </div>
            <div v-if="result.options" class="card-text">
                <div v-for="opt in result.options" :key="opt">
                    <p><strong>Option : </strong>{{ template.options[opt.toString()] }}</p>
                    <p v-if="optionComment(opt)" class="ml-3">
                        <em>{{ optionComment(opt) }}</em>
                    </p>
                </div>
            </div>
        </b-card>
    </div>
</template>

<script>
import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue'

export default {
    props: ['answer', 'template'],
    data: function () {
        return {
            result: {}
        }
    },
    computed: {
        choiceComment: function () {
            if (!this.result.choices) return '';

            for (let c in this.result.choiceText) {
                if (this.result.choices == this.result.choiceText[c].id) {
                    return this.result.choiceText[c].text;
                }
            }
        },
        choice: function () {
            if (!this.result.choices) return '';

            return this.template;
        }
    },
    methods: {
        optionComment: function(option) {
            for (let c in this.result.optionText) {
                if (option == this.result.optionText[c].id) {
                    return this.result.optionText[c].text;
                }
            }
            return '';
        }
    },
    mounted: function () {
        this.result = JSON.parse(this.answer);
    }
}
</script>

<style>
</style>
