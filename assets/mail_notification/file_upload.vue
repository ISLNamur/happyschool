<template>
    <b-list-group-item>
        <icon v-if="uploading" name="spinner" scale="1" :pulse="uploading"></icon>
        <b-btn v-else @click="deleteEntry" size="sm" variant="danger">Enlever</b-btn>
         {{ file.name }}
    </b-list-group-item>
</template>

<script>
import axios from 'axios';
import Icon from 'vue-awesome/components/Icon.vue'

export default {
    props: ['file'],
    data: function () {
        return {
            uploading: true,
            id: null,
        }
    },
    methods: {
        deleteEntry: function() {
            axios.delete('/mail_notification/upload_file/' + this.id,
                {
                    xsrfCookieName: 'csrftoken',
                    xsrfHeaderName: 'X-CSRFToken',
                }
            ).then(response => {
                this.$emit('delete');
            });
        },
    },
    mounted: function() {
        var data = new FormData();
        data.append('file', this.file);
        axios.put('/mail_notification/upload_file/', data,
            {
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {'Content-Disposition': 'form-data; name="file"; filename="' + this.file.name + '"'},
            })
        .then(response => {
            this.id = response.data.id;
            console.log("id resp " + this.id);
            this.$emit('setid', response.data.id);
            this.uploading = false;
       });
   },
   components: {Icon},
}
</script>

<style>
</style>
