<template>
    <div>
        <p>Coucou {{ msg }}</p>
    </div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'Export form'
    }
  }
}
</script>

<style>
.message {
  color: blue;
}
</style>
