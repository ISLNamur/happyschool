<template>
    <div>
        <b-form>
            <b-form-row>
                <b-form-group
                    id="date-start-input-group"
                    description="Date de début de l'absence"
                    label="Date début :"
                    >
                    <b-form-input id="date-start" type="date" required=true></b-form-input>
                </b-form-group>
                <b-form-group
                    id="time-start-input-group"
                    description="Heure de début de l'absence"
                    label="Heure de début :"
                    >
                    <b-form-input id="time-start" type="time"></b-form-input>
                </b-form-group>
            </b-form-row>
        </b-form>
    </div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'Tooto'
    }
  }
}
</script>

<style>
</style>
